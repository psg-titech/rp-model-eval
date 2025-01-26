import numpy as np

from task import Task
from task_gen import (
    PeriodGenerator,
    DeadlineGenerator,
    TaskGenerator
)

class LogUniformPeriodGenerator(PeriodGenerator):
    def generate(self, n: int, min_period: int, max_period: int) -> list[int]:
        return np.round(np.exp(np.random.uniform(np.log(min_period), np.log(max_period), n))).astype(int).tolist()

class ImplicitDeadlineGenerator1(DeadlineGenerator):
    def generate(self, period: int, wcet: int) -> int:
        return period

class UniformDeadlineGenerator1(DeadlineGenerator):
    def generate(self, period: int, wcet: int) -> int:
        return np.round(np.random.uniform((period + wcet) / 2, period)).astype(int)

class StandardTaskGenerator(TaskGenerator):
    def generate(self, id: int, period: int, deadline: int, wcet: int) -> Task:
        return Task(id, period, deadline, wcet)
