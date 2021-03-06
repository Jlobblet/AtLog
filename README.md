# AtLog

A simple logging decorator for functions and coroutines.

## Installation

`pip install atlog`

## Usage

It is recommended to create a file-level binding to `log_func` which you then use on the objects you wish to log:

```py
import logging
from atlog import log_func

logging.basicConfig(filename="example.log", level=logging.DEBUG)
logger = logging.getLogger()
log = log_func(logger)

@log
def hello(name):
    return f"Hello, {name}."


class Greeter:
    @log
    def __init__(self, name):
        self.greeting = f"Hello, {name}."

    @log
    def greet(self):
        print(self.greeting)


if __name__ == "__main__":
    print(hello("John"))
    Greeter("John").greet()
```

This will produce the following `example.log`:
```
DEBUG:root:Calling hello(name)
DEBUG:root:hello is defined in path/to/example.py on line 8
DEBUG:root:Arguments: 'John'
DEBUG:root:hello returned 'Hello, John.'
DEBUG:root:Calling __init__(self, name)
DEBUG:root:__init__ is defined in path/to/example.py on line 14
DEBUG:root:Arguments: <__main__.Greeter object at 0x000001E95F84FDF0>, 'John'
DEBUG:root:__init__ returned None
DEBUG:root:Calling greet(self)
DEBUG:root:greet is defined in path/to/example.py on line 18
DEBUG:root:Arguments: <__main__.Greeter object at 0x000001E95F84FDF0>
DEBUG:root:greet returned None
```
