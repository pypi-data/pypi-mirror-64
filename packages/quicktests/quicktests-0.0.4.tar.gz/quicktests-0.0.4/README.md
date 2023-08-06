# quicktests

A library for python for easy testing.

## Example

### Example 1: TestBase
```python
from quicktests import print_report, TestBase


class Test(TestBase):
    def test_one_equals_one(self):
        assert 1 == 1, "One does not equal one"

    def test_one_equals_one_str(self):
        assert "One" == "One", "\"One\" does not equal \"One\""


if __name__ == '__main__':
    print_report(Test())
```

The code above provides the following information:

```
Ran 2 tests.
Running tests took 4.887580871582031e-05 seconds.
No failed tests.
No errors were found. Add more code to verify your code is working.
```

### Example 2: MiniTest

```python
from quicktests import print_report, MiniTest


if __name__ == '__main__':
    def complex_test():
        return False

    print_report(
        MiniTest(
            test_true=[
                lambda: True,
                "Returns True"
            ],
            test_false=[
                lambda: False,
                "Returns False"
            ],
            test_error=[
                lambda: 1 / 0,
                "This is wrong"
            ],
            test_complex=[
                complex_test,
                "This is complex"
            ],
            test_with_really_long_name=[
                lambda: False,
                "This is a long name",
            ]
        )
    )
```

The code above provides the following information:

```
Ran 5 tests.
Running tests took 4.076957702636719e-05 seconds.
4 failed tests:
1. test 'complex':               <class 'AssertionError'> -> This is complex
2. test 'error':                 <class 'ZeroDivisionError'> -> division by zero
3. test 'false':                 <class 'AssertionError'> -> Returns False
5. test 'with really long name': <class 'AssertionError'> -> This is a long name
```