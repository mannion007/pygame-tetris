import pygame
import math
import random

board_width = 13
board_height = 24
block_size = 40
size = [board_width * block_size, board_height * block_size]

block_color = (39,119,168)
empty_color = (0,0,0)

move_down_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_down_event, 150)

tetrominoes = {
    'i' : [
        [
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,0,0,0,0],
            [1,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
    ],
    'o' : [
        [
            [0,1,1,0,0],
            [0,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
    ],
    't' : [
        [
            [0,1,1,1,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,0,0,1,0],
            [0,0,1,1,0],
            [0,0,0,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,0,0,0,0],
            [0,0,1,0,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,1,0,0,0],
            [0,1,1,0,0],
            [0,1,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
    ],
    's' : [
        [
            [0,0,1,1,0],
            [0,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,0,1,0,0],
            [0,0,1,1,0],
            [0,0,0,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
    ],
    'z' : [
        [
            [0,1,1,0,0],
            [0,0,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,0,0,1,0],
            [0,0,1,1,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
    ],
    'j' : [
        [
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ],
        [
            [0,1,0,0,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,0,1,1,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,0,0,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
    ],
    'l' : [
        [
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,1,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ]
    ]
}

colors = {
    1 : (255,0,0),
    2 : (0,255,0),
    3 : (0,255,255),
    4 : (255,255,0)
}

class piece:

    def __init__(self):
        self.x = 4
        self.y = 0
        self.tetromino_name = random.choice(tetrominoes.keys())
        self.color = colors[random.choice(colors.keys())]
        self.frames = len(tetrominoes[self.tetromino_name]) - 1
        self.current_frame = random.randint(0,self.frames)
        self.tetromino = tetrominoes[self.tetromino_name][self.current_frame]

    def draw(self, screen):
        for row_count, row in enumerate(self.tetromino):
            for col_count, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(screen, self.color, ((block_size * col_count) + (self.x * block_size), (block_size * row_count) + ((self.y * block_size)), block_size, block_size))

    def rotate(self):
        if self.current_frame == self.frames:
            self.current_frame = 0
        else:
            self.current_frame += 1
        
        self.tetromino = tetrominoes[self.tetromino_name][self.current_frame]

    def move_down(self, speed):
        if self.can_move():
            self.y = self.y + speed

    def move_left(self):
        self.x = self.x - 1

    def move_right(self):
        self.x = self.x + 1

    def can_move(self):
        return True
 
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

    if piece.y > board_height:
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