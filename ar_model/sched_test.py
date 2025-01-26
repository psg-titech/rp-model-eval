from math import ceil
from itertools import permutations

from task import TaskSet
from priority import execution_time_monotonic

"""
ARモデルにおける優先度iのタスクのスケジュール可能性検査
"""
def schedulability_test_ar_at(task_set: TaskSet, i: int) -> bool:
    ti = task_set.ordered_tasks[i]
    C = ti.wcet
    D = ti.deadline
    hp = task_set.higher_priority_tasks(i)

    C_ij = {
        tj: tj.wcet + max(
            [tk.wcet for tk in task_set.ordered_tasks[j+1:i+1]],
            default=0
        ) for j, tj in enumerate(hp)
    }

    R = C
    while True:
        R_next = C + sum(
            [ceil(R / tj.period) * C_ij[tj] for tj in hp]
        )
        if R_next > D:
            return False
        if R_next == R:
            break
        R = R_next
    return True

"""
ARモデルにおけるスケジュール可能性検査
"""
def schedulability_test_ar(task_set: TaskSet) -> bool:
    for i in range(task_set.n):
        if not schedulability_test_ar_at(task_set, i):
            return False
    return True

"""
ARモデルにおけるEUMアルゴリズムによる優先度割り当てとスケジュール可能性検査
"""
def schedulability_test_ar_with_eum(task_set: TaskSet) -> bool:
    task_set.set_priority(execution_time_monotonic(task_set))
    i = 0
    while True:
        if schedulability_test_ar_at(task_set, i):
            if i == task_set.n - 1:
                return True
            i += 1
        else:
            ti = task_set.ordered_tasks[i]
            lowered_priority_task = None
            for th in reversed(task_set.higher_priority_tasks(i)):
                if th.utilization < ti.utilization:
                    lowered_priority_task = th
                    break
            if lowered_priority_task is None:
                return False
            else:
                pi = task_set.priority(ti)
                ph = task_set.priority(lowered_priority_task)
                task_set.ordered_tasks.insert(pi, task_set.ordered_tasks.pop(ph))
                task_set.set_priority(task_set.ordered_tasks)
                i = ph

"""
ARモデルにおけるERMアルゴリズムによる優先度割り当てとスケジュール可能性検査
"""
def schedulability_test_ar_with_erm(task_set: TaskSet) -> bool:
    task_set.set_priority(execution_time_monotonic(task_set))
    i = 0
    while True:
        if schedulability_test_ar_at(task_set, i):
            if i == task_set.n - 1:
                return True
            i += 1
        else:
            ti = task_set.ordered_tasks[i]
            lowered_priority_task = None
            for th in reversed(task_set.higher_priority_tasks(i)):
                if th.wcet > ti.wcet:
                    lowered_priority_task = th
                    break
            if lowered_priority_task is None:
                return False
            else:
                pi = task_set.priority(ti)
                ph = task_set.priority(lowered_priority_task)
                task_set.ordered_tasks.insert(pi, task_set.ordered_tasks.pop(ph))
                task_set.set_priority(task_set.ordered_tasks)
                i = ph

"""
ARモデルにおけるスケジュール可能性検査（全探索）
"""
def schedulability_test_ar_exhaustive(task_set: TaskSet) -> bool:
    for perm in permutations(list(task_set.tasks)):
        task_set.set_priority(perm)
        if schedulability_test_ar(task_set):
            return True
