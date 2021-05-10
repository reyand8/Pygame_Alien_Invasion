import pygame as pg
import pygame.font as pgf


class Message:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        # Properties of the message
        self.width, self.height = 400, 200
        self.text_colour = (255, 255, 255)
        self.message_colour = (189, 236, 182)
        self.font = pgf.SysFont(None, 80)
        # Build Rect object
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        # Add message
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_colour,
                                          self.message_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.message_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
