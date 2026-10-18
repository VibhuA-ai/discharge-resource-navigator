import csv
from pathlib import Path
import streamlit as st
from matcher import assess, is_unsafe

st.set_page_config(page_title='IHH NextDoor', page_icon='🚪', layout='centered')
with (Path(__file__).parent/'data/resources.csv').open(encoding='utf-8', newline='') as f:
    RESOURCES = list(csv.DictReader(f))

WORDS = {
'English': {'title':'Find your next step', 'need':'What help do you need?', 'plan':'Create my plan', 'staff':'Ask an IHH staff member to help you with these steps.'},
'Español': {'title':'Encuentre su próximo paso', 'need':'¿Qué ayuda necesita?', 'plan':'Crear mi plan', 'staff':'Pida ayuda a un miembro del personal de IHH.'},
'Tiếng Việt': {'title':'Tìm bước tiếp theo', 'need':'Bạn cần giúp đỡ về việc gì?', 'plan':'Tạo kế hoạch', 'staff':'Hãy nhờ nhân viên IHH giúp bạn thực hiện các bước này.'},
}
LABELS = {'housing':'Safe place to sleep / Vivienda / Chỗ ở', 'work':'Find work / Empleo / Việc làm', 'loan':'Small loan or financial help / Ayuda financiera / Hỗ trợ tài chính', 'family':'Return to family / Regresar con familia / Về với gia đình'}

st.title('🚪 IHH NextDoor')
st.caption('Prototype • Orange County • No accounts, no paid AI, no external submissions')
mode = st.radio('Mode', ['Client navigator', 'Case manager profile review'], horizontal=True)
lang = st.selectbox('Language / Idioma / Ngôn ngữ', list(WORDS))
st.header(WORDS[lang]['title'])
st.info('No information is sent to service providers. This prototype does not save client profiles to a database. Avoid entering names, DOB, medical details or other identifying information.')

with st.form('intake'):
    needs = st.multiselect(WORDS[lang]['need'], list(LABELS), format_func=lambda n:LABELS[n], default=['housing'])
    discharge = st.selectbox('When is discharge?', ['Unknown','Today','Within 7 days','Later'])
    sleep_tonight = st.selectbox('Do you have a safe place to sleep tonight?', ['Unknown','Yes','No'])
    work_ready = st.selectbox('Ready to pursue work now?', ['Unknown','Yes','No'])
    has_phone = st.selectbox('Can you make a phone call?', ['Unknown','Yes','No'])
    has_id = st.selectbox('Do you have identification documents?', ['Unknown','Yes','No'])
    transport = st.selectbox('Do you have transportation?', ['Unknown','Yes','No'])
    family_contact = st.selectbox('Is family contact established and wanted?', ['Unknown','Yes','No'])
    if mode.startswith('Case manager'):
        st.caption('Optional non-identifying profile summary: e.g. "Discharging tomorrow; no housing; wants work after recovery".')
        summary = st.text_area('Client profile summary (de-identified only)', max_chars=1000)
    else:
        summary = ''
    danger = st.checkbox('Client says they are in danger or experiencing abuse')
    submitted = st.form_submit_button(WORDS[lang]['plan'], type='primary')

if submitted:
    if danger or is_unsafe(summary):
        st.error('SAFETY FIRST: If there is immediate danger, call 911 and bring in IHH staff now. For domestic violence, call 800-799-SAFE (7233). Never disclose a confidential shelter address.')
        st.stop()
    profile = dict(needs=needs, discharge=discharge, sleep_tonight=sleep_tonight, work_ready=work_ready, has_phone=has_phone, has_id=has_id, transport=transport, family_contact=family_contact)
    result = assess(profile, RESOURCES)
    st.subheader('Recommended next steps')
    if not result['priorities']:
        st.warning('Select at least one need, or ask staff to review the situation.')
    for idx, rec in enumerate(result['recommendations'], 1):
        st.markdown(f"### {idx}. {LABELS[rec['need']].split(' / ')[0]}")
        st.write('**Why:**', rec['reason'])
        if rec['resource']:
            r = rec['resource']
            st.write('**Starting point:**', r['name'])
            st.write('**Phone:**', r['phone'])
            st.markdown(f"**Official source:** [{r['url']}]({r['url']})")
            st.write('**Check before referral:**', r['eligibility'])
            st.caption(f"Source last checked: {r['verification_date']}. {r['notes']}. Not live availability.")
            st.write(f"**Suggested call:** Hello, I am leaving recuperative care in Orange County. I need help with {rec['need']}. Can you explain the intake process and whether there are programs I may qualify for?")
        else:
            st.warning('No verified specific program available in this prototype. Ask IHH staff to investigate; do not assume a loan or ride exists.')
    if result['barriers']:
        st.subheader('Barriers staff should address')
        for b in result['barriers']: st.write('•', b)
    if 'family' in result['priorities']:
        st.info('Family travel: obtain client consent; confirm destination, receiving person, safety and funding with staff before arranging travel.')
    if lang != 'English':
        st.warning('Only navigation labels and general instructions are translated in this prototype. Resource details and call scripts remain in English; request a qualified interpreter from staff. Do not assume automatic translation is complete.')
    st.success(WORDS[lang]['staff'])
    st.caption('Decision support only. Human review required before any discharge or placement decision.')
