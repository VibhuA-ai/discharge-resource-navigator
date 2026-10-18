from matcher import assess, is_unsafe

def test_housing_prioritized():
    p={'needs':['work','housing'], 'sleep_tonight':'No', 'discharge':'Today'}
    r=assess(p,[{'id':'211oc','category':'housing','name':'211'}, {'id':'workforce','category':'work','name':'Jobs'}])
    assert r['priorities'][0]=='housing'

def test_unknown_loan_no_invention():
    r=assess({'needs':['loan']}, [])
    assert r['recommendations'][0]['resource'] is None

def test_danger_detection():
    assert is_unsafe('I am in danger')
