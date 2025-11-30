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
