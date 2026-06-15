# CivicLens

**Making democracy readable.**

CivicLens pulls real, current bills from the official [Congress.gov API](https://api.congress.gov/) and rewrites their official summaries into short, neutral, plain-English explainers using AI — so anyone can understand what Congress is actually working on without a law degree. It also includes a "find your representatives" tool.

Built for the **[Congressional App Challenge](https://www.congressionalappchallenge.us/)**.

> 🟡 **Runs entirely on free tools.** No paid APIs, no required signup to try it (it ships with demo data), and no hosting costs — everything runs on your own computer.

---

## Features

- **Browse & search bills** — see the most recently updated bills in the current Congress, or search by keyword.
- **Plain-English summaries** — every bill's official Congressional Research Service summary is rewritten by AI into a short "what it does / who it affects / key provisions / why it matters" breakdown.
- **Always shows the source** — the original official summary is always shown alongside the AI version, with a link to the full bill on Congress.gov.
- **Find your representatives** — look up your current U.S. Senators and House representative(s) by state (and district).
- **Works with zero setup** — no API keys? CivicLens automatically falls back to clearly-labeled sample bills and sample representatives so the whole app is explorable immediately.
- **Local caching** — AI summaries are cached in a local SQLite file so each bill is only summarized once, keeping you comfortably within free API limits.

---

## Quick start

Requires Python 3.9+.

```bash
git clone https://github.com/YOUR_USERNAME/civiclens.git
pip install -r requirements.txt
python api/app.py
```

Then open **http://127.0.0.1:5000** — CivicLens will run in **demo mode** with bundled sample bills and representatives, no API keys needed.

### Enable live data (free, ~10 minutes)

CivicLens uses two free APIs. Neither requires a credit card.

1. **Congress.gov API key** — sign up at [api.congress.gov/sign-up](https://api.congress.gov/sign-up/) (instant, by email). This gives you real, current bill data (5,000 requests/hour).
2. **Groq API key** — sign up at [console.groq.com/keys](https://console.groq.com/keys) (Google or email login). This powers the AI plain-English rewriting using Llama 3.3, on Groq's free tier.

Then:

```bash
cp .env.example .env
```

Open `.env` and paste in both keys:

```
CONGRESS_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

Restart `python api/app.py`. The yellow demo banner disappears once both keys are set, and the app pulls live bills and generates real AI summaries.

### Deploying to Vercel

If you are deploying to Vercel, you should **not** upload your `.env` file. Instead, add these same keys as **Environment Variables** in your Vercel Project Settings:

1. Go to your project on the Vercel Dashboard.
2. Go to **Settings** > **Environment Variables**.
3. Add `CONGRESS_API_KEY` and `GROQ_API_KEY` with your respective values.
4. Redeploy your project for the changes to take effect.

Full setup instructions are also built into the app's **About** page.

---

## How it works

```
Congress.gov API  ──►  Flask backend  ──►  Jinja templates  ──►  Browser
 (official bill         (api/app.py +
  text + summaries)       services/)
                              │
                              ▼
                        Groq API (Llama 3.3)
                     rewrites official summary
                       into plain English
                              │
                              ▼
                     SQLite cache (data/cache.db)
                    so each bill is only summarized once
```

- **`api/app.py`** — Flask routes for the home/search page, bill detail pages, the representatives lookup, and the about page.
- **`services/congress_api.py`** — thin wrapper around the Congress.gov API (bills, summaries, members).
- **`services/ai_summarizer.py`** — sends the official summary to Groq's free Llama 3.3 model with a strict, neutral prompt and gets back structured JSON.
- **`services/cache.py`** — local SQLite cache for AI summaries.
- **`services/demo_data.py`** — bundled sample bills + sample representatives used when API keys aren't set.
- **`templates/`** — server-rendered HTML (Jinja2).
- **`static/css/style.css`** — the whole design system (no front-end framework).

---

## Project structure

```
.
├── api/
│   └── app.py               # Flask app + routes (entry point for Vercel)
├── services/
│   ├── congress_api.py      # Congress.gov API client
│   ├── ai_summarizer.py      # Groq AI plain-English rewriter
│   ├── cache.py              # SQLite cache for AI summaries
│   └── demo_data.py          # bundled sample data
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── bill.html
│   ├── representatives.html
│   ├── _member_card.html
│   ├── about.html
│   └── error.html
├── static/
│   ├── css/style.css
│   └── js/main.js
├── config.py                # env vars, constants, US states list
├── requirements.txt
├── vercel.json              # Vercel deployment configuration
├── .env.example
└── .gitignore
```

---

## Notes on accuracy & AI use

- AI summaries are generated from the **official** Congressional Research Service summary only — the model is instructed not to add outside information and to stay neutral.
- The original official summary is always displayed alongside the AI version.
- AI summaries are cached locally, not regenerated on every page load.
- Every bill page links back to the full text and legislative history on Congress.gov.
- This is a civics literacy tool, not legal or political advice — always verify anything important against the official source.

---

## Data sources

- Bill data, summaries, and member info: [Congress.gov API](https://api.congress.gov/) (U.S. Library of Congress), public data.
- AI summarization: [Groq](https://groq.com/) free tier, running Meta's open Llama 3.3 model.

---

## Roadmap ideas

- Filter bills by policy area / sponsor's state
- "Track this bill" list saved locally
- Reading-level toggle (e.g. even simpler / more detail)
- Optional support for other free LLM providers (e.g. Google Gemini's free tier)

Contributions and forks welcome!

---

## License

MIT — see [LICENSE](LICENSE).
