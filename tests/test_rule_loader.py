# -*- coding: utf-8

from richtypo import Richtypo
from richtypo.rules import load_from_file

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


def test_rule_loader():
    rules = dict(load_from_file('generic'))

    assert len(rules.keys()) >= 1

    rule = rules['cleanup_before']
    assert rule.pattern == '\s+'
    assert rule.replacement == ' '


def test_rule_loader_with_non_breaking_spaces():
    rules = dict(load_from_file('generic'))

    nbsp = rules['nbsp']
    assert nbsp.replacement == u'\xa0'


@patch('richtypo.Richtypo._get_ruleset_rules')
def test_loading_generic_ruledef(rules):
    """
    If not specified, all rules should be taken from the generic ruledef (rules/generic.yaml)
    """
    rules.return_value = ['one', 'two']

    with patch('richtypo.Richtypo.build_rule_chain'):  # dont actualy build rule chain
        with patch('richtypo.Richtypo._load_rules_from_file') as loader:
            Richtypo()
            assert loader.call_count == 1
            loader.assert_called_with('generic')


@patch('richtypo.Richtypo._get_ruleset_rules')
def test_loading_specified_ruledef(get_ruleset):
    """
    Check for loading specified ruledef

    ruledefs are specified when constructing a ruleset, like this:
        ruledef: rulename

    """
    get_ruleset.return_value = ['ru: test']

    with patch('richtypo.Richtypo.build_rule_chain'):  # dont actualy build rule chain
        with patch('richtypo.Richtypo._load_rules_from_file') as loader:
            Richtypo()
            assert loader.call_count == 1
            loader.assert_called_with('ru')


@patch('richtypo.Richtypo._get_ruleset_rules')
def test_loading_ruledef_only_once(get_ruleset):
    """
    Check if ruledefs are loaded only once
    """
    get_ruleset.return_value = ['ru:test', 'tst-ruledef:test', 'ru:test1', 'ru:test2']

    with patch('richtypo.Richtypo.build_rule_chain'):  # dont actualy build rule chain
        with patch('richtypo.Richtypo._load_rules_from_file') as loader:
            Richtypo()
            assert loader.call_count == 2  #
            loader.assert_any_call('ru')
            loader.assert_any_call('tst-ruledef')
