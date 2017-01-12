# -*- coding: utf-8
import re

import six

from richtypo import Richtypo
from richtypo.rules import ABRule, Rule

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


def test_rule_generic():
    r = Rule(
        pattern='b{2}',
        replacement='c'
    )
    assert r.apply('abb') == 'ac'


def test_rule_generic_no_match():
    r = Rule(
        pattern='b{2}',
        replacement='c'
    )
    assert r.apply('acc') == 'acc'


def test_rule_applying():
    r1 = Rule(
        pattern='b{2}',
        replacement='cc'
    )
    r2 = Rule(
        pattern='c{2}',
        replacement='dd'
    )

    r = Richtypo()
    r.rules = [r1, r2]
    r.text = 'abb'
    r.apply_rule_chain()

    assert r.text == 'add'


def test_rule_order():
    """
    Check if rules are applyied in order they are supplied
    """
    r1 = Rule(
        pattern='b{2}',
        replacement='cc'
    )
    r2 = Rule(
        pattern='c{2}',
        replacement='dd'
    )
    r = Richtypo()
    r.rules = [r2, r1]  # r2 works only after r1
    r.text = 'abb'
    r.apply_rule_chain()

    assert r.text == 'acc'  # so the text should not be changed


def test_get_rule_from_available():
    r = Richtypo()
    r.available_rules = {
        'b': Rule(pattern='b', replacement='d')
    }
    rule = r._get_rule('b')

    assert rule.pattern == 'b'


def test_get_rule_from_predefined_rules():
    r = Richtypo()
    rule = r._get_rule(ABRule)

    assert rule == ABRule


def test_rule_flags():
    rule = Rule(pattern='A', replacement='b')
    rule._compile()

    if six.PY2:
        reference_flags = re.UNICODE
    else:
        reference_flags = 0

    assert rule._re == re.compile('A', flags=reference_flags)

    rule.flags = ['I']
    rule._compile()
    assert rule._re == re.compile('A', flags=reference_flags | re.I)


def test_all_occurancies_are_replaced():
    rule = Rule(pattern='(a|b)', replacement=r'\1c')
    assert rule.apply('aab') == 'acacbc'


@patch('richtypo.Richtypo._get_ruleset_rules')
def test_build_rule_chain(rules):
    r = Richtypo()
    r.available_rules = {
        'b': Rule(pattern='b', replacement='d')
    }

    with patch('richtypo.Richtypo._get_ruleset_rules') as rules:
        rules.return_value = ['b', ABRule]

        r.build_rule_chain('generic')
        assert len(r.rules) == 2


@patch('richtypo.Richtypo._get_ruleset_rules')
def test_ruleset_input_param(get_ruleset):
    get_ruleset.return_value = [
        ABRule,
    ]
    r = Richtypo(ruleset='generic')  # this ruleset realy should exist
    assert len(r.rules) == 1
    assert ABRule in r.rules


def test_rule_loading_by_default():
    r = Richtypo()
    assert len(r.available_rules.keys()) >= 1
