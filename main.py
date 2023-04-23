import pygame
from pygame.math import Vector2
import random


CELL_SIZE = 20
CELL_NUMS = 20
SIZE = WIDTH, HEIGHT = [CELL_NUMS * CELL_SIZE] * 2
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)


pygame.init()
screen = pygame.display.set_mode(SIZE)

pygame.display.set_caption("haha")


class Food:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, CELL_NUMS - 1)
        self.y = random.randint(0, CELL_NUMS - 1)
        self.pos = Vector2(self.x, self.y)

    def draw(self):
        pygame.draw.rect(screen, "orange",
                         pygame.Rect(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)  # Vector2(0, 0) 表示不移动，本质是蛇在不断reset
        self.eat = False

    def draw(self):
        for block in self.body:
            pygame.draw.rect(screen, "green",
                             pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def move(self):
        if not self.eat:
            new_body = self.body[:-1]
        else:
            new_body = self.body[:]
            self.eat = False

        new_body.insert(0, self.body[0] + self.direction)
        self.body = new_body

    def handle_direction(self):
        press_keys = pygame.key.get_pressed()
        if press_keys[pygame.K_UP] and self.direction != Vector2(0, 1):
            self.direction = Vector2(0, -1)
        elif press_keys[pygame.K_DOWN] and self.direction != Vector2(0, -1):
            self.direction = Vector2(0, 1)
        elif press_keys[pygame.K_LEFT] and self.direction != Vector2(1, 0):
            self.direction = Vector2(-1, 0)
        elif press_keys[pygame.K_RIGHT] and self.direction != Vector2(-1, 0):
            self.direction = Vector2(1, 0)

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)


class Game:
    def __init__(self):
        self.food = Food()
        self.snake = Snake()

    def handle_snake_direction(self):
        press_keys = pygame.key.get_pressed()
        if press_keys[pygame.K_UP] and self.snake.direction != DOWN:
            self.snake.direction = Vector2(0, -1)
        elif press_keys[pygame.K_DOWN] and self.snake.direction != UP:
            self.snake.direction = Vector2(0, 1)
        elif press_keys[pygame.K_LEFT] and self.snake.direction != RIGHT:
            self.snake.direction = Vector2(-1, 0)
        elif press_keys[pygame.K_RIGHT] and self.snake.direction != LEFT:
            self.snake.direction = Vector2(1, 0)

    def draw_glass(self):
        for i in range(CELL_NUMS):
            pygame.draw.line(screen, "black", (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 1)
            pygame.draw.line(screen, "black", (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 1)

    def check_eat(self):
        if self.food.pos == self.snake.body[0]:
            self.snake.eat = True
            self.food.reset()

    def check_collision(self):
        # 检测是否撞墙
        if self.snake.body[0].x >= CELL_NUMS or self.snake.body[0].x < 0:
            self.snake.reset()
        if self.snake.body[0].y >= CELL_NUMS or self.snake.body[0].y < 0:
            self.snake.reset()

        # 检测和自己重叠
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.snake.reset()


game = Game()

SNAKE_MOVE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_MOVE, 150)
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == SNAKE_MOVE:
            game.snake.move()

    # 控制蛇运动的方向
    game.handle_snake_direction()
    game.check_eat()
    game.check_collision()

    screen.fill("white")
    game.draw_glass()
    game.food.draw()
    game.snake.draw()

    pygame.display.flip()
    clock.tick(60)
