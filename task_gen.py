from abc import ABC, abstractmethod

import numpy as np

from task import Task, TaskSet

def uunifast(n: int, u_sum: float) -> list[float]:
    utilizations = []
    sumU = u_sum
    for i in range(1, n):
        nextSumU = sumU * np.power(np.random.uniform(), (1 / (n - i)))
        utilizations.append(sumU - nextSumU)
        sumU = nextSumU
    utilizations.append(sumU)
    return utilizations

class PeriodGenerator(ABC):
    @abstractmethod
    def generate(self, n: int, min_period: int, max_period: int) -> list[int]:
        pass

class DeadlineGenerator(ABC):
    @abstractmethod
    def generate(self, period: int, wcet: int) -> int:
        pass

class TaskGenerator(ABC):
    @abstractmethod
    def generate(self, id: int, period: int, deadline: int, wcet: int) -> Task:
        return Task(id, period, deadline, wcet)
    
def generate_taskset(
    n: int,
    u_sum: float,
    min_period: int,
    max_period: int,
    period_generator: PeriodGenerator,
    deadline_generator: DeadlineGenerator,
    task_generator: TaskGenerator
) -> TaskSet:
    utilizations = uunifast(n, u_sum)
    periods = period_generator.generate(n, min_period, max_period)
    tasks = set()
    for i in range(n):
        wcet = int(np.round(utilizations[i] * periods[i]))
        if wcet == 0:
            wcet = 1
        deadline = deadline_generator.generate(periods[i], wcet)
        tasks.add(task_generator.generate(i, periods[i], deadline, wcet))
    task_set = TaskSet(tasks)
    return task_set
