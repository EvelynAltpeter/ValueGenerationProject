import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.models.domain import Candidate, CandidateProfile, SkillTrack


def test_candidate_model_defaults():
    profile = CandidateProfile(name="Evelyn", email="evelyn@example.com")
    candidate = Candidate(id="cand-1", profile=profile)
    assert candidate.selectedTracks == []
    assert candidate.profile.name == "Evelyn"
    assert isinstance(SkillTrack.python_core_v1.value, str)
