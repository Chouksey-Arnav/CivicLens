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
        raise CongressAPIError(
            "No CONGRESS_API_KEY set. Get a free key at "
            "https://api.congress.gov/sign-up/ and add it to your .env file."
        )

    params = dict(params or {})
    params["api_key"] = CONGRESS_API_KEY
    params["format"] = "json"

    url = f"{CONGRESS_API_BASE}{path}"
    try:
        response = requests.get(url, params=params, timeout=TIMEOUT)
    except requests.RequestException as exc:
        raise CongressAPIError(f"Couldn't reach Congress.gov ({exc}).") from exc

    if response.status_code == 403:
        raise CongressAPIError("Congress.gov rejected the API key (403). Double-check CONGRESS_API_KEY in .env.")
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


def search_bills(query, congress=None, fetch_limit=250, max_results=25):
    """
    Search bills by keyword across multiple congresses.
    """
    query_lower = query.lower().strip()
    if not query_lower:
        return get_recent_bills(limit=max_results)

    # If a specific congress is provided, only search that one.
    # Otherwise, search the current one and the previous two.
    congresses_to_search = [congress] if congress else [CURRENT_CONGRESS, CURRENT_CONGRESS - 1, CURRENT_CONGRESS - 2]

    all_matches = []
    for c in congresses_to_search:
        try:
            data = _get(f"/bill/{c}", params={"limit": fetch_limit, "sort": "updateDate+desc"})
            bills = data.get("bills", [])
            matches = [b for b in bills if query_lower in b.get("title", "").lower()]
            all_matches.extend(matches)
        except CongressAPIError:
            continue

        if len(all_matches) >= max_results:
            break

    return all_matches[:max_results]


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


def search_members_by_name(name_query):
    """
    Search for current members of Congress by name.
    The API doesn't have a direct name search, so we fetch all current members
    and filter locally.
    """
    # Fetching all current members (around 540 total)
    data = _get("/member", params={"currentMember": "true", "limit": 1000})
    members = data.get("members", [])

    query_lower = name_query.lower().strip()
    matches = [m for m in members if query_lower in m.get("name", "").lower()]
    return matches
