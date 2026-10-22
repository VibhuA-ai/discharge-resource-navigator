"""Render the whole app, so a broken or cut-off app.py fails the tests."""
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / 'app.py')


def run(needs, **choices):
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.multiselect[0].set_value(needs)
    for label, value in choices.items():
        [s for s in at.selectbox if s.label == label][0].set_value(value)
    at.button[0].click().run()
    assert not at.exception
    return at


def test_form_renders():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    assert at.multiselect and at.button[0].label == 'Create my plan'


def test_housing_first_and_no_invented_programs():
    at = run(['work', 'loan', 'family'], **{'Do you have a safe place to sleep tonight?': 'No'})
    headings = [m.value for m in at.markdown if m.value.startswith('###')]
    assert headings[0] == '### 1. Safe place to sleep'
    assert len(headings) == 4  # one heading per need
    assert any('do not assume a loan or ride exists' in w.value for w in at.warning)


def test_danger_stops_the_plan():
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.checkbox[0].check()
    at.button[0].click().run()
    assert any('911' in e.value for e in at.error)
    assert not [m for m in at.markdown if m.value.startswith('###')]
