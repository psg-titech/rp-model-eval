from matplotlib import pyplot as plt
from tqdm import tqdm

from task_gen import generate_taskset
from util import (
    LogUniformPeriodGenerator,
    UniformDeadlineGenerator1,
    StandardTaskGenerator
)
from priority import deadline_monotonic
from nonpreemptive.sched_test import (
    schedulability_test_np,
    schedulability_test_np_audsley
)

def main():
    n = 15
    us = [i / 100 for i in range(1, 100, 3)]
    min_period = 500
    max_period = 5000
    times = 1000
    ratio_schedulable_dm = []
    ratio_schedulable_audsley = []
    for u in tqdm(us):
        num_schedulable_dm = 0
        num_schedulable_audsley = 0
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
            # Deadline monotonic
            task_set.set_priority(deadline_monotonic(task_set))
            shedulable = schedulability_test_np(task_set, False)
            if shedulable:
                num_schedulable_dm += 1
            # Audsley's algorithm
            schedulable = schedulability_test_np_audsley(task_set)
            if schedulable:
                num_schedulable_audsley += 1
            
        ratio_schedulable_dm.append(num_schedulable_dm / times)
        ratio_schedulable_audsley.append(num_schedulable_audsley / times)
    
    _, ax = plt.subplots()
    ax.plot(us, ratio_schedulable_dm, label="Deadline monotonic")
    ax.plot(us, ratio_schedulable_audsley, label="Audsley's algorithm", linestyle="--")
    ax.set_xlabel("Utilization")
    ax.set_ylabel("Ratio of schedulable task sets")
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()