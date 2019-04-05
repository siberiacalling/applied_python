from functools import wraps
import time
from datetime import timedelta
import types


def profile_func(func, class_name=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_of_working = timedelta.total_seconds(timedelta(end - start))
        if class_name:
            print(class_name, end=" ")
        print(func.__name__, "started")
        if class_name:
            print(class_name, end=" ")
        print(func.__name__, "finished in", time_of_working, "\n")
        return result

    return wrapper


def profile_class(my_class):
    print()
    for attr_name in my_class.__dict__:
        attr = getattr(my_class, attr_name)
        if callable(attr):
            attr = profile_func(attr, class_name=my_class.__name__)
            setattr(my_class, attr_name, attr)
    return my_class


def profile(obj):
    if isinstance(obj, types.FunctionType):
        obj = profile_func(obj)
    elif isinstance(obj, type):
        obj = profile_class(obj)
    return obj
