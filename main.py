import pygame
import os

pygame.display.set_caption("Test")

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # WIN = window
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
SPACESHIP_HEIGHT, SPACESHIP_WIDTH = 55, 40
VEL = 4
BULLET_VEL = 8
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

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


def draw_window(player_red, player_yellow):
    WIN.fill(WHITE)
    WIN.blit(YELLOW_SPACESHIP, (player_yellow.x, player_yellow.y))
    WIN.blit(RED_SPACESHIP, (player_red.x, player_red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)

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


def main():
    player_red = pygame.Rect(700, 100, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    player_yellow = pygame.Rect(200, 100, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)

    red_player_bullets = []
    yellow_player_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:  # KEYDOWN = key pressed
                if event.key == pygame.K_LSHIFT:
                    bullet = pygame.Rect(
                        player_yellow.x + player_yellow.width,
                        player_yellow.y + player_yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_player_bullets.append(bullet)
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(
                        player_red.x,
                        player_red.y + player_red.height // 2 - 2,
                        10,
                        5,
                    )
                    red_player_bullets.append(bullet)
        key_pressed = pygame.key.get_pressed()
        move_player_yellow(player_yellow, key_pressed)
        move_player_red(player_red, key_pressed)
        draw_window(player_red, player_yellow)

    pygame.quit()


if __name__ == "__main__":
    main()
