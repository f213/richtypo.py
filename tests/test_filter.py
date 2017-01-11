# -*- coding: utf-8
from richtypo.filter import filter

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


@patch('richtypo.filter.richtypo.Richtypo._get_ruleset_rules')
def test_filter_caching(rules):
    rules.return_value = []
    with patch('richtypo.filter.richtypo.Richtypo.load_rules_for_ruleset') as loader:
        for i in range(0, 10):
            filter(u'a -- b', 'some-ruleset') == u'a — b'

        assert loader.call_count == 1  # rules should be loaded from file only once


def test_filter():
    from richtypo.rules import NBSP
    got = filter(u'Из-под топота копыт', 'ru-lite')
    assert got == u'Из-под%sтопота копыт' % NBSP


def test_filter_with_default_ruleset():
    got = filter(u'a -- b')
    assert got == u'a — b'
