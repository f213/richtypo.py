
def pytest_generate_tests(metafunc):
    """
    Generate tests for ruledefs in yaml files according to their specs defined in-place
    """
    if 'rule_name' in metafunc.fixturenames:
        from richtypo.rules import load_from_file
        rules = []
        for ruledef in ['generic', 'ru', 'en']:
            rules += [(name, rule) for name, rule in load_from_file(ruledef)]

        metafunc.parametrize('rule_name, rule', rules)
