from math import ceil

from task import TaskSet

def schedulability_test_fp(task_set: TaskSet) -> bool:
    """
    R_i = C_i + sum_{j in hp(i)}{ceil{R_i / T_j} C_j}
    """
    n = task_set.n
    tasks = task_set.ordered_tasks
    for i in range(n):
        ti = tasks[i]
        R = ti.wcet
        higher_priority_tasks = tasks[:i]
        while True:
            R_next = ti.wcet + sum([ceil(R / tj.period) * tj.wcet for tj in higher_priority_tasks])
            if R_next == R:
                break
            R = R_next
        if R > ti.deadline:
            return False
    return True
