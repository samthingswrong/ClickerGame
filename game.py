import Additional as Add
import os
import pygame

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
TEXT_SCORE_POS = (275, 75)
TEXT_2X_PRICE_POS = (40, 80)
TEXT_3X_PRICE_POS = (40, 160)
TEXT_5X_PRICE_POS = (40, 240)
TEXT_AUTO_CLICK_PRICE_POS = (50, 320)
TEXT_DELTA_PTS_POS = (WIDTH / 2 - 16, 350)
DEFAULT_COL = (180, 0, 0)

pygame.init()
map_sprites = pygame.sprite.Group()
obj_sprites = pygame.sprite.Group()
frames_counter = 0


def add_auto_click_bonus():
    global frames_counter
    if frames_counter % FPS == 0:
        game.score += game.auto_click
        frames_counter = 0
    frames_counter += 1


# Create object textures and add them to the queue for processing
def obj_create():
    obj_sprites.add(Add.Texture(WIDTH / 2, 80, egg_texture))
    obj_sprites.add(Add.Texture(60, 60, x2_texture))
    obj_sprites.add(Add.Texture(60, 140, x3_texture))
    obj_sprites.add(Add.Texture(60, 220, x5_texture))
    obj_sprites.add(Add.Texture(60, 300, auto_click_texture))
    obj_sprites.add(Add.Texture(WIDTH / 2, 300, chicken_texture))


# Create map texture and add them to the queue for processing
def map_construct():
    for i in range(WIDTH // map_texture_width):
        for j in range(HEIGHT // map_texture_height):
            map_sprites.add(Add.Texture(map_texture_width * (i + 0.5), map_texture_height * (j + 0.5), map_texture))


# Draw map textures, object textures and text
def draw():
    global screen, tap_flag
    map_sprites.draw(screen)  # Draw map
    obj_sprites.draw(screen)  # Draw objects
    # Create text
    text_size1 = pygame.font.Font(None, 30)
    text_size2 = pygame.font.Font(None, 36)
    # Draw text
    text_score = text_size2.render(str(game.score), True, DEFAULT_COL)
    text_2x_price = text_size1.render(str(game.bonus_x2_price), True, DEFAULT_COL)
    text_3x_price = text_size1.render(str(game.bonus_x3_price), True, DEFAULT_COL)
    text_5x_price = text_size1.render(str(game.bonus_x5_price), True, DEFAULT_COL)
    text_auto_click_price = text_size1.render(str(game.bonus_auto_click_price), True, DEFAULT_COL)
    if tap_flag:
        text_delta_pts = text_size1.render('+' + str(game.tap_bonus), True, DEFAULT_COL)
        screen.blit(text_delta_pts, TEXT_DELTA_PTS_POS)
        tap_flag = False
    screen.blit(text_score, TEXT_SCORE_POS)
    screen.blit(text_2x_price, TEXT_2X_PRICE_POS)
    screen.blit(text_3x_price, TEXT_3X_PRICE_POS)
    screen.blit(text_5x_price, TEXT_5X_PRICE_POS)
    screen.blit(text_auto_click_price, TEXT_AUTO_CLICK_PRICE_POS)
    # Show processed screen
    pygame.display.flip()


# Create screen with specific parameters
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clicker")
clock = pygame.time.Clock()

# Set default parameters
tap_flag = False
gameOver = False
game = Add.Gameplay()
map_construct()
obj_create()

# General game loop
while not gameOver:
    clock.tick(FPS)
    # processing of clicks
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
    add_auto_click_bonus()
    draw()

# Disable pygame
pygame.quit()
