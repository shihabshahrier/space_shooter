import pygame
import os
import time

pygame.font.init()  # init font
pygame.mixer.init()  # init sound
pygame.display.set_caption("Test") # set window title

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # WIN = window

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)

FPS = 60
SPACESHIP_HEIGHT, SPACESHIP_WIDTH = 55, 40
VEL = 4
BULLET_VEL = 8
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
MAX_BULLETS = 2
PLAYER_HEALTH = 9

# Fonts
HEALTH_FONT = pygame.font.SysFont("comicsans", 30)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

# USEREVENT = pygame.event.custom_type()
RED_PLAYER_HIT = pygame.USEREVENT + 1
YELLOW_PLAYER_HIT = pygame.USEREVENT + 2

# Images and scaling
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "yellowShip.png")
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH)),
    90,
)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "redShip.png")
)
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (55, 40)), 270
)

SPACE_VIEW = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space_view.png")), (WIDTH, HEIGHT)
)

# Sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "hit_sound.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "shooting_sound.mp3"))


# Draw window
def draw_window(player_red, player_yellow, yellow_player_bullets, red_player_bullets, red_player_health, yellow_player_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE_VIEW, (0, 0))
    # draw text
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_player_health), 1, RED_COLOR
    )
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_player_health), 1, YELLOW_COLOR
    )
    quit_text = SMALL_FONT.render("Press ESC to quit", 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(quit_text, (WIDTH - quit_text.get_width() - 10, HEIGHT - quit_text.get_height() - 10))

    WIN.blit(YELLOW_SPACESHIP, (player_yellow.x, player_yellow.y))
    WIN.blit(RED_SPACESHIP, (player_red.x, player_red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # draw bullets
    for bullet in yellow_player_bullets:
        pygame.draw.rect(WIN, YELLOW_COLOR, bullet)

    for bullet in red_player_bullets:
        pygame.draw.rect(WIN, RED_COLOR, bullet)

    pygame.display.update()


def move_player_yellow(player_yellow, key_pressed):
    if key_pressed[pygame.K_a] and player_yellow.x - VEL > 0:  # LEFT
        player_yellow.x -= VEL
    if (
        key_pressed[pygame.K_d]
        and player_yellow.x + VEL + player_yellow.width < BORDER.x
    ):  # RIGHT
        player_yellow.x += VEL
    if key_pressed[pygame.K_w] and player_yellow.y - VEL > 0:  # UP
        player_yellow.y -= VEL
    if (
        key_pressed[pygame.K_s]
        and player_yellow.y + 2 * VEL + player_yellow.height < HEIGHT
    ):  # DOWN
        player_yellow.y += VEL


def move_player_red(player_red, key_pressed):
    if (
        key_pressed[pygame.K_LEFT] and player_red.x - VEL > BORDER.x + BORDER.width
    ):  # LEFT
        player_red.x -= VEL
    if (
        key_pressed[pygame.K_RIGHT] and player_red.x + VEL + player_red.width < WIDTH
    ):  # RIGHT
        player_red.x += VEL
    if key_pressed[pygame.K_UP] and player_red.y - VEL > 0:  # UP
        player_red.y -= VEL
    if (
        key_pressed[pygame.K_DOWN]
        and player_red.y + 2 * VEL + player_red.height < HEIGHT
    ):
        player_red.y += VEL

def bullet_control(yellow_player_bullets, red_player_bullets, player_yellow, player_red):
    for bullet in yellow_player_bullets:
        bullet.x += BULLET_VEL
        if player_red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_PLAYER_HIT))
            yellow_player_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_player_bullets.remove(bullet)
    for bullet in red_player_bullets:
        bullet.x -= BULLET_VEL
        if player_yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_PLAYER_HIT))
            red_player_bullets.remove(bullet)
        elif bullet.x < 0:
            red_player_bullets.remove(bullet)

def winner(winner_text):
    winner_text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    player_red = pygame.Rect(700, 100, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    player_yellow = pygame.Rect(200, 100, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)

    red_player_bullets = []
    yellow_player_bullets = []

    red_player_health = PLAYER_HEALTH
    yellow_player_health = PLAYER_HEALTH
    

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # QUIT = close window
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:  # KEYDOWN = key pressed
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

                if event.key == pygame.K_LSHIFT and len(yellow_player_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        player_yellow.x + player_yellow.width,
                        player_yellow.y + player_yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_player_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RSHIFT and len(red_player_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        player_red.x,
                        player_red.y + player_red.height // 2 - 2,
                        10,
                        5,
                    )
                    red_player_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type == RED_PLAYER_HIT:
                red_player_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_PLAYER_HIT:
                yellow_player_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_player_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_player_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        move_player_yellow(player_yellow, key_pressed)
        move_player_red(player_red, key_pressed)
        bullet_control(yellow_player_bullets, red_player_bullets, player_yellow, player_red)
        draw_window(player_red, player_yellow, yellow_player_bullets, red_player_bullets, red_player_health, yellow_player_health)

    # pygame.quit()
    main()

if __name__ == "__main__":
    main()
