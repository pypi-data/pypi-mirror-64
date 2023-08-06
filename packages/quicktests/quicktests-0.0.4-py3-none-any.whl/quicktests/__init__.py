import time


def check_error(func, *args, **kwargs):
    try:
        func.__call__(*args, **kwargs)
        return None
    except Exception as e:
        return e


def check_statement(statement):
    assert statement.__call__()


# This test class is useful for complex tests
class TestBase:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        return

    def __call__(self, *args, **kwargs):
        results = {}
        # run all functions of this class if they are marked as quicktests by starting with "test_"
        for i, function in enumerate([func for func in dir(self) if func.startswith("test_")]):
            error = check_error(self.__getattribute__(function))
            if error:
                results[function] = error
        return results


# This test class is useful for short and very easy tests
class MiniTest:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, *args, **kwargs):
        results = {}
        for test in [t for t in dir(self) if t.startswith("test_")]:
            try:
                assert self.__getattribute__(test)[0].__call__(), self.__getattribute__(test)[1]
                continue
            except Exception as e:
                results[test] = e
        return results


def get_report(test_object: [MiniTest, TestBase]):
    return test_object()


def print_report(test_object: MiniTest):
    test_names = [x for x in dir(test_object) if x.startswith('test')]
    print(f"Ran {len(test_names)} tests.")
    begin = time.time()
    results = get_report(test_object)
    print(f"Running tests took {time.time() - begin} seconds.")
    print(f"{'No' if not results else len(results)} failed tests{':' if results else '.'}")
    for r in results:
        desc = f"{[x for x in test_names].index(r) + 1}. test '{r[5:].replace('_', ' ')}'"
        hint = f"{str(type(results[r])) + ' -> ' if isinstance(results[r], Exception) else ''}{results[r]}"
        print(desc + ":" + " " * (max([len(n) for n in test_names if n in results]) - len(r)) + " " + hint)
    if not results:
        print("No errors were found. Add more code to verify your code is working.")
