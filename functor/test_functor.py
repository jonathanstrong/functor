from functor import functor
from toolz import compose, curry

def use_local_name():
    return 1
  
@functor
def a():
    one = 1 
    
    def init(self, x):
        self.two = 2
        self.x = x
        
    def add(n):
        return one + n
    
    times2 = compose(lambda x: x * 2, add)
    
    @curry
    def mul(a, b):
        return a * b
    
    times3 = mul(3)
    
    curry_compose = compose(mul(4), add)
    
    def __call__():
        return 5
    
    def use_param(self):
        return self.x * 2
    
    def use_local_name():
        return 2
        
    return locals()

def test_basic_functionality():
    b = a(1)
    assert b.one == 1
    assert b.two == 2
    assert b.add(1) == 2
    assert b.times2(1) == 4
    assert b.mul(10, 10) == 100
    assert b.times3(10) == 30
    assert b.curry_compose(1) == 8
    assert b() == 5
    assert b.use_param() == 2
    assert use_local_name() == 1
    assert b.use_local_name() == 2
