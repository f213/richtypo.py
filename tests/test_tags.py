# -*- coding: utf-8

import re

import pytest

from richtypo import Richtypo


@pytest.mark.parametrize("input, expected", [
    ('<h1>test</h1>', '~1~test~2~'),
    ('<h1>тест</h1>', '~1~тест~2~'),
    (r'<h1>test</', r'~1~test</'),
    ('тест', 'тест'),
    ('<!-- h1 -->test</-->', '~1~test~2~'),
    ('<H1>test</H1>', '~1~test~2~'),
    ('<h1>test<h1>', '~1~test~2~'),
    ('<h1><1>test</h1>', '~1~~2~test~3~'),
    ('<p>test is a <a class="testclass">test link</a></p>', '~1~test is a ~2~test link~3~~4~'),
])
def test_strip_tags_simple(input, expected):
    r = Richtypo()
    r.text = input
    r.strip_tags()

    expected = re.sub(r'~(\d+)~', '~([^~]+)~', expected)  # it is a regex now
    expected = re.compile(expected)
    assert expected.match(r.text)


@pytest.mark.parametrize("input", [
    '<h1>test</h1>',
    '<h1>тест</h1>',
    '<h1>test</',
    'тест',
    '<!-- h1 -->test</-->',
    '<H1>test</H1>',
    '<h1>test<h1>',
    '<h1><3>test</h1>',
    '<h1><10>test</h1>',
    '<p>test is a <a class="testclass">test link</a></p>',
])
def test_restore_tags(input):
    r = Richtypo()
    r.text = input

    r.strip_tags()
    r.restore_tags()
    assert r.text == input


@pytest.mark.parametrize("input, expected", [
    (
        '<script type="text/javascript">script_code()</script><h1>test</h1>',
        '~1~~2~test~3~'
    ),
    (
        """
        <script type="text/javascript">
            console.log("<script type="text/javascript">alert('test');</script>");
        </script>
        <h1>test<h2>
        """,

        """
        ~1~
        ~2~test~3~
        """
    ),
    (
        """
        <script type="text/javascript">
            scriptcode()
        </script>
        <h1>test</h1>
        """,

        """
        ~1~
        ~2~test~3~
        """
    ),
])
def test_strip_tags_in_scripts(input, expected):
    r = Richtypo()
    r.text = input
    r.strip_tags()

    expected = re.sub(r'~(\d+)~', '~([^~]+)~', expected)  # it is a regex now
    expected = re.compile(expected)
    assert expected.match(r.text)


@pytest.mark.parametrize("input", [
    '<script type="text/javascript">scriptcode()</script><h1>test</h1>',

    """
    <script type="text/javascript">
        console.log("<script type="text/javascript">alert('test');</script>");
    </script><h1>test<h2>
    """,

    """
    <script type="text/javascript">
            script_code()
    </script>
    <h1>test</h1>
    """,
    """
    <p>This is my fancy code:
        <div class="code">
            <code>Test();</code>
        </div>
    </p>
    """,
])
def test_restore_tags_in_scripts(input):
    r = Richtypo()
    r.text = input

    r.strip_tags()
    r.restore_tags()
    assert r.text == input


@pytest.mark.parametrize("input, expected", [
    ('test <h1> ~dff~', 'test <h1> ~dff~'),
    ('test <h1>~~dff~~</h1>', 'test <h1>~~dff~~</h1>'),
    ('test <h1> ~~dff~x~', 'test <h1> ~~dff~x~'),
])
def test_strip_tags_when_input_already_contains_richtypo_marks(input, expected):
    r = Richtypo()
    r.text = input
    r.strip_tags()
    r.restore_tags()
    assert r.text == expected
