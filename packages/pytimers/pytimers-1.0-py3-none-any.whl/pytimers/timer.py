from abc import ABC, abstractmethod
from typing import Callable, List, Any
from logging import Logger, getLogger
from timeit import default_timer
import random
import string


class Timer(ABC):

    @abstractmethod
    def __init__(
        self,
        logging: bool = True,
        logger: Logger = getLogger(__name__),
        exec: List[Callable[[float], Any]] = None,
    ):
        pass


class TimerDecorator(ABC):

    def __init__(
            self,
            callable_object: Callable[..., Any] = None,
            logging: bool = True,
            logger: Logger = getLogger(__name__),
            exec: List[Callable[[float], Any]] = None,
    ):
        if callable_object is not None:
            # called as @decorator
            return TimeDecoratorHelper(callable_object)
        else:
            # called as @decorator(arg1, arg2, ...)
            pass

    def __call__(self, callable_object: Callable[..., Any]):
        return TimeDecoratorHelper(callable_object)

    def _init(self, *args, **kwargs):
        pass


class TimeDecoratorHelper:

    def __init__(self, callable_object: Callable[..., Any]):
        self.callable_object = callable_object

    def __call__(self, *args, **kwargs) -> Any:
        return self.callable_object(*args, **kwargs)
