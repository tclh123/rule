# Rule

A rule engine written in python.

The rule is a json/yaml string or python object of a list expression.
The expression is like `[op, arg0, arg1, ..., argn]`, the `op` is the operator,
and `arg0..n` is the arguments for the operator. Any argument can be another expression.

For writing convenience, the first argument will be tried to resolve as the context parameter.
Or, you can just use the special `var` operator to indicate the context parameter.

## Installing

```bash
pip install rule
```

## Usage

```python
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
```


See [rule/op.py](rule/op.py) for more supported operators.

## Development

```
make init
# make install
make test
```

## License

http://tclh123.mit-license.org/

