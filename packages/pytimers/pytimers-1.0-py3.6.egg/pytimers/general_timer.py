from timeit import default_timer
import random
import string
from typing import List


class GeneralTimer:

    def __init__(self, random_timer_name_length = 10):
        self._timers = {}
        self.random_timer_name_length = random_timer_name_length

    def create(self, timer_name: str = None) -> str:
        if not timer_name:
            while not self._valid_timer_name(timer_name):
                timer_name = ''.join(
                    ['timer_'] + random.choices(string.ascii_letters + string.digits, k=self.random_timer_name_length)
                )
        elif not self._valid_timer_name(timer_name):
            raise ValueError(f'Timer "{timer_name}" already set.')

        self._timers[timer_name] = default_timer()

        return timer_name

    def _valid_timer_name(self, timer_name: str) -> bool:
        return timer_name and timer_name not in self._timers

    def get(self, timer_name: str) -> float:
        return default_timer() - self._timers[timer_name]

    def reset(self, timer_name: str) -> float:
        time = self.remove(timer_name)
        self.create(timer_name)
        return time

    def remove(self, timer_name: str) -> float:
        time = self.get(timer_name)
        self._timers.pop(timer_name)
        return time

    def timers(self) -> List[str]:
        return list(self.timers().keys())


GlobalTimer = GeneralTimer()
