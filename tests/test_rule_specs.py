import pytest
import six

from richtypo.rules import SPECIAL_CHARACTERS_MAP


def _replace_unicode_back_to_special_characters(unicode_input):
    reverse_map = dict((v, k) for k, v in SPECIAL_CHARACTERS_MAP.items())
    return unicode_input.translate(str.maketrans(reverse_map))


@pytest.mark.skipif(six.PY2, reason="I'm too lazy to make this work on python2")
def test_rule_specs(rule_name, rule):
    for spec in rule.specs:
        (input, expected) = spec.split('|')
        got = rule.apply(input)
        got = _replace_unicode_back_to_special_characters(got)

        assert got == expected, 'Rule: %s' % rule_name
