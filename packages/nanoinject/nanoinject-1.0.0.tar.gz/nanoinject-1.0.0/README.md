# Nanoinject

Nanoinject is a terrifically small and simple dependency injection container
for Python 3.6+. Its' key features:

* Easy enough to use in five minutes.
* Configurable in code or config files.
* Pretty feature complete.

## Installation

`pip install nanoinject`

## Use guide

Dependency injection is a way to achieve [Inversion of Control][ioc]. 

### Use in code

```python
class A:
    value = 42

class B:
    def __init__(self, a):
        self.a = a


c = Container()
c.add('a', lambda c: A())
c.add('b', lambda c: B(c.get('a')))

assert 42 == c.get('b').a.value
```

### Using configuration

It starts with declaring your services in YAML format:

```yaml
values:
  scalar_value: 42

services:
  a:
    class: A
    module: example.a
    dependencies:
      - value:scalar_value

  b:
    class: B
    module: example.b
    dependencies:
      - a
```

And then letting the config object configure the container based on that YAML file:

```python
import os
from nanoinject import Container, Config

class A:
    def __init__(self, value):
        self.value = value

class B:
    def __init__(self, a):
        self.a = a


c = Container()
config = Config.from_yaml_file(os.path.dirname(__file__) + '/services.yaml')
config.config(c)

assert 42 == c.get('b').a.value
```



[ioc]: https://www.martinfowler.com/articles/injection.html