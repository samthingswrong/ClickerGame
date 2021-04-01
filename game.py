import pygame
import random
import os

WIDTH = 480
HEIGHT = 640
map_texture_width: int = 32
map_texture_height: int = 32
FPS = 30

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
egg_texture = pygame.image.load(os.path.join(img_folder, 'egg.png'))
map_texture = pygame.image.load(os.path.join(img_folder, 'grass.png'))
x2_texture = pygame.image.load(os.path.join(img_folder, 'x2.png'))
x3_texture = pygame.image.load(os.path.join(img_folder, 'x3.png'))
x5_texture = pygame.image.load(os.path.join(img_folder, 'x5.png'))
auto_click_texture = pygame.image.load(os.path.join(img_folder, 'auto_click.png'))
chicken_texture = pygame.image.load(os.path.join(img_folder, 'chicken.png'))

pygame.init()
pygame.mixer.init()
map_sprites = pygame.sprite.Group()
obj_sprites = pygame.sprite.Group()
frames_counter = 0


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


def obj_create():
    obj_sprites.add(Texture(WIDTH / 2, 80, egg_texture))
    obj_sprites.add(Texture(60, 60, x2_texture))
    obj_sprites.add(Texture(60, 140, x3_texture))
    obj_sprites.add(Texture(60, 220, x5_texture))
    obj_sprites.add(Texture(60, 300, auto_click_texture))
    obj_sprites.add(Texture(WIDTH / 2, 300, chicken_texture))


def map_construct():
    for i in range(WIDTH // map_texture_width):
        for j in range(HEIGHT // map_texture_height):
            map_sprites.add(Texture(map_texture_width * (i + 0.5), map_texture_height * (j + 0.5), map_texture))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicker")
clock = pygame.time.Clock()

tap_flag = False
gameOver = False
game = Gameplay()
map_construct()
obj_create()

while not gameOver:
    clock.tick(FPS)
    f1 = pygame.font.Font(None, 30)
    f2 = pygame.font.Font(None, 36)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.score += game.tap_bonus
                tap_flag = True
            elif event.key == pygame.K_q:
                game.use_bonus_x2()
            elif event.key == pygame.K_w:
                game.use_bonus_x3()
            elif event.key == pygame.K_e:
                game.use_bonus_x5()
            elif event.key == pygame.K_r:
                game.use_bonus_auto_click()
    if frames_counter % FPS == 0:
        game.score += game.auto_click
    frames_counter += 1

    text_score = f2.render(str(game.score), True, (180, 0, 0))
    text_2x_price = f1.render(str(game.bonus_x2_price), True, (180, 0, 0))
    text_3x_price = f1.render(str(game.bonus_x3_price), True, (180, 0, 0))
    text_5x_price = f1.render(str(game.bonus_x5_price), True, (180, 0, 0))
    text_auto_click_price = f1.render(str(game.bonus_auto_click_price), True, (180, 0, 0))
    map_sprites.draw(screen)
    obj_sprites.draw(screen)
    if tap_flag:
        text_delta_pts = f1.render('+' + str(game.tap_bonus), True, (180, 0, 0))
        screen.blit(text_delta_pts, (WIDTH / 2 - 16, 350))
        tap_flag = False
    screen.blit(text_score, (275, 75))
    screen.blit(text_2x_price, (40, 80))
    screen.blit(text_3x_price, (40, 160))
    screen.blit(text_5x_price, (40, 240))
    screen.blit(text_auto_click_price, (50, 320))

    pygame.display.flip()

pygame.quit()
