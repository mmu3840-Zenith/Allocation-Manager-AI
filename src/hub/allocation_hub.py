import math

class AllocationHub:
    def __init__(self, workers, items):
        self.workers = workers
        self.items = items

    def assign_tasks(self):
        free = [w for w in self.workers if w.target is None]

        for w in free:
            available = [i for i in self.items if not i.picked]

            if not available:
                return

            best = min(
                available,
                key=lambda i: math.hypot(i.x-w.x, i.y-w.y)
            )

            w.target = best

    def draw(self, screen):
        pass
