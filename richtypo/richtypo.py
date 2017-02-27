# -*- coding: utf-8
from __future__ import absolute_import

import re
from uuid import uuid4

import six

from richtypo import rules


class Richtypo(object):
    rulesets = {
        'generic': [
            'cleanup_before',
            'emdash-forced',
            'emdash-middle',
            'generic:nbsp',
            'generic:hanging_emdash',
            'generic:punctuation_spaces',
            'generic:spaces_eol',
            'generic:multiple_spaces',
        ],
        'ru-lite': [
            'cleanup_before',
            'emdash-forced',
            'emdash-middle',

            'generic:numbers',

            'ru:hanging_pretexts',
            'ru:hanging_unions',
            'ru:hanging_particles',
            'ru:hanging_pronouns',
            'ru:what_if',
            'ru:year',

            'generic:punctuation_spaces',
            'generic:spaces_eol',
            'generic:multiple_spaces',
            'generic:nbsp',
            'generic:hanging_emdash',
        ],
        'en-lite': [
            'cleanup_before',
            'emdash-forced',
            'emdash-middle',

            'en:hanging_pretexts',
            'en:hanging_articles',
            'en:hanging_pronouns',
            'en:hanging_to_be',
            'en:hanging_numbers',

            'generic:punctuation_spaces',
            'generic:spaces_eol',
            'generic:multiple_spaces',
            'generic:numbers',
            'generic:nbsp',
            'generic:hanging_emdash',
        ],
    }

    bypass_tags = [
        'script',
        'pre',
        'code'
    ]

    def __init__(self, ruleset='generic'):
        self.rules = []
        self.available_rules = {}

        self.init_tag_regexes()

        self.load_rules_for_ruleset(ruleset)
        self.build_rule_chain(ruleset)

    def richtypo(self, text):
        """
        Actualy do the stuff
        """
        self.text = text

        self.strip_tags()
        self.apply_rule_chain()
        self.restore_tags()

        return self.text

    @classmethod
    def _get_ruleset_rules(cls, ruleset):
        """
        Returns an iterable of rules, defined in the particular ruleset.

        Raises KeyError when ruleset is not defined.
        """
        return cls.rulesets[ruleset]

    @classmethod
    def _ruleset_files(cls, ruleset):
        """
        Returns an iterable with rule files, that are required to be loaded
        for the particular ruleset to work.
        """
        ruledefs = []
        for rule in cls._get_ruleset_rules(ruleset):
            if isinstance(rule, six.string_types):  # deal only with non-special rules, defined in YAML
                try:
                    (ruledef, rule_name) = rule.split(':')
                except ValueError:
                    ruledef = 'generic'

                if ruledef not in ruledefs:
                    ruledefs.append(ruledef)

                    yield ruledef

    @classmethod
    def init_tag_regexes(cls):
        """
        Build a list of regexps used by strip_tags()
        """
        cls.strip_tag_regexps = []

        cls.strip_tag_regexps.append(
            re.compile(r'(~+[^~]+~+)')  # strip all ~stuff~ occurences, because this mark is used by richtypo
        )

        for tag in cls.bypass_tags:
            cls.strip_tag_regexps.append(
                re.compile(r'(<%s[^>]*>.+</%s>)' % (tag, tag), flags=re.MULTILINE | re.DOTALL)  # add a regex for every tag in a list of tags to bypass
            )

        cls.strip_tag_regexps.append(
            re.compile(r'(<[^>]+>)')  # generic regex to strip all <tags>
        )

    def _get_rule(self, rule):
        """
        Finds the rule in the list of loaded rules. Raises KeyError if rule is not found.

        Rules are devided into two types — string name (like `'emdash'`) or a class name
        of rule defined in richtypo.rules (like `StripDashes`).

        String rules have prefixes of files, from which they were loaded, i.e. rule
        loaded from `rules/ru.yaml` and called `emdash` can be found by name 'ru:emdash'.
        There is only one exception — you can find rules loaded from `rules/generic.yaml`
        without the 'generic:' prefix, simply `'cleanup_before'`.
        """
        if isinstance(rule, six.string_types):
            try:
                return self.available_rules[rule]
            except KeyError:
                try:
                    return self.available_rules['generic:' + rule]
                except KeyError:
                    raise KeyError('Rule not found:', rule)

        else:
            if issubclass(rule, rules.Rule):
                return rule
            else:
                raise KeyError('Got unkown rule reference', rule)

    def strip_tags(self):
        """
        Replace all tags with ~<tag_num>~
        """
        self.saved_tags = {}

        def repl(m):
            tag = m.group(1)
            uuid = uuid4()
            self.saved_tags[str(uuid)] = tag

            return '~%s~' % uuid

        for regex in self.strip_tag_regexps:
            self.text = regex.sub(repl, self.text)

    def restore_tags(self):
        """
        Restore tags, stripped by strip_tags
        """
        restore_tags = re.compile(r'~(?P<saved_tag_id>[^~]+)~')  # find each tag uuid
        self.text = restore_tags.sub(lambda m: self.saved_tags.pop(m.group('saved_tag_id')), self.text)  # and replace it from self.saved_tags dict

    def apply_rule_chain(self):
        for rule in self.rules:
            self.text = rule.apply(self.text)

    def build_rule_chain(self, ruleset):
        """
        Build rule chain for a particular ruleset

        Will throw KeyError if ruleset is not found.
        """
        self.rules = [self._get_rule(r) for r in self._get_ruleset_rules(ruleset)]

    def load_rules_for_ruleset(self, ruleset):
        """
        Load rule files needed by the particular ruleset
        """
        for ruledef in self._ruleset_files(ruleset):
            self._load_rules_from_file(ruledef)

    def _load_rules_from_file(self, file):
        """
        Load rules from the rule file
        """
        for rule_name, rule in rules.load_from_file(file):
            rule_name = '%s:%s' % (file, rule_name)
            if self.available_rules.get(rule_name) is None:
                self.available_rules[rule_name] = rule
