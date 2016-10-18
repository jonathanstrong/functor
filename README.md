Functor
-------

Implements a function-object pattern in Python. 

Inspired by Toby Ho's [prototype.py](https://github.com/airportyh/misc/tree/master/prototype.py), the `functor` decorator let you define variables and functions in an isolated scope with a great deal of flexibility.

The main advantages to this are 1) readability: at some point you realize `self.` this and `self.` that is somewhat annoying, and 2) all the encapsulation of a class with none of the state. 

Initially I found it frustrating to try to mimic this pattern in Python. The key is having the decorated function `return locals()`. In a way, this is very Pythonic because it's explciit. 

However, be warned: without returning `locals`, the decorator **will not work**.  

Quick example:

```python

@functor
def f(a, b):
    c = 3

    def d():
        return a + c

    def __call__(e):
        return a + b + c + d() + e

    return locals()

g = f(1, 2)
g.a     # -> 1
g.d()   # -> 4
g(5)    # -> 1 + 2 + 3 + (1 + 3) + 5 = 14
```

Each instantiated function-object has its own local scope, like you'd expect (but was one of the more difficult aspects to implement). 

```python

@functor
def f(x):
    def y():
        return x

one = f(x=1)
one.y()     # -> 1
two = f(x=2)
two.y()     # -> 2
one.y()     # -> still 1
```

Rules:

- The decorated function **must** return `locals()`. Without this step, the decorator does not work. Returning locals just means returning a call to the global built-in `locals`:

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

Extended example: 

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
