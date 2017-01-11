from richtypo import Richtypo


def filter(value, ruleset='generic'):
    r = Richtypo(ruleset=ruleset)
    return r.richtypo(value)
