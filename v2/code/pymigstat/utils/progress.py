import os
from math import floor
import timeit

os.system('color')


def format_duration(total_seconds: float):
    if total_seconds > 3600:
        total_minutes = total_seconds / 60
        return f"{floor(total_minutes / 60)}h:{round(total_minutes % 60)}m"
    if total_seconds > 60:
        return f"{floor(total_seconds / 60)}m:{round(total_seconds % 60)}s"

    return f"{total_seconds:.2f}s"


class Progress:
    def __init__(self, total_items: int, label: str = None):
        self._total_items = total_items
        self.label = label
        self._completed = 0
        self._start_time = timeit.default_timer()

    def update(self):
        self._completed += 1
        elapsed_time = timeit.default_timer() - self._start_time
        part_done = self._completed / self._total_items
        part_remains = 1 - part_done
        estimated_time = part_remains * (elapsed_time / part_done)
        message = f"{self.label}: {self._completed} of {self._total_items} ({part_done:.2%}) " \
                  f"done in {format_duration(elapsed_time)}. " \
                  f"Estimating {format_duration(estimated_time)} more."
        print(message)
