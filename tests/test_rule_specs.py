# -*- coding: utf-8
import six

from richtypo.rules import SPECIAL_CHARACTERS_MAP


def _replace_unicode_back_to_special_characters(unicode_input):
    """
    Translate the output of richtypo to the language used in rule files,
    e.g. translate ` ` (non-breakable space) to `_`
    """
    for k, v in six.iteritems(SPECIAL_CHARACTERS_MAP):
        unicode_input = unicode_input.replace(v, k)

    return unicode_input


def test_rule_specs(rule_name, rule):
    for spec in rule.specs:
        (input, expected) = spec.split('|')
        got = rule.apply(input)
        got = _replace_unicode_back_to_special_characters(got)

        assert got == expected, 'Rule: %s, Pattern: %s' % (rule_name, rule.pattern)
