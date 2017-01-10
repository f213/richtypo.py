# -*- coding: utf-8
from richtypo import Richtypo
from richtypo.rules import NBSP


def test_russian_simple():
    r = Richtypo(ruleset='ru-lite')
    text = u'Из-под топота копыт'
    assert r.richtypo(text) == u'Из-под%sтопота копыт' % NBSP


def test_unicode_with_ascii_only_characters():
    """
    If this test does not fail, and the above test is failing
    then i've messed up with unicode
    """
    r = Richtypo(ruleset='en-lite')
    text = u'2 to 3'
    assert r.richtypo(text) == u'2 to%s3' % NBSP
