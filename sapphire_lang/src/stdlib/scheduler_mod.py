"""
Sapphire Scheduler & Delay Standard Library
"""
import time
import threading

class SchedulerModule:
    @staticmethod
    def sleep(seconds: float):
        time.sleep(seconds)

    @staticmethod
    def delay(ms: int):
        time.sleep(ms / 1000.0)

    @staticmethod
    def run_later(seconds: float, callback_fn):
        def _target():
            time.sleep(seconds)
            callback_fn()
        t = threading.Thread(target=_target, daemon=True)
        t.start()
        return t
