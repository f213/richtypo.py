# -*- coding: utf-8
import re

import six

from richtypo import Richtypo
from richtypo.rules import ABRule, Rule, load_rules_from


def test_rule_generic():
    r = Rule(
        regex='b{2}',
        replacement='c'
    )
    assert r.apply('abb') == 'ac'


def test_rule_generic_no_match():
    r = Rule(
        regex='b{2}',
        replacement='c'
    )
    assert r.apply('acc') == 'acc'


def test_rule_applying():
    r1 = Rule(
        regex='b{2}',
        replacement='cc'
    )
    r2 = Rule(
        regex='c{2}',
        replacement='dd'
    )

    r = Richtypo()
    r.rules = [r1, r2]
    r.text = 'abb'
    r.apply_rules()

    assert r.text == 'add'


def test_rule_order():
    """
    Check if rules are applyied in order they are supplied
    """
    r1 = Rule(
        regex='b{2}',
        replacement='cc'
    )
    r2 = Rule(
        regex='c{2}',
        replacement='dd'
    )
    r = Richtypo()
    r.rules = [r2, r1]  # r2 works only after r1
    r.text = 'abb'
    r.apply_rules()

    assert r.text == 'acc'  # so the text should not be changed


def test_rule_loader():
    rules = dict(load_rules_from(path='rules/generic.yaml'))

    assert len(rules.keys()) >= 1

    rule = rules['cleanup_before']
    assert rule.regex == re.compile('\s+')
    assert rule.replacement == ' '


def test_rule_loader_with_non_breaking_spaces():
    rules = dict(load_rules_from(path='rules/generic.yaml'))

    nbsp = rules['nbsp']
    assert nbsp.replacement == six.u(' ')  # todo make it working for py2


def test_getrule_from_available():
    r = Richtypo()
    r.available_rules = {
        'b': Rule(regex='b', replacement='d')
    }
    rule = r._getrule('b')

    assert rule.regex == re.compile('b')


def test_getrule_from_predefined_rules():
    r = Richtypo()
    rule = r._getrule(ABRule)

    assert rule == ABRule
