import pygame, random

from utilities import Projectile, Sun

class Plant:

    def __init__(self, game, type, pos, max_health):
        self.game = game
        self.type = type
        self.pos = pos
        self.img = game.assets["plants"][type]
        self.max_health = max_health
        self.health = max_health

        self.damage_cooldown = 30

    def rect(self):
        return pygame.Rect((self.pos[0]*24) + 56, (self.pos[1]*24) + 50, 16, 16)

    def update(self, draw_pos):
        self.damage_cooldown -= 1

    def draw(self, display, draw_pos):
        display.blit(self.img, draw_pos)

    def damage(self):
        if self.damage_cooldown <= 0:
            self.health -= 1
            self.damage_cooldown = 30


class Walnut(Plant):
    
    def __init__(self, game, pos):
        self.game = game
        self.type = "walnut"
        self.pos = pos
        self.max_health = 30
        self.health = 30

        self.img = game.assets["plants"]["walnut"][0]

        self.damage_cooldown = 30

    def update(self, draw_pos):
        if self.health <= 20:
            self.img = self.game.assets["plants"]["walnut"][1]
            if self.health <= 10:
                self.img = self.game.assets["plants"]["walnut"][2]

        return super().update(draw_pos)
    
    def draw(self, display, draw_pos):
        super().draw(display, draw_pos)