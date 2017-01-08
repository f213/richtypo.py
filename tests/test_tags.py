from richtypo import Richtypo
import pytest


@pytest.mark.parametrize("input, expected", [
    ('<h1>test</h1>', '<1>test<2>'),
    ('<h1>тест</h1>', '<1>тест<2>'),
    (r'<h1>test</', r'<1>test</'),
    ('тест', 'тест'),
    ('<!-- h1 -->test</-->', '<1>test<2>'),
    ('<H1>test</H1>', '<1>test<2>'),
    ('<h1>test<h1>', '<1>test<2>'),
    ('<h1><1>test</h1>', '<1><2>test<3>'),
])
def test_strip_tags(input, expected):
    r = Richtypo(input)
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
    r = Richtypo(input)
    r.strip_tags()
    r.restore_tags()
    assert r.text == input
