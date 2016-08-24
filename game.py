import pygame
 
# initialize game engine
pygame.init()
# set screen width/height and caption
size = [400, 400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Tetris')

#########################
### Basic tetris code ###
#########################

def draw_board(board):
    for row_count, row in enumerate(board):
            for col_count, col in enumerate(row):
                if [row_count, col_count] == pivot:
                    color = (0, 255, 0)
                elif col == 1:
                    color = (0, 0, 255)
                else:
                    color = (255, 255, 255)
                pygame.draw.rect(screen, color, (40 * col_count, 40 * row_count, 40, 40))

board = []

for i in range(0,10):
    board.append([0,0,0,0,0,0,0,0,0,0])

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