import re


class Rule(object):
    def __init__(self, regex, replacement):
        self.regex = re.compile(regex)
        self.replacement = replacement

    def apply(self, text):
        return self.regex.sub(self.replacement, text)
