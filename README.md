# Allocation Manager AI

**Multi-Agent Resource Allocation and Coordination System**

Allocation Manager AI is a computational multi-agent system designed to study how autonomous worker agents can be coordinated to allocate tasks and resources efficiently under changing workloads, priorities, and failure conditions.

The project models a warehouse-like environment containing tasks, resources, and autonomous worker robots. A centralized allocation hub evaluates the environment and assigns work to available agents while experimental strategies provide alternative allocation policies for comparison.

> **Research scope:** This project is a computational simulation. The worker robots, warehouse environment, and allocation mechanisms are software abstractions and do not represent a physically deployed robotic system.

---

## Research Objective

Large multi-agent systems face a fundamental coordination problem:

> **How can tasks be distributed among many autonomous agents while balancing workload, task priority, resource availability, distance, and agent failures?**

Allocation Manager AI investigates this problem through a controlled computational environment.

The system is designed to evaluate:

* Multi-agent task allocation
* Priority-aware scheduling
* Resource-aware assignment
* Worker utilization
* Load balancing
* Failure handling
* High-load behavior
* Allocation efficiency
* Strategy performance under stress

The architecture separates the environment, allocation logic, workers, items, metrics, and experimental strategies so that different coordination approaches can be evaluated without rewriting the entire system.

---

# System Architecture

```text
                    ┌──────────────────────┐
                    │   Allocation Hub     │
                    │                      │
                    │ Task Assignment      │
                    │ Priority Handling     │
                    │ Resource Allocation  │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌────────────┐    ┌────────────┐    ┌────────────┐
      │ Worker     │    │ Worker     │    │ Worker     │
      │ Robot 01   │    │ Robot 02   │    │ Robot ...  │
      └────────────┘    └────────────┘    └────────────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Warehouse Environment│
                    │                      │
                    │ Tasks                │
                    │ Resources            │
                    │ Locations            │
                    │ Constraints          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Metrics Engine     │
                    │                      │
                    │ Efficiency           │
                    │ Completion            │
                    │ Utilization          │
                    │ Failures             │
                    └──────────────────────┘
```

---

# Core Components

## Allocation Hub

`src/hub/allocation_hub.py`

The allocation hub acts as the coordination layer of the system.

Its responsibilities include:

* Evaluating available work
* Assigning tasks to workers
* Considering task priority
* Managing allocation decisions
* Coordinating worker availability
* Handling changing environment conditions

The hub provides the central decision-making mechanism used by the simulation.

---

## Worker Robots

`src/workers/worker_robot.py`

Worker robots represent autonomous computational agents.

Each worker maintains its own simulated state and can participate in task execution and allocation decisions.

The abstraction allows the system to investigate how allocation performance changes as the number and state of workers change.

---

## Warehouse Environment

`src/environment/warehouse_env.py`

The warehouse environment represents the simulated operating space.

It provides the state against which allocation decisions are evaluated, including:

* Available tasks
* Resource conditions
* Worker state
* Environmental constraints
* Workload conditions

The environment is intentionally separated from the allocation logic so that different controllers can be tested against the same conditions.

---

## Items and Tasks

`src/items/item.py`

Items represent units of work or resources within the simulated environment.

They provide the allocation system with information required to determine which work should be assigned to which worker.

---

## Metrics Engine

`src/metrics/metrics_engine.py`

The metrics layer records experimental outcomes rather than relying only on visual demonstrations.

Depending on the experiment, measurements can include:

* Task completion
* Allocation efficiency
* Worker utilization
* Remaining workload
* Failure counts
* Processing time
* Allocation performance

This makes the system suitable for controlled comparisons between allocation strategies.

---

# Experimental Strategies

The repository contains a strategy layer designed to make allocation policies independently testable.

```text
src/
├── environment/
├── hub/
├── items/
├── metrics/
├── strategies/
└── workers/
```

This allows experiments to compare different decision-making approaches under identical environmental conditions.

The objective is not simply to demonstrate that an allocation system works, but to measure **how different allocation policies behave under different operating conditions**.

---

# Experimental Evaluation

Experiments are organized into separate scenarios:

```text
experiments/
├── baseline/
├── failure_test/
├── high_load/
└── priority_stress/
```

### Baseline

Measures normal system behavior under standard operating conditions.

### Failure Test

Introduces worker failures to evaluate how the allocation system responds when available agents change.

### High Load

Increases workload pressure to evaluate scalability and allocation behavior when demand exceeds normal conditions.

### Priority Stress

Tests the allocation mechanism when tasks have competing priorities.

---

# Reproducibility

Experiments are executed through:

```text
experiments/run_experiments.py
```

Generated experimental data and figures are stored under:

```text
results/
├── figures/
└── logs/
```

Visual outputs are generated using:

```text
scripts/generate_figures.py
```

This separation allows the experimental pipeline to be rerun without manually constructing the results.

---

# Visualization

The project includes visual outputs for communicating system behavior:

```text
visuals/
├── architecture.png
├── results_plot.png
└── swarm_demo.gif
```

The visualizations are intended to provide an intuitive representation of the computational system while the numerical experiments provide the primary basis for evaluation.

---

# Validation

The repository includes automated tests covering core system components.

Run:

```bash
python -m pytest -q
```

The project can also be compiled before execution:

```bash
python -m compileall src experiments scripts -q
```

A successful validation pipeline checks that:

1. Source modules compile successfully.
2. Automated tests pass.
3. Experiments execute successfully.
4. Experimental outputs are generated.
5. Figures can be produced from recorded results.

---

# Installation

Clone the repository:

```bash
git clone https://github.com/mmu3840-Zenith/Allocation-Manager-AI.git
cd Allocation-Manager-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the test suite:

```bash
python -m pytest -q
```

Run the experiments:

```bash
python experiments/run_experiments.py
```

Generate figures:

```bash
python scripts/generate_figures.py
```

---

# Project Structure

```text
Allocation-Manager-AI/
│
├── main.py
├── README.md
├── requirements.txt
├── LICENSE
│
├── docs/
│   ├── experiments.md
│   ├── methodology.md
│   └── system_design.md
│
├── experiments/
│   ├── run_experiments.py
│   ├── baseline/
│   ├── failure_test/
│   ├── high_load/
│   └── priority_stress/
│
├── results/
│   ├── figures/
│   └── logs/
│
├── scripts/
│   ├── gif_recorder.py
│   └── generate_figures.py
│
├── src/
│   ├── environment/
│   │   └── warehouse_env.py
│   ├── hub/
│   │   └── allocation_hub.py
│   ├── items/
│   │   └── item.py
│   ├── metrics/
│   │   ├── metrics_engine.py
│   │   └── plotter.py
│   ├── strategies/
│   └── workers/
│       └── worker_robot.py
│
├── tests/
│
└── visuals/
    ├── architecture.png
    ├── results_plot.png
    └── swarm_demo.gif
```

---

# Research Methodology

The system follows a controlled experimental workflow:

```text
Environment
     │
     ▼
Generate workload
     │
     ▼
Initialize workers
     │
     ▼
Apply allocation strategy
     │
     ▼
Execute simulated tasks
     │
     ▼
Record system state
     │
     ▼
Calculate metrics
     │
     ▼
Compare strategies
     │
     ▼
Generate figures
```

The same computational environment can be used to compare multiple strategies, reducing the influence of unrelated environmental changes on the comparison.

---

# Limitations

This project should be interpreted within the scope of its computational model.

It does **not** demonstrate:

* Physical warehouse deployment
* Real robotic hardware coordination
* Real-world wireless communication
* Physical navigation
* Industrial safety certification
* Production warehouse optimization
* Biological or physical autonomy

The worker robots and warehouse are simulated abstractions intended to investigate the underlying **multi-agent allocation problem**.

---

# Why This Project Matters

As the number of autonomous agents increases, centralized decision-making can become increasingly difficult.

An effective allocation system must continuously balance competing objectives:

```text
Task Priority
      +
Worker Availability
      +
Resource Constraints
      +
Distance / Cost
      +
Failures
      +
System Load
      ↓
Allocation Decision
```

Allocation Manager AI provides a controlled environment for studying these trade-offs and testing how allocation strategies behave under increasingly difficult conditions.

---

# Future Research

Potential extensions include:

* Reinforcement-learning-based allocation
* Decentralized allocation
* Multi-objective optimization
* Dynamic task arrival
* Communication constraints
* Adaptive worker specialization
* Larger-scale swarm experiments
* Learned task-to-worker assignment
* Robust optimization under uncertainty
* Real robotic hardware integration

---

# Research Positioning

Allocation Manager AI is part of a broader exploration of **multi-agent artificial intelligence and autonomous coordination systems**.

The central research question is:

> **How can autonomous agents efficiently coordinate limited resources when workload, priorities, and agent availability continuously change?**

The project approaches this question through simulation, controlled experimentation, automated validation, and quantitative comparison.

---

## Disclaimer

**Allocation Manager AI is a research-oriented computational simulation. Results produced by the system describe the behavior of the implemented simulation model and should not be interpreted as evidence of equivalent performance in physical robotic or industrial environments.**
