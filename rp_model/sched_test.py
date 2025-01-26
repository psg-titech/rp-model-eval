from math import ceil, floor
from operator import attrgetter

from rp_model.task import RPTaskSet

def schedulability_test_rp(task_set: RPTaskSet) -> bool:
    priority_assigned = []
    priority_unassigned = task_set.tasks.copy()
    local_preemptibility = task_set.local_preemptibility.copy()
    for i in range(task_set.n - 1, -1, -1):
        tasks_preemption_disabled = {task: None for task in priority_unassigned}
        for tj in priority_unassigned:
            locally_preemptible_tasks = [t for t in priority_unassigned if local_preemptibility[tj][t]]
            locally_preemptible_tasks.sort(key=lambda x: x.deadline)
            C = tj.wcet
            D = tj.deadline
            T = tj.period
            lower_priority_tasks = priority_assigned
            higher_eq_priority_tasks = priority_unassigned
            higher_priority_tasks = priority_unassigned - {tj}
            len_locally_preemptible_tasks = len(locally_preemptible_tasks)
            left = 0
            right = len_locally_preemptible_tasks
            mid = 0
            while True:
                mid = (left + right) // 2
                schedulable = True
                tasks_preemptible = set(locally_preemptible_tasks[:mid])
                # Schedulability_test
                B = max([tj.wcet - 1 for tj in lower_priority_tasks if any(not local_preemptibility[tj][th] for th in priority_unassigned)], default=0)
                L = B + C
                while True:
                    L_next = B + sum([ceil(L / t.period) * t.wcet for t in higher_eq_priority_tasks])
                    if L_next == L:
                        break
                    L = L_next
                K = ceil(L / T)
                for k in range(K):
                    s = B + k * C + sum([t.wcet for t in higher_priority_tasks])
                    while True:
                        s_next = B + k * C + sum([(floor(s / t.period) + 1) * t.wcet for t in higher_priority_tasks])
                        if s_next == s:
                            break
                        s = s_next
                    f = s + C
                    while True:
                        f_next = s + C + sum([(ceil(f / tj.period) - (floor(s / tj.period) + 1)) * tj.wcet for tj in higher_priority_tasks if tj in tasks_preemptible])
                        if f_next - k * T > D:
                            schedulable = False
                            break
                        if f_next == f:
                            break
                        f = f_next
                    if not schedulable:
                        break
                if schedulable:
                    left = mid + 1
                else:
                    right = mid - 1
                if left > right:
                    break
            if right < 0:
                tasks_preemption_disabled[tj] = None
            else:
                tasks_preemption_disabled[tj] = set(locally_preemptible_tasks[right:])
        if all([v is None for v in tasks_preemption_disabled.values()]):
            return False
        task_priority_i = max([k for k, v in tasks_preemption_disabled.items() if v is not None], key=attrgetter('deadline'))
        priority_assigned.append(task_priority_i)
        priority_unassigned.remove(task_priority_i)
        for tj in tasks_preemption_disabled[task_priority_i]:
            local_preemptibility[task_priority_i][tj] = False
    return True