import window as w
import constants
import pygame
import spaceship
import random
import enemy_tools


class Enemy:
    def __init__(self,enemy_type, is_boss, stage):
        self.enemy_type = enemy_type
        self.health = constants.health[enemy_type]
        self.speed = random.choice([-1, 1]) * 2
        self.mouth_state = 'closed'
        self._last_shot = pygame.time.get_ticks()
        self.width = enemy_tools.get_enemy_size_from_type(enemy_type)
        self.height = enemy_tools.get_enemy_size_from_type(enemy_type)
        self._x = random.randint(0, w.WIDTH - self.width)
        self.y = 50 if stage >= 3 else random.randint(50, 150)
        self.is_boss = is_boss

    # getter for x
    @property
    def x(self):
        return self._x
    
    # setter for x
    @x.setter
    def x(self, value):
        self._x = value

    # getter and setter for _last_shot
    @property
    def last_shot(self):
        return self._last_shot
    
    @last_shot.setter
    def last_shot(self, value):
        self._last_shot = value

    def mouthIsOpen(self):
        return self.mouth_state == 'open'
    
    def toggleMouthState(self):
        self.mouth_state = 'open' if self.mouth_state == 'closed' else 'closed'
    
    def toggle_direction(self):
        self.speed *= -1