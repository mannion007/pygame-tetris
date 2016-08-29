import pygame
import math
import random

board_width = 13
board_height = 24
block_size = 40
size = [board_width * block_size, board_height * block_size]

empty_color = (0,0,0)

move_down_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_down_event, 200)

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

class piece(object):

    def __init__(self):
        self.x = 4
        self.y = 0
        self.tetromino_name = random.choice(tetrominoes.keys())
        self.color = random.choice(colors.keys())
        self.frames = len(tetrominoes[self.tetromino_name]) - 1
        self.current_frame = random.randint(0,self.frames)
        self.tetromino = tetrominoes[self.tetromino_name][self.current_frame]

        self.has_vertical_collision = False

    def draw(self, screen):
        for row_count, row in enumerate(self.tetromino):
            for col_count, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(screen, colors[self.color], ((block_size * col_count) + (self.x * block_size), (block_size * row_count) + ((self.y * block_size)), block_size, block_size))

    def get_next_frame(self):
        if self.current_frame == self.frames:
            return 0
        else:
            return self.current_frame + 1

    def can_move_horizontal(self, x_speed):
        for row_count, row in enumerate(self.tetromino):
            for col_count, col in enumerate(row):
                if col > 0:
                    if col_count + self.x + x_speed < 0 or col_count + self.x + x_speed > board_width - 1:
                        return False
        return True

    def move_horizontal(self, x_speed):
        if self.can_move_horizontal(x_speed):
            self.x = self.x + x_speed

    def can_move_down(self):
        for row_count, row in enumerate(self.tetromino):
            for col_count, col in enumerate(row):
                if col > 0:
                    if row_count + self.y + 1 > board_height - 1:
                        self.has_vertical_collision = True
                        return False
        self.has_vertical_collision = False
        return True        

    def move_down(self, speed):
        if self.can_move_down():
            self.y = self.y + speed

    def can_rotate(self):
        for row_count, row in enumerate(tetrominoes[self.tetromino_name][self.get_next_frame()]):
            for col_count, col in enumerate(row):
                if col > 0:
                    if col_count + self.x < 0 or col_count + self.x > board_width - 1 or row_count + self.y + 1 > board_height - 1:
                        return False
        return True

    def rotate(self):
        if self.can_rotate():
            self.current_frame = self.get_next_frame()
            self.tetromino = tetrominoes[self.tetromino_name][self.current_frame]

    def add_to_board(self, board):
        for row_count, row in enumerate(tetrominoes[self.tetromino_name][self.current_frame]):
            for col_count, col in enumerate(row):
                if col > 0:
                    board.board[row_count + self.y][col_count + self.x] = self.color

class board(object):

    def __init__(self):
        self.board = []
        for i in range(0,board_height):
            self.board.append([0] * board_width)

    def draw(self, screen):
        for row_count, row in enumerate(self.board):
                for col_count, col in enumerate(row):
                    if col > 0:
                        pygame.draw.rect(screen, colors[col], (block_size * col_count, block_size * row_count, block_size, block_size))

# initialize game engine
pygame.init()
board = board()
piece = piece()

# set screen width/height and caption
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pytris')


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
                piece.move_horizontal(-1)
            elif pygame.K_d == event.key:
                piece.move_horizontal(1)

    # write game logic here

    #if piece.y > board_height:
    if piece.has_vertical_collision and not piece.can_move_down():
        piece.add_to_board(board)
        piece.__init__()

    # clear the screen before drawing
    screen.fill(empty_color)
    
    # write draw code here
    board.draw(screen)
    piece.draw(screen)

    # display what's drawn. this might change.
    pygame.display.update()
    # run at 10 fps
    clock.tick(60)
 
# close the window and quit
pygame.quit()