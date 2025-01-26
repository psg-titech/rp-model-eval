from operator import attrgetter

from task import Task, TaskSet

def deadline_monotonic(task_set: TaskSet) -> list[Task]:
    tasks = list(task_set.tasks)
    tasks.sort(key=attrgetter('deadline'))
    return tasks

def utilization_monotonic(task_set: TaskSet) -> list[Task]:
    tasks = list(task_set.tasks)
    tasks.sort(key=attrgetter('utilization'), reverse=True)
    return tasks

def execution_time_monotonic(task_set: TaskSet) -> list[Task]:
    # Wang and Burns, 2014
    tasks = list(task_set.tasks)
    tasks.sort(key=attrgetter('deadline'))
    tasks.sort(key=attrgetter('wcet'), reverse=True)
    return tasks
