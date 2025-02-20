import pygame
import sys
import random

pygame.init()

width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with Tomatoes")

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

def show_score(score):
    value = score_font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(value, [0, 0])

def startScreen():
    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        message("Press any key to start", (255, 255, 255))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def gameLoop():
    game_over = False     
    game_close = False    

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    Length_of_snake = 3
    snake_List = []
    for i in range(Length_of_snake):
        snake_List.append([x1 - i * snake_block, y1])

    score = 0

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    obstacles = []
    num_obstacle_rows = 3      
    obstacles_per_row = 10     
    
    margin = snake_block * 2    
    available_width = width - 2 * margin
    spacing_x = available_width // (obstacles_per_row - 1) if obstacles_per_row > 1 else 0

    y_start = 50                
    row_spacing = snake_block * 2  

    for row in range(num_obstacle_rows):
        for col in range(obstacles_per_row):
            ox = margin + col * spacing_x
            oy = y_start + row * row_spacing
            obstacles.append([ox, oy])

    waiting_for_direction = True
    while waiting_for_direction:
        screen.fill((0, 0, 0))
        message("Press an arrow key to move", (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                    waiting_for_direction = False
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                    waiting_for_direction = False
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                    waiting_for_direction = False
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                    waiting_for_direction = False

    while not game_over:
        
        while game_close:
            screen.fill((0, 0, 0))
            message("You Lost! Press Q to Quit or C to Play Again", (255, 0, 0))
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change != snake_block:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        screen.fill((0, 0, 0))
        
        pygame.draw.circle(screen, (255, 0, 0), 
                           (int(foodx + snake_block / 2), int(foody + snake_block / 2)), 
                           snake_block // 2)

        for obs in obstacles:
            pygame.draw.rect(screen, (0, 255, 0), [obs[0], obs[1], snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        for obs in obstacles:
            if snake_Head == obs:
                game_close = True
                break

        for segment in snake_List:
            pygame.draw.rect(screen, (255, 255, 255), [segment[0], segment[1], snake_block, snake_block])

        show_score(score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            Length_of_snake += 1
            score += 1
            while True:
                new_foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
                new_foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
                if [new_foodx, new_foody] not in obstacles and [new_foodx, new_foody] not in snake_List:
                    break
            foodx, foody = new_foodx, new_foody

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    startScreen()
    gameLoop()
