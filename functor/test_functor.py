from functor import functor, static, pure, readable
from toolz import compose, curry
import numpy as np
import pytest

def use_local_name():
    return 1
  
@functor
def a(x):
    one = 1 
    
    def add(n):
        return one + n
    
    times2 = compose(lambda x: x * 2, add)
    
    @curry
    def mul(a, b):
        return a * b
    
    times3 = mul(3)
    
    curry_compose = compose(mul(4), add)
    
    def use_param():
        return x * 2
    
    def use_local_name():
        return 2

    return locals()


def test_basic_functionality():
    b = a(1)
    assert b.add(1) == 2
    assert b.times2(1) == 4
    assert b.mul(10, 10) == 100
    assert b.times3(10) == 30
    assert b.curry_compose(1) == 8
    assert b.use_param() == 2
    assert use_local_name() == 1
    assert b.use_local_name() == 2


def test_magic___call___method():

    @functor
    def One(x, y):
        def __call__(z):
            return x + y + z
        return locals()
    
    one = One(1, 1)

    #import pdb; pdb.set_trace()

    assert one(1) == 3


def test_docs_example():

    @functor
    def f(a, b):
        c = 3

        def d():
            return a + c

        def __call__(e):
            return a + b + c + d() + e

        return locals()

    g = f(1, 2)
    assert g.d() == 4
    assert g(5) == 15

def test_forget_to_return_locals_raises_typeerror():
    @functor
    def add(x):
        def __call__(y):
            return x + y

    with pytest.raises(TypeError):
        _ = add(1)


def test_side_effect_function():

    @functor
    def A():
        one = { 'a': 1 } 

        def side_effect():
            one['a'] = 2

        def get_one():
            return one

        return locals()

    a = A()
    assert a.get_one() == {'a': 1}
    a.side_effect()
    assert a.get_one() == {'a': 2}

def test_d3_style_callable():

    @functor
    def A():
        def one(new_value=None):
            if new_value is not None:
                one.value = new_value
            return one.value

        one(1)

        def square():
            return one() * one()

        def get_one():
            return one()
        return locals()

    a = A()
    assert a.one.value == 1
    assert a.one() == 1
    assert a.square() == 1
    a.one(2)
    assert a.one() == 2
    assert a.get_one() == 2
    assert a.square() == 4

def test_local_variable_not_readable():

    @functor
    def A():
        one = 1

        def square():
            return one * one

        return locals()

    a = A()
    assert not hasattr(a, 'one')
    assert a.square() == 1

def test_pure_gets_memoized():
    import time

    def A(delay):
        one = {'a': 1}
        
        def add(x):
            time.sleep(delay)
            return x + one['a']

        def side_effect():
            one['a'] = 2

        return locals()

    as_pure = pure(A)
    as_functor = functor(A)
    delay = .01
    a = as_pure(delay)
    b = as_functor(delay)
    start = time.time()
    r = a.add(1)
    first_pure = time.time() - start
    assert r == 2
    assert first_pure > delay
    assert b.add(1) == 2

    start = time.time()
    r2 = a.add(1)
    second_pure = time.time() - start
    assert second_pure < delay
    assert r2 == 2

    start = time.time()
    r3 = b.add(1)
    second_functor = time.time() - start
    assert second_functor > delay
    assert r3 == 2

    a.side_effect()
    r4 = a.add(1)
    assert r4 == 2

    b.side_effect()
    r5 = b.add(1)
    assert r5 == 3

def test_pure_functions_called_from_peer_functions_are_memoized():
    import time
    delay = .1

    @pure
    def A():
        def f(x):
            time.sleep(delay)
            return x + 1

        def g(x):
            return f(x)

        return locals()

    a = A()
    start = time.time()
    r1 = a.g(1)
    t1 = time.time() - start
    assert r1 == 2
    assert t1 > delay
    start = time.time()
    r2 = a.g(1)
    t2 = time.time() - start
    assert r2 == 2
    assert t2 < delay

def test_decorators_on_functions_inside_pure_decorated_function():
    """make sure the memoization doesn't treat two functions
    decorated with the same decorator as the same function"""

    def identity(f):
        def inner(*args, **kwargs):
            return f(*args, **kwargs)
        return inner

    @pure
    def A():

        @identity
        def f(x):
            return x

        @identity
        def g(x):
            return x + 1

        return locals()

    a = A()

    assert a.f(1) == 1
    assert a.g(1) == 2
    assert a.f(2) == 2
    assert a.g(2) == 3

def test_readable_allows_access_to_values():

    @readable
    def A():
        one = 1
        return locals()
    a = A()
    assert a.one == 1

def test_showing_monkeypatching_closure_function_is_useless(monkeypatch):
    @pure
    def A():
        def one():
            return 1

        def one_plus_one():
            return one() + 1

        return locals()

    monkeypatch.setattr(A(), 'one', lambda: 2)
    a = A()
    assert a.one() == 1
    monkeypatch.setattr(a, 'one', lambda: 2)
    assert a.one() == 2
    assert a.one_plus_one() == 2



