import pygame
import math
import random

board_width = 10
board_height = 24
block_size = 30

size = [board_width * block_size, board_height * block_size]

pivot_color = (142,39,168)
block_color = (39,119,168)
empty_color = (0,0,0)

# Create event to move down every 1 second
move_down_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_down_event, 150)

tetrominoes = {
    'i' : [
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,0,0,0,0]],
    'o' : [
    [0,0,0,0,0],
    [0,1,1,0,0],
    [0,1,1,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]],
    't' : [
    [0,0,0,0,0],
    [0,1,1,1,0],
    [0,0,1,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]],
    'z' : [
    [0,0,0,0,0],
    [0,0,1,1,0],
    [0,1,1,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]],
    's' : [
    [0,0,0,0,0],
    [0,1,1,0,0],
    [0,0,1,1,0],
    [0,0,0,0,0],
    [0,0,0,0,0]],
    'j' : [
    [0,0,0,0,0],
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,1,1,0,0],
    [0,0,0,0,0]],
    'l' : [
    [0,0,0,0,0],
    [0,0,1,0,0],
    [0,0,1,0,0],
    [0,0,1,1,0],
    [0,0,0,0,0]]
}

pivots = {
    'i' : [2,2],
    't' : [2,2],
    'o' : [2,2],
    'z' : [2,2],
    's' : [2,2],
    'j' : [2,2],
    'l' : [2,2]
}

colors = {
    'red'       : (255,0,0),
    'lime'      : (0,255,0),
    'cyan'      : (0,255,255),
    'yellow'    : (255,255,0)
}

class piece:

    def __init__(self):
        self.x = 2
        self.y = 0
        self.tetromino = random.choice(tetrominoes.keys())
        self.color = colors[random.choice(colors.keys())]
        self.piece = tetrominoes[self.tetromino]
        self.pivot = pivots[self.tetromino]

    def rotate(self):
        if self.tetromino is not 'o':
            temp = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

            for row_count, row in enumerate(self.piece):
                for col_count, col in enumerate(row):
                    if self.piece[row_count][col_count] == 1:
                        new_location = self.rotate_block(row_count, col_count, self.pivot[0], self.pivot[1], -90)
                        temp[new_location[0]][new_location[1]] = 1
                    elif self.piece[row_count][col_count] == 2:
                        temp[row_count][col_count] = 2
            self.piece = temp
        
    def rotate_block(self, x, y, pivot_x, pivot_y, degrees):
        new_x = (x - pivot_x) * math.cos(math.radians(degrees)) - (y - pivot_y) * math.sin(math.radians(degrees)) + pivot_x
        new_y = (y - pivot_y) * math.cos(math.radians(degrees)) + (x - pivot_x) * math.sin(math.radians(degrees)) + pivot_y
        return int(round(new_x)), int(round(new_y))

    def draw(self, screen):
        for row_count, row in enumerate(self.piece):
            for col_count, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(screen, self.color, ((block_size * col_count) + (self.x * block_size), (block_size * row_count) + ((self.y * block_size)), block_size, block_size))

    def move_down(self, speed):
        self.y = self.y + speed

    def move_left(self):
        self.x = self.x - 1

    def move_right(self):
        self.x = self.x + 1
 
# initialize game engine
pygame.init()

# set screen width/height and caption
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pytris')

def draw_board(board):
    for row_count, row in enumerate(board):
            for col_count, col in enumerate(row):
                if [row_count, col_count] == pivot:
                    pygame.draw.rect(screen, pivot_color, (block_size * col_count, block_size * row_count, block_size, block_size))
                elif col == 1:
                    pygame.draw.rect(screen, block_color, (block_size * col_count, block_size * row_count, block_size, block_size))

def build_board():
    board = []
    for i in range(0,10):
        board.append([0] * 10)
    return board


board = build_board()
piece = piece()

# initialize clock. used later in the loop.
clock = pygame.time.Clock()
 
# Loop until the user clicks close button
done = False
while done == False:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == move_down_event:
            piece.move_down(1)        
        elif event.type == pygame.KEYDOWN:
            if pygame.K_SPACE == event.key:
                piece.rotate()
            elif pygame.K_a == event.key:
                piece.move_left()
            elif pygame.K_d == event.key:
                piece.move_right()

    # write game logic here

    if piece.y > 22:
        piece.__init__()

    # clear the screen before drawing
    screen.fill(empty_color)
    #screen.fill((255,255,255))
    
    # write draw code here
    #draw_board(board)
    piece.draw(screen)

    # display what's drawn. this might change.
    pygame.display.update()
    # run at 10 fps
    clock.tick(10)
 
# close the window and quit
pygame.quit()