import optparse
import pytest
from hypothesis import given
from hypothesis import strategies as st

from flake8_rst.checker import inject_options, RstFileChecker


@given(key=st.sampled_from(['ignore', 'select']))
@pytest.mark.parametrize('values, expected', [
    ('F, E302, E304', ['F', 'E302', 'E304']),
    ('F821,L02,N', ['F821', 'L02', 'N'])])
def test_set_options(key, values, expected):
    options = optparse.Values({key: ['F821', 'E305']})
    injected = inject_options({'set-' + key: values}, options)

    assert expected.sort() == injected.__dict__[key].sort()
    assert ['F821', 'E305'] == options.__dict__[key]


@given(key=st.sampled_from(['ignore', 'select']))
@pytest.mark.parametrize('values, expected', [
    ('F, E302, E304', ['F821', 'E305', 'F', 'E302', 'E304']),
    ('F821,L02,N', ['F821', 'E305', 'L02', 'N'])])
def test_add_options(key, values, expected):
    options = optparse.Values({key: ['F821', 'E305']})
    injected = inject_options({'add-' + key: values}, options)

    assert expected.sort() == injected.__dict__[key].sort()
    assert ['F821', 'E305'] == options.__dict__[key]


def test_selecting_decision_engine(mocker):
    style_guide = mocker.Mock(decider=mocker.Mock())
    decider = mocker.Mock()
    options = mocker.Mock(max_line_length=80, verbose=0, hang_closing=False)

    checker = RstFileChecker('dummy.py', {}, options)
    checker.style_guide = style_guide
    checker.decider = decider

    checker.results

    assert decider is style_guide.__dict__['decider']
