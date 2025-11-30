"""
Design and Behavior Rules (Rule IDs)

This module documents and enforces all system rules defined in the spec sheet.
Reference: VGP_Technical_Proficiency_Platform_Spec.md Part B5
"""

# R-PRIV-01: Privacy
# All candidate data must be stored securely and never shared without explicit consent.
RULE_PRIVACY = "R-PRIV-01"

# R-PERF-01: Performance
# Code submissions must be evaluated within 3 seconds per test case.
RULE_PERFORMANCE = "R-PERF-01"
PERFORMANCE_TIMEOUT_SECONDS = 3  # Per test case

# R-SCOR-01: Scoring Consistency
# Scoring must follow the standardized scoring algorithm (raw → scaled → percentile).
RULE_SCORING = "R-SCOR-01"

# R-UX-01: User Experience
# Error messages must be clear, non-technical, and actionable.
RULE_UX = "R-UX-01"

# R-ETH-01: Ethics/Fairness
# System must ensure fairness — tests cannot show different questions based on demographics.
RULE_ETHICS = "R-ETH-01"

# R-REP-01: Report Consistency
# Every score report must include score, percentile, strengths, and weaknesses.
RULE_REPORT = "R-REP-01"

# R-LOG-01: Trace Logging
# System must log all test events for auditability.
RULE_LOGGING = "R-LOG-01"


def check_privacy_consent(candidate_id: str, employer_id: str, shared_employers: list[str]) -> bool:
    """
    R-PRIV-01: Verify that candidate has explicitly shared data with employer.
    
    Returns True if sharing is authorized, False otherwise.
    """
    return employer_id in shared_employers


def format_user_error(message: str, technical_detail: str = "") -> str:
    """
    R-UX-01: Format error messages to be clear, non-technical, and actionable.
    
    Converts technical errors into user-friendly messages.
    """
    user_friendly_messages = {
        "session not found": "Your test session could not be found. Please start a new test.",
        "session expired": "Your test session has expired. Please start a new test.",
        "question not found": "The question could not be loaded. Please try again.",
        "unauthorized": "You don't have permission to access this information.",
        "timeout": "Your code took too long to run. Please optimize your solution.",
    }
    
    message_lower = message.lower()
    for key, friendly in user_friendly_messages.items():
        if key in message_lower:
            return friendly
    
    # Default: return a generic friendly message
    return "Something went wrong. Please try again or contact support if the problem persists."


def ensure_fairness(candidate_data: dict) -> dict:
    """
    R-ETH-01: Remove any demographic data that could influence test selection.
    
    Ensures tests are fair and not biased by demographics.
    """
    # Remove demographic fields that should not influence testing
    excluded_fields = ["age", "gender", "race", "ethnicity", "nationality", "religion"]
    cleaned = {k: v for k, v in candidate_data.items() if k not in excluded_fields}
    return cleaned

