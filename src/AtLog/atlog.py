import asyncio
import logging
from functools import wraps
from inspect import getfile, getsourcelines, signature

__all__ = ["get_representation", "log_func"]


def get_representation(arg):
    if type(arg).__repr__ is not object.__repr__:
        return repr(arg)
    elif type(arg).__str__ is not object.__str__:
        return str(arg)
    else:
        return repr(arg)


def log_func(logger: logging.Logger):
    def decorator(func):
        def log_call(f, *args, **kwargs):
            args_repr = [get_representation(a) for a in args]
            kwargs_repr = [f"{k}={get_representation(v)}" for k, v in kwargs.items()]
            function_signature = f"{f.__name__}{signature(f)}"
            arguments = ", ".join(args_repr + kwargs_repr)
            logger.debug(f"Calling {function_signature}")
            logger.debug(
                f"{f.__name__} is defined in {getfile(f)} on line {getsourcelines(f)[-1]}"
            )
            logger.debug(f"Arguments: {arguments}")

        def log_result(f, r):
            logger.debug(f"{f.__name__} returned {get_representation(r)}")

        @wraps(func)
        def wrapper(*args, **kwargs):
            log_call(func, *args, **kwargs)
            result = func(*args, **kwargs)
            log_result(func, result)
            return result

        @wraps(func)
        async def coro_wrapper(*args, **kwargs):
            log_call(func, *args, **kwargs)
            result = await func(*args, **kwargs)
            log_result(func, result)
            return result

        if asyncio.iscoroutinefunction(func):
            return coro_wrapper
        else:
            return wrapper

    return decorator
