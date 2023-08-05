from contextlib import AbstractContextManager
from timeit import default_timer
from logging import getLogger, Logger
from typing import List, Callable, Any


class CodeBlockTimer(AbstractContextManager):

    def __init__(
            self,
            metric_name: str,
            logging: bool = True,
            logger: Logger = getLogger(__name__),
            handlers: List[Callable[[float], Any]] = None,
    ):
        self.metric_name = metric_name
        self.start_time = None
        self.logger = logger
        self.logging = logging
        self.handlers = handlers if handlers else []

    def __enter__(self):
        self.start_time = default_timer()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        assert self.start_time is not None
        delta_time = default_timer() - self.start_time

        if self.logging:
            self.logger.info(f'Finished timing for {self.metric_name} in {delta_time}s.')

        for handler in self.handlers:
            handler(metric_name=self.metric_name, time=delta_time)
