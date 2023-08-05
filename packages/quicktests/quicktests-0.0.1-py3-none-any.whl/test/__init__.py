import time


def check_error(func, *args, **kwargs):
    try:
        func.__call__(*args, **kwargs)
        return None
    except Exception as e:
        return e


# Provide a base class for automated tests
class TestBase:
    def __call__(self, *args, **kwargs):
        errors = {}
        # run all functions of this class if they are marked as test by starting with "test_"
        for function in [func for func in self.__dir__() if func.startswith("test_")]:
            error = check_error(self.__getattribute__(function))
            if error:
                errors[function] = error
        return errors


# Provide human readable tests
class HRTest(TestBase):
    def __call__(self):
        beginning = time.time()
        test_result = super().__call__()
        """
        # run all functions of this class if they are marked as test by starting with "test_"
        for function in [func for func in self.__dir__() if func.startswith("test_")]:
            error = check_error(self.__getattribute__(function))
            if error:
                test_result[function] = error"""

        print(f"Running tests took {time.time() - beginning} seconds.")
        print(f"Ran {len([f for f in self.__dir__() if f.startswith('test_')])} tests.")
        print(f"Found {len(test_result)} error{'s' if len(test_result) != 1 else ''}:")
        if test_result:
            for test in test_result:
                print(f"{test} failed due to {type(test_result[test])} {test_result[test]}")
        else:
            print("No error was found. Add more test to make sure your code works.")
        return bool(test_result)
