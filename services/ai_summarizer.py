"""
Turns an official, legalese bill summary into a short plain-English
explainer using a free LLM API.

Default provider: Groq (https://console.groq.com) - free tier, no credit
card required, OpenAI-compatible API. Swap GROQ_MODEL in .env for any
model Groq offers if you want a different one.
"""

import json

import requests

from config import GROQ_API_KEY, GROQ_API_BASE, GROQ_MODEL, XAI_API_KEY, XAI_API_BASE, XAI_MODEL

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

GLOBAL_SEARCH_PROMPT = """You are CivicLens, a neutral civics explainer. \
A user is searching for a bill that was not found in the US Congress.gov database. \
Use your internal knowledge to provide a neutral summary of the bill or legislation they are likely looking for. \
It could be a historical US bill, a state bill, or an international bill.

If the query is clearly not a bill or you have no information, return a JSON with empty fields and an "error" message.

Respond with ONLY a JSON object matching this schema:
{
  "title": "Full formal title of the bill",
  "jurisdiction": "e.g. 'United States (Historical)', 'California', 'United Kingdom'",
  "plain_summary": "2-4 sentence overview",
  "who_it_affects": ["phrase", "phrase"],
  "key_provisions": ["point", "point"],
  "why_it_matters": "1-2 sentences",
  "error": null or "message if not found"
}"""


class SummarizerError(Exception):
    """Raised when the AI summarizer can't produce a result."""


def _call_ai(api_base, api_key, model, messages, response_format=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 1000,
    }
    if response_format:
        payload["response_format"] = response_format

    try:
        response = requests.post(
            f"{api_base}/chat/completions",
            headers=headers,
            json=payload,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        # Grok sometimes wraps JSON in markdown fences even when requested not to
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
             content = content.split("```")[1].split("```")[0].strip()
        return json.loads(content)
    except Exception as exc:
        raise SummarizerError(f"AI API error: {exc}")


def summarize_bill(title, official_summary, policy_area=None):
    """
    Call Grok (preferrd) or Groq to translate an official bill summary.
    """
    if XAI_API_KEY:
        api_base, api_key, model = XAI_API_BASE, XAI_API_KEY, XAI_MODEL
    elif GROQ_API_KEY:
        api_base, api_key, model = GROQ_API_BASE, GROQ_API_KEY, GROQ_MODEL
    else:
        raise SummarizerError("No AI API key set (XAI_API_KEY or GROQ_API_KEY).")

    user_content = f"Bill title: {title}\n"
    if policy_area:
        user_content += f"Policy area: {policy_area}\n"
    user_content += f"\nOfficial summary:\n{official_summary}"

    parsed = _call_ai(
        api_base, api_key, model,
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"} if "grok" not in model.lower() else None
    )

    # Defensive defaults
    parsed.setdefault("plain_summary", "")
    parsed.setdefault("who_it_affects", [])
    parsed.setdefault("key_provisions", [])
    parsed.setdefault("why_it_matters", "")
    return parsed


def summarize_from_knowledge(query):
    """
    Use Grok/Groq's internal knowledge to search for a bill globally.
    """
    if XAI_API_KEY:
        api_base, api_key, model = XAI_API_BASE, XAI_API_KEY, XAI_MODEL
    elif GROQ_API_KEY:
        api_base, api_key, model = GROQ_API_BASE, GROQ_API_KEY, GROQ_MODEL
    else:
        raise SummarizerError("No AI API key set.")

    return _call_ai(
        api_base, api_key, model,
        [
            {"role": "system", "content": GLOBAL_SEARCH_PROMPT},
            {"role": "user", "content": f"Search for a bill related to: {query}"},
        ],
        response_format={"type": "json_object"} if "grok" not in model.lower() else None
    )
