"""
CivicLens - Flask app entry point.

Run locally with:
    python app.py

See README.md / the "About" page in the app for setup instructions
(two free API keys, no credit card needed).
"""

from flask import Flask, render_template, request

import sys
import os

# Add the parent directory to sys.path so we can import from services and config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    US_STATES,
    BILL_TYPES,
    CURRENT_CONGRESS,
    DEMO_MODE_BILLS,
    DEMO_MODE_AI,
    FLASK_SECRET_KEY,
)
from services import congress_api, ai_summarizer, cache, demo_data
from services.congress_api import CongressAPIError
from services.ai_summarizer import SummarizerError

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = FLASK_SECRET_KEY

RECENT_BILLS_LIMIT = 24

# Maps a Congress.gov bill "type" code to the path segment Congress.gov's
# website uses for that bill type, e.g. /bill/119th-congress/house-bill/4210
CHAMBER_URL_PATHS = {
    "hr": "house-bill",
    "s": "senate-bill",
    "hjres": "house-joint-resolution",
    "sjres": "senate-joint-resolution",
    "hconres": "house-concurrent-resolution",
    "sconres": "senate-concurrent-resolution",
    "hres": "house-resolution",
    "sres": "senate-resolution",
}


# ---------------------------------------------------------------------------
# Template helpers
# ---------------------------------------------------------------------------

def bill_label(bill):
    """e.g. {"type": "HR", "number": 4210} -> 'H.R. 4210'"""
    bill_type = (bill.get("type") or "").lower()
    label = BILL_TYPES.get(bill_type, bill.get("type", ""))
    return f"{label} {bill.get('number')}"


def origin_chamber_path(bill):
    """Path segment Congress.gov uses for this bill type in its URLs."""
    bill_type = (bill.get("type") or "").lower()
    return CHAMBER_URL_PATHS.get(bill_type, "house-bill")


def status_label(latest_action_text):
    """Turn a latest-action string into a short status + CSS class for the stamp badge."""
    text = (latest_action_text or "").lower()
    if "became public law" in text or "signed by president" in text:
        return {"label": "Became law", "css_class": "stamp-green"}
    if "passed" in text or "agreed to" in text:
        return {"label": "Passed", "css_class": "stamp-blue"}
    if "introduced" in text:
        return {"label": "Introduced", "css_class": "stamp-blue"}
    if not text:
        return {"label": "Status unknown", "css_class": "stamp-red"}
    return {"label": "In committee", "css_class": "stamp-red"}


def normalize_member(member):
    """Flatten the Congress.gov member record into the shape templates expect."""
    terms = (member.get("terms") or {}).get("item") or []
    chamber = terms[-1].get("chamber") if terms else None
    depiction = member.get("depiction") or {}
    return {
        "bioguideId": member.get("bioguideId"),
        "name": member.get("name"),
        "partyName": member.get("partyName"),
        "state": member.get("state"),
        "chamber": chamber,
        "district": member.get("district"),
        "url": member.get("url"),
        "image_url": depiction.get("imageUrl"),
    }


app.jinja_env.globals.update(
    bill_label=bill_label,
    origin_chamber_path=origin_chamber_path,
    status_label=status_label,
)


@app.context_processor
def inject_globals():
    return dict(
        demo_mode_bills=DEMO_MODE_BILLS,
        demo_mode_ai=DEMO_MODE_AI,
        current_congress=CURRENT_CONGRESS,
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    error = None
    ai_result = None

    if DEMO_MODE_BILLS:
        bills = demo_data.search_sample_bills(query)
    else:
        try:
            if query:
                bills = congress_api.search_bills(query)
                # If no US bills found, try AI global search
                if not bills and not DEMO_MODE_AI:
                    try:
                        ai_result = ai_summarizer.summarize_from_knowledge(query)
                        if ai_result.get("error"):
                            ai_result = None
                    except Exception:
                        ai_result = None
            else:
                bills = congress_api.get_recent_bills(limit=RECENT_BILLS_LIMIT)
        except CongressAPIError as exc:
            bills = []
            error = str(exc)

    return render_template("index.html", bills=bills, query=query, error=error, ai_result=ai_result)


@app.route("/bill/<int:congress>/<bill_type>/<int:number>")
def bill_detail(congress, bill_type, number):
    bill_type = bill_type.lower()
    bill_id = f"{congress}-{bill_type}-{number}"
    error = None
    summary = None

    if DEMO_MODE_BILLS:
        bill, official_summary, summary = demo_data.get_sample_bill(congress, bill_type, number)
        if bill is None:
            return render_template(
                "error.html",
                message=(
                    "That bill isn't in the bundled demo data. Try one of the bills on the "
                    "home page, or add a free Congress.gov API key to look up any real bill."
                ),
            ), 404
        return render_template(
            "bill.html", bill=bill, official_summary=official_summary, summary=summary,
            error=error, bill_id=bill_id,
        )

    # --- Live mode ---------------------------------------------------------
    try:
        bill = congress_api.get_bill(congress, bill_type, number)
        if bill is None:
            return render_template("error.html", message="That bill couldn't be found on Congress.gov."), 404
        summaries = congress_api.get_bill_summaries(congress, bill_type, number)
    except CongressAPIError as exc:
        return render_template("error.html", message=str(exc)), 502

    official_summary = summaries[0]["text"] if summaries else None

    if official_summary:
        cached = cache.get_summary(bill_id)
        if cached:
            summary = cached
        elif not DEMO_MODE_AI:
            try:
                policy_area = (bill.get("policyArea") or {}).get("name")
                summary = ai_summarizer.summarize_bill(bill["title"], official_summary, policy_area)
                cache.save_summary(bill_id, summary)
            except SummarizerError as exc:
                error = str(exc)

    return render_template(
        "bill.html", bill=bill, official_summary=official_summary, summary=summary,
        error=error, bill_id=bill_id,
    )


@app.route("/representatives")
def representatives():
    state = request.args.get("state", "").strip().upper()
    district = request.args.get("district", "").strip()
    name = request.args.get("name", "").strip()
    members = []
    error = None

    if name:
        if DEMO_MODE_BILLS:
            # Simple demo filter for name search
            all_demo = []
            for m_list in demo_data.SAMPLE_MEMBERS.values():
                all_demo.extend(m_list)
            members = [m for m in all_demo if name.lower() in m.get("name", "").lower()]
        else:
            try:
                raw_members = congress_api.search_members_by_name(name)
                members = [normalize_member(m) for m in raw_members]
            except CongressAPIError as exc:
                error = str(exc)
    elif state:
        if DEMO_MODE_BILLS:
            members = demo_data.SAMPLE_MEMBERS.get(state, [])
        else:
            try:
                if district:
                    raw_members = congress_api.get_members_by_state_district(state, district)
                else:
                    raw_members = congress_api.get_members_by_state(state)
                members = [normalize_member(m) for m in raw_members]
            except CongressAPIError as exc:
                error = str(exc)

    return render_template(
        "representatives.html", states=US_STATES, state=state, district=district,
        name=name, members=members, error=error,
    )


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
