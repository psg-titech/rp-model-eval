from math import ceil, floor

from task import TaskSet

def schedulability_test_np_at(task_set: TaskSet, i: int, schedulable_fp, verbose=False) -> bool:
    """
    B_i = max_{j in lp(i)}{C_j - 1}
    if schedulable_fp:
        S_i = B_i + sum_{j in hp(i)}{(floor{S_i / T_j} + 1) C_j}
    else:
        L_i = B_i + sum_{j in hp(i)}{ceil{L_i / T_j} C_j}
        K_i = ceil{L_i / T_i}
        s_i,k = B_i + (k - 1) C_i + sum_{j in hp(i)}{(floor{s_i,k / T_j} + 1) C_j}
        f_i,k = s_i,k + C_i
        R_i = max{f_i,k - (k - 1) T_i}
    """
    tasks = task_set.ordered_tasks
    ti = tasks[i]
    C = ti.wcet
    T = ti.period
    D = ti.deadline

    lp = task_set.lower_priority_tasks(i)
    hp = task_set.higher_priority_tasks(i)
    hep = task_set.higher_eq_priority_tasks(i)

    B = max([tj.wcet - 1 for tj in lp], default=0)

    if schedulable_fp:
        # Start time of the first job of task i
        S = B + sum([tj.wcet for tj in hp])
        while True:
            S_next = B + sum([(floor(S / tj.period) + 1) * tj.wcet for tj in hp])
            if S_next == S:
                break
            S = S_next
        # Response time
        R = S + C
        if R > D:
            return False
    else:
        # Level-i Active Period
        L = B + C
        while True:
            L_next = B + sum([ceil(L / tj.period) * tj.wcet for tj in hep])
            if L_next == L:
                break
            L = L_next
        K = ceil(L / T)

        for k in range(K):
            # Start time of the k-th job of task i
            s = B + k * C + sum(j.wcet for j in hp)
            while True:
                s_next = B + k * C + sum([(floor(s / j.period) + 1) * j.wcet for j in hp])
                if s_next == s:
                    break
                s = s_next
            # Finish time of the k-th job of task i
            f = s + C
            f_limit = k * T + D
            if f > f_limit:
                return False
    return True

def schedulability_test_np(task_set: TaskSet, schedulable_fp) -> bool:
    n = task_set.n
    for i in range(n):
        if not schedulability_test_np_at(task_set, i, schedulable_fp):
            return False
    return True

def schedulability_test_np_audsley(task_set: TaskSet) -> bool:
    n = task_set.n
    assigned_priority_tasks = []
    unassigned_priority_tasks = task_set.tasks.copy()
    for i in range(n):
        priority_i_task = None
        for task in unassigned_priority_tasks:
            ordered_tasks = list((unassigned_priority_tasks - {task}))
            ordered_tasks.append(task)
            ordered_tasks.extend(assigned_priority_tasks)
            task_set.set_priority(ordered_tasks)
            schedulable = schedulability_test_np_at(task_set, (n - i - 1), False)
            if schedulable:
                priority_i_task = task
                break
        if priority_i_task is None:
            return False
        assigned_priority_tasks.insert(0, priority_i_task)
        unassigned_priority_tasks.remove(priority_i_task)
    return True
