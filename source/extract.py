import anthropic
from dotenv import load_dotenv

load_dotenv()                      # loads ANTHROPIC_API_KEY from .env
client = anthropic.Anthropic()     # SDK auto-reads the key from env

INSTRUCTIONS = """You are a data extraction tool. Extract fields from the \
job posting and return ONLY valid JSON — no markdown, no code fences, no \
extra text.

JSON structure:
{
  "title": string,
  "company": string,
  "location": string,
  "employment_type": string or null,
  "salary_min": integer or null,
  "salary_max": integer or null,
  "remote": boolean,
  "skills": [list of strings],
  "experience_years": integer or null
}

Rules:
- Convert salaries like "130k" to integers (130000).
- Infer remote as true/false from the text.
- Use null for anything not stated."""


def extract_job(text: str) -> str:
    """Send messy job text to Claude, return the raw JSON string."""
    prompt = INSTRUCTIONS + '\n\nJob posting:\n"""\n' + text + '\n"""'
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text

def repair_job(original_text: str, bad_output: str, error: str) -> str:
    """Ask Claude to fix output that failed validation."""
    prompt = (
        INSTRUCTIONS
        + '\n\nJob posting:\n"""\n' + original_text + '\n"""'
        + "\n\nYour previous response was INVALID:\n" + bad_output
        + "\n\nThe validation error was:\n" + error
        + "\n\nReturn corrected, valid JSON only."
    )
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text