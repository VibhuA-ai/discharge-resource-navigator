import json
import re
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title='IHH NextDoor | Profile Navigator', page_icon='🏠', layout='wide')

# Demonstration-only directory. Check every listing against its source before real use.
RESOURCES = [
    {'name':'211 Orange County','needs':['housing','financial','family'],'url':'https://www.211oc.org/','phone':'211','description':'Community information and referral starting point.','status':'Verify current referral pathway, eligibility and availability.'},
    {'name':'Orange County Coordinated Entry System','needs':['housing'],'url':'https://www.ochealthinfo.com/','phone':'','description':'Housing assessment and coordinated referral pathway; ask staff how to access it.','status':'Official program page and referral pathway must be verified by staff.'},
    {'name':'OC Workforce Solutions','needs':['employment'],'url':'https://www.ocworkforcesolutions.com/','phone':'','description':'Employment and job-search assistance starting point.','status':'Verify site, intake, accessibility and current services.'},
]

CATEGORIES = {
    'housing': {'title':'Safe place to sleep', 'terms':['homeless','no place to stay','sleep outside','shelter','housing','rent','eviction','couch surfing','no address','street','sleep in car','no safe place']},
    'employment': {'title':'Work and income', 'terms':['job','work','unemployed','employment','resume','interview','training','hire','career']},
    'financial': {'title':'Money and small loans', 'terms':['loan','money','financial','cash','bill','debt','deposit','funds','income','food','afford','bank']},
    'family': {'title':'Getting home to family', 'terms':['family','relative','mother','father','sister','brother','daughter','son','reunite','bus ticket','train ticket','return home','go home','travel home']},
}
BARRIERS = {
    'transport': ['no car','transport','bus','ride','cannot travel','can’t travel','cant travel','wheelchair'],
    'documents': ['no id','lost id','identification','birth certificate','documents','no documents'],
    'language': ['interpreter','translation','spanish','vietnamese','limited english'],
    'phone': ['no phone','lost phone','cannot call','no minutes'],
}
SAFETY_TERMS = ['immediate danger','being attacked','threatened with violence','unsafe right now','suicidal','kill myself','domestic violence','being abused','hurt myself']


def term_hits(text, terms):
    # Whole-phrase matching avoids matches inside unrelated words.
    return [term for term in terms if re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', text, re.I)]


def analyze(notes, selected, discharge, housing, ready, family_contact, barriers, safety):
    notes = notes.strip()[:6000]
    text = notes.lower()
    detected = {key:term_hits(text, value['terms']) for key,value in CATEGORIES.items()}
    barrier_hits = {key:term_hits(text, terms) for key,terms in BARRIERS.items()}
    active = set(selected) | {key for key,hits in detected.items() if hits}
    if housing == 'No safe place to sleep': active.add('housing')
    if family_contact: active.add('family')
    urgent = safety or bool(term_hits(text, SAFETY_TERMS))
    result = []
    for key in active:
        score = 10
        reasons = []
        if key in selected: score += 25; reasons.append('Selected by client or case manager')
        if detected[key]: score += min(20, 5*len(detected[key])); reasons.append('Case-note phrases: '+', '.join(detected[key][:4]))
        if key == 'housing':
            score += 30
            if housing == 'No safe place to sleep': score += 45; reasons.append('No safe sleeping arrangement reported')
            if discharge == 'Today or tomorrow': score += 20; reasons.append('Discharge is imminent')
        if key == 'family':
            if family_contact: score += 15; reasons.append('Potential family contact to confirm')
            if discharge == 'Today or tomorrow': score += 10
        if key == 'financial': score += 10
        if key == 'employment':
            if ready: score += 15; reasons.append('Client reports readiness to seek work')
            else: reasons.append('Confirm work readiness before acting')
        result.append({'key':key,'title':CATEGORIES[key]['title'],'score':score,'reasons':reasons,'resources':[r for r in RESOURCES if key in r['needs']]})
    result.sort(key=lambda r:(-r['score'],r['key']))
    identified_barriers = sorted(set(barriers) | {key for key,hits in barrier_hits.items() if hits})
    return {'urgent':urgent,'safety_hits':term_hits(text,SAFETY_TERMS),'matches':result,'barriers':identified_barriers,'detected':detected,'uncertainty':'Keyword-assisted draft, not a diagnosis or eligibility determination. Staff must validate all inferences.'}


def build_plan(profile, analysis):
    lines = ['IHH NEXTDOOR | DRAFT TRANSITION PLAN',f"Created: {datetime.now():%Y-%m-%d %H:%M}",'DEMONSTRATION ONLY — DO NOT USE REAL CLIENT DATA','',f"Reference: {profile['reference']}",f"Language: {profile['language']}",f"Discharge: {profile['discharge']}",'']
    if analysis['urgent']:
        lines += ['SAFETY ESCALATION: Immediate danger: call 911 and involve IHH staff.','Domestic violence hotline: 800-799-7233.','Do not disclose confidential shelter addresses.','']
    else:
        for i,m in enumerate(analysis['matches'],1):
            lines += [f"{i}. {m['title']}", 'Why: '+('; '.join(m['reasons']) or 'Need indicated')]
            if not m['resources']: lines += ['No verified provider in this prototype; IHH staff to investigate.']
            for r in m['resources']:
                lines += [f"Starting point: {r['name']}",f"Website: {r['url']}",f"Phone: {r['phone'] or 'Not verified'}",f"Check: {r['status']}"]
            lines += ['Next: Confirm eligibility, availability and an accessible way to contact the program.','']
        if analysis['barriers']: lines += ['Barriers for staff to resolve: '+', '.join(analysis['barriers'])]
    lines += ['No outreach or referral was sent. Staff review is required.']
    return '\n'.join(lines)


for key,default in [('stage',1),('profile',{}),('analysis',None)]:
    if key not in st.session_state: st.session_state[key]=default

st.title('🏠 IHH NextDoor')
st.caption('Client transition navigator • free, offline profile analysis • staff-reviewed referrals')
with st.sidebar:
    st.header('Navigation')
    st.write('1. Intake and case notes')
    st.write('2. Review profile insights')
    st.write('3. Personalized action plan')
    if st.button('Start new assessment',use_container_width=True):
        st.session_state.stage=1; st.session_state.profile={}; st.session_state.analysis=None; st.rerun()
