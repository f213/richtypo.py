import re


class Richtypo(object):
    text = ''

    bypass_tags = [
        'script',
        'pre',
        'code'
    ]

    def __init__(self, text, bypass_tags=bypass_tags):
        self.text = text

        self.save_tags_re = []
        for tag in bypass_tags:
            self.save_tags_re.append(self._tag_bypass_regex(tag))

        self.save_tags_re.append(re.compile(r'<([^>]+)>'))  # generic regex to strip all <tags>

        self.saved_tags = []

    def _tag_bypass_regex(self, tag):
        return re.compile(r'<(%s[^>]*>.+</%s)>' % (tag, tag), flags=re.MULTILINE | re.DOTALL)

    def strip_tags(self):
        """
        Replace all tags with ~<tag_num>~
        """
        replacement_count = 0

        def repl(m):
            nonlocal replacement_count  # TODO: make py2-compatible

            tag = m.group(1)
            self.saved_tags.append(tag)
            print(self.saved_tags)

            replacement_count += 1
            return '~%d~' % replacement_count

        for regex in self.save_tags_re:
            self.text = regex.sub(repl, self.text)

    def restore_tags(self):
        """
        Restore tags, stripped by strip_tags
        """
        restore_tags = re.compile(r'~(\d+)~')

        self.text = restore_tags.sub(lambda f: '<%s>' % self.saved_tags.pop(0), self.text)
