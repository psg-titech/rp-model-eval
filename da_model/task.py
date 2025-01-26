from task import Task, TaskSet

class TaskSetWithNPRegion(TaskSet):
    def __init__(self, tasks: set[Task]):
        super().__init__(tasks)
        self.__np_regions: dict[Task, int] = {task: task.wcet for task in tasks}

    @staticmethod
    def from_task_set(task_set: TaskSet):
        return TaskSetWithNPRegion(task_set.tasks)

    @property
    def np_regions(self) -> dict[Task, int]:
        return self.__np_regions
