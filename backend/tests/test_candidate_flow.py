import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.main import app
from backend.app.state import db

client = TestClient(app)


def reset_state():
    db.candidates.clear()
    db.test_sessions.clear()
    db.score_reports.clear()
    db.employers.clear()
    db.jobs.clear()


def test_candidate_can_complete_python_flow():
    reset_state()
    resp = client.post(
        "/api/candidates",
        json={"name": "Evelyn", "email": "evelyn@example.com"},
    )
    candidate_id = resp.json()["data"]["candidateId"]

    session_resp = client.post(
        f"/api/candidates/{candidate_id}/tracks",
        json={"trackId": "python_core_v1"},
    )
    session_id = session_resp.json()["data"]["sessionId"]

    next_q = client.get(f"/api/tests/{session_id}/next").json()["data"]
    question_id = next_q["question"]["questionId"]

    client.post(
        f"/api/tests/{session_id}/responses",
        json={
            "questionId": question_id,
            "responseType": "mcq",
            "answer": "dict",
            "code": None,
            "timeTakenSeconds": 30,
        },
    )

    report = client.post(f"/api/tests/{session_id}/submit").json()["data"]
    assert report["overallScore"] >= 0
