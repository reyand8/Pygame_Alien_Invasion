class Settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (245, 245, 220)
        self.ship_limit = 3

        self.bullets_allowed = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)

        self.fleet_drop_speed = 20
        self.score_scale = 1.1618
        self.speedup_scale = 1.5
        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 4.0
        self.alien_speed = 1.5
        self.fleet_direction = 1
        self.alien_points = 10

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
