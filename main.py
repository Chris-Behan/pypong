import pygame
from dataclasses import dataclass
from typing import Any

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

fps_clock = pygame.time.Clock()


@dataclass
class Player:
    image: Any
    x_pos: int
    y_pos: int
    width: int
    height: int
    score: int = 0
    y_vel: int = 0


@dataclass
class Ball:
    image: Any
    x_pos: int
    y_pos: int
    width: int
    height: int
    y_vel: int = 0
    x_vel: int = 0


def main():
    pygame.init()

    pygame.display.set_caption('pypong')

    screen = pygame.display.set_mode((800, 600))

    img1 = pygame.image.load('assets/paddle_1.png')
    p1 = Player(image=img1,
                x_pos=0,
                y_pos=SCREEN_HEIGHT / 2 - img1.get_height() / 2,
                width=img1.get_width(),
                height=img1.get_height())

    img2 = pygame.image.load('assets/paddle_2.png')
    p2 = Player(image=img2,
                x_pos=SCREEN_WIDTH - img2.get_width(),
                y_pos=SCREEN_HEIGHT / 2 - img2.get_height() / 2,
                width=img2.get_width(),
                height=img2.get_height())

    ball_img = pygame.image.load('assets/ball.png')
    ball = Ball(
        image=ball_img,
        x_pos=SCREEN_WIDTH / 2 - ball_img.get_width() / 2,
        y_pos=SCREEN_HEIGHT / 2 - ball_img.get_height() / 2,
        width=ball_img.get_width(),
        height=ball_img.get_height(),
        y_vel=0,
        x_vel=1
    )

    game_loop(screen, p1, p2, ball)


def game_loop(screen: Any, p1: Player, p2: Player, ball: Ball):
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            handle_input(event, p1, p2)

        update_state(p1, p2, ball)
        draw(screen, p1, p2, ball)
        fps_clock.tick(FPS)


def handle_input(event: Any, p1: Player, p2: Player):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            p1.y_vel += 1
        if event.key == pygame.K_w:
            p1.y_vel -= 1
        if event.key == pygame.K_k:
            p2.y_vel += 1
        if event.key == pygame.K_i:
            p2.y_vel -= 1

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_s:
            p1.y_vel -= 1
        if event.key == pygame.K_w:
            p1.y_vel += 1
        if event.key == pygame.K_k:
            p2.y_vel -= 1
        if event.key == pygame.K_i:
            p2.y_vel += 1


def update_state(p1: Player, p2: Player, ball: Ball):
    player_speed = 15
    ball_speed = 7
    # Update player 1 position, keeping them in bounds
    if p1.y_vel < 0 and p1.y_pos > 0:
        p1.y_pos += p1.y_vel * player_speed
    elif p1.y_vel > 0 and p1.y_pos + p1.height < SCREEN_HEIGHT:
        p1.y_pos += p1.y_vel * player_speed

    # Update player 2 position, keeping them in bounds
    if p2.y_vel < 0 and p2.y_pos > 0:
        p2.y_pos += p2.y_vel * player_speed
    elif p2.y_vel > 0 and p2.y_pos + p2.height < SCREEN_HEIGHT:
        p2.y_pos += p2.y_vel * player_speed

    # Get easy to read coordinates
    ball_x_left = ball.x_pos
    ball_x_right = ball.x_pos + ball.width
    ball_y_top = ball.y_pos
    ball_y_bottom = ball.y_pos + ball.height
    ball_y_center = ball.y_pos + ball.height / 2
    p1_y_center = p1.y_pos + p1.height / 2
    p2_y_center = p2.y_pos + p1.height / 2

    # Handle collisions
    if (ball_x_left <= p1.x_pos + p1.width and ball_y_bottom >= p1.y_pos and ball_y_top <= p1.y_pos + p1.height):
        ball.x_vel = abs(ball.x_vel)
        ball.y_vel = (ball_y_center - p1_y_center) / p1.height

    elif (ball_x_right >= p2.x_pos and ball_y_bottom >= p2.y_pos and ball_y_top <= p2.y_pos + p2.height):
        ball.x_vel = -abs(ball.x_vel)
        ball.y_vel = (ball_y_center - p2_y_center) / p2.height

    elif ball_y_top <= 0:
        ball.y_vel *= -1

    elif ball_y_bottom >= SCREEN_HEIGHT:
        ball.y_vel *= -1

    elif ball_x_left <= 0:
        p2.score += 1
        ball.x_pos = SCREEN_WIDTH/2 - ball.width / 2
        ball.y_pos = SCREEN_HEIGHT/2 - ball.height / 2

    elif ball_x_right >= SCREEN_WIDTH:
        p1.score += 1
        ball.x_pos = SCREEN_WIDTH/2 - ball.width / 2
        ball.y_pos = SCREEN_HEIGHT/2 - ball.height / 2

    # Update ball position
    ball.x_pos += ball.x_vel * ball_speed
    ball.y_pos += ball.y_vel * ball_speed


def draw(screen, p1: Player, p2: Player, ball: Ball):
    # Fill screen with black to clear previously drawn frames
    screen.fill([255, 255, 255])

    score_font = pygame.font.SysFont('Comic Sans MS', 60)
    p1_score = score_font.render(f'{p1.score}', False, (0, 0, 0))
    p2_score = score_font.render(f'{p2.score}', False, (0, 0, 0))

    screen.blit(p1_score, (100, 100))
    screen.blit(p2_score, (SCREEN_WIDTH - 100, 100))

    screen.blit(p1.image, (p1.x_pos, p1.y_pos))
    screen.blit(p2.image, (p2.x_pos, p2.y_pos))
    screen.blit(ball.image, (ball.x_pos, ball.y_pos))

    pygame.display.flip()


if __name__ == '__main__':
    main()
