import math
import pygame
import random

class WorkerRobot:
    def __init__(self, id):
        self.id = id
        self.x = random.randint(100, 900)
        self.y = random.randint(100, 600)
        self.speed = 3
        self.target = None

    def move(self):
        if self.target is None:
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)

        if dist > 1:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

        if dist < 10:
            self.target.picked = True
            self.target.delivered = True
            self.target = None

    def draw(self, screen):
        pygame.draw.circle(screen, (50,150,255), (int(self.x), int(self.y)), 12)

        if self.target:
            pygame.draw.line(screen, (0,200,0),
                             (self.x,self.y),
                             (self.target.x,self.target.y), 2)
