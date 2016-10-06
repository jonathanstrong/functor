Functor
-------

Implements a function-object pattern in Python. 

Most of this (what's in `functor.prototype`) came from Toby Ho's [prototype.py](https://github.com/airportyh/misc/tree/master/prototype.py).

The `functor` decorator builds on this to let you define variables and functions in a local scope with a lot of flexibility. (Maybe too much, we'll see.)

Key points:

- The initialization arguments go in init, not in the top-level function declaration:
  ```
      @functor
      def a():
        def init(self, a):
          self.a = a
  ```

  If init is not defined, the following default is used: 

  ```
      def default_init(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
  ```
- The decorated function **must** return `locals()`. Without this step, the decorator does not work. For example:

  ```
      @functor
      def a():
        def square(x):
          return x * x
        return locals()
  ```
- Any `callable` defined in the decorated function may *optionally* call `self` as its first argument. If it does not call `self` (the actual string "self" is compared against the name of the first argument), the function is converted into a `staticmethod`. The reason to call `self` is to access object state via `self`.
- The resulting object becomes callable by defining a `__call__` function, which, like other functions, may optionally call `self` as its first argument. Other Python magic methods are available like this in theory but have not been tested. 

Example use: 

```
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
```
