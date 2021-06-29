import pygame
from dataclasses import dataclass
from typing import Any

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

fps_clock = pygame.time.Clock()


@dataclass
class Player:
    """
    Class containing all information on a p.
    """
    image: Any
    x_pos: int
    y_pos: int
    width: int
    height: int
    score: int
    y_vel: int = 0


def main():
    pygame.init()

    pygame.display.set_caption('pypong')

    screen = pygame.display.set_mode((800, 600))

    img1 = pygame.image.load('assets/paddle_1.png')
    p1 = Player(image=img1,
                x_pos=0,
                y_pos=SCREEN_HEIGHT // 2 - img1.get_height() // 2,
                width=img1.get_width(),
                height=img1.get_height(),
                score=0)

    img2 = pygame.image.load('assets/paddle_2.png')
    p2 = Player(image=img2,
                x_pos=SCREEN_WIDTH - img2.get_width(),
                y_pos=SCREEN_HEIGHT // 2 - img2.get_height() // 2,
                width=img2.get_width(),
                height=img2.get_height(),
                score=0)

    screen.blit(p1.image, (p1.x_pos, p1.y_pos))
    screen.blit(p2.image, (p2.x_pos, p2.y_pos))
    pygame.display.flip()

    running = True
    while running:
        # screen.blit(p_1, (50, 50))
        # screen.blit(p_2, (500, 500))
        # pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
        update_state(p1, p2)
        draw(screen, p1, p2)
        fps_clock.tick(FPS)


def update_state(p1: Player, p2: Player):
    speed = 15
    # Update player 1 position, keeping them in bounds
    if p1.y_vel < 0 and p1.y_pos > 0:
        p1.y_pos += p1.y_vel * speed
    elif p1.y_vel > 0 and p1.y_pos + p1.height < SCREEN_HEIGHT:
        p1.y_pos += p1.y_vel * speed

    # Update player 2 position, keeping them in bounds
    if p2.y_vel < 0 and p2.y_pos > 0:
        p2.y_pos += p2.y_vel * speed
    elif p2.y_vel > 0 and p2.y_pos + p2.height < SCREEN_HEIGHT:
        p2.y_pos += p2.y_vel * speed


def draw(screen, p1: Player, p2: Player):
    # Fill screen with black to clear previously drawn frames
    screen.fill([255, 255, 255])
    screen.blit(p1.image, (p1.x_pos, p1.y_pos))
    screen.blit(p2.image, (p2.x_pos, p2.y_pos))
    pygame.display.flip()


if __name__ == '__main__':
    main()
