# -*- coding: utf-8
import re

import six
import yaml

try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans


SPECIAL_CHARACTERS_MAP = {  # defines a key-value for unicode replacement characters, used in YAML
    '_': six.u(' ')          # Test_Phrase maps to Test&nbsp;Phrase for example
}


class Rule(object):
    def __init__(self, regex=None, replacement=None, specs=[]):
        if regex is not None:
            self.regex = re.compile(regex)

        if replacement is not None:
            self.replacement = self._prepare_replacement(replacement)

        self.specs = specs

    def apply(self, text):
        return self.regex.sub(self.replacement, text)

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
    regex = re.compile('a')
    replacement = 'b'


def load_rules_from(path):
    with open(path, 'rb') as f:
        for rule_name, rule in six.iteritems(yaml.load(f)):
            yield rule_name, Rule(
                regex=rule['regex'],
                replacement=rule['replacement'],
                specs=rule.get('specs')
            )
