
import pygame
import sys
import random
import os

# --- 常數設定 ---
# 螢幕設定
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 蛇的設定
SNAKE_COLOR = GREEN
SNAKE_INITIAL_SPEED = 10 # 初始速度 (等級1)

# 食物設定
FOOD_COLOR = RED

# --- 遊戲初始化 ---
pygame.init()
pygame.mixer.init() # 初始化音效模組

# 設定螢幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('貪食蛇')

# 時脈控制
clock = pygame.time.Clock()

# 字型設定
font = pygame.font.SysFont(None, 35)

# --- 音效與音樂 ---
# 請將您的音檔放在 'assets' 資料夾中
# 背景音樂
try:
    pygame.mixer.music.load(os.path.join('assets', 'background.mp3'))
    pygame.mixer.music.play(-1) # -1 表示無限循環播放
except pygame.error as e:
    print(f"無法載入背景音樂: {e}")

# 音效
try:
    eat_sound = pygame.mixer.Sound(os.path.join('assets', 'eat_sound.wav'))
    game_over_sound = pygame.mixer.Sound(os.path.join('assets', 'game_over_sound.wav'))
except pygame.error as e:
    print(f"無法載入音效: {e}")


# --- 遊戲物件 ---
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.color = SNAKE_COLOR
        self.score = 0
        self.speed = SNAKE_INITIAL_SPEED
        self.level = 1

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y*GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        if 'game_over_sound' in globals():
            game_over_sound.play()
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])
        self.score = 0
        self.speed = SNAKE_INITIAL_SPEED
        self.level = 1
        # 可以在這裡加入遊戲結束畫面

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, BLACK, r, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, BLACK, r, 1)

# --- 遊戲主迴圈 ---
def main():
    snake = Snake()
    food = Food()
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_q: # 新增的停止按鈕
                    pygame.quit()
                    sys.exit()
                elif not paused:
                    if event.key == pygame.K_UP:
                        snake.turn((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.turn((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.turn((1, 0))

        if not paused:
            snake.move()

            if snake.get_head_position() == food.position:
                snake.length += 1
                snake.score += 1
                if 'eat_sound' in globals():
                    eat_sound.play()
                food.randomize_position()

                # 等級提升邏輯
                if snake.score % 5 == 0: # 每得到5分就提升一個等級
                    snake.level += 1
                    snake.speed += 2 # 速度加快

            # 碰撞檢測 (撞到牆壁)
            head = snake.get_head_position()
            if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
                snake.reset()

            # 碰撞檢測 (撞到自己)
            if len(snake.positions) > 1 and head in snake.positions[1:]:
                snake.reset()

        # 繪製畫面
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)

        # 顯示分數和等級
        score_text = font.render(f"Score: {snake.score}", True, WHITE)
        level_text = font.render(f"Level: {snake.level}", True, WHITE)
        screen.blit(score_text, (5, 10))
        screen.blit(level_text, (5, 40))

        if paused:
            pause_text = font.render("Paused", True, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(pause_text, text_rect)


        pygame.display.update()
        clock.tick(snake.speed)

if __name__ == '__main__':
    main()
