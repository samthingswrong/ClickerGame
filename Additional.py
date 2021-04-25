import pygame


class Gameplay:
    score = 0
    tap_bonus = 5
    auto_click = 0
    bonus_x2_price = 100
    bonus_x3_price = 500
    bonus_x5_price = 1000
    bonus_auto_click_lvl = 0
    bonus_auto_click_price = 50

    def use_bonus_auto_click(self):
        if self.score >= self.bonus_auto_click_price:
            self.score -= self.bonus_auto_click_price
            self.bonus_auto_click_price *= 2
            self.auto_click += self.tap_bonus

    def use_bonus_x2(self):
        if self.score >= self.bonus_x2_price:
            self.score -= self.bonus_x2_price
            self.tap_bonus *= 2
            self.bonus_x2_price *= 2

    def use_bonus_x3(self):
        if self.score >= self.bonus_x3_price:
            self.score -= self.bonus_x3_price
            self.tap_bonus *= 3
            self.bonus_x3_price *= 3

    def use_bonus_x5(self):
        if self.score >= self.bonus_x5_price:
            self.score -= self.bonus_x5_price
            self.tap_bonus *= 5
            self.bonus_x5_price *= 5


class Texture(pygame.sprite.Sprite):
    def __init__(self, x_coord, y_coord, texture):
        pygame.sprite.Sprite.__init__(self)
        self.image = texture
        self.rect = self.image.get_rect()
        self.rect.center = (x_coord, y_coord)
