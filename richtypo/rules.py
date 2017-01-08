import re
import yaml
import six


class Rule(object):
    def __init__(self, regex, replacement):
        self.regex = re.compile(regex)
        self.replacement = replacement

    def apply(self, text):
        return self.regex.sub(self.replacement, text)


def load_rules_from(path):
    with open(path) as f:
        for rule_name, rule in six.iteritems(yaml.safe_load(f)):
            yield rule_name, Rule(
                regex=rule['regex'],
                replacement=rule['replacement']
            )
