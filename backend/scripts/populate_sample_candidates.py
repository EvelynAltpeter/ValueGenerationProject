#!/usr/bin/env python3
"""
Script to populate sample candidates with scores for employer testing
Creates multiple candidates with various scores across different tracks
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
    ScoreBreakdown, Employer
)
from app.services.candidate_service import create_candidate, share_with_employer
from app.services.employer_service import create_employer
from app.database import get_score_reports_collection, get_employers_collection
from app.utils.time import utc_now_iso
from app.utils.ids import new_id
from app.models.domain import Employer


# Sample candidates with diverse scores
SAMPLE_CANDIDATES = [
    # High performers
    {"name": "Alice Johnson", "email": "alice.j@email.com", "github": "alicej", 
     "education": "Master's", "python": 87, "sql": 92, "javascript": 85},
    {"name": "Bob Smith", "email": "bob.smith@email.com", "github": "bobsmith",
     "education": "Bachelor's", "python": 91, "sql": 88, "javascript": 89},
    {"name": "Carol White", "email": "carol.white@email.com", "github": "carolw",
     "education": "Bachelor's", "python": 85, "sql": 95, "javascript": 82},
    
    # Mid-high performers
    {"name": "David Lee", "email": "david.lee@email.com", "github": "davidl",
     "education": "Bachelor's", "python": 78, "sql": 85, "javascript": 80},
    {"name": "Emma Davis", "email": "emma.d@email.com", "github": "emmad",
     "education": "Master's", "python": 88, "sql": 82, "javascript": 79},
    {"name": "Frank Chen", "email": "frank.chen@email.com", "github": "frankc",
     "education": "Bachelor's", "python": 82, "sql": 79, "javascript": 85},
    
    # Mid-range performers
    {"name": "Grace Park", "email": "grace.park@email.com", "github": "gracep",
     "education": "Bootcamp", "python": 72, "sql": 75, "javascript": 70},
    {"name": "Henry Brown", "email": "henry.b@email.com", "github": "henryb",
     "education": "Bachelor's", "python": 75, "sql": 72, "javascript": 74},
    {"name": "Iris Martinez", "email": "iris.m@email.com", "github": "irism",
     "education": "Bachelor's", "python": 70, "sql": 78, "javascript": 73},
    
    # Specialized candidates
    {"name": "Jack Taylor", "email": "jack.t@email.com", "github": "jackt",
     "education": "Self-taught", "python": 65, "sql": 90, "javascript": 68},
    {"name": "Kelly Anderson", "email": "kelly.a@email.com", "github": "kellya",
     "education": "Bachelor's", "python": 89, "sql": 71, "javascript": 92},
    {"name": "Liam Wilson", "email": "liam.w@email.com", "github": "liamw",
     "education": "Master's", "python": 76, "sql": 81, "javascript": 77},
    
    # More candidates for variety
    {"name": "Maya Patel", "email": "maya.p@email.com", "github": "mayap",
     "education": "Bachelor's", "python": 83, "sql": 87, "javascript": 81},
    {"name": "Noah Garcia", "email": "noah.g@email.com", "github": "noahg",
     "education": "Bootcamp", "python": 68, "sql": 73, "javascript": 71},
    {"name": "Olivia Rodriguez", "email": "olivia.r@email.com", "github": "oliviar",
     "education": "Master's", "python": 90, "sql": 84, "javascript": 88},
    {"name": "Paul Kim", "email": "paul.k@email.com", "github": "paulk",
     "education": "Bachelor's", "python": 74, "sql": 76, "javascript": 75},
    {"name": "Quinn Moore", "email": "quinn.m@email.com", "github": "quinnm",
     "education": "Self-taught", "python": 81, "sql": 69, "javascript": 83},
    {"name": "Rachel Thompson", "email": "rachel.t@email.com", "github": "rachelt",
     "education": "Bachelor's", "python": 86, "sql": 88, "javascript": 84},
    {"name": "Sam Johnson", "email": "sam.j@email.com", "github": "samj",
     "education": "Bootcamp", "python": 71, "sql": 74, "javascript": 72},
    {"name": "Tina Zhang", "email": "tina.z@email.com", "github": "tinaz",
     "education": "Master's", "python": 92, "sql": 89, "javascript": 90},
]


def _calculate_subscores(overall_score: int) -> ScoreBreakdown:
    """Calculate realistic subscores based on overall score"""
    base = overall_score
    # Add some variation but keep it realistic
    algorithms = max(0, min(100, base + (hash(str(base)) % 10) - 5))
    data_structures = max(0, min(100, base + (hash(str(base + 1)) % 10) - 5))
    code_quality = max(0, min(100, base + (hash(str(base + 2)) % 10) - 5))
    
    return ScoreBreakdown(
        algorithms=algorithms,
        data_structures=data_structures,
        code_quality=code_quality
    )


def _calculate_percentile(score: int) -> int:
    """Calculate percentile based on score"""
    if score >= 90:
        return int(85 + (score - 90))
    elif score >= 80:
        return int(70 + ((score - 80) * 1.5))
    elif score >= 70:
        return int(50 + ((score - 70) * 2))
    elif score >= 60:
        return int(30 + ((score - 60) * 2))
    else:
        return max(5, int(30 - ((60 - score) * 2)))


def _get_strengths_weaknesses(score: int, track: str) -> tuple[list[str], list[str]]:
    """Generate strengths and weaknesses based on score"""
    strengths = []
    weaknesses = []
    
    if score >= 85:
        strengths.append(f"Strong {track} fundamentals")
        strengths.append("Excellent problem-solving")
    elif score >= 75:
        strengths.append(f"Good {track} knowledge")
    
    if score < 75:
        weaknesses.append(f"{track} concepts need improvement")
    if score < 70:
        weaknesses.append("Practice more coding problems")
    
    return strengths, weaknesses


async def create_candidate_with_scores(candidate_data: dict, employer_ids: list[str]):
    """Create a candidate profile and score reports"""
    # Create candidate profile
    profile = CandidateProfile(
        name=candidate_data["name"],
        email=candidate_data["email"],
        github=candidate_data["github"],
        educationLevel=candidate_data["education"],
        graduationYear=2024
    )
    
    candidate = await create_candidate(profile)
    
    # Share with all employers
    for employer_id in employer_ids:
        await share_with_employer(candidate.id, employer_id)
    
    # Create score reports for each track
    reports_collection = get_score_reports_collection()
    
    tracks_and_scores = [
        (SkillTrack.python_core_v1, candidate_data.get("python", 0)),
        (SkillTrack.sql_core_v1, candidate_data.get("sql", 0)),
        (SkillTrack.javascript_core_v1, candidate_data.get("javascript", 0)),
    ]
    
    for track, score in tracks_and_scores:
        if score > 0:  # Only create report if score exists
            subscores = _calculate_subscores(score)
            strengths, weaknesses = _get_strengths_weaknesses(score, track.value.split('_')[0])
            percentile = _calculate_percentile(score)
            
            report = CandidateScoreReport(
                candidateId=candidate.id,
                trackId=track,
                overallScore=score,
                subscores=subscores,
                percentile=percentile,
                strengths=strengths,
                weaknesses=weaknesses,
                completedAt=utc_now_iso(),
            )
            
            await reports_collection.update_one(
                {"candidateId": candidate.id, "trackId": track.value},
                {"$set": report.model_dump()},
                upsert=True
            )
    
    return candidate


async def populate_sample_candidates():
    """Populate database with sample candidates"""
    
    print("🚀 Connecting to database...")
    await MongoDB.connect_db()
    
    print("\n📝 Creating/Getting demo employer...")
    
    # Create a fixed demo employer with known ID for easy testing
    DEMO_EMPLOYER_ID = "emp-demo-test"
    employers_collection = get_employers_collection()
    
    # Check if demo employer exists
    demo_employer_doc = await employers_collection.find_one({"id": DEMO_EMPLOYER_ID})
    
    if not demo_employer_doc:
        # Create demo employer with fixed ID
        demo_employer = Employer(id=DEMO_EMPLOYER_ID, name="Demo Company")
        await employers_collection.insert_one(demo_employer.model_dump())
        print(f"✅ Created demo employer: {DEMO_EMPLOYER_ID} (Demo Company)")
    else:
        print(f"✅ Demo employer already exists: {DEMO_EMPLOYER_ID} (Demo Company)")
    
    # Get or create other sample employers
    existing_employers = [DEMO_EMPLOYER_ID]
    
    async for emp_doc in employers_collection.find({}):
        emp_doc.pop('_id', None)
        emp_id = emp_doc.get('id')
        if emp_id != DEMO_EMPLOYER_ID:  # Don't duplicate the demo employer
            existing_employers.append(emp_id)
    
    # Create additional employers if needed
    if len(existing_employers) == 1:  # Only demo employer exists
        employer1 = await create_employer("TechCorp Inc")
        employer2 = await create_employer("DataSystems LLC")
        employer3 = await create_employer("CodeFactory")
        employer_ids = [DEMO_EMPLOYER_ID, employer1.id, employer2.id, employer3.id]
        print(f"✅ Created additional employers: {employer1.id}, {employer2.id}, {employer3.id}")
    else:
        employer_ids = existing_employers
        print(f"✅ Found {len(employer_ids)} total employers (including demo)")
    
    print(f"\n👥 Creating {len(SAMPLE_CANDIDATES)} sample candidates with scores...")
    
    created_count = 0
    for candidate_data in SAMPLE_CANDIDATES:
        try:
            candidate = await create_candidate_with_scores(candidate_data, employer_ids)
            created_count += 1
            
            scores = []
            if candidate_data.get("python"):
                scores.append(f"Python: {candidate_data['python']}")
            if candidate_data.get("sql"):
                scores.append(f"SQL: {candidate_data['sql']}")
            if candidate_data.get("javascript"):
                scores.append(f"JavaScript: {candidate_data['javascript']}")
            
            print(f"  ✅ {candidate_data['name']} - {', '.join(scores)}")
            
        except Exception as e:
            print(f"  ❌ Failed to create {candidate_data['name']}: {e}")
            continue
    
    print(f"\n✨ Successfully created {created_count} candidates with scores!")
    print(f"📊 All candidates are shared with all employers")
    print(f"\n🎯 DEMO EMPLOYER ID: {DEMO_EMPLOYER_ID}")
    print(f"   Company Name: Demo Company")
    print(f"   All {created_count} candidates are shared with this employer")
    print("\n💡 Use this employer ID in the frontend to see all candidates!")


if __name__ == "__main__":
    asyncio.run(populate_sample_candidates())

