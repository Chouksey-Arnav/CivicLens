"""
CivicLens configuration.

All settings come from environment variables (loaded from a local .env file
if present). Nothing here is a secret on its own - copy .env.example to .env
and fill in your own free API keys.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- API keys -----------------------------------------------------------
# Free key: https://api.congress.gov/sign-up/
CONGRESS_API_KEY = os.environ.get("CONGRESS_API_KEY", "").strip()

# Free key (no credit card): https://console.groq.com/keys
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()

# xAI Grok API key: https://console.x.ai/
XAI_API_KEY = os.environ.get("XAI_API_KEY", "").strip()

FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-key-change-me")

# --- API endpoints --------------------------------------------------------
CONGRESS_API_BASE = "https://api.congress.gov/v3"
GROQ_API_BASE = "https://api.groq.com/openai/v1"
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

XAI_API_BASE = "https://api.x.ai/v1"
XAI_MODEL = os.environ.get("XAI_MODEL", "grok-2-1212")

# The Congress currently in session. 119th Congress = 2025-2027.
# Update this every two years (odd-numbered years, January).
CURRENT_CONGRESS = int(os.environ.get("CURRENT_CONGRESS", "119"))

# --- Paths -----------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Vercel's filesystem is read-only except for /tmp.
if os.environ.get("VERCEL"):
    CACHE_DB_PATH = "/tmp/cache.db"
else:
    CACHE_DB_PATH = os.path.join(BASE_DIR, "data", "cache.db")

# --- Feature flags -----------------------------------------------------------
# If a key is missing, CivicLens automatically falls back to bundled sample
# data so the app is fully explorable with zero setup.
DEMO_MODE_BILLS = not CONGRESS_API_KEY
DEMO_MODE_AI = not (GROQ_API_KEY or XAI_API_KEY)

# --- Reference data --------------------------------------------------------
US_STATES = [
    ("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"),
    ("CA", "California"), ("CO", "Colorado"), ("CT", "Connecticut"), ("DE", "Delaware"),
    ("FL", "Florida"), ("GA", "Georgia"), ("HI", "Hawaii"), ("ID", "Idaho"),
    ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"),
    ("KY", "Kentucky"), ("LA", "Louisiana"), ("ME", "Maine"), ("MD", "Maryland"),
    ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"), ("MS", "Mississippi"),
    ("MO", "Missouri"), ("MT", "Montana"), ("NE", "Nebraska"), ("NV", "Nevada"),
    ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"), ("NY", "New York"),
    ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"),
    ("OR", "Oregon"), ("PA", "Pennsylvania"), ("RI", "Rhode Island"), ("SC", "South Carolina"),
    ("SD", "South Dakota"), ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"),
    ("VT", "Vermont"), ("VA", "Virginia"), ("WA", "Washington"), ("WV", "West Virginia"),
    ("WI", "Wisconsin"), ("WY", "Wyoming"), ("DC", "District of Columbia"),
    ("PR", "Puerto Rico"),
]

BILL_TYPES = {
    "hr": "H.R.", "s": "S.", "hjres": "H.J.Res.", "sjres": "S.J.Res.",
    "hconres": "H.Con.Res.", "sconres": "S.Con.Res.",
    "hres": "H.Res.", "sres": "S.Res.",
}
