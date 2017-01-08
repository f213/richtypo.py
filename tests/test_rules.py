from richtypo.rules import Rule
from richtypo import Richtypo


def test_rule_generic():
    r = Rule(
        regex='b{2}',
        replacement='c'
    )
    assert r.apply('abb') == 'ac'


def test_rule_generic_no_match():
    r = Rule(
        regex='b{2}',
        replacement='c'
    )
    assert r.apply('acc') == 'acc'


def test_rule_applying():
    r1 = Rule(
        regex='b{2}',
        replacement='cc'
    )
    r2 = Rule(
        regex='c{2}',
        replacement='dd'
    )

    r = Richtypo(rules=[r1, r2])
    r.text = 'abb'
    r.apply_rules()

    assert r.text == 'add'


def test_rule_order():
    """
    Check if rules are applyied in order they are supplied
    """
    r1 = Rule(
        regex='b{2}',
        replacement='cc'
    )
    r2 = Rule(
        regex='c{2}',
        replacement='dd'
    )
    r = Richtypo(rules=[r2, r1])  # r2 works only after r1
    r.text = 'abb'
    r.apply_rules()

    assert r.text == 'acc'  # so the text should not be changed
