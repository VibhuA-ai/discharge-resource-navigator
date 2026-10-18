
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="IHH NextDoor",
    page_icon="🏠",
    layout="wide"
)

# ---------------------------
# Resource starting points
# ---------------------------
# These are navigation starting points, not guarantees of
# eligibility, availability, funding, or placement.

RESOURCES = [
    {
        "name": "211 Orange County",
        "needs": ["Housing", "Financial assistance", "Family reunification"],
        "description": "Community resource information and referrals.",
        "phone": "211",
        "website": "https://www.211oc.org/",
        "status": "Starting point — verify specific program"
    },
    {
        "name": "Orange County Coordinated Entry System",
        "needs": ["Housing"],
        "description": "A process for assessing and connecting people experiencing homelessness with housing resources.",
        "phone": None,
        "website": "https://www.ochealthinfo.com/",
        "status": "Referral process and eligibility require confirmation"
    },
    {
        "name": "OC Workforce Solutions",
        "needs": ["Employment"],
        "description": "Employment and job-search support.",
        "phone": None,
        "website": "https://www.ocworkforcesolutions.com/",
        "status": "Confirm current services and intake"
    }
]

NEEDS = [
    "Housing",
    "Employment",
    "Financial assistance",
    "Family reunification"
]

TRANSLATIONS = {
    "English": {
        "title": "Find your next step",
        "intro": "Tell us what you need. We will help you prepare a plan.",
        "next": "Continue",
        "plan": "Create my plan"
    },
    "Español": {
        "title": "Encuentre su próximo paso",
        "intro": "Díganos qué necesita. Le ayudaremos a preparar un plan.",
        "next": "Continuar",
        "plan": "Crear mi plan"
    },
    "Tiếng Việt": {
        "title": "Tìm bước tiếp theo",
        "intro": "Hãy cho chúng tôi biết bạn cần gì. Chúng tôi sẽ giúp bạn lập kế hoạch.",
        "next": "Tiếp tục",
        "plan": "Tạo kế hoạch"
    }
}

# ---------------------------
# Session state
# ---------------------------
if "step" not in st.session_state:
    st.session_state.step = 1

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "matches" not in st.session_state:
    st.session_state.matches = []

# ---------------------------
# Matching engine
# ---------------------------
def priority_for_need(need, profile):
    score = 10
    reasons = []

    if need == "Housing":
        score += 30
        reasons.append("Housing stability is important for a safe transition.")
        if profile["housing_status"] == "No safe place to sleep":
            score += 50
            reasons.append("The client reports no safe place to sleep.")

    if need == "Employment":
        score += 10
        reasons.append("The client is requesting employment assistance.")
        if profile["work_ready"]:
            score += 10
            reasons.append("The client reports being ready to seek work.")

    if need == "Financial assistance":
        score += 15
        reasons.append("The client needs help with financial resources.")

    if need == "Family reunification":
        score += 20
        reasons.append("The client wants help reconnecting with family.")
        if profile["family_contact"]:
            score += 10
            reasons.append("The client reports having a family contact.")

    if profile["discharge"] == "Today or tomorrow":
        if need in ["Housing", "Family reunification"]:
            score += 20
            reasons.append("Discharge is imminent.")

    return score, reasons


def create_matches(profile):
    results = []

    for need in profile["needs"]:
        score, reasons = priority_for_need(need, profile)

        resources = [
            resource for resource in RESOURCES
            if need in resource["needs"]
        ]

        results.append({
            "need": need,
            "score": score,
            "reasons": reasons,
            "resources": resources
        })

    return sorted(
        results,
        key=lambda result: result["score"],
        reverse=True
    )


def make_plan(profile, matches):
    lines = [
        "IHH NEXTDOOR — TRANSITION ACTION PLAN",
        f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "FICTIONAL / DE-IDENTIFIED PROFILE",
        f"Client reference: {profile['reference']}",
        f"Discharge: {profile['discharge']}",
        f"Language: {profile['language']}",
        "",
        "PRIORITIZED NEEDS"
    ]

    for index, match in enumerate(matches, 1):
        lines.append(f"\n{index}. {match['need']}")

        for reason in match["reasons"]:
            lines.append(f"   - {reason}")

        if not match["resources"]:
            lines.append(
                "   - No verified matching program in this prototype."
            )
            lines.append("   - Request IHH staff assistance.")

        for resource in match["resources"]:
            lines.append(f"   Resource: {resource['name']}")
            lines.append(f"   Purpose: {resource['description']}")
            lines.append(f"   Status: {resource['status']}")
            if resource["phone"]:
                lines.append(f"   Phone: {resource['phone']}")
            if resource["website"]:
                lines.append(f"   Website: {resource['website']}")

        lines.append("   Next step: Confirm eligibility and availability.")

    lines.extend([
        "",
        "STAFF REVIEW",
        "Confirm the plan with the client and appropriate IHH staff.",
        "No referrals, calls, or applications were submitted.",
        "Do not treat these suggestions as confirmed placements."
    ])

    return "\n".join(lines)


# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.title("🏠 IHH NextDoor")
    st.caption("Resource navigation and transition planning")

    mode = st.radio(
        "Choose a view",
        ["Client Navigator", "Case Manager Review"]
    )

    st.divider()

    st.write("**Workflow**")
    st.write("1. Client Profile")
    st.write("2. Review Matches")
    st.write("3. Action Plan")

    if st.button("Start a new profile"):
        st.session_state.step = 1
        st.session_state.profile = {}
        st.session_state.matches = []
        st.rerun()

    st.warning(
        "Prototype: use fictional or de-identified information only. "
        "Do not enter real client medical records or identifying details."
    )

# ---------------------------
# Header
# ---------------------------
st.title("🏠 IHH NextDoor")
st.write("Helping people leaving recuperative care find their next step.")

# ---------------------------
# Safety
# ---------------------------
with st.expander("🚨 Need immediate help or safety support?"):
    st.error(
        "If someone is in immediate danger, call 911 and involve IHH staff."
    )
    st.write(
        "For domestic violence support, call the National Domestic "
        "Violence Hotline at 800-799-7233."
    )
    st.write(
        "Confidential domestic violence shelter addresses are never "
        "displayed by this application."
    )

if st.session_state.step == 1:
    st.subheader("Step 1 of 3 — Client Profile")

    language = st.selectbox(
        "Preferred language",
        ["English", "Español", "Tiếng Việt"]
    )

    t = TRANSLATIONS[language]
    st.markdown(f"### {t['title']}")
    st.write(t["intro"])

    with st.form("client_profile_form"):
        reference = st.text_input(
            "Fictional client reference",
            value="DEMO-001"
        )

        discharge = st.selectbox(
            "When is the client leaving recuperative care?",
            [
                "Today or tomorrow",
                "Within 7 days",
                "More than 7 days",
                "Not sure"
            ]
        )

        needs = st.multiselect(
            "What help does the client need?",
            NEEDS,
            default=["Housing"]
        )

        housing_status = st.selectbox(
            "Where can the client safely sleep after discharge?",
            [
                "No safe place to sleep",
                "Temporary place available",
                "Stable housing available",
                "Not sure"
            ]
        )

        work_ready = st.checkbox(
            "Client says they are ready to look for work"
        )

        family_contact = st.checkbox(
            "Client has a family member they may be able to contact"
        )

        transport_barrier = st.checkbox(
            "Client has difficulty accessing transportation"
        )

        documents_barrier = st.checkbox(
            "Client may need help obtaining identification or documents"
        )

        safety_concern = st.checkbox(
            "Client reports an immediate safety concern"
        )

        submitted = st.form_submit_button(
            t["next"],
            use_container_width=True
        )

    if submitted:
        if not needs and not safety_concern:
            st.error("Please select at least one need.")
        else:
            st.session_state.profile = {
                "reference": reference,
                "language": language,
                "discharge": discharge,
                "needs": needs,
                "housing_status": housing_status,
                "work_ready": work_ready,
                "family_contact": family_contact,
                "transport_barrier": transport_barrier,
                "documents_barrier": documents_barrier,
                "safety_concern": safety_concern
            }

            if safety_concern:
                st.session_state.step = 4
            else:
                st.session_state.matches = create_matches(
                    st.session_state.profile
                )
                st.session_state.step = 2

            st.rerun()

elif st.session_state.step == 2:
    st.subheader("Step 2 of 3 — Review Resource Matches")

    profile = st.session_state.profile
    matches = st.session_state.matches

    st.info(
        "These are suggested starting points, not confirmed "
        "eligibility or service availability."
    )

    for index, match in enumerate(matches, 1):
        with st.container(border=True):
            st.markdown(f"### {index}. {match['need']}")

            for reason in match["reasons"]:
                st.write(f"• {reason}")

            if not match["resources"]:
                st.warning(
                    "No matching program has been verified in this "
                    "prototype. Ask IHH staff to assist."
                )

            for resource in match["resources"]:
                st.markdown(f"**{resource['name']}**")
                st.write(resource["description"])
                st.caption(resource["status"])

                if resource["phone"]:
                    st.write(f"Phone: {resource['phone']}")

                if resource["website"]:
                    st.markdown(
                        f"[Visit official website]({resource['website']})"
                    )

    if profile["transport_barrier"]:
        st.warning(
            "Transportation barrier: ask IHH staff to review "
            "how the client can access recommended services."
        )

    if profile["documents_barrier"]:
        st.warning(
            "Documentation barrier: ask IHH staff to identify "
            "documents required before making referrals."
        )

    if mode == "Case Manager Review":
        st.divider()
        st.subheader("Case Manager Assessment")

        st.write(
            "Review the recommendations against discharge safety, "
            "client preferences, eligibility, and actual availability."
        )

        approved = st.checkbox(
            "I have reviewed these suggestions for planning purposes"
        )
    else:
        approved = True

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back to profile", use_container_width=True):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button(
            "Create my plan →",
            type="primary",
            disabled=not approved,
            use_container_width=True
        ):
            st.session_state.step = 3
            st.rerun()

elif st.session_state.step == 3:
    st.subheader("Step 3 of 3 — Your Action Plan")

    profile = st.session_state.profile
    matches = st.session_state.matches

    st.success("Your draft transition plan is ready.")

    st.write(
        "This plan should be reviewed with IHH staff before "
        "making decisions about discharge or referrals."
    )

    for index, match in enumerate(matches, 1):
        st.markdown(f"### Priority {index}: {match['need']}")

        if match["resources"]:
            for resource in match["resources"]:
                st.write(f"**Starting point:** {resource['name']}")

                if resource["phone"]:
                    st.write(f"**Call:** {resource['phone']}")

                if resource["website"]:
                    st.markdown(
                        f"[Open resource website]({resource['website']})"
                    )

                st.write(
                    "**Suggested words:** "
                    "\"I'm preparing to leave recuperative care "
                    f"and need help with {match['need'].lower()}. "
                    "Can you explain the next step and whether "
                    "I may qualify?\""
                )
        else:
            st.warning(
                "Ask your IHH case manager to help identify "
                "a suitable program."
            )

        st.write(
            "**Before acting:** Confirm program eligibility, "
            "availability and any required documents."
        )

        st.divider()

    if profile["transport_barrier"]:
        st.write(
            "🚗 **Transportation:** Discuss transportation "
            "options with IHH staff."
        )

    if profile["documents_barrier"]:
        st.write(
            "📄 **Documents:** Ask staff what identification "
            "or paperwork may be needed."
        )

    plan_text = make_plan(profile, matches)

    st.download_button(
        label="⬇️ Download my action plan",
        data=plan_text,
        file_name="IHH_NextDoor_Action_Plan.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.caption(
        "This tool does not send referrals, submit applications, "
        "place calls or confirm service availability."
    )

    if st.button("← Review matches"):
        st.session_state.step = 2
        st.rerun()

elif st.session_state.step == 4:
    st.error("Immediate safety concern — staff assistance required")

    st.write(
        "If someone is in immediate danger, call 911 immediately."
    )

    st.write(
        "Bring in an IHH staff member to assess the situation "
        "and help identify an appropriate safe next step."
    )

    st.write(
        "For domestic violence support, call "
        "**800-799-7233**."
    )

    st.warning(
        "Automated resource recommendations are paused "
        "until the safety concern has been reviewed."
    )

    if st.button("Start over"):
        st.session_state.step = 1
        st.rerun()

# ---------------------------
# Footer
# ---------------------------
st.divider()
st.caption(
    "IHH NextDoor | Free prototype | "
    "No automated referrals | Human review required"
)
