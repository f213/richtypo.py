import six

from richtypo import Richtypo
from richtypo.rules import load_rules_for

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


def test_rule_loader():
    rules = dict(load_rules_for('generic'))

    assert len(rules.keys()) >= 1

    rule = rules['cleanup_before']
    assert rule.pattern == '\s+'
    assert rule.replacement == ' '


def test_rule_loader_with_non_breaking_spaces():
    rules = dict(load_rules_for('generic'))

    nbsp = rules['nbsp']
    assert nbsp.replacement == six.u(' ')  # todo make it working for py2


@patch('richtypo.Richtypo._get_ruleset')
def test_loading_generic_ruledef(get_ruleset):
    """
    If not specified, all rules should be taken from the generic ruledef (rules/generic.yaml)
    """
    get_ruleset.return_value = ['one', 'two']

    with patch('richtypo.Richtypo.build_rule_chain'):  # dont actualy build rule chain
        with patch('richtypo.Richtypo.load_ruledef') as load_ruledef:
            Richtypo()
            assert load_ruledef.call_count == 1
            load_ruledef.assert_called_with('generic')


@patch('richtypo.Richtypo._get_ruleset')
def test_loading_specified_ruledef(get_ruleset):
    """
    Check for loading specified ruledef

    ruledefs are specified when constructing a ruleset, like this:
        ruledef: rulename

    """
    get_ruleset.return_value = ['ru: test']

    with patch('richtypo.Richtypo.build_rule_chain'):  # dont actualy build rule chain
        with patch('richtypo.Richtypo.load_ruledef') as load_ruledef:
            Richtypo()
            assert load_ruledef.call_count == 1
            load_ruledef.assert_called_with('ru')


@patch('richtypo.Richtypo._get_ruleset')
def test_loading_ruledef_only_once(get_ruleset):
    """
    Check if ruledefs are loaded only once
    """
    get_ruleset.return_value = ['ru:test', 'tst-ruledef:test', 'ru:test1', 'ru:test2']

    with patch('richtypo.Richtypo.build_rule_chain'):  # dont actualy build rule chain
        with patch('richtypo.Richtypo.load_ruledef') as load_ruledef:
            Richtypo()
            assert load_ruledef.call_count == 2  #
            load_ruledef.assert_any_call('ru')
            load_ruledef.assert_any_call('tst-ruledef')
