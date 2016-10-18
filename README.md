Functor
-------

Implements a function-object pattern in Python. 

Inspired by Toby Ho's [prototype.py](https://github.com/airportyh/misc/tree/master/prototype.py), the `functor` decorator let you define variables and functions in a local scope with a lot of flexibility. (Maybe too much, we'll see.)

Quick example:

```python

@functor
def A(x, y):
    def z():
        return x * y
    return locals()

a = A(2, 2)
a.x     # -> 2
a.z()   # -> 4
```

Each instantiated function-object has its own local scope, like you'd expect:

```python

b = A(4, 4)
b.x     # -> 4
a.x     # -> 2
```

Rules:

- The decorated function **must** return `locals()`. Without this step, the decorator does not work. For example:

  ```python
  @functor
  def a():
    def square(x):
      return x * x
    return locals()
  ```
- If you define a `__call__` function in the body of a `functor`-decorated function, the object returned from the initial call is itself callable. Unlike the magic `__call__`, there is no `self` to speak of; the function is like a `staticmethod` method.   
  
  Example:
  
  ```python
  @functor
  def add(x, y):
      def __call__(z):
          return x + y + z
  
  a = add(1, 1)
  a(1) # -> 3
  ```

Example use: 

```python
from functor import functor
from toolz import compose, curry

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
    
    def use_arg():
        return x * 2
    
    def use_local_name():
        return 2
        
    return locals()

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
```
