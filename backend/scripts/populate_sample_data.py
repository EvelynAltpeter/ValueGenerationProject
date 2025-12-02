"""
Script to populate sample data for demo
Creates sample candidates with scores for employer testing
R-LOG-01: All data creation logged
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_path))

from app.database import MongoDB
from app.models.domain import (
    CandidateProfile, SkillTrack, CandidateScoreReport, 
    ScoreBreakdown, Employer, JobRequirement
)
from app.services.candidate_service import create_candidate, share_with_employer
from app.services.employer_service import create_employer, upsert_job
from app.database import get_score_reports_collection
from app.utils.time import utc_now_iso


async def populate_sample_data():
    """Populate database with sample data for demo"""
    
    print("🚀 Connecting to MongoDB...")
    await MongoDB.connect_db()
    
    print("\n📝 Creating sample employers...")
    
    # Create sample employers
    employer1 = await create_employer("TechCorp Inc")
    employer2 = await create_employer("DataSystems LLC")
    employer3 = await create_employer("CodeFactory")
    
    print(f"✅ Created employers: {employer1.id}, {employer2.id}, {employer3.id}")
    
    # Create sample jobs
    job1 = JobRequirement(
        jobId="job_001",
        employerId=employer1.id,
        requiredTracks=[SkillTrack.python_core_v1],
        minScores={SkillTrack.python_core_v1: 70}
    )
    
    job2 = JobRequirement(
        jobId="job_002",
        employerId=employer2.id,
        requiredTracks=[SkillTrack.sql_core_v1],
        minScores={SkillTrack.sql_core_v1: 65}
    )
    
    job3 = JobRequirement(
        jobId="job_003",
        employerId=employer3.id,
        requiredTracks=[SkillTrack.javascript_core_v1, SkillTrack.python_core_v1],
        minScores={SkillTrack.javascript_core_v1: 75, SkillTrack.python_core_v1: 75}
    )
    
    await upsert_job(employer1.id, job1)
    await upsert_job(employer2.id, job2)
    await upsert_job(employer3.id, job3)
    
    print("✅ Created sample jobs")
    
    print("\n👥 Creating sample candidates with scores...")
    
    # Sample candidates
    candidates_data = [
        {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "github": "github.com/alice",
            "track": SkillTrack.python_core_v1,
            "score": 85,
            "percentile": 82,
            "strengths": ["algorithms", "data_structures"],
            "weaknesses": ["code_quality"]
        },
        {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "github": "github.com/bobsmith",
            "track": SkillTrack.python_core_v1,
            "score": 72,
            "percentile": 68,
            "strengths": ["data_structures"],
            "weaknesses": ["algorithms"]
        },
        {
            "name": "Carol White",
            "email": "carol@example.com",
            "github": "github.com/carolwhite",
            "track": SkillTrack.sql_core_v1,
            "score": 90,
            "percentile": 88,
            "strengths": ["database", "optimization"],
            "weaknesses": []
        },
        {
            "name": "David Lee",
            "email": "david@example.com",
            "github": "github.com/davidlee",
            "track": SkillTrack.javascript_core_v1,
            "score": 78,
            "percentile": 74,
            "strengths": ["async", "DOM"],
            "weaknesses": ["algorithms"]
        },
        {
            "name": "Emma Davis",
            "email": "emma@example.com",
            "github": "github.com/emmadavis",
            "track": SkillTrack.python_core_v1,
            "score": 95,
            "percentile": 94,
            "strengths": ["algorithms", "data_structures", "code_quality"],
            "weaknesses": []
        }
    ]
    
    reports_collection = get_score_reports_collection()
    
    for data in candidates_data:
        # Create candidate
        profile = CandidateProfile(
            name=data["name"],
            email=data["email"],
            github=data["github"],
            educationLevel="Bachelor's",
            graduationYear=2025
        )
        
        candidate = await create_candidate(profile)
        print(f"✅ Created candidate: {candidate.profile.name} ({candidate.id})")
        
        # Share with all employers
        await share_with_employer(candidate.id, employer1.id)
        await share_with_employer(candidate.id, employer2.id)
        await share_with_employer(candidate.id, employer3.id)
        
        # Create score report
        score_report = CandidateScoreReport(
            candidateId=candidate.id,
            trackId=data["track"],
            overallScore=data["score"],
            subscores=ScoreBreakdown(
                algorithms=data["score"] + 5,
                data_structures=data["score"],
                code_quality=data["score"] - 5
            ),
            percentile=data["percentile"],
            strengths=data["strengths"],
            weaknesses=data["weaknesses"],
            completedAt=utc_now_iso()
        )
        
        await reports_collection.insert_one(score_report.model_dump())
        print(f"  📊 Score: {data['score']}, Percentile: {data['percentile']}")
    
    print("\n✨ Sample data population complete!")
    print(f"\n📊 Summary:")
    print(f"  - Employers: 3")
    print(f"  - Jobs: 3")
    print(f"  - Candidates: {len(candidates_data)}")
    print(f"  - Score Reports: {len(candidates_data)}")
    
    await MongoDB.close_db()


if __name__ == "__main__":
    asyncio.run(populate_sample_data())

