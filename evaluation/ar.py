"""
ARモデルのスケジュール可能性の優先度割り当てアルゴリズムでの比較
アルゴリズム： DM, UM, EM, EUM, ERM
"""

from concurrent.futures import ProcessPoolExecutor as Executor

from matplotlib import pyplot as plt
from tqdm import trange

from task_gen import generate_taskset
from util import (
    LogUniformPeriodGenerator,
    UniformDeadlineGenerator1,
    StandardTaskGenerator
)
from priority import (
    deadline_monotonic,
    utilization_monotonic,
    execution_time_monotonic
)
from ar_model.sched_test import (
    schedulability_test_ar,
    schedulability_test_ar_with_eum,
    schedulability_test_ar_with_erm
)

def test(u_sum, times) -> tuple[int, int, int, int, int]:
    n = 15
    min_period = 500
    max_period = 5000

    num_schedulable_with_dm = 0
    num_schedulabile_with_um = 0
    num_schedulable_with_em = 0
    num_schedulable_with_eum = 0
    num_schedulable_with_erm = 0
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
        # DM
        task_set.set_priority(deadline_monotonic(task_set))
        schedulable = schedulability_test_ar(task_set)
        if schedulable:
            num_schedulable_with_dm += 1
        # UM
        task_set.set_priority(utilization_monotonic(task_set))
        schedulable = schedulability_test_ar(task_set)
        if schedulable:
            num_schedulabile_with_um += 1
        # EM
        task_set.set_priority(execution_time_monotonic(task_set))
        schedulable = schedulability_test_ar(task_set)
        if schedulable:
            num_schedulable_with_em += 1
        # EUM
        schedulable = schedulability_test_ar_with_eum(task_set)
        if schedulable:
            num_schedulable_with_eum += 1
        # ERM
        schedulable = schedulability_test_ar_with_erm(task_set)
        if schedulable:
            num_schedulable_with_erm += 1
    return num_schedulable_with_dm, num_schedulabile_with_um, num_schedulable_with_em, num_schedulable_with_eum, num_schedulable_with_erm

def main():
    us = [i / 100 for i in range(10, 50, 3)]
    times = 5000

    ratio_schedulable_with_dm = []
    ratio_schedulable_with_um = []
    ratio_schedulable_with_em = []
    ratio_schedulable_with_eum = []
    ratio_schedulable_with_erm = []
    workers = 8
    for ui in trange(len(us)):
        u = us[ui]
        with Executor(max_workers=workers) as executor:
            results = list(executor.map(test, [u] * workers, [times // workers] * workers))
        ratio_schedulable_with_dm.append(sum([r[0] for r in results]) / times)
        ratio_schedulable_with_um.append(sum([r[1] for r in results]) / times)
        ratio_schedulable_with_em.append(sum([r[2] for r in results]) / times)
        ratio_schedulable_with_eum.append(sum([r[3] for r in results]) / times)
        ratio_schedulable_with_erm.append(sum([r[4] for r in results]) / times)

    fontsize = 18
    figsize = (8, 6)

    _, ax = plt.subplots(figsize=figsize)
    ax.plot(us, ratio_schedulable_with_dm, label="DM", linestyle="dashdot")
    ax.plot(us, ratio_schedulable_with_um, label="UM", linestyle="dashed")
    ax.plot(us, ratio_schedulable_with_em, label="EM", linestyle="dotted")
    ax.plot(us, ratio_schedulable_with_eum, label="EUM", linestyle="dashdot")
    ax.plot(us, ratio_schedulable_with_erm, label="ERM")

    ax.set_xlabel("Utilization", fontsize=fontsize)
    ax.set_ylabel("Schedulability ratio", fontsize=fontsize)
    ax.set_ymargin(0.02)
    ax.legend(fontsize=fontsize)
    ax.tick_params(labelsize=fontsize)

    plt.show()

if __name__ == "__main__":
    main()
