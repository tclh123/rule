# coding: utf-8

import six
import yaml

from rule.op import get_op

__all__ = ['Rule', 'Expr']


def is_simple_type(obj):
    return isinstance(obj, (six.integer_types, float, six.string_types, bool, type(None)))


class Expr(object):
    def __init__(self, rule):
        if not isinstance(rule, list):
            rule = list(rule)

        self.op = None
        self.args = []

        self.build_expr(rule)

    def __str__(self):
        return '%s(%s)' % (self.op.__class__.name, ', '.join(str(arg) for arg in self.args))

    __repr__ = __str__

    def build_expr(self, rule):
        self.op = get_op(rule[0])
        args = rule[1:]
        self.args = [arg if is_simple_type(arg) else Expr(arg) for arg in args]

    def match(self, context):
        args = [arg.match(context) if isinstance(arg, Expr) else arg for arg in self.args]
        return self.op(context, *args)


class Rule(object):
    """
    >>> from rule import Rule
    >>>
    >>> context = dict(a=1, world='hello')
    >>> Rule(['=', ['var', 'a'], 1]).match(context)
    True
    >>> Rule("['=', ['var', 'a'], 1]").match(context)
    True
    >>> Rule(['=', 'a', 1]).match(context)
    True
    >>> Rule(['=', 'hello', 'hello']).match(context)
    True
    >>> Rule(['=', 'world', 'hello']).match(context)
    True
    >>> Rule(['<', 'a', 10]).match(context)
    True
    >>> Rule(['=', ['>', 'a', 10], False]).match(context)
    True
    >>>
    >>> context = dict(ldap_id='Harry', hosts='sa,sb,sc', reason='hehe', nologin=False,
    ...                group='wheel,sysadmin,platform', package='dev-python/sa-tools',
    ...                branch='release', cc='Tony,Mike',)
    >>> Rule(['contains', 'hosts', 'sa,']).match(context)
    True
    >>> Rule(['contains', ['split', 'hosts', ','], 'sa']).match(context)
    True
    >>> Rule(['in', 'branch', 'master', 'release']).match(context)
    True
    >>> Rule(['=', 'ldap_id', 'Harry']).match(context)
    True
    >>> Rule(['match', 'package', 'dev-python/*']).match(context)
    True
    >>> Rule(['regex', 'package', 'dev-python/.*']).match(context)
    True
    >>> Rule(['is', 'nologin', False]).match(context)
    True
    """

    def __init__(self, rule, return_bool=False):
        if isinstance(rule, six.string_types):
            self.rule = yaml.safe_load(rule)
        else:
            self.rule = rule

        self.expr = Expr(self.rule)
        self.return_bool = return_bool

    def __str__(self):
        return 'Rule(rule=%s, expr=%s)' % (self.rule, self.expr)

    __repr__ = __str__

    def match(self, context=None):
        ret = self.expr.match(context or {})
        return bool(ret) if self.return_bool else ret


if __name__ == '__main__':
    context = dict(a=1, world='hello')
    rules = [
        Rule("['=', ['var', 'a'], 1]"),
        Rule(['=', ['var', 'a'], 1]),
        Rule(['=', 'a', 1]),
        Rule(['=', 'hello', 'hello']),
        Rule(['=', 'world', 'hello']),
        Rule(['<', 'a', 10]),
        Rule(['=', ['>', 'a', 10], False]),
        ]
    for r in rules:
        print(r, r.match(context))
        assert r.match(context)

    # test2
    context = dict(ldap_id='Harry', hosts='sa,sb,sc', reason='hehe', nologin=False,
                   group='wheel,sysadmin,platform', package='dev-python/sa-tools',
                   branch='release', cc='Tony,Mike',
                   )
    rules = [
        Rule(['contains', 'hosts', 'sa,']),
        Rule(['contains', ['split', 'hosts', ','], 'sa']),
        Rule(['in', 'branch', 'master', 'release']),
        Rule(['=', 'ldap_id', 'Harry']),
        Rule(['match', 'package', 'dev-python/*']),
        Rule(['regex', 'package', 'dev-python/.*']),
        Rule(['is', 'nologin', False]),
        ]
    for r in rules:
        print(r, r.match(context))
        assert r.match(context)
