from prototype import constructor
import inspect
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

def static(fn):
    """for some reason the builtin staticmethod 
    only seems to work as a decorator, not when
    called on a function manually, hence this"""
    def inner(self, *args, **kwargs):
        return fn(*args, **kwargs)
    return inner

def arg_names(f):
    try:
        return inspect.getargspec(f)[0]
    except TypeError:
        return inspect.getargspec(f.__call__)[0]

def is_magic_method(name):
    return name.startswith('__') and name.endswith('__')

def default_init(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs

def functor(func):
    attrs = func()
    if 'init' not in attrs:
        logger.warning('creating default init function from functor.default_init')
        attrs['init'] = default_init
    cls = constructor(attrs['init'])
    del attrs['init']
    cls.__name__ = func.__name__
    for name in attrs.keys():
        if callable(attrs[name]):
            args = arg_names(attrs[name])
            if len(args) < 1 or args[0] != 'self':
                logger.warning('converting function "{}" to a staticmethod'.format(name))
                attrs[name] = static(attrs[name])
            if is_magic_method(name):                
                setattr(cls, name, attrs[name])
            else:    
                setattr(cls.prototype, name, attrs[name])
        else:
            setattr(cls.prototype, name, attrs[name])
    return cls
