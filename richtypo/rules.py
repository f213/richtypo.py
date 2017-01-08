import re

import six
import yaml

SPECIAL_CHARACTERS_MAP = {  # defines a key-value for unicode replacement characters, used in YAML
    '_': u'\u00A0'          # Test_Phrase maps to Test&nbsp;Phrase for example
}


class Rule(object):
    def __init__(self, regex, replacement, specs=[]):
        self.regex = re.compile(regex)
        self.replacement = self._prepare_replacement(replacement)
        self.specs = specs

    def apply(self, text):
        return self.regex.sub(self.replacement, text)

    def _prepare_replacement(self, replacement):
        """
        Unicode non-breaking spaces are marked as '_' in the config
        """
        return replacement.translate(str.maketrans(SPECIAL_CHARACTERS_MAP))


def load_rules_from(path):
    with open(path) as f:
        for rule_name, rule in six.iteritems(yaml.safe_load(f)):
            yield rule_name, Rule(
                regex=rule['regex'],
                replacement=rule['replacement'],
                specs=rule.get('specs')
            )
