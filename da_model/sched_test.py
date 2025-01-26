from math import ceil, floor

from task import Task
from da_model.task import TaskSetWithNPRegion

def schedulability_test_da_at(task_set: TaskSetWithNPRegion, i: int) -> bool:
    ti = task_set.ordered_tasks[i]
    C = ti.wcet
    D = ti.deadline
    F = task_set.np_regions[ti]
    T = ti.period
    hp = task_set.higher_priority_tasks(i)
    hep = task_set.higher_eq_priority_tasks(i)
    lp = task_set.lower_priority_tasks(i)
    c_ij = {
        tj: tj.wcet + max(
            [k.wcet - task_set.np_regions[k] - 1 for k in task_set.ordered_tasks[j+1:i+1]] + [0])
            for j, tj in enumerate(hep)
    }
    B = max([task_set.np_regions[j] - 1 for j in lp] + [0])
    L = B + C
    too_large_L = 1e9
    while True:
        L_next = B + sum([ceil(L / tj.period) * c_ij[tj] for tj in hep])
        if L_next > too_large_L:
            L = L_next
            break
        if L_next == L:
            break
        L = L_next
    K = ceil(L / T)
    for k in range(K):
        w = B + (k + 1) * C - F + sum(c_ij[tj] for tj in hp)
        w_lim = k * T + D - F
        while True:
            w_next = B + (k + 1) * C - F + sum([(floor(w / tj.period) + 1) * c_ij[tj] for tj in hp])
            if w_next > w_lim:
                return False
            if w_next == w:
                break
            w = w_next
    return True

def schedulability_test_da_with_maxar(task_set: TaskSetWithNPRegion) -> bool:
    assigned_priority_tasks = []
    unassigned_priority_tasks = task_set.tasks.copy()
    for i in range(task_set.n - 1, -1, -1):
        task_priority_i_ar: dict[Task, int | None] = {}
        for ti in unassigned_priority_tasks:
            ordered_tasks = list((unassigned_priority_tasks - {ti}))
            ordered_tasks.append(ti)
            ordered_tasks.extend(assigned_priority_tasks)
            task_set.set_priority(ordered_tasks)
            for tj in unassigned_priority_tasks:
                task_set.np_regions[tj] = tj.wcet
            # binary search
            schedulable_last_np: int | None = None
            if i == task_set.n - 1:
                left = 0
            else:
                th = task_set.ordered_tasks[i + 1]
                max_ar = th.wcet - task_set.np_regions[th]
                left = max(0, ti.wcet - max_ar)
            right = ti.wcet
            while True:
                mid = (left + right) // 2
                task_set.np_regions[ti] = mid
                schedulable = schedulability_test_da_at(task_set, i)
                if left == mid:
                    if schedulable:
                        schedulable_last_np = mid
                    elif schedulable_last_np is None:
                        task_set.np_regions[ti] = right
                        schedulable = schedulability_test_da_at(task_set, i)
                        if schedulable:
                            schedulable_last_np = right
                    break
                if schedulable:
                    right = mid
                    schedulable_last_np = mid
                else:
                    left = mid
            if schedulable_last_np is not None:
                task_priority_i_ar[ti] = ti.wcet - schedulable_last_np
            else:
                task_priority_i_ar[ti] = None
        if all([v is None for v in task_priority_i_ar.values()]):
            return False
        priority_i_task = max([k for k, v in task_priority_i_ar.items() if v is not None], key=lambda x: task_priority_i_ar[x])
        assigned_priority_tasks.insert(0, priority_i_task)
        unassigned_priority_tasks.remove(priority_i_task)
        np_region = priority_i_task.wcet - task_priority_i_ar[priority_i_task]
        task_set.np_regions[priority_i_task] = np_region
    return True
