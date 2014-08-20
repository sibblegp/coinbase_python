import collections

try:
    stringtype = basestring  # python 2
except:
    stringtype = str  # python 3


def coerce_to_list(x):
    if isinstance(x, stringtype):
        return x.replace(',', ' ').split()
    return x or []


def namedtuple(name, args=None, optional=None):
    args = coerce_to_list(args)
    optional = coerce_to_list(optional)
    x = collections.namedtuple(name, args + optional)
    if hasattr(x.__new__, 'func_defaults'):  # python 2
        x.__new__.func_defaults = tuple([None] * len(optional))
    elif hasattr(x.__new__, '__defaults__'):  # python 3
        x.__new__.__defaults__ = tuple([None] * len(optional))
    else:
        raise Exception('???')
    return x


def optional(fn):
    def opt(x):
        if x is not None:
            return fn(x)
    return opt
