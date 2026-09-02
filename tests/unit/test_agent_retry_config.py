import re
from pathlib import Path


def test_gemini_retry_attempts_configured_for_transient_failures() -> None:
    source = Path("app/agent.py").read_text(encoding="utf-8")
    assert re.search(
        r"retry_options\s*=\s*types\.HttpRetryOptions\(\s*attempts\s*=\s*6\s*\)",
        source,
    ), "HttpRetryOptions(attempts=6) not found in app/agent.py"
