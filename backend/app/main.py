from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api import candidates, employers, tests, trace, admin
from .database import MongoDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle
    R-LOG-01: Log startup and shutdown events
    """
    # Startup
    await MongoDB.connect_db()
    
    # Try to load questions from JSON files if database is empty
    try:
        from .database import get_item_bank_collection
        collection = get_item_bank_collection()
        count = await collection.count_documents({})
        
        if count == 0:
            print("📚 No questions found in database, attempting to load from JSON files...")
            try:
                from .api.admin import load_questions
                result = await load_questions()
                if result.get("data", {}).get("questionsLoaded", 0) > 0:
                    print(f"✅ Loaded {result['data']['questionsLoaded']} questions from JSON files")
                else:
                    print("⚠️  No questions loaded. Run load_questions.py or POST /api/admin/load-questions")
            except Exception as e:
                print(f"⚠️  Could not auto-load questions: {e}")
                print("💡 You can load questions manually via POST /api/admin/load-questions")
        else:
            print(f"📚 Found {count} questions in database")
    except Exception as e:
        print(f"⚠️  Could not check question count: {e}")
    
    # Try to load sample candidates if database is empty
    try:
        from .database import get_candidates_collection
        candidates_collection = get_candidates_collection()
        candidate_count = await candidates_collection.count_documents({})
        
        if candidate_count == 0:
            print("👥 No candidates found in database, auto-populating demo data...")
            try:
                from .api.admin import populate_demo_data
                result = await populate_demo_data()
                if result.get("data", {}).get("candidatesCreated", 0) > 0:
                    print(f"✅ Auto-created {result['data']['candidatesCreated']} sample candidates")
                    print(f"   Demo Employer ID: {result['data'].get('demoEmployerId', 'emp-demo-test')}")
                else:
                    print("⚠️  No candidates created. Use POST /api/admin/populate-demo-data manually")
            except Exception as e:
                print(f"⚠️  Could not auto-populate demo data: {e}")
                print("💡 Use POST /api/admin/populate-demo-data to create sample candidates manually")
        else:
            print(f"👥 Found {candidate_count} candidates in database")
    except Exception as e:
        print(f"⚠️  Could not check candidate count: {e}")
    
    print("🚀 VGP Platform started")
    yield
    # Shutdown
    await MongoDB.close_db()
    print("👋 VGP Platform shutdown")


app = FastAPI(
    title="VGP Technical Proficiency Platform",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(candidates.router)
app.include_router(tests.router)
app.include_router(employers.router)
app.include_router(trace.router)
app.include_router(admin.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "database": "mongodb"}
