import re


class Richtypo(object):
    text = ''

    save_tags_re = [
        re.compile(r'<([^\>]+)>'),
    ]

    def __init__(self, text=''):
        self.text = text
        self.saved_tags = []

    def strip_tags(self):
        replacement_count = 0

        def repl(m):
            nonlocal replacement_count  # TODO: migrate to py2

            tag = m.group(1)
            self.saved_tags.append(tag)

            replacement_count += 1
            return '<%d>' % replacement_count

        for re_num, regex in enumerate(self.save_tags_re):
            self.text = regex.sub(repl, self.text)

    def restore_tags(self):
        restore_tags = re.compile(r'<(\d+)>')

        self.text = restore_tags.sub(lambda f: '<%s>' % self.saved_tags.pop(0), self.text)
