# -*- coding: utf-8

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
])
def test_strip_tags_simple(input, expected):
    r = Richtypo()
    r.text = input
    r.strip_tags()
    assert r.text == expected


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
    assert r.text == expected


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
])
def test_restore_tags_in_scripts(input):
    r = Richtypo()
    r.text = input

    r.strip_tags()
    r.restore_tags()
    assert r.text == input
