import richtypo

try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache


__all__ = ['filter']


@lru_cache(maxsize=128)
def _get_typograph(ruleset):
    return richtypo.Richtypo(ruleset)


def filter(value, ruleset='generic'):
    r = _get_typograph(ruleset)
    return r.richtypo(value)
