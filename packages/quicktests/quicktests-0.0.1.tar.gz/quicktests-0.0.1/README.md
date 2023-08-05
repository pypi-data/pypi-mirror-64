# quicktests

A library for python for easy testing

## Example

```python
from test import HRTest


class Test(HRTest):
    def test_one_equals_one(self):
        assert 1 == 1, "One does not equal one"

    def test_one_equals_one_str(self):
        assert "One" == "One", "\"One\" does not equal \"One\""


if __name__ == '__main__':
    t = Test()
    result = t()
    print(result)
```

The code above provides the following information:

```
Running tests took 5.14984130859375e-05 seconds.
Ran 2 tests.
Found 0 errors:
No error was found. Add more test to make sure your code works.
```