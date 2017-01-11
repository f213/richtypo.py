# -*- coding: utf-8
from richtypo.filter import filter


def test_filter():
    from richtypo.rules import NBSP
    got = filter(u'Из-под топота копыт', 'ru-lite')
    assert got == u'Из-под%sтопота копыт' % NBSP


def test_filter_with_default_ruleset():
    got = filter(u'a -- b')
    assert got == u'a — b'
