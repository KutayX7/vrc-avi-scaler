
import time
from collections.abc import Callable
from typing import Any, Self
from threading import Lock, Semaphore, Thread, Timer

type Callback = Callable[..., None]

class Task:
    def __init__(self, name: str) -> None:
        self.name = name
        self.callbacks: list[Callback] = []
        self.args: list[Any] = []
        self.running = False
        self.complete = False
        self.dependencies: list[Self] = []

    def attach_callback(self, callback: Callback) -> Self:
        self.callbacks.append(callback)
        return self

    def add_arg(self, arg: Any) -> Self:
        self.args.append(arg)
        return self

    def add_dependency(self, dependency: Self) -> Self:
        self.dependencies.append(dependency)
        return self

    def can_run(self) -> bool:
        for dependency in self.dependencies:
            if not dependency.complete:
                return False
        return True

    def run(self) -> None:
        if self.running:
            return
        try:
            self.running = True
            for callback in self.callbacks:
                callback(*(self.args))
        except Exception as e:
            raise e
        finally:
            self.running = False
            self.complete = True

class TaskManager:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._deadlines: list[float] = [] # bad naming
        self._lock: Lock = Lock()
        self._semaphore: Semaphore = Semaphore()
        self._start_time = time.monotonic()
        loop_thread = Thread(target=self._loop)
        loop_thread.daemon = True
        loop_thread.start()

    def add_task(self, task: Task, delay: float = 0.0) -> None:
        with self._lock:
            self._tasks.append(task)
            self._deadlines.append(time.monotonic() + delay)
        Timer(delay, self._semaphore.release).start()

    def _loop(self) -> None:
        while True:
            self._semaphore.acquire()
            indices_to_clean: list[int] = []
            with self._lock:
                for i in range(len(self._deadlines)):
                    task = self._tasks[i]
                    deadline = self._deadlines[i]
                    if task.complete:
                        indices_to_clean.append(i)
                        self._semaphore.release()
                        continue
                    if deadline <= time.monotonic() and not task.running:
                        if task.can_run():
                            thread = Thread(target=task.run)
                            thread.daemon = True
                            thread.start()
                for i in reversed(indices_to_clean):
                    self._tasks.pop(i)
                    self._deadlines.pop(i)

task_manager = TaskManager()
