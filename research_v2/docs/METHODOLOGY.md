# Allocation Engine 2.0 — Experimental Methodology

## Research objective

Evaluate how allocation policies behave under increasing synthetic task
workloads and worker availability constraints.

## Environment

The model represents a computational warehouse allocation abstraction.
It does not simulate physical robot movement, collision dynamics, travel
distance, battery discharge, wireless communication, or real warehouse
operations.

There are ten workers, each with a capacity of 10 workload units.

## Workload scales

10, 25, 50, 100, 150, and 200 tasks.

Each task receives:
- A workload sampled uniformly between 1 and 5.
- An integer priority between 1 and 3.

## Worker availability

Three worker failure probabilities are examined:
- 0%
- 10%
- 25%

Worker availability is sampled once for each scenario and shared across
all allocation policies in that scenario.

## Allocation policies

1. Random: randomized task order and feasible worker selection.
2. First Fit: descending workload order and first feasible worker.
3. Best Fit: descending workload order and smallest remaining capacity.
4. Least Loaded: priority-ordered tasks and currently least-loaded worker.
5. Priority Balanced: priority/workload ordered tasks and least-loaded feasible worker.

These are operational definitions for this implementation, not claims
that each algorithm is globally optimal.

## Repetition and reproducibility

The default experiment uses 20 seeds per workload/failure configuration.
Each policy receives the same generated task set and failed-worker set.

This creates paired scenario comparisons.

## Outcomes

- Task allocation rate.
- Workload completion rate.
- Priority-weighted completion rate.
- Mean and standard deviation of active-worker utilization.
- Coefficient-of-variation load imbalance.
- Jain fairness index.
- Composite objective score.
- Algorithm execution time.

The composite score is an exploratory weighted metric:
35% workload completion, 25% Jain fairness, 20% mean utilization,
and 20% priority completion.

It is not a universally validated measure of allocation quality.
Its component metrics must also be reported independently.

## Statistical analysis

The analysis reports means, standard deviations and percentile bootstrap
95% confidence intervals. Paired objective-score differences are computed
against First Fit within each matched scenario.

The default bootstrap uses 2,000 resamples. The bootstrap interval is
descriptive and does not by itself establish statistical significance.

## Limitations

- Synthetic workloads only.
- Static task batch; no online task arrivals.
- No task travel or spatial routing.
- No worker recovery or dynamic reassignment.
- Worker failures are sampled before allocation.
- No energy or communication model.
- No physical robot validation.
- Runtime depends on the execution machine.

All limitations must remain visible in any resulting manuscript.
