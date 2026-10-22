# LandingPad

> For IHH clients leaving recuperative care, and the case managers helping them: answer a few
> questions and get a short, sourced list of next steps for shelter, work, money and getting home.

**Challenge:** 2, Finding the right resource
**Built at:** Orange County | Claude Impact Lab, October 17, 2026, with Illumination Health + Home

A **non-production** prototype. No paid AI, no accounts, no database. Nothing is sent to any
provider: no calls, emails or referrals.

## The problem

A client is about to leave recuperative care and needs somewhere safe to sleep, a way to earn, a
little money, or a way home to family. The help exists in Orange County, but it is scattered, the
eligibility rules differ, and a wrong phone number or a closed program costs a client a day they
don't have.

## What it does

1. **Answer a few questions:** what help is needed, when discharge is, whether there is a safe place
   to sleep tonight, and whether the client has a phone, ID, transport and family contact.
2. **Get a plan, housing first.** If there is no safe place to sleep, housing goes to the top. Each
   step says why it appears, names a starting point with its official source link, phone and
   "check before referral" note, and suggests what to say on the call.
3. **No invented programs.** If the directory has no vetted program for a need (loans and travel
   home today), it says so and hands it to staff instead of guessing.
4. **Safety first.** If the client says they are in danger, the plan stops and shows 911 and the
   National Domestic Violence Hotline instead.
5. **Barriers for staff:** no phone, no ID, no transport, readiness for work, safe family contact.

English, Spanish and Vietnamese labels (resource details and call scripts stay in English).

## Run it

Needs Python 3.10 or newer.

```bash
git clone https://github.com/VibhuA-ai/landingpad.git
cd landingpad
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501. In GitHub Codespaces, open forwarded port 8501 and keep it private.

Run the tests: `python -m pytest -q`. They check the matching rules and render the whole app
(the form, a housing-first plan, the "no invented programs" warning and the safety stop).

## How it works

Structured answers feed `matcher.assess`, which is plain, deterministic Python: no AI model. It
orders needs (housing first when there is nowhere safe to sleep, work last when the client isn't
ready), matches each need to records in `data/resources.csv`, and lists barriers for staff.

The optional case manager summary is **not sent to an AI model**. It is only scanned for a short
list of safety phrases.

## What is real and what is mocked

| Part | Status |
|---|---|
| Intake questions, housing-first ordering, barriers | working |
| Safety stop | working (keyword list and checkbox; not a full safety screen) |
| Resource directory | working, 3 sourced records: 211 OC, Coordinated Entry System, OC Workforce Solutions |
| Loans and travel home | no programs listed yet: the app says so rather than inventing one |
| Translations | partial: labels only |

## Source data

`data/resources.csv` is intentionally small and sourced from official public websites. The phone
numbers match the event's sourced directory. Review and reverify each record before use; dates show
manual research dates, not a live feed. No claims of openings, eligibility, loan approval or travel
funds are made. Sources:

- https://211oc.org/get-help/
- https://ceo.oc.gov/care-coordination/homeless-services/coordinated-entry-system-ces
- https://www.ocworkforcesolutions.com/finding-a-job/find-a-job

## Important limitations and safety

- Prototype is **not HIPAA-compliant** and is not approved for protected health information. Do not enter real names, medical history, addresses, identifiers, or detailed case notes, especially on public GitHub or free hosted services.
- Staff must verify services, intake, eligibility, current availability, accessibility and transportation. CES placement is not guaranteed.
- No DV shelter addresses are stored or displayed. For immediate danger call 911 and involve IHH staff; National DV Hotline: 800-799-SAFE (7233).
- This application has no persistent database and no sending function. Hosting providers may still process app traffic and logs; only use synthetic profiles.
- Spanish/Vietnamese UI is partial; service descriptions and scripts are English-only. Do not represent it as full translation.
- No live resource lookup, automatic fact verification, clinical discharge clearance, or loan matching.

## Before a real deployment

Obtain IHH privacy/security approval, role-based access, appropriate hosting and agreements, consent workflow, retention rules, incident handling, vetted translations, accessible design, complete safety triage, approved referral escalation, human review, and a resource verification owner. Do not use a public repository to store client data.

## Next upgrades

1. Approved de-identified structured client profile import with explicit consent and validation.
2. Curated resources with region, verified criteria, last-checked owner, source evidence and review reminders.
3. Optional LLM to **extract proposed structured needs** from de-identified notes, with staff confirmation; never allow LLM to create service facts.
4. Staff-reviewed multilingual scripts and a printable one-page discharge action plan.
5. Add the event directory's sourced microloan and travel-home programs.
6. Referral follow-up outcomes (contacted / intake completed / connected), only in approved secure storage.

## Data and privacy

This project uses only public sources. It contains no real patient or client information and does
not connect to any Illumination Health + Home system.

## License

[MIT](LICENSE)
