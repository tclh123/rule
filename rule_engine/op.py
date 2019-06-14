# coding: utf-8

import re
import operator
from fnmatch import fnmatch

import six


_ops = {}


def register(aliases=None):
    aliases = aliases or []
    if isinstance(aliases, six.string_types):
        aliases = [aliases]

    def _(cls):
        if not cls.name:
            cls.name = cls.__name__
        _aliases = aliases + [cls.name, cls.name.lower()]
        _op = cls()
        _ops.update({a: _op for a in _aliases})
        return cls
    return _


class Op(object):
    name = ''

    def __call__(self, context, *args):
        # NOTE: always try the first arg as var
        var = args[0]
        if isinstance(var, six.string_types):
            try:
                var = context.get(var, var)
            except Exception:
                pass
        return self.calc(context, var, *args[1:])

    def calc(self, context, *args):
        name = self.name.lower()
        searches = ['__%s__', '%s', '%s_']
        for s in searches:
            func = getattr(operator, s % name, None)
            if func:
                break
        return func(*args)


@register()
class Var(Op):
    def __call__(self, context, *args):
        return self.calc(context, *args)

    def calc(self, context, *args):
        context = context or {}
        return context.get(args[0])


@register('=')
class Eq(Op):
    pass


def quick_op(name, aliases=None):
    class _(Op):
        pass
    _.name = name
    _ = register(aliases)(_)
    return _


simple_ops = [
    ('lt', '<'),
    ('le', '<='),
    ('ne', '!='),
    ('ge', '>='),
    ('gt', '>'),

    ('not', '!'),
    ('and', '&'),
    ('or', '|'),
    ('xor', '^'),
    ('inv', '~'),
    ('lshift', '<<'),
    ('rshift', '>>'),

    ('add', '+'),
    ('sub', '-'),
    ('neg', None),
    ('mul', '*'),
    ('pow', '**'),
    ('div', '/'),
    ('floordiv', '//'),
    ('truediv', None),
    ('mod', '%'),

    ('is', None),
    ('is_not', None),

    ('abs', None),

    ('concat', None),

    ('contains', None),
    ('getitem', None),
]


[quick_op(name, aliases) for name, aliases in simple_ops]


@register()
class In(Op):
    def calc(self, context, *args):
        return args[0] in args[1:]


@register()
class Startswith(Op):
    def calc(self, context, *args):
        return args[0].startswith(args[1])


@register()
class Endswith(Op):
    def calc(self, context, *args):
        return args[0].endswith(args[1])


@register()
class Num(Op):
    def calc(self, context, *args):
        try:
            return int(args[0])
        except Exception:
            return float(args[0])


@register()
class String(Op):
    def calc(self, context, *args):
        return str(args[0])


@register()
class Lower(Op):
    def calc(self, context, *args):
        return args[0].lower()


@register()
class Upper(Op):
    def calc(self, context, *args):
        return args[0].upper()


@register()
class Split(Op):
    '''split(sep=None, maxsplit=-1)'''
    def calc(self, context, *args):
        return args[0].split(*args[1:])


@register()
class Match(Op):
    def calc(self, context, *args):
        return fnmatch(args[0], args[1])


@register()
class Regex(Op):
    def calc(self, context, *args):
        return bool(re.match(args[1], args[0]))


def get_op(name):
    return _ops.get(name)


if __name__ == '__main__':
    print(_ops)
