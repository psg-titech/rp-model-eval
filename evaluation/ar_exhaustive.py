"""
ARモデルのスケジュール可能性の優先度割り当てアルゴリズムでの比較
アルゴリズム： ERM, Exhaustive Search
"""

from concurrent.futures import ProcessPoolExecutor as Executor

from tqdm import trange
from pandas import DataFrame

from task_gen import generate_taskset
from util import (
    LogUniformPeriodGenerator,
    UniformDeadlineGenerator1,
    StandardTaskGenerator
)
from ar_model.sched_test import (
    schedulability_test_ar_with_erm,
    schedulability_test_ar_exhaustive
)

def test(u_sum, times) -> tuple[int, int]:
    n = 8
    min_period = 500
    max_period = 5000

    num_schedulable_with_erm = 0
    num_schedulable_with_exhaustive = 0
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
        # ERM
        schedulable = schedulability_test_ar_with_erm(task_set)
        if schedulable:
            num_schedulable_with_erm += 1
        # Exhaustive Search
        schedulable = schedulability_test_ar_exhaustive(task_set)
        if schedulable:
            num_schedulable_with_exhaustive += 1
    return num_schedulable_with_erm, num_schedulable_with_exhaustive

def main():
    us = [0.20, 0.24, 0.28, 0.32, 0.36, 0.40]
    times = 500
    num_schedulable_with_erm = []
    num_schedulable_with_exhaustive = []
    workers = 8
    for ui in trange(len(us)):
        u = us[ui]
        with Executor(max_workers=workers) as executor:
            results = list(executor.map(test, [u] * workers, [times // workers] * workers))
            rest = times % workers
            if rest != 0:
                results += [test(u, rest)]
        num_schedulable_with_erm.append(sum(r[0] for r in results))
        num_schedulable_with_exhaustive.append(sum(r[1] for r in results))
    
    df = DataFrame({
        "Utilization": us,
        "ERM": num_schedulable_with_erm,
        "Exhaustive Search": num_schedulable_with_exhaustive
    })
    print(df)

if __name__ == "__main__":
    main()
