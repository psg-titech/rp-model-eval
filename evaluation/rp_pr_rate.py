"""
RP modelの、局所的なpreemptibilityの比率を変化させたときの比較
"""

from concurrent.futures import ProcessPoolExecutor as Executor

from matplotlib import pyplot as plt
from tqdm import trange

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
from rp_model.sched_test import schedulability_test_rp

def test(u_sum, times) -> tuple[int, int, int, int, int, int]:
    n = 15
    min_period = 500
    max_period = 5000

    rates = [0.1, 0.3, 0.5, 0.7, 0.9]

    num_schedulable_fp = 0
    num_schedulable_np = 0
    num_schedulable_rp = [0] * len(rates)
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
            num_schedulable_fp += 1
        # Nonpreemptive Scheduling
        schedulable = schedulability_test_np_audsley(task_set)
        if schedulable:
            num_schedulable_np += 1
        # RP model
        for i in range(len(rates)):
            task_set = RPTaskSet.from_task_set(task_set)
            task_set.set_random_local_preemptibility(rates[i])
            schedulable = schedulability_test_rp(task_set)
            if schedulable:
                num_schedulable_rp[i] += 1
    return num_schedulable_fp, num_schedulable_np, *num_schedulable_rp

def main():
    us = [i / 100 for i in range(20, 93, 3)]
    times = 500

    ratio_schedulable_fp = []
    ratio_schedulable_np = []
    ratio_schedulable_rp = [[] for _ in range(5)]
    workers = 8
    with Executor(max_workers=workers) as executor:
        for ui in trange(len(us)):
            u = us[ui]
            results = list(executor.map(test, [u] * workers, [times // workers] * workers))
            ratio_schedulable_fp.append(sum(r[0] for r in results) / times)
            ratio_schedulable_np.append(sum(r[1] for r in results) / times)
            for i in range(5):
                ratio_schedulable_rp[i].append(sum(r[i + 2] for r in results) / times)

    fontsize = 18
    figsize = (8, 6)

    _, ax = plt.subplots(figsize=figsize)
    ax.plot(us, ratio_schedulable_fp, label="Preemptive", linestyle="dotted")
    for i in range(5):
        ax.plot(us, ratio_schedulable_rp[i], label=f"0.{1 + 2 * i}")
    ax.plot(us, ratio_schedulable_np, label="Nonpreemptive", linestyle="dotted")

    ax.set_xlabel("Utilization", fontsize=fontsize)
    ax.set_ylabel("Schedulability Ratio", fontsize=fontsize)
    ax.set_ymargin(0.02)
    ax.legend(fontsize=fontsize)
    plt.show()

if __name__ == "__main__":
    main()
