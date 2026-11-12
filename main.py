import pygame
import random

pygame.init()
pygame.mixer.init()

WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

BACKGROUND = (0, 0, 0)
SNAKE_COLOUR = (0, 255, 0)
CELL_SIZE = 20
GRID_COLOUR = (35, 35, 35)
SNAKE_HEAD_COLOUR = (79, 121, 66)

EAT_SOUND = pygame.mixer.Sound("eat.wav")
CRASH_SOUND = pygame.mixer.Sound("crash.wav")

snake = [
        [100, 100],
        [80, 100],
        [60, 100]
    ]

def create_food():
    while True:
        position = [
            random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE)
        ]

        if position not in snake:
            return position

def reset_game():
    new_snake = [
        [100, 100],
        [80, 100],
        [60, 100]
    ]

    new_direction = "RIGHT"
    new_food = create_food()
    new_score = 0

    return new_snake, new_food, new_direction, new_score


snake, food, direction, score = reset_game()
FOOD_COLOUR = (255, 0 , 0)

MOVE_DELAY = 200
last_move_time = pygame.time.get_ticks()

running = True

font = pygame.font.SysFont(None, 60)

game_state = "MENU"
difficulty = "MEDIUM"

DIFFICULTIES = {
    "EASY" : 250,
    "MEDIUM" : 150,
    "HARD" : 80
}

MOVE_DELAY = DIFFICULTIES[difficulty]

def draw_text(text, size, colour, x, y):
    text_font = pygame.font.SysFont(None, size)
    text_surface = text_font.render(
        text,
        True,
        colour
    )

    text_rect = text_surface.get_rect(center = (x, y))
    screen.blit(text_surface, text_rect)

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())

    except (FileNotFoundError, ValueError):
        return 0

high_score = load_high_score()   

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(
            screen,
            GRID_COLOUR,
            (x, 0),
            (x, HEIGHT)
        )

    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(
            screen,
            GRID_COLOUR,
            (0, y),
            (WIDTH, y)
        )

def  draw_food():
    pygame.draw.rect(
        screen,
        (120, 0, 0),
        (food[0], food[1], CELL_SIZE, CELL_SIZE)
    )

    pygame.draw.rect(
        screen,
        FOOD_COLOUR,
        (food[0] + 4, food[1] + 4, CELL_SIZE - 8, CELL_SIZE - 8)
    )

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "MENU":
                if event.key == pygame.K_1:
                    difficulty = "EASY"

                elif event.key == pygame.K_2:
                    difficulty = "MEDIUM"

                elif event.key == pygame.K_3:
                    difficulty = "HARD"

                elif event.key == pygame.K_RETURN:
                    snake, food, direction, score = reset_game()
                    MOVE_DELAY = DIFFICULTIES[difficulty]
                    last_move_time = pygame.time.get_ticks()
                    game_state = "PLAYING"
   
            elif game_state == "PLAYING":

                if event.key == pygame.K_SPACE:
                    game_state = "PAUSED"

                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"

                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"

                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"

                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

            elif game_state =="PAUSED":
                if event.key == pygame.K_SPACE:
                    game_state = "PLAYING"


            elif game_state == "GAME_OVER":
                if event.key == pygame.K_r:

                    snake, food, direction, score = reset_game()

                    last_move_time = pygame.time.get_ticks()

                    game_state = "PLAYING"

                elif event.key == pygame.K_m:
                    game_state = "MENU"


    current_time = pygame.time.get_ticks()

    if (game_state == "PLAYING" and current_time - last_move_time >= MOVE_DELAY):
        new_head = snake[0].copy()

        if direction == "UP":
            new_head[1] -= CELL_SIZE

        elif direction == "DOWN":
            new_head[1] += CELL_SIZE

        elif direction == "LEFT":
            new_head[0] -= CELL_SIZE

        elif direction == "RIGHT":
            new_head[0] += CELL_SIZE

        snake.insert(0, new_head)

        if(
            new_head[0] < 0 or
            new_head[0] >= WIDTH or
            new_head[1] < 0 or
            new_head[1] >= HEIGHT
        ):
            CRASH_SOUND.play()
            game_state = "GAME_OVER"
            high_score = max(high_score, score)
            save_high_score(high_score)

        elif new_head in snake[1:]:
            CRASH_SOUND.play()
            game_state = "GAME_OVER"
            high_score = max(high_score, score)
            save_high_score(high_score)        

        else:
            if new_head == food:
                score += 1
                EAT_SOUND.play()
                food = create_food()

            else:
                snake.pop()

        last_move_time = current_time

        
    screen.fill(BACKGROUND)
    draw_grid()

    if game_state == "MENU":

        draw_text("SNAKE GAME", 80, (0, 255, 0), WIDTH//2, 150)

        draw_text("Select Difficulty", 45, (255, 255, 255), WIDTH//2, 260)

        draw_text("1 - EASY", 35, (255, 255, 255), WIDTH//2, 330)

        draw_text("2 - MEDIUM", 35, (255, 255, 255), WIDTH//2, 380)

        draw_text("3 - HARD", 35, (255, 255, 255), WIDTH//2, 430)

        draw_text(f"Selected: {difficulty}", 35, (255, 255, 0), WIDTH//2, 500)

        draw_text("Press ENTER to Start", 35, (255, 255, 255), WIDTH//2, 570)

    elif game_state == "PLAYING":
        draw_food()

        for index, segment in enumerate(snake):
            if index == 0:
                colour = SNAKE_HEAD_COLOUR
            else:
                colour = SNAKE_COLOUR
            pygame.draw.rect(
                screen,
                colour,
            (segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            )

        draw_text(f"Score: {score}", 40, (255, 255, 255), 100, 30)

        draw_text(f"Highest Score: {high_score}", 40, (255, 255, 255), 1050, 30)

    elif game_state == "GAME_OVER":

        draw_text("GAME OVER", 80, (255, 0, 0), WIDTH//2, 230)

        draw_text(f"Final Score: {score}", 45, (255, 255, 255), WIDTH//2, 320)

        draw_text(f"High Score: {high_score}", 45, (255, 255, 0), WIDTH//2, 380)

        draw_text("R - Restart", 35, (255, 255, 255), WIDTH//2, 460)

        draw_text("M - Main Menu", 35, (255, 255, 255), WIDTH//2, 510)

    elif game_state == "PAUSED":

        draw_food()
  
        for index, segment in enumerate(snake):
            if index == 0:
                colour = SNAKE_HEAD_COLOUR
            else:
                colour = SNAKE_COLOUR
            pygame.draw.rect(
                screen,
                colour,
            (segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            )

        draw_text("PAUSED", 80, (255, 255, 0), WIDTH//2, 280)

        draw_text("Press SPACE to Resume", 40, (255, 255, 255), WIDTH//2, 370)
    clock.tick(60)
    pygame.display.update()
pygame.quit()