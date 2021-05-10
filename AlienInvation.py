import sys
import pygame as pg
from time import sleep
import os.path

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:

    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        if not os.path.exists(self.stats.my_scores):
            self.stats.create_high_score_json()
        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self._create_fleet()

        # Main Title Buttons

        self.title = Button(self, "Alien Invasion")
        self.title._prep_button_to_title()

        self.play_button = Button(self, "Start")

        self.high_score_button = Button(self, "High-Scores")
        self.high_score_button._change_rect_to(self.play_button.screen_rect.centerx,
                                               self.play_button.screen_rect.centery + 100)
        self.instructions_button = Button(self, "Instructions")
        self.instructions_button._change_rect_to(self.play_button.screen_rect.centerx,
                                                 self.play_button.screen_rect.centery + 200)

        self.is_next_level = False
        self.is_instructions_pane = False
        self.is_high_score_pane = False

    def run_game(self):

        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_instructions_button(mouse_pos)
                self._check_scores_button(mouse_pos)
                self._check_play_button(mouse_pos)
            elif event.type == pg.KEYDOWN:  # checks if user presses a key
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if (event.key == pg.K_RIGHT) and (not self.is_next_level):
            self.ship.moving_right = True
        elif (event.key == pg.K_LEFT) and (not self.is_next_level):
            self.ship.moving_left = True
        elif (event.key == pg.K_SPACE) and (not self.is_next_level):
            self._fire_bullet()
        elif (event.key == pg.K_q) or (event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        elif event.key == pg.K_x:
            self.settings.fleet_drop_speed = 150
        elif event.key == pg.K_g:
            self.settings.bullet_speed = 20
            self.settings.ship_speed = 10
        elif (event.key == pg.K_RETURN) and (self.is_next_level):
            self.is_next_level = False
            self.settings.alien_speed = 1
            sleep(0.5)
        elif event.key == pg.K_BACKSPACE:
            self.is_instructions_pane = False
            self.is_high_score_pane = False

    def _check_keyup_events(self, event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_colour)
        if self.stats.game_active:
            self.ship.blitme()
            self.sb.show_score()
            if self.is_next_level:
                self.settings.alien_speed = 0
                next_level = Button(self, f"Level {self.stats.level}")
                next_level._prep_button_to_message()
                next_level.draw_button()
            else:
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                self.aliens.draw(self.screen)
        else:
            if self.is_instructions_pane:
                self.sb.draw_instructions()
            elif self.is_high_score_pane:
                self.sb.draw_high_scores()
            else:
                self.title.draw_button()
                self.play_button.draw_button()
                self.high_score_button.draw_button()
                self.instructions_button.draw_button()

        pg.display.flip()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _remove_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_bullets(self):
        self.bullets.update()
        self._remove_bullets()
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)  # bullets are key; aliens are values
        if collisions:
            self.stats.score += self.settings.alien_points
            self.sb.game_score()
            self.sb.check_best_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.is_next_level = True
            self.sb.new_levels()
            self.settings.alien_speed = 0

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):

        self._check_fleet_edges()
        self.aliens.update()
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= - 1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(1.0)
        else:
            self.stats.update_high_scores()
            self.stats.game_active = False
            pg.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(
            mouse_pos)  # check whether the click coordinate is within the rect of the button
        in_menu = self.stats.game_active or self.is_high_score_pane or self.is_instructions_pane
        if button_clicked and not in_menu:
            self.settings.initialise_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.game_score()
            self.sb.new_levels()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pg.mouse.set_visible(False)

            self.is_next_level = True

    def _check_instructions_button(self, mouse_pos):
        button_clicked = self.instructions_button.rect.collidepoint(mouse_pos)
        in_menu = self.stats.game_active or self.is_high_score_pane
        if button_clicked and not in_menu:
            self.is_instructions_pane = True

    def _check_scores_button(self, mouse_pos):
        button_clicked = self.high_score_button.rect.collidepoint(mouse_pos)
        in_menu = self.stats.game_active or self.is_instructions_pane
        if button_clicked and not in_menu:
            self.is_high_score_pane = True


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
