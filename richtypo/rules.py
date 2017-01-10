# -*- coding: utf-8
import os
import re

import six
import yaml

try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans


NBSP = u'\xa0'


SPECIAL_CHARACTERS_MAP = {  # defines a key-value for unicode replacement characters, used in YAML

    '_': NBSP               # Test_Phrase maps to Test&nbsp;Phrase
}


class Rule(object):
    flags = []

    def __init__(self, pattern=None, replacement=None, flags=[], specs=[]):
        if flags is not None:
            self.flags = flags

        if pattern is not None:
            self.pattern = pattern

        if replacement is not None:
            self.replacement = self._prepare_replacement(replacement)

        self._re = None
        self.specs = specs

    def apply(self, text):
        if not self._re:
            self._compile()

        return self._re.sub(self.replacement, text)

    def _compile(self):
        """
        One-time compile of the regex
        """
        resulting_re_flags = 0
        if six.PY2:
            resulting_re_flags |= re.UNICODE

        if len(self.flags):
            for flag in self.flags:
                resulting_re_flags |= getattr(re, flag)

        self._re = re.compile(self.pattern, flags=resulting_re_flags)

    def _prepare_replacement(self, replacement):
        """
        Unicode non-breaking spaces are marked as '_' in the config
        """
        for p, r in six.iteritems(SPECIAL_CHARACTERS_MAP):
            replacement = replacement.replace(p, r)
        return replacement


class ABRule(Rule):
    """
    A special rule for testing, replaces all a's in text by b's
    """
    pattern = 'a'
    replacement = 'b'


def load_rules_for(ruledef):
    path = os.path.join('rules', ruledef + '.yaml')
    with open(path, 'rb') as f:
        for rule_name, rule in six.iteritems(yaml.load(f)):
            yield rule_name, Rule(
                pattern=rule['pattern'],
                replacement=rule['replacement'],
                flags=rule.get('flags'),
                specs=rule.get('specs')
            )
