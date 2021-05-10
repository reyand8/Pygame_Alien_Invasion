import pygame as pg
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pg.image.load("img/spaceship.png").convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        # Store horizontal position of ship
        self.x = float(self.rect.x)
        # Flags for continuous movement
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if (self.moving_right) and (
                self.rect.right < self.screen_rect.right):  # limit ship's movement so it doesn't go off screen
            self.x += self.settings.ship_speed
        if (self.moving_left) and (self.rect.left > 0):
            self.x -= self.settings.ship_speed
        self.rect.x = self.x  # update the rectangle's position once the ship has moved

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
