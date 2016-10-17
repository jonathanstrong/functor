from functor import functor
from toolz import compose, curry
import numpy as np

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
    assert b.one == 1
    assert b.add(1) == 2
    assert b.times2(1) == 4
    assert b.mul(10, 10) == 100
    assert b.times3(10) == 30
    assert b.curry_compose(1) == 8
    assert b.use_param() == 2
    assert use_local_name() == 1
    assert b.use_local_name() == 2

#def test_default_init():
#
#    @functor
#    def B():
#
#        def get_args(self):
#            return self.args, self.kwargs 
#        
#        return locals()
#
#    b = B()
#
#    args, kwargs = b.get_args()
#
#    assert args == ()
#    assert kwargs == {}
#
#    b = B(1, 2, 3, a=1)
#
#    args, kwargs = b.get_args()
#
#    assert np.allclose(args, [1,2,3])
#    assert kwargs == {'a': 1}


