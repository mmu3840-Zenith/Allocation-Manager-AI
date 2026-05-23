import pygame
import random
from src.hub.allocation_hub import AllocationHub
from src.workers.worker_robot import WorkerRobot
from src.items.item import Item
from src.metrics.metrics_engine import MetricsEngine

WIDTH, HEIGHT = 1000, 700

class WarehouseEnv:
    def __init__(self, mode='NORMAL'):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.mode = mode

        self.items = [Item() for _ in range(self._item_count())]
        self.workers = [WorkerRobot(i) for i in range(self._worker_count())]
        self.hub = AllocationHub(self.workers, self.items)
        self.metrics = MetricsEngine()

        self.running = True

    def _worker_count(self):
        return {
            'NORMAL': 6,
            'STRESS_TEST': 6,
            'FAILURE_CONDITIONS': 6,
            'SCALABILITY': 20,
            'EXTREME_LOAD': 40
        }.get(self.mode, 6)

    def _item_count(self):
        return {
            'NORMAL': 40,
            'STRESS_TEST': 120,
            'FAILURE_CONDITIONS': 120,
            'SCALABILITY': 200,
            'EXTREME_LOAD': 400
        }.get(self.mode, 40)

    def run(self):
        while self.running:
            self.screen.fill((255,255,255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.hub.assign_tasks()

            for w in self.workers:
                w.move()
                w.draw(self.screen)

            for i in self.items:
                i.draw(self.screen)

            self.hub.draw(self.screen)

            completed = self.metrics.update(self.items)

            pygame.display.set_caption(
                f"Mode: {self.mode} | Completed: {completed}"
            )

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
