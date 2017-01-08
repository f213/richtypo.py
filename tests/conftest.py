import os


def pytest_generate_tests(metafunc):
    """
    Generate tests for ruledefs in yaml files according to their specs defined in-place
    """
    if 'rule_name' in metafunc.fixturenames:
        from richtypo.rules import load_rules_from
        for ruledef in ['generic']:
            metafunc.parametrize(
                'rule_name, rule',
                load_rules_from(os.path.join('rules', '%s.yaml' % ruledef))
            )
