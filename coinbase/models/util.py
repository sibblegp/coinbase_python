import collections


def coerce_to_list(x):
    if isinstance(x, basestring):
        return x.replace(',', ' ').split()
    return x or []


def namedtuple(name, args=None, optional=None):
    args = coerce_to_list(args)
    optional = coerce_to_list(optional)
    x = collections.namedtuple(name, args + optional)
    x.__new__.func_defaults = tuple([None] * len(optional))
    return x


def optional(fn):
    def opt(x):
        if x is not None:
            return fn(x)
    return opt
