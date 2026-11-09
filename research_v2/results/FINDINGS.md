# Allocation Engine 2.0 — Experimental Findings

## Experiment overview

- 1,800 policy evaluations.
- 360 matched scenarios.
- Five allocation policies.
- Six task-volume levels: 10, 25, 50, 100, 150, and 200.
- Three worker-failure probabilities: 0%, 10%, and 25%.
- 20 random seeds per task-volume/failure condition.
- Ten workers, each with capacity 10 workload units.

## Best policy by scenario

| Tasks | Worker failures | Highest mean objective score | Score | Workload completion | Jain fairness |
|---:|---:|---|---:|---:|---:|
| 10 | 0% | least_loaded | 0.8260 | 1.0000 | 0.8703 |
| 10 | 10% | priority_balanced | 0.8468 | 1.0000 | 0.9192 |
| 10 | 25% | priority_balanced | 0.8688 | 1.0000 | 0.9500 |
| 25 | 0% | priority_balanced | 0.9444 | 1.0000 | 0.9862 |
| 25 | 10% | priority_balanced | 0.9470 | 0.9715 | 0.9913 |
| 25 | 25% | priority_balanced | 0.9200 | 0.8834 | 0.9940 |
| 50 | 0% | priority_balanced | 0.8177 | 0.6316 | 0.9982 |
| 50 | 10% | priority_balanced | 0.7842 | 0.5622 | 0.9986 |
| 50 | 25% | least_loaded | 0.7263 | 0.4512 | 0.9984 |
| 100 | 0% | least_loaded | 0.6540 | 0.3183 | 0.9987 |
| 100 | 10% | least_loaded | 0.6280 | 0.2766 | 0.9988 |
| 100 | 25% | least_loaded | 0.5880 | 0.2119 | 0.9990 |
| 150 | 0% | least_loaded | 0.5885 | 0.2134 | 0.9990 |
| 150 | 10% | least_loaded | 0.5722 | 0.1884 | 0.9990 |
| 150 | 25% | least_loaded | 0.5506 | 0.1545 | 0.9993 |
| 200 | 0% | least_loaded | 0.5544 | 0.1609 | 0.9991 |
| 200 | 10% | least_loaded | 0.5463 | 0.1507 | 0.9990 |
| 200 | 25% | least_loaded | 0.5312 | 0.1263 | 0.9991 |

## Paired comparison against First Fit

| Policy | Mean paired objective difference | Conditions better | Conditions worse | Tied |
|---|---:|---:|---:|---:|
| best_fit | -0.00000 | 0 | 3 | 15 |
| least_loaded | +0.04930 | 16 | 2 | 0 |
| priority_balanced | +0.04731 | 18 | 0 | 0 |
| random | +0.02331 | 18 | 0 | 0 |

## Interpretation and limitations

The objective score is an exploratory weighted metric, not a universally
validated measure of allocation quality. Its component metrics must be
considered independently.

The model uses synthetic task workloads and static worker availability.
It does not simulate physical robot movement, spatial routing, collisions,
energy consumption, communication, online arrivals, worker recovery, or
dynamic reassignment. It is not evidence of physical robot performance.

The reported confidence intervals are descriptive bootstrap intervals.
The paired objective differences are not, by themselves, proof of
statistical significance. No multiplicity-adjusted hypothesis testing
is claimed.

All numerical findings above are generated from the saved experiment data.
Do not replace them with manually estimated or invented values.
