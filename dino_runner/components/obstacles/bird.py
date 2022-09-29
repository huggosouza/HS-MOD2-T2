import random
from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.utils.constants import BIRD

class Bird(Obstacle):
    def __init__(self, image, bird_y):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        if bird_y == 0:
            self.rect.y = 260
        else:
            self.rect.y = 315
        
        self.index = 0
        
    def draw(self, SCREEN):
        if self.index >= 10:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1