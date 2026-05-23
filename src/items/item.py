import random
import pygame

ITEM_TYPES = ["Metal","Wood","Plastic","Glass"]

class Item:
    def __init__(self):
        self.type = random.choice(ITEM_TYPES)
        self.x = random.randint(50, 950)
        self.y = random.randint(50, 650)
        self.picked = False
        self.delivered = False

    def draw(self, screen):
        if not self.delivered:
            pygame.draw.circle(screen, (0,200,200), (self.x,self.y), 8)
