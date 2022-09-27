from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        
    def update(self, game_speed, player):
        if len(self.obstacles) == 0:
            self.obstacles.append(Cactus(SMALL_CACTUS))
            
        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)