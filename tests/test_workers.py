from src.workers.worker_robot import WorkerRobot


def test_worker_capacity():
    worker = WorkerRobot(
        worker_id=1,
        capacity=10,
    )

    assert worker.can_accept(5)
    assert worker.assign(1, 5)
    assert worker.allocated_workload == 5
    assert worker.remaining_capacity == 5


def test_worker_rejects_over_capacity():
    worker = WorkerRobot(
        worker_id=1,
        capacity=5,
    )

    assert not worker.assign(1, 6)
