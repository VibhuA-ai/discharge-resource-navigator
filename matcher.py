"""Deterministic, auditable decision support; never a benefit eligibility decision."""
from dataclasses import dataclass

NEEDS = ('housing', 'work', 'loan', 'family')


def assess(profile, resources):
    """Return priorities and candidates. No network or data transmission."""
    needs = [n for n in profile.get('needs', []) if n in NEEDS]
    if profile.get('sleep_tonight') == 'No' and 'housing' not in needs:
        needs.insert(0, 'housing')
    if profile.get('discharge') == 'Today' and 'housing' in needs:
        needs = ['housing'] + [n for n in needs if n != 'housing']
    if profile.get('sleep_tonight') == 'No':
        needs = ['housing'] + [n for n in needs if n != 'housing']
    if profile.get('work_ready') == 'No' and 'work' in needs:
        needs = [n for n in needs if n != 'work'] + ['work']
    seen = set()
    needs = [n for n in needs if not (n in seen or seen.add(n))]
    recommendations = []
    for need in needs:
        candidates = [r for r in resources if r['category'] == need]
        if need == 'housing':
            candidates.sort(key=lambda r: (r['id'] != '211oc', r['name']))
        for r in candidates:
            reasons = {'housing':'Housing or shelter navigation requested', 'work':'Employment support requested', 'loan':'Financial support requested', 'family':'Family reunification requested'}
            recommendations.append({'need':need, 'resource':r, 'reason':reasons[need], 'status':'Potential starting point; eligibility and availability not confirmed'})
        if not candidates:
            recommendations.append({'need':need, 'resource':None, 'reason':'No vetted program in the current database', 'status':'Staff verification required; do not promise funding or transportation'})
    barriers = []
    if profile.get('has_phone') == 'No': barriers.append('Client may need staff help placing calls')
    if profile.get('has_id') == 'No': barriers.append('Ask staff to help identify documentation requirements')
    if profile.get('transport') == 'No': barriers.append('Ask staff to plan transport to appointments')
    if profile.get('work_ready') == 'No' and 'work' in needs: barriers.append('Discuss readiness and recovery needs before job referrals')
    if profile.get('family_contact') == 'No' and 'family' in needs: barriers.append('Staff should help confirm safe, consent-based family contact')
    return {'priorities':needs, 'recommendations':recommendations, 'barriers':barriers}


def is_unsafe(text):
    text = (text or '').lower()
    return any(x in text for x in ['in danger','unsafe at home','domestic violence','being abused','threatened','someone will hurt me'])
