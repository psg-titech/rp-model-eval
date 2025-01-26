from itertools import permutations
from random import sample

from task import Task, TaskSet

class RPTaskSet(TaskSet):
    def __init__(self, tasks: set[Task]):
        super().__init__(tasks)
        self.__local_preemptibility: dict[Task, dict[Task, bool]] = {
            ti : {tj: False for tj in tasks} for ti in tasks
        }

    @staticmethod
    def from_task_set(task_set: TaskSet):
        return RPTaskSet(task_set.tasks)

    @property
    def local_preemptibility(self):
        return self.__local_preemptibility

    def set_local_preemptibility(self, ti: Task, tj: Task, preemptible: bool):
        self.local_preemptibility[ti][tj] = preemptible

    def is_locally_preemptible(self, ti: Task, tj: Task) -> bool:
        return self.local_preemptibility[ti][tj]
    
    def is_preemptible(self, ti: Task, tj: Task) -> bool:
        return all(self.is_locally_preemptible(ti, tk) for tk in self.higher_priority_tasks(self.priority(ti)))

    def set_random_local_preemptibility(self, preemptible_rate: float):
        self.__local_preemptibility = {
            ti: {tj: False for tj in self.tasks} for ti in self.tasks
        }
        perm_tasks = permutations(self.tasks, 2)
        perm_num = self.n * (self.n - 1)
        preemptible_num = int(perm_num * preemptible_rate)
        preemptible_pairs = sample(list(perm_tasks), preemptible_num)
        for ti, tj in preemptible_pairs:
            self.set_local_preemptibility(ti, tj, True)
