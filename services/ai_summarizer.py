"""
Turns an official, legalese bill summary into a short plain-English
explainer using a free LLM API.

Default provider: Groq (https://console.groq.com) - free tier, no credit
card required, OpenAI-compatible API. Swap GROQ_MODEL in .env for any
model Groq offers if you want a different one.
"""

import json

import requests

from config import GROQ_API_KEY, GROQ_API_BASE, GROQ_MODEL

TIMEOUT = 30

SYSTEM_PROMPT = """You are CivicLens, a neutral civics explainer. You rewrite \
official congressional bill summaries into plain English that a busy adult \
or high school student can read in under a minute.

Rules:
- Only use information present in the source summary. Never invent facts, \
numbers, or effects that aren't stated.
- Write at roughly an 8th-9th grade reading level. Short sentences. No jargon \
without a quick explanation.
- Stay strictly neutral. Do not argue for or against the bill, and do not \
guess at political motives.
- If the source summary is vague or incomplete, say so plainly instead of \
filling in gaps.

Respond with ONLY a JSON object (no markdown fences, no extra text) matching \
exactly this schema:

{
  "plain_summary": "2-4 sentence overview in plain English",
  "who_it_affects": ["short phrase", "short phrase"],
  "key_provisions": ["short bullet point", "short bullet point"],
  "why_it_matters": "1-2 sentence note on real-world impact, written neutrally"
}

Use 2-5 items for "who_it_affects" and 3-6 items for "key_provisions"."""


class SummarizerError(Exception):
    """Raised when the AI summarizer can't produce a result."""


def summarize_bill(title, official_summary, policy_area=None):
    """
    Call the free LLM API to translate an official bill summary into the
    structured plain-English format CivicLens displays.

    Returns a dict matching the schema in SYSTEM_PROMPT.
    """
    if not GROQ_API_KEY:
        raise SummarizerError(
            "No GROQ_API_KEY set. Get a free key (no credit card) at "
            "https://console.groq.com/keys and add it to your .env file."
        )

    user_content = f"Bill title: {title}\n"
    if policy_area:
        user_content += f"Policy area: {policy_area}\n"
    user_content += f"\nOfficial summary:\n{official_summary}"

    try:
        response = requests.post(
            f"{GROQ_API_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                "temperature": 0.3,
                "max_tokens": 700,
                "response_format": {"type": "json_object"},
            },
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        raise SummarizerError(f"Couldn't reach the Groq API ({exc}).") from exc

    if response.status_code == 401:
        raise SummarizerError("Groq rejected the API key (401). Double-check GROQ_API_KEY in .env.")
    if response.status_code == 429:
        raise SummarizerError(
            "Groq's free tier rate limit was hit (429). Wait a minute and reload the page."
        )

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise SummarizerError(f"Groq returned an error: {exc}") from exc

    data = response.json()
    try:
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        raise SummarizerError(f"Couldn't parse the AI response: {exc}") from exc

    # Defensive defaults in case the model omits a field.
    parsed.setdefault("plain_summary", "")
    parsed.setdefault("who_it_affects", [])
    parsed.setdefault("key_provisions", [])
    parsed.setdefault("why_it_matters", "")
    return parsed
