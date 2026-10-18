# IHH NextDoor — free prototype

A lightweight, **non-production** Orange County recuperative-care transition navigator. It combines structured, non-identifying client profile review with deterministic, explainable resource matching. No paid API key required. No calls, emails, or referrals are sent.

## Start in GitHub Codespaces

1. Create a public GitHub repository named `ihh-nextdoor` and upload these files (or push with Git).
2. Open **Code → Codespaces → Create codespace on main**.
3. In the Codespaces terminal run:

```bash
pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0
```

4. In **Ports**, open forwarded port 8501. Keep the port **private** when testing; do not expose real client information.

For local Windows development:

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Run tests with `python -m pytest -q`.

## Profile review and matching

Structured profile answers feed `matcher.assess`. If a person lacks safe sleeping arrangements, housing comes first. Discharge timing, work readiness, phone access, ID and transport are considered. Recommendations explain why they appear, show source URLs and call scripts, and flag unverified service types for staff. The optional summary is **not sent to an LLM** and is only scanned for limited safety phrases; it is not interpreted as a complete clinical or social history. Use structured inputs for decisions.

## Source data

`data/resources.csv` is intentionally small and sourced from official public websites. Review and reverify each record before use; dates show manual research dates, not a live feed. No claims of openings, eligibility, loan approval or travel funds are made. Sources:

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
5. Referral follow-up outcomes (contacted / intake completed / connected), only in approved secure storage.
