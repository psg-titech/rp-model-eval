"""
RP model, DA model, Preemptive Scheduling, Nonpreemptive Schedulingの比較
"""

from concurrent.futures import ProcessPoolExecutor as Executor

from matplotlib import pyplot as plt
from tqdm import trange

from da_model.task import TaskSetWithNPRegion
from rp_model.task import RPTaskSet
from task_gen import generate_taskset
from util import (
    LogUniformPeriodGenerator,
    UniformDeadlineGenerator1,
    StandardTaskGenerator
)
from priority import deadline_monotonic
from preemptive.sched_test import schedulability_test_fp
from nonpreemptive.sched_test import schedulability_test_np_audsley
from da_model.sched_test import schedulability_test_da_with_maxar
from rp_model.sched_test import schedulability_test_rp

def test(u_sum, times) -> tuple[int, int, int, int]:
    n = 15
    min_period = 500
    max_period = 5000
    preemptible_ratio = 0.5

    num_schedulable_preemptive = 0
    num_schedulable_nonpreemptive = 0
    num_schedulable_da = 0
    num_schedubable_rp = 0
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
        # Preemptive Scheduling
        task_set.set_priority(deadline_monotonic(task_set))
        schedulable = schedulability_test_fp(task_set)
        if schedulable:
            num_schedulable_preemptive += 1
        # Nonpreemptive Scheduling
        schedulable = schedulability_test_np_audsley(task_set)
        if schedulable:
            num_schedulable_nonpreemptive += 1
        # DA model
        task_set = TaskSetWithNPRegion.from_task_set(task_set)
        schedulable = schedulability_test_da_with_maxar(task_set)
        if schedulable:
            num_schedulable_da += 1
        task_set = RPTaskSet.from_task_set(task_set)
        task_set.set_random_local_preemptibility(preemptible_ratio)
        schedulable = schedulability_test_rp(task_set)
        if schedulable:
            num_schedubable_rp += 1
    return num_schedulable_preemptive, num_schedulable_nonpreemptive, num_schedulable_da, num_schedubable_rp

def main():
    us = [i / 100 for i in range(20, 93, 3)]
    times = 5000

    ratio_schedulable_preemptive = []
    ratio_schedulable_nonpreemptive = []
    ratio_schedulable_da = []
    ratio_schedulable_rp = []
    workers = 8
    with Executor() as executor:
        for ui in trange(len(us)):
            u = us[ui]
            results = list(executor.map(test, [u] * workers, [times // workers] * workers))
            ratio_schedulable_preemptive.append(sum([r[0] for r in results]) / times)
            ratio_schedulable_nonpreemptive.append(sum([r[1] for r in results]) / times)
            ratio_schedulable_da.append(sum([r[2] for r in results]) / times)
            ratio_schedulable_rp.append(sum([r[3] for r in results]) / times)

    fontsize = 18
    figsize = (8, 6)

    _, ax = plt.subplots(figsize=figsize)
    ax.plot(us, ratio_schedulable_rp, label="RP model")
    ax.plot(us, ratio_schedulable_nonpreemptive, label="Nonpreemptive", linestyle="dashdot")
    ax.plot(us, ratio_schedulable_da, label="DA model", linestyle="dashed")
    ax.plot(us, ratio_schedulable_preemptive, label="Preemptive", linestyle="dotted")

    ax.set_xlabel("Utilization", fontsize=fontsize)
    ax.set_ylabel("Schedulability Ratio", fontsize=fontsize)
    ax.set_ymargin(0.02)
    ax.tick_params(labelsize=fontsize)
    ax.legend(fontsize=fontsize)

    plt.show()

if __name__ == "__main__":
    main()
