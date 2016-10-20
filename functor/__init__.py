from toolz import curry, memoize
import inspect
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

import types

def copy_func(f, name=None):
    return types.FunctionType(f.func_code, f.func_globals, name or f.func_name,
        f.func_defaults, f.func_closure)

def static(fn):
    """for some reason the builtin staticmethod 
    only seems to work as a decorator, not when
    called on a function manually, hence this"""
    def inner(self, *args, **kwargs):
        return fn(*args, **kwargs)
    return inner

def is_magic_method(name):
    return name.startswith('__') and name.endswith('__')

def identity(x):
    return x

def functor(f):
    def inner(*args, **kwargs):
        f = copy_func(inner.f)

        attrs = f(*args, **kwargs)

        if not(isinstance(attrs, dict)):
            raise TypeError('Functions decorated with @functor must return locals()') 

        if '__call__' in attrs:
            f = copy_func(attrs['__call__'])
            del attrs['__call__']

        for name in attrs.keys():
            if is_magic_method(name):
                raise TypeError('Operation not permitted.')

            if callable(attrs[name]):
                setattr(f, name, attrs[name])
        return f

    inner.f = f
    
    return inner

def readable(f):
    """like functor, but non-callable variables are readable as well. 
    please note that mutating a variable from outside a readble, while
    appearing to work, does not change the value of the variable inside
    the closure of a function defined inside the readable."""
    def inner(*args, **kwargs):
        f = copy_func(inner.f)

        attrs = f(*args, **kwargs)

        if not(isinstance(attrs, dict)):
            raise TypeError('Functions decorated with @functor must return locals()') 

        if '__call__' in attrs:
            f = copy_func(attrs['__call__'])
            del attrs['__call__']

        for name in attrs.keys():
            if is_magic_method(name):
                raise TypeError('Operation not permitted.')

            setattr(f, name, attrs[name])
        return f

    inner.f = f
    
    return inner



def pure(f):
    "like functor, but applies memoize to every function"
    def inner(*args, **kwargs):
        f = copy_func(inner.f)

        attrs = f(*args, **kwargs)

        if not(isinstance(attrs, dict)):
            raise TypeError('Functions decorated with @pure must return locals()') 

        if '__call__' in attrs:
            f = copy_func(attrs['__call__'])
            del attrs['__call__']

        for name in attrs.keys():
            if is_magic_method(name):
                raise TypeError('Operation not permitted.')

            if callable(attrs[name]):
                attrs[name] = memoize(attrs[name])
                setattr(f, name, attrs[name])

        return f

    #inner.f = copy_func(f)
    inner.f = f
    return inner




def arg_names(f):
    try:
        return inspect.getargspec(f)[0]
    except TypeError:
        return inspect.getargspec(f.__call__)[0]

#def default_init(self, *args, **kwargs):
#    self.args = args
#    self.kwargs = kwargs

#def functor(func):
#    attrs = func()
#    if 'init' not in attrs:
#        logger.warning('creating default init function from functor.default_init')
#        attrs['init'] = default_init
#    cls = constructor(attrs['init'])
#    del attrs['init']
#    cls.__name__ = func.__name__
#    for name in attrs.keys():
#        if callable(attrs[name]):
#            args = arg_names(attrs[name])
#            if len(args) < 1 or args[0] != 'self':
#                logger.warning('converting function "{}" to a staticmethod'.format(name))
#                attrs[name] = static(attrs[name])
#            if is_magic_method(name):                
#                setattr(cls, name, attrs[name])
#            else:    
#                setattr(cls.prototype, name, attrs[name])
#        else:
#            setattr(cls.prototype, name, attrs[name])
#    return cls


#class functor3cls(object):
#    def __init__(self, f, *args, **kwargs):
#        attrs = f(*args, **kwargs)
#        for name in attrs.keys():
#            if callable(attrs[name]):
#                setattr(self, name, static(attrs[name]))
#            else:
#                setattr(self, name, attrs[name])
#        self.self = lambda: self
#
#def functor3(f):
#    def inner(*args, **kwargs):
#        self = functor3cls(f, *args, **kwargs)
#        return self
#    return inner





