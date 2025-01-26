class Task:
    def __init__(self, id: int, period: int, deadline: int, wcet: int):
        # parameters are positive integers
        if period <= 0 or deadline <= 0 or wcet <= 0:
            raise ValueError("Task parameters must be positive integers")
        if wcet > period:
            raise ValueError("WCET must be less than or equal to period")
        self.id = id
        self.period = period
        self.deadline = deadline
        self.wcet = wcet
        self.utilization = wcet / period
    
    def __str__(self):
        return f"t{self.id}(T: {self.period}, D: {self.deadline}, C: {self.wcet})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

class TaskSet:
    def __init__(self, tasks: set[Task]):
        self.__tasks = tasks
        self.__n = len(tasks)
        self.__utilization = sum(task.utilization for task in tasks)
        self.__priorities: dict[Task, int] = {}
        self.__ordered_tasks: list[Task] = []

    def __str__(self):
        return f"TaskSet({self.__tasks})"
    
    def __repr__(self):
        return self.__str__()
    
    @property
    def n(self):
        return self.__n
    
    @property
    def tasks(self):
        return self.__tasks
    
    @property
    def ordered_tasks(self):
        return self.__ordered_tasks

    def set_priority(self, order: list[Task]):
        self.__ordered_tasks = order
        self.__priorities = {task: i for i, task in enumerate(order)}

    def higher_priority_tasks(self, i: int) -> list[Task]:
        return self.__ordered_tasks[:i]

    def higher_eq_priority_tasks(self, i: int) -> list[Task]:
        return self.__ordered_tasks[:i+1]
    
    def lower_priority_tasks(self, i: int) -> list[Task]:
        return self.__ordered_tasks[i+1:]

    def priority(self, task: Task) -> int:
        return self.__priorities[task]
    