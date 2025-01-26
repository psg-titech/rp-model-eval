from task import Task, TaskSet
from nonpreemptive.sched_test import schedulability_test_np_at

def schedulability_test_np_audsley_verbose(task_set: TaskSet) -> bool:
    print("Task set:")
    for task in task_set.tasks:
        print("  ", task)
    n = task_set.n
    assigned_priority_tasks = []
    unassigned_priority_tasks = task_set.tasks.copy()
    for i in range(n):
        print(f"Priority {n - i}")
        priority_i_task = None
        for task in unassigned_priority_tasks:
            ordered_tasks = list((unassigned_priority_tasks - {task}))
            ordered_tasks.append(task)
            ordered_tasks.extend(assigned_priority_tasks)
            task_set.set_priority(ordered_tasks)
            schedulable = schedulability_test_np_at(task_set, (n - i - 1), False)
            if schedulable:
                print(f"  {task.id} is schedulable")
                priority_i_task = task
                break
            else:
                print(f"  {task.id} is not schedulable")
        if priority_i_task is None:
            print(f"Priority {n - i} failed")
            return False
        assigned_priority_tasks.insert(0, priority_i_task)
        unassigned_priority_tasks.remove(priority_i_task)
    return True

def main():
    t1 = Task(1, 5, 5, 2)
    t2 = Task(2, 8, 8, 3)
    t3 = Task(3, 10, 10, 2)
    task_set = TaskSet({t1, t2, t3})

    schedulability_test_np_audsley_verbose(task_set)

if __name__ == "__main__":
    main()
