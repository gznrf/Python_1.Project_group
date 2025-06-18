from test import test_storage

def __main__():
    storage_test = test_storage.test()
    result = storage_test.first_test()
    print(result, 123)
