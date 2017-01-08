from __future__ import absolute_import

import re

import six

from richtypo import rules


class Richtypo(object):
    text = ''

    rulesets = {
        'generic': [
            'cleanup_before',
            'emdash-forced',
            'emdash-middle',
            'nbsp',
        ],
    }

    bypass_tags = [
        'script',
        'pre',
        'code'
    ]

    def __init__(self, bypass_tags=bypass_tags, lang=[], ruleset=''):
        self.save_tags_re = []
        self.rules = []
        self.available_rules = {}

        for tag in bypass_tags:
            self.save_tags_re.append(self._tag_bypass_regex(tag))
        self.save_tags_re.append(re.compile(r'<([^>]+)>'))  # generic regex to strip all <tags>

        self.parse_ruleset(ruleset)

        self.saved_tags = []

    def richtypo(self, text):
        self.text = text
        self.strip_tags()
        self.apply_rules()
        self.restore_tags()

        return self.text

    def _tag_bypass_regex(self, tag):
        return re.compile(r'<(%s[^>]*>.+</%s)>' % (tag, tag), flags=re.MULTILINE | re.DOTALL)

    def _get_rule(self, rule):
        if isinstance(rule, six.string_types):
            return self.available_rules[rule]
        else:
            if issubclass(rule, rules.Rule):
                return rule

    @classmethod
    def _get_ruleset(cls, ruleset):
        return cls.rulesets.get(ruleset, [])

    def strip_tags(self):
        """
        Replace all tags with ~<tag_num>~
        """
        replacement_count = {'n': 0}  # we use a dict to replace `nonlocal` keyword for py2

        def repl(m):
            tag = m.group(1)
            self.saved_tags.append(tag)

            replacement_count['n'] += 1
            return '~%d~' % replacement_count['n']

        for regex in self.save_tags_re:
            self.text = regex.sub(repl, self.text)

    def restore_tags(self):
        """
        Restore tags, stripped by strip_tags
        """
        restore_tags = re.compile(r'~(\d+)~')

        self.text = restore_tags.sub(lambda f: '<%s>' % self.saved_tags.pop(0), self.text)

    def apply_rules(self):
        for rule in self.rules:
            self.text = rule.apply(self.text)

    def parse_ruleset(self, ruleset):
        for r in self._get_ruleset(ruleset):
            rule = self._get_rule(r)
            if rule is not None:
                self.rules.append(rule)
