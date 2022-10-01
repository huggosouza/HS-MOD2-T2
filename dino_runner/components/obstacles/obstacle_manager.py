import random
import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.largecactus import LargeCactus
from dino_runner.utils.constants import LARGE_CACTUS, BIRD, SMALL_CACTUS


class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        
    def removeHeart(self, game):
        game.player.hearts - 1
        
    def update(self, game):
        if len(self.obstacles) == 0:
            ran = random.randint(1, 3)
            if ran == 1:
                self.obstacles.append(Cactus(SMALL_CACTUS))
            elif ran == 2:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            elif ran == 3:
                bird_y = random.randint(0, 1)
                self.obstacles.append(Bird(BIRD, bird_y))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                        pygame.time.delay(500)
                        game.playing = False
                        game.death_count += 1
                else:
                    if game.player.type == 'hammer':
                        self.obstacles.remove(obstacle)
                    elif game.player.type == 'shield':
                        pass
    
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            
    def reset_obstacles(self):
        self.obstacles = []