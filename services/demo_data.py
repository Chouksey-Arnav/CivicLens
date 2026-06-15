"""
Bundled sample data so CivicLens works out of the box with zero setup.

When CONGRESS_API_KEY / GROQ_API_KEY aren't set, the app serves this data
instead of calling the real APIs, clearly labeled as demo content. Everything
here is fictional/illustrative - bill numbers, member names, and text are
made up for demo purposes only.
"""

CONGRESS = 119

# Each entry mirrors the shape of a real Congress.gov bill record closely
# enough that the templates render identically in demo and live mode.
SAMPLE_BILLS = [
    {
        "congress": CONGRESS,
        "type": "HR",
        "number": 4210,
        "title": "Rural Broadband Access Acceleration Act",
        "originChamber": "House",
        "policyArea": {"name": "Telecommunications"},
        "latestAction": {"actionDate": "2026-05-12", "text": "Referred to the House Committee on Energy and Commerce."},
        "updateDate": "2026-05-12",
        "official_summary": (
            "This bill directs the Federal Communications Commission to establish a grant "
            "program for providers that extend broadband internet service to unserved rural "
            "census blocks. Grants may cover up to 75 percent of infrastructure costs for "
            "projects that deliver minimum download speeds of 100 megabits per second. The "
            "bill requires recipients to offer a low-cost service tier to eligible households "
            "and to report buildout progress annually to the Commission."
        ),
        "ai_summary": {
            "plain_summary": (
                "This bill would create a grant program to help internet companies build "
                "high-speed broadband in rural areas that don't have it yet. The government "
                "would pay for up to 75% of the cost of laying new internet infrastructure."
            ),
            "who_it_affects": [
                "People living in rural areas without reliable internet",
                "Internet service providers applying for grants",
                "Low-income households eligible for discounted plans",
                "The Federal Communications Commission (FCC)",
            ],
            "key_provisions": [
                "Creates a new FCC grant program for rural broadband buildout",
                "Covers up to 75% of infrastructure costs for qualifying projects",
                "Requires minimum internet speeds of 100 Mbps download",
                "Providers must offer a low-cost plan to eligible households",
                "Recipients must report progress to the FCC every year",
            ],
            "why_it_matters": (
                "If passed, this could make high-speed internet available to more rural "
                "communities, which can affect everything from remote work to online learning."
            ),
        },
        "sponsors": [{"firstName": "Dana", "lastName": "Whitfield", "party": "D", "state": "NM", "bioguideId": "D000000"}],
        "introducedDate": "2026-04-02",
    },
    {
        "congress": CONGRESS,
        "type": "S",
        "number": 1187,
        "title": "K-12 School Cybersecurity Support Act",
        "originChamber": "Senate",
        "policyArea": {"name": "Education"},
        "latestAction": {"actionDate": "2026-04-28", "text": "Committee on Commerce, Science, and Transportation. Hearings held."},
        "updateDate": "2026-04-28",
        "official_summary": (
            "This bill establishes a Department of Education grant program to help public "
            "school districts improve cybersecurity. Eligible uses include staff training, "
            "network security upgrades, and incident response planning. The bill caps "
            "individual district awards at $250,000 per year and requires the Department to "
            "publish best-practice guidance for districts within one year of enactment. The "
            "Cybersecurity and Infrastructure Security Agency (CISA) is directed to provide "
            "technical assistance to participating districts upon request."
        ),
        "ai_summary": {
            "plain_summary": (
                "This bill would give public school districts grant money to improve their "
                "cybersecurity, like training staff and upgrading network protections. Each "
                "district could get up to $250,000 per year, and the federal government would "
                "publish a guide on best practices."
            ),
            "who_it_affects": [
                "Public K-12 school districts",
                "School IT staff and administrators",
                "Students and families (through protection of school data)",
                "The Department of Education and CISA",
            ],
            "key_provisions": [
                "Creates a Department of Education cybersecurity grant program for districts",
                "Grants can fund staff training, network upgrades, and incident response plans",
                "Caps awards at $250,000 per district per year",
                "Requires published best-practice guidance within one year",
                "CISA must provide technical help to districts that request it",
            ],
            "why_it_matters": (
                "School districts have increasingly been targeted by ransomware and data "
                "breaches, so this funding could help protect student records and keep "
                "school systems running."
            ),
        },
        "sponsors": [{"firstName": "Marcus", "lastName": "Beane", "party": "R", "state": "OH", "bioguideId": "B000000"}],
        "introducedDate": "2026-03-10",
    },
    {
        "congress": CONGRESS,
        "type": "HR",
        "number": 5502,
        "title": "Veterans Telehealth Access Expansion Act",
        "originChamber": "House",
        "policyArea": {"name": "Armed Forces and National Security"},
        "latestAction": {"actionDate": "2026-06-01", "text": "Passed/agreed to in House."},
        "updateDate": "2026-06-01",
        "official_summary": (
            "This bill requires the Department of Veterans Affairs (VA) to expand telehealth "
            "services to veterans living more than 30 miles from a VA facility. The VA must "
            "provide eligible veterans with a loaner tablet or connectivity stipend if they "
            "lack adequate home internet access. The bill also directs the VA to recruit "
            "additional mental health providers for telehealth appointments and to report to "
            "Congress annually on wait times for virtual mental health care."
        ),
        "ai_summary": {
            "plain_summary": (
                "This bill would require the VA to offer more telehealth (video call) "
                "appointments to veterans who live far from a VA facility. If a veteran "
                "doesn't have good internet at home, the VA would lend them a tablet or help "
                "pay for internet service."
            ),
            "who_it_affects": [
                "Veterans living far from VA facilities",
                "VA mental health providers",
                "The Department of Veterans Affairs",
                "Congress (receives annual wait-time reports)",
            ],
            "key_provisions": [
                "Expands telehealth access for veterans 30+ miles from a VA facility",
                "VA must provide a loaner tablet or internet stipend if needed",
                "VA must hire more telehealth mental health providers",
                "VA must report annually to Congress on virtual care wait times",
            ],
            "why_it_matters": (
                "This could make it easier for veterans in rural areas to get medical and "
                "mental health care without a long drive, especially for ongoing appointments."
            ),
        },
        "sponsors": [{"firstName": "Renee", "lastName": "Castillo", "party": "D", "state": "AZ", "bioguideId": "C000000"}],
        "introducedDate": "2026-02-18",
    },
    {
        "congress": CONGRESS,
        "type": "S",
        "number": 998,
        "title": "Plastic Packaging Recycling Innovation Act",
        "originChamber": "Senate",
        "policyArea": {"name": "Environmental Protection"},
        "latestAction": {"actionDate": "2026-05-20", "text": "Read twice and referred to the Committee on Environment and Public Works."},
        "updateDate": "2026-05-20",
        "official_summary": (
            "This bill establishes a competitive grant program at the Environmental "
            "Protection Agency to fund research and pilot projects for recycling flexible "
            "plastic packaging, such as film and pouches, which are not widely accepted by "
            "curbside recycling programs. The bill authorizes $50,000,000 per year for five "
            "years and requires grantees to share results publicly. It also directs the EPA "
            "to study labeling standards that would help consumers identify recyclable "
            "packaging."
        ),
        "ai_summary": {
            "plain_summary": (
                "This bill would give the EPA money to fund research into recycling soft "
                "plastic packaging, like chip bags and shipping pouches, which most curbside "
                "recycling programs don't accept right now. It would also look into clearer "
                "labels so people know what can actually be recycled."
            ),
            "who_it_affects": [
                "The Environmental Protection Agency (EPA)",
                "Recycling companies and researchers applying for grants",
                "Consumers (through future labeling changes)",
                "Local recycling programs",
            ],
            "key_provisions": [
                "Creates an EPA grant program for flexible plastic recycling research",
                "Authorizes $50 million per year for 5 years",
                "Grant recipients must share their results publicly",
                "EPA must study new recyclable packaging labeling standards",
            ],
            "why_it_matters": (
                "Soft plastics are a big part of household waste that usually can't be "
                "recycled today, so new methods or clearer labels could change what ends up "
                "in landfills."
            ),
        },
        "sponsors": [{"firstName": "Owen", "lastName": "Tran", "party": "I", "state": "ME", "bioguideId": "T000000"}],
        "introducedDate": "2026-03-25",
    },
    {
        "congress": CONGRESS,
        "type": "HR",
        "number": 3877,
        "title": "Youth Financial Literacy in Schools Act",
        "originChamber": "House",
        "policyArea": {"name": "Education"},
        "latestAction": {"actionDate": "2026-04-15", "text": "Ordered to be reported by the Committee on Education and the Workforce."},
        "updateDate": "2026-04-15",
        "official_summary": (
            "This bill establishes a grant program through the Department of Education to "
            "help states develop and integrate personal finance curricula into existing high "
            "school courses. Topics must include budgeting, credit, saving for college, and "
            "understanding student loans. States receiving grants must report on which "
            "districts have implemented the curriculum within two years. The bill does not "
            "mandate a standalone course and leaves implementation decisions to states and "
            "local districts."
        ),
        "ai_summary": {
            "plain_summary": (
                "This bill would give states grant money to add personal finance topics, "
                "like budgeting, credit, and student loans, into existing high school "
                "classes. It doesn't require a brand-new class - states and districts decide "
                "how to fit it in."
            ),
            "who_it_affects": [
                "High school students",
                "State education departments",
                "Local school districts",
                "Teachers who develop or teach the new content",
            ],
            "key_provisions": [
                "Creates a Department of Education grant program for personal finance education",
                "Required topics: budgeting, credit, saving for college, student loans",
                "States choose how to integrate the content into existing courses",
                "States must report which districts implemented it within 2 years",
            ],
            "why_it_matters": (
                "This could mean more students graduate having learned practical money "
                "skills, though the actual content would vary a lot by state and district."
            ),
        },
        "sponsors": [{"firstName": "Priya", "lastName": "Nair", "party": "D", "state": "NC", "bioguideId": "N000000"}],
        "introducedDate": "2026-02-09",
    },
    {
        "congress": CONGRESS,
        "type": "HR",
        "number": 6044,
        "title": "Small Business AI Adoption Resource Act",
        "originChamber": "House",
        "policyArea": {"name": "Commerce"},
        "latestAction": {"actionDate": "2026-06-08", "text": "Introduced in House."},
        "updateDate": "2026-06-08",
        "official_summary": (
            "This bill directs the Small Business Administration (SBA) to create a free "
            "online resource center offering training materials on adopting artificial "
            "intelligence tools for small businesses, including guidance on data privacy and "
            "vendor evaluation. The SBA must partner with at least 10 Small Business "
            "Development Centers to offer in-person workshops in the first year. The bill "
            "authorizes such sums as necessary and requires a report to Congress after two "
            "years assessing adoption rates among participating businesses."
        ),
        "ai_summary": {
            "plain_summary": (
                "This bill would have the Small Business Administration build a free online "
                "hub with training on how small businesses can safely start using AI tools, "
                "plus in-person workshops at Small Business Development Centers."
            ),
            "who_it_affects": [
                "Small business owners and employees",
                "The Small Business Administration (SBA)",
                "Small Business Development Centers",
                "Congress (receives a 2-year adoption report)",
            ],
            "key_provisions": [
                "SBA must build a free online AI adoption resource center",
                "Includes guidance on data privacy and choosing AI vendors",
                "SBA partners with at least 10 Small Business Development Centers for workshops",
                "SBA reports to Congress after 2 years on adoption rates",
            ],
            "why_it_matters": (
                "This could make it easier and lower-risk for small businesses to start using "
                "AI tools, especially ones that don't have in-house tech expertise."
            ),
        },
        "sponsors": [{"firstName": "Leah", "lastName": "Okafor", "party": "R", "state": "TX", "bioguideId": "O000000"}],
        "introducedDate": "2026-06-08",
    },
]


def _matches(bill, query_lower):
    return query_lower in bill["title"].lower()


def search_sample_bills(query):
    """Filter the bundled sample bills by title (case-insensitive substring)."""
    query_lower = query.lower().strip()
    if not query_lower:
        return SAMPLE_BILLS
    return [b for b in SAMPLE_BILLS if _matches(b, query_lower)]


def get_sample_bill(congress, bill_type, number):
    """
    Look up a sample bill by (congress, type, number).

    Returns (bill_dict, official_summary, ai_summary) or (None, None, None)
    if not found.
    """
    for bill in SAMPLE_BILLS:
        if (
            bill["congress"] == congress
            and bill["type"].lower() == bill_type.lower()
            and bill["number"] == number
        ):
            return bill, bill["official_summary"], bill["ai_summary"]
    return None, None, None


# --- Sample "find your representatives" data --------------------------------
# Fictional placeholder members, clearly marked as demo data. Add a free
# Congress.gov API key to see real, current members.
SAMPLE_MEMBERS = {
    "NC": [
        {
            "bioguideId": "DEMO001",
            "name": "Jordan Ellery (Demo)",
            "partyName": "Democratic",
            "state": "NC",
            "chamber": "Senate",
            "district": None,
            "url": "https://www.congress.gov/member/demo",
        },
        {
            "bioguideId": "DEMO002",
            "name": "Casey Tomlinson (Demo)",
            "partyName": "Republican",
            "state": "NC",
            "chamber": "Senate",
            "district": None,
            "url": "https://www.congress.gov/member/demo",
        },
        {
            "bioguideId": "DEMO003",
            "name": "Riley Sandoval (Demo)",
            "partyName": "Republican",
            "state": "NC",
            "chamber": "House of Representatives",
            "district": 4,
            "url": "https://www.congress.gov/member/demo",
        },
        {
            "bioguideId": "DEMO004",
            "name": "Sam Whitaker (Demo)",
            "partyName": "Democratic",
            "state": "NC",
            "chamber": "House of Representatives",
            "district": 2,
            "url": "https://www.congress.gov/member/demo",
        },
    ]
}
