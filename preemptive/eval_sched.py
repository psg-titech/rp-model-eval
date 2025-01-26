from matplotlib import pyplot as plt
from tqdm import tqdm

from task_gen import generate_taskset
from util import (
    LogUniformPeriodGenerator,
    UniformDeadlineGenerator1,
    StandardTaskGenerator
)
from priority import deadline_monotonic
from preemptive.sched_test import schedulability_test_fp

def main():
    n = 15
    us = [i / 100 for i in range(1, 101, 3)]
    min_period = 500
    max_period = 5000
    times = 1000
    ratio_schedulable = []
    for u in tqdm(us):
        num_schedulable = 0
        for _ in range(times):
            task_set = generate_taskset(
                n,
                u,
                min_period,
                max_period,
                LogUniformPeriodGenerator(),
                UniformDeadlineGenerator1(),
                StandardTaskGenerator()
            )
            task_set.set_priority(deadline_monotonic(task_set))
            shedulable = schedulability_test_fp(task_set)
            if shedulable:
                num_schedulable += 1
        ratio_schedulable.append(num_schedulable / times)
    
    _, ax = plt.subplots()
    ax.plot(us, ratio_schedulable)
    ax.set_xlabel("Utilization")
    ax.set_ylabel("Ratio of schedulable task sets")
    plt.show()

if __name__ == "__main__":
    main()