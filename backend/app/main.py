from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import candidates, employers, tests, trace

app = FastAPI(title="VGP Technical Proficiency Platform")

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


@app.get("/health")
async def health_check():
    return {"status": "ok"}
