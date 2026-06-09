import json
from pydantic import ValidationError
from source.schema import JobPosting
from source.extract import extract_job, repair_job


def clean_json(raw: str) -> str:
    """Strip markdown code fences the LLM sometimes wraps around JSON."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]   # drop the opening ```json line
        if raw.endswith("```"):
            raw = raw[:-3]
    return raw.strip()


def run_pipeline(text: str, max_retries: int = 3) -> JobPosting:
    """Extract → validate → repair loop. Returns a validated JobPosting."""
    raw = extract_job(text)

    for attempt in range(1, max_retries + 1):
        cleaned = clean_json(raw)
        try:
            data = json.loads(cleaned)        # fails if not valid JSON
            job = JobPosting(**data)          # fails if schema doesn't match
            print(f"✅ Validated on attempt {attempt}")
            return job
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"⚠️  Attempt {attempt} failed: {e}\n")
            if attempt == max_retries:
                raise RuntimeError(f"Could not get valid output after {max_retries} tries")
            raw = repair_job(text, raw, str(e))   # send the error back to fix