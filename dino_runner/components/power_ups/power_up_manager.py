import random
import pygame
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.shield import Shield

class PowerUpManager():
    rand_power_up = 0
    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        
    def generate_power_up(self, score):
        if len(self.power_ups) == 0 and self.when_appears == score:
            self.when_appears += random.randint(150, 300)
            rand_power_up = random.randint(1, 2)
            if rand_power_up == 1:
                self.power_ups.append(Shield())
            elif rand_power_up == 2:
                self.power_ups.append(Hammer())
            
    def update(self, score, game_speed, player):
        self.generate_power_up(score)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.has_power_up = True
                player.type = power_up.type
                player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)
        
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
            
    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)