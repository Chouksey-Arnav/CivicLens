"""
Thin wrapper around the official Congress.gov API (v3).

Docs: https://api.congress.gov/
Get a free key (no cost, no credit card): https://api.congress.gov/sign-up/

Rate limit on the free key: 5,000 requests/hour - plenty for a single
person browsing bills locally.
"""

import requests

from config import CONGRESS_API_KEY, CONGRESS_API_BASE, CURRENT_CONGRESS

TIMEOUT = 12


class CongressAPIError(Exception):
    """Raised when the Congress.gov API can't be reached or returns an error."""


def _get(path, params=None):
    if not CONGRESS_API_KEY:
        print("DEBUG: CONGRESS_API_KEY is missing")
        raise CongressAPIError(
            "No CONGRESS_API_KEY set. Get a free key at "
            "https://api.congress.gov/sign-up/ and add it to your .env file."
        )

    params = dict(params or {})
    params["api_key"] = CONGRESS_API_KEY
    params["format"] = "json"

    url = f"{CONGRESS_API_BASE}{path}"
    print(f"DEBUG: Calling Congress.gov API: {url} with params { {k:v for k,v in params.items() if k != 'api_key'} }")
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
    except requests.RequestException as exc:
        print(f"DEBUG: Request failed: {exc}")
        raise CongressAPIError(f"Couldn't reach Congress.gov ({exc}).") from exc

    print(f"DEBUG: Response status: {response.status_code}")
    if response.status_code == 403:
        print("DEBUG: API key rejected (403)")
        raise CongressAPIError("Congress.gov rejected the API key (403). Double-check CONGRESS_API_KEY in your Vercel settings.")
    if response.status_code == 429:
        raise CongressAPIError("Congress.gov rate limit hit (429). Wait a bit and try again.")

    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        raise CongressAPIError(f"Congress.gov returned an error: {exc}") from exc

    return response.json()


def get_recent_bills(limit=20, congress=CURRENT_CONGRESS):
    """Most recently updated bills/resolutions for the given Congress."""
    data = _get(f"/bill/{congress}", params={"limit": limit, "sort": "updateDate+desc"})
    return data.get("bills", [])


def search_bills(query, congress=CURRENT_CONGRESS, fetch_limit=250, max_results=25):
    """
    Search bills by keyword.

    The Congress.gov API has no full-text search endpoint, so this pulls a
    batch of the most recently updated bills for the current Congress and
    filters by title on our side.

    If no matches are found in the current Congress, it automatically
    checks the previous Congress (118th) as well.
    """
    query_lower = query.lower().strip()
    if not query_lower:
        data = _get(f"/bill/{congress}", params={"limit": fetch_limit, "sort": "updateDate+desc"})
        return data.get("bills", [])[:max_results]

    # Try current congress first
    data = _get(f"/bill/{congress}", params={"limit": fetch_limit, "sort": "updateDate+desc"})
    bills = data.get("bills", [])
    matches = [b for b in bills if query_lower in b.get("title", "").lower()]

    # If no matches and we are in the current congress, fallback to the previous one
    if not matches and congress == CURRENT_CONGRESS:
        previous_congress = congress - 1
        try:
            data = _get(f"/bill/{previous_congress}", params={"limit": fetch_limit, "sort": "updateDate+desc"})
            bills = data.get("bills", [])
            matches = [b for b in bills if query_lower in b.get("title", "").lower()]
        except CongressAPIError:
            # If previous congress fails, just return the empty current matches
            pass

    return matches[:max_results]


def get_bill(congress, bill_type, number):
    """Full detail record for a single bill."""
    data = _get(f"/bill/{congress}/{bill_type.lower()}/{number}")
    return data.get("bill")


def get_bill_summaries(congress, bill_type, number):
    """Official (CRS-written) summaries for a bill, most recent first."""
    data = _get(f"/bill/{congress}/{bill_type.lower()}/{number}/summaries")
    summaries = data.get("summaries", [])
    # The API returns these oldest -> newest; flip so [0] is most current.
    return list(reversed(summaries))


def get_members_by_state(state_code):
    """Current members of Congress (House + Senate) for a state."""
    data = _get(f"/member/{state_code.upper()}", params={"currentMember": "true", "limit": 250})
    return data.get("members", [])


def get_members_by_state_district(state_code, district):
    """Current House member for a specific state + district number."""
    data = _get(
        f"/member/{state_code.upper()}/{district}",
        params={"currentMember": "true"},
    )
    return data.get("members", [])
