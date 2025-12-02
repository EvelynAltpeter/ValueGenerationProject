"""
Admin API Endpoints
For managing item bank, scraping, and system maintenance
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json

from ..services.leetcode_scraper import LeetCodeScraper
from ..utils.api import envelope

router = APIRouter(prefix="/api/admin", tags=["admin"])


class ScrapeRequest(BaseModel):
    limit: int = 50


@router.post("/scrape-leetcode")
async def scrape_leetcode(request: ScrapeRequest):
    """
    Scrape problems from LeetCode and store in database
    R-LOG-01: All scraping operations logged
    """
    try:
        scraper = LeetCodeScraper()
        count = await scraper.scrape_and_store(limit=request.limit)
        return envelope({
            "status": "success",
            "problemsStored": count,
            "message": f"Successfully scraped and stored {count} problems"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@router.get("/item-bank-stats")
async def item_bank_stats():
    """Get statistics about the item bank"""
    from ..database import get_item_bank_collection
    
    collection = get_item_bank_collection()
    
    total_count = await collection.count_documents({})
    
    # Count by track
    python_count = await collection.count_documents({"trackId": "python_core_v1"})
    sql_count = await collection.count_documents({"trackId": "sql_core_v1"})
    js_count = await collection.count_documents({"trackId": "javascript_core_v1"})
    
    # Count by difficulty
    easy_count = await collection.count_documents({"difficulty": "easy"})
    medium_count = await collection.count_documents({"difficulty": "medium"})
    hard_count = await collection.count_documents({"difficulty": "hard"})
    
    return envelope({
        "total": total_count,
        "byTrack": {
            "python_core_v1": python_count,
            "sql_core_v1": sql_count,
            "javascript_core_v1": js_count
        },
        "byDifficulty": {
            "easy": easy_count,
            "medium": medium_count,
            "hard": hard_count
        }
    })


@router.post("/populate-demo-data")
async def populate_demo_data():
    """Populate demo data (employers, candidates with scores) for testing"""
    from ..services.candidate_service import create_candidate, share_with_employer
    from ..services.employer_service import create_employer
    from ..models.domain import CandidateProfile, SkillTrack, CandidateScoreReport, ScoreBreakdown, Employer
    from ..database import get_score_reports_collection, get_employers_collection
    from ..utils.time import utc_now_iso
    
    # Sample candidates data (inline to avoid import issues)
    SAMPLE_CANDIDATES = [
        {"name": "Alice Johnson", "email": "alice.j@email.com", "github": "alicej", 
         "education": "Master's", "python": 87, "sql": 92, "javascript": 85},
        {"name": "Bob Smith", "email": "bob.smith@email.com", "github": "bobsmith",
         "education": "Bachelor's", "python": 91, "sql": 88, "javascript": 89},
        {"name": "Carol White", "email": "carol.white@email.com", "github": "carolw",
         "education": "Bachelor's", "python": 85, "sql": 95, "javascript": 82},
        {"name": "David Lee", "email": "david.lee@email.com", "github": "davidl",
         "education": "Bachelor's", "python": 78, "sql": 85, "javascript": 80},
        {"name": "Emma Davis", "email": "emma.d@email.com", "github": "emmad",
         "education": "Master's", "python": 88, "sql": 82, "javascript": 79},
        {"name": "Frank Chen", "email": "frank.chen@email.com", "github": "frankc",
         "education": "Bachelor's", "python": 82, "sql": 79, "javascript": 85},
        {"name": "Grace Park", "email": "grace.park@email.com", "github": "gracep",
         "education": "Bootcamp", "python": 72, "sql": 75, "javascript": 70},
        {"name": "Henry Brown", "email": "henry.b@email.com", "github": "henryb",
         "education": "Bachelor's", "python": 75, "sql": 72, "javascript": 74},
        {"name": "Iris Martinez", "email": "iris.m@email.com", "github": "irism",
         "education": "Bachelor's", "python": 70, "sql": 78, "javascript": 73},
        {"name": "Jack Taylor", "email": "jack.t@email.com", "github": "jackt",
         "education": "Self-taught", "python": 65, "sql": 90, "javascript": 68},
        {"name": "Kelly Anderson", "email": "kelly.a@email.com", "github": "kellya",
         "education": "Bachelor's", "python": 89, "sql": 71, "javascript": 92},
        {"name": "Liam Wilson", "email": "liam.w@email.com", "github": "liamw",
         "education": "Master's", "python": 76, "sql": 81, "javascript": 77},
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
        base = overall_score
        algorithms = max(0, min(100, base + (hash(str(base)) % 10) - 5))
        data_structures = max(0, min(100, base + (hash(str(base + 1)) % 10) - 5))
        code_quality = max(0, min(100, base + (hash(str(base + 2)) % 10) - 5))
        return ScoreBreakdown(algorithms=algorithms, data_structures=data_structures, code_quality=code_quality)
    
    def _calculate_percentile(score: int) -> int:
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
    
    # Create demo employer
    DEMO_EMPLOYER_ID = "emp-demo-test"
    employers_collection = get_employers_collection()
    
    demo_employer_doc = await employers_collection.find_one({"id": DEMO_EMPLOYER_ID})
    if not demo_employer_doc:
        demo_employer = Employer(id=DEMO_EMPLOYER_ID, name="Demo Company")
        await employers_collection.insert_one(demo_employer.model_dump())
    
    # Get all employer IDs (including demo)
    employer_ids = [DEMO_EMPLOYER_ID]
    async for emp_doc in employers_collection.find({}):
        emp_doc.pop('_id', None)
        emp_id = emp_doc.get('id')
        if emp_id != DEMO_EMPLOYER_ID:
            employer_ids.append(emp_id)
    
    # Create candidates
    created_count = 0
    for candidate_data in SAMPLE_CANDIDATES:
        try:
            profile = CandidateProfile(
                name=candidate_data["name"],
                email=candidate_data["email"],
                github=candidate_data["github"],
                educationLevel=candidate_data["education"],
                graduationYear=2024
            )
            
            candidate = await create_candidate(profile)
            
            # Share with all employers (including demo employer)
            # Get all employer IDs from database
            all_employer_ids = [DEMO_EMPLOYER_ID]
            async for emp_doc in employers_collection.find({}):
                emp_doc.pop('_id', None)
                emp_id = emp_doc.get('id')
                if emp_id and emp_id not in all_employer_ids:
                    all_employer_ids.append(emp_id)
            
            # Share candidate with all employers
            for emp_id in all_employer_ids:
                await share_with_employer(candidate.id, emp_id)
            
            # Create score reports
            reports_collection = get_score_reports_collection()
            tracks_and_scores = [
                (SkillTrack.python_core_v1, candidate_data.get("python", 0)),
                (SkillTrack.sql_core_v1, candidate_data.get("sql", 0)),
                (SkillTrack.javascript_core_v1, candidate_data.get("javascript", 0)),
            ]
            
            for track, score in tracks_and_scores:
                if score > 0:
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
            
            created_count += 1
        except Exception as e:
            continue
    
    return envelope({
        "status": "success",
        "candidatesCreated": created_count,
        "demoEmployerId": DEMO_EMPLOYER_ID,
        "message": f"Created {created_count} sample candidates with scores"
    })


@router.post("/load-questions")
async def load_questions():
    """Load questions from JSON files into the database"""
    from ..database import get_item_bank_collection
    from ..models.domain import QuestionMetadata
    
    collection = get_item_bank_collection()
    
    # Try to load from multiple possible locations
    data_dir = Path(__file__).parent.parent.parent / "app" / "data"
    
    # Check for generated questions first
    generated_dir = data_dir / "generated_questions"
    json_files = []
    
    if generated_dir.exists():
        all_questions_file = generated_dir / "all_questions.json"
        if all_questions_file.exists():
            json_files.append(all_questions_file)
        else:
            # Load individual track files
            for track_file in generated_dir.glob("*_questions.json"):
                json_files.append(track_file)
    
    # Fallback to original item_bank.json
    if not json_files:
        item_bank_file = data_dir / "item_bank.json"
        if item_bank_file.exists():
            json_files.append(item_bank_file)
    
    if not json_files:
        raise HTTPException(
            status_code=404,
            detail="No question JSON files found. Please run generate_questions.py first."
        )
    
    total_loaded = 0
    errors = []
    
    for json_file in json_files:
        try:
            with open(json_file, "r") as f:
                questions_data = json.load(f)
            
            # Ensure it's a list
            if isinstance(questions_data, dict):
                questions_data = [questions_data]
            
            for q_data in questions_data:
                try:
                    # Validate and convert to QuestionMetadata
                    question = QuestionMetadata(**q_data)
                    
                    # Insert or update (upsert based on questionId)
                    await collection.update_one(
                        {"questionId": question.questionId},
                        {"$set": question.model_dump()},
                        upsert=True
                    )
                    total_loaded += 1
                except Exception as e:
                    errors.append(f"Error loading question {q_data.get('questionId', 'unknown')}: {str(e)}")
                    continue
                    
        except Exception as e:
            errors.append(f"Error reading file {json_file}: {str(e)}")
            continue
    
    return envelope({
        "status": "success",
        "questionsLoaded": total_loaded,
        "filesProcessed": len(json_files),
        "errors": errors if errors else None
    })

