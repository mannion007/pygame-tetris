import pygame
import math

pivot_color = (142,39,168)
block_color = (39,119,168)
 
# initialize game engine
pygame.init()
# set screen width/height and caption
size = [400, 400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tetris')

def draw_board(board):
    for row_count, row in enumerate(board):
            for col_count, col in enumerate(row):
                if [row_count, col_count] == pivot:
                    pygame.draw.rect(screen, pivot_color, (40 * col_count, 40 * row_count, 40, 40))
                elif col == 1:
                    pygame.draw.rect(screen, block_color, (40 * col_count, 40 * row_count, 40, 40))

def rotate(x, y, pivot_x, pivot_y, degrees):
    new_x = (x - pivot_x) * math.cos(math.radians(degrees)) - (y - pivot_y) * math.sin(math.radians(degrees)) + pivot_x
    new_y = (y - pivot_y) * math.cos(math.radians(degrees)) + (x - pivot_x) * math.sin(math.radians(degrees)) + pivot_y
    return int(round(new_x)), int(round(new_y))

def build_board():
    board = []
    for i in range(0,10):
        board.append([0] * 10)
    return board


board = build_board()
pivot = []

# initialize clock. used later in the loop.
clock = pygame.time.Clock()
 
# Loop until the user clicks close button
done = False
while done == False:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 1 == event.button:
                board[int(pygame.mouse.get_pos()[1] / 40)][int(pygame.mouse.get_pos()[0] / 40)] = 1
            elif 2 == event.button:
                board[int(pygame.mouse.get_pos()[1] / 40)][int(pygame.mouse.get_pos()[0] / 40)] = 0
            elif 3 == event.button:
                pivot = [int(pygame.mouse.get_pos()[1] / 40), int(pygame.mouse.get_pos()[0] / 40)]
        
        elif event.type == pygame.KEYDOWN:
            if pygame.K_SPACE == event.key:
                new_board = build_board()
                for row_count, row in enumerate(board):
                    for col_count, col in enumerate(row):
                        if board[row_count][col_count] == 1:
                            new_location = rotate(row_count, col_count, pivot[0], pivot[1], -90)
                            new_board[new_location[0]][new_location[1]] = 1
                board = new_board
                        
    # write game logic here
 
    # clear the screen before drawing
    screen.fill((255, 255, 255)) 
    
    # write draw code here
    draw_board(board)

    # display what's drawn. this might change.
    pygame.display.update()
    # run at 20 fps
    clock.tick(20)
 
# close the window and quit
pygame.quit()