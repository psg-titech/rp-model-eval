from concurrent.futures import ProcessPoolExecutor

from matplotlib import pyplot as plt
from tqdm import trange

from task_gen import generate_taskset
from util import (
    LogUniformPeriodGenerator,
    UniformDeadlineGenerator1,
    StandardTaskGenerator
)
from rp_model.sched_test import schedulability_test_rp
from rp_model.task import RPTaskSet

def test(u_sum, times) -> int:
    n = 15
    min_period = 500
    max_period = 5000
    num_schedulable = 0
    for _ in range(times):
        task_set = generate_taskset(
            n,
            u_sum,
            min_period,
            max_period,
            LogUniformPeriodGenerator(),
            UniformDeadlineGenerator1(),
            StandardTaskGenerator()
        )
        rp_task_set = RPTaskSet.from_task_set(task_set)
        rp_task_set.set_random_local_preemptibility(0.5)
        schedulable = schedulability_test_rp(rp_task_set)
        if schedulable:
            num_schedulable += 1
    return num_schedulable

def main():
    us = [i / 100 for i in range(50, 90, 3)]
    times = 1000
    ratio_schedulable = []
    workers = 8
    for ui in trange(len(us)):
        u = us[ui]
        with ProcessPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(test, [u] * workers, [times // workers] * workers))
        ratio_schedulable.append(sum(results) / (times))
    
    _, ax = plt.subplots()
    ax.plot(us, ratio_schedulable)
    ax.set_xlabel("Utilization")
    ax.set_ylabel("Ratio of schedulable task sets")
    plt.show()

if __name__ == "__main__":
    main()

        