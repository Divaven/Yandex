import pygame
import random
from random import randrange

# константы
WIDTH, HEIGHT = 1200, 800
FPS = 60
PW = 315
PH = 40
SPEED = 15
PADDLE = pygame.Rect(WIDTH // 2 - PW // 2, HEIGHT - PH - 10, PW, PH)

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

img = pygame.image.load('Wallpaper.jpg').convert()

sound1 = pygame.mixer.Sound("Music1.mp3")
sound2 = pygame.mixer.Sound("Music2.mp3")
sound3 = pygame.mixer.Sound("Music3.mp3")
sound4 = pygame.mixer.Sound("Music4.mp3")
sound5 = pygame.mixer.Sound("Music5.mp3")

music = [sound1, sound2, sound3, sound4, sound5]

now_plaeing = random.choice(music)


def collision(x, y, ball, rect):
    if x > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if y > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        x, y = -x, -y
    elif delta_x > delta_y:
        y = -y
    elif delta_y > delta_x:
        x = -x
    return x, y


if __name__ == '__main__':
    now_plaeing.play()

    # задаем харатеристики мяча
    radius_of_ball = 18
    speed_of_ball = 5
    rect_of_ball = int(radius_of_ball * 2 ** 0.5)
    ball = pygame.Rect(randrange(rect_of_ball, WIDTH - rect_of_ball), HEIGHT // 2, rect_of_ball, rect_of_ball)
    x, y = 1, -1

    # задаем блоки
    block_list = [pygame.Rect(8 + 120 * i, 8 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
    color_list = [(randrange(30, 256), randrange(30, 256), randrange(30, 256)) for i in range(10) for j in range(4)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        sc.blit(img, (0, 0))
        # карта
        [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(sc, pygame.Color('darkgreen'), PADDLE)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, radius_of_ball)
        # перемещение мяча
        ball.x += speed_of_ball * x
        ball.y += speed_of_ball * y

        if ball.centerx < radius_of_ball or ball.centerx > WIDTH - radius_of_ball:
            x = -x

        if ball.centery < radius_of_ball:
            y = -y

        if ball.colliderect(PADDLE) and y > 0:
            x, y = collision(x, y, ball, PADDLE)

        index = ball.collidelist(block_list)
        if index != -1:
            rect = block_list.pop(index)
            col = color_list.pop(index)
            x, y = collision(x, y, ball, rect)

            rect.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(sc, col, rect)
            FPS += 2

        if ball.bottom > HEIGHT:
            exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and PADDLE.left > 0:
            PADDLE.left -= SPEED
        if key[pygame.K_RIGHT] and PADDLE.right < WIDTH:
            PADDLE.right += SPEED

        pygame.display.flip()
        clock.tick(FPS)
