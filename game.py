import pygame
import math
import random

board_width = 13
board_height = 24
block_size = 40
size = [board_width * block_size + 250, board_height * block_size]

game_speed = 200
move_down_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_down_event, game_speed)

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
        ],
        [
            [0,1,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        [
            [0,0,0,1,0],
            [0,1,1,1,0],
            [0,0,0,0,0],
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

    def __init__(self, tetromino):
        self.x = 4
        self.y = 0

        self.tetromino_name = tetromino['tetromino']
        self.color = tetromino['color']
        self.current_frame = tetromino['frame']
        self.tetromino = tetrominoes[self.tetromino_name][self.current_frame]
        self.has_vertical_collision = False

    def draw(self, screen):
        for row_count, row in enumerate(self.tetromino):
            for col_count, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(screen, colors[self.color], ((block_size * col_count) + (self.x * block_size), (block_size * row_count) + ((self.y * block_size)), block_size, block_size))

    def get_next_frame(self):
        if self.current_frame == len(tetrominoes[self.tetromino_name]) - 1:
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

    def can_move_down(self, board):
        for row_count, row in enumerate(self.tetromino):
            for col_count, col in enumerate(row):
                if col > 0:
                    if (row_count + self.y + 1 > board_height - 1) or (board[row_count + self.y + 1][col_count + self.x] > 0):
                        self.has_vertical_collision = True
                        return False
        self.has_vertical_collision = False
        return True        

    def move_down(self, board):
        if self.can_move_down(board):
            self.y = self.y + 1

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

    def remove_completed_lines(self):
        completed_count = 0
        for row_count, row in enumerate(self.board):
            row_completed = True
            for col in row:
                if col < 1:
                    row_completed = False
            if row_completed:
                completed_count = completed_count + 1
                self.board.pop(row_count)
                self.board.insert(row_count, [0] * board_width)
                for row_to_pull_down in range(row_count, 0, -1):
                    for col_count in range(board_width):
                        self.board[row_to_pull_down][col_count] = self.board[row_to_pull_down-1][col_count]
        return completed_count

class game(object):

    score = 0

    def __init__(self):
        self.next_tetromino = self.get_tetromino()
        self.current_tetromino = self.get_tetromino()

    def get_tetromino(self):
        tetromino = random.choice(tetrominoes.keys())
        tetromino_color = random.choice(colors.keys())
        teromino_frame = random.randint(0, len(tetrominoes[tetromino]) - 1)
        return {'tetromino' : tetromino, 'color' : tetromino_color, 'frame' : teromino_frame}

    def get_next_tetromino(self):
        self.current_tetromino = self.next_tetromino
        self.next_tetromino = self.get_tetromino()

    def update_score(self, lines_cleared):
        self.score = self.score + (100 * lines_cleared)

# initialize game engine
pygame.init()
game = game()
board = board()

piece = piece(game.current_tetromino)

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
            piece.move_down(board.board)        
        elif event.type == pygame.KEYDOWN:
            if pygame.K_SPACE == event.key:
                piece.rotate()
            elif pygame.K_a == event.key:
                piece.move_horizontal(-1)
            elif pygame.K_d == event.key:
                piece.move_horizontal(1)

    # write game logic here
    if piece.has_vertical_collision and not piece.can_move_down(board.board):
        piece.add_to_board(board)
        completed_lines = board.remove_completed_lines()
        game.update_score(completed_lines)
        game.get_next_tetromino()
        piece.__init__(game.current_tetromino)

    # clear the screen before drawing
    screen.fill((0,0,0))
    
    # write draw code here
    board.draw(screen)
    piece.draw(screen)

    #font = pygame.font.Font(None, 36)
    font=pygame.font.SysFont("comicsansms",30)
    text = font.render('score ' + str(game.score), 0, (255, 255, 255))
    textpos = text.get_rect()
    textpos.top = 50
    textpos.left = size[0] - 200
    screen.blit(text, textpos)

    # display what's drawn. this might change.
    pygame.display.update()
    # run at 10 fps
    clock.tick(60)
 
# close the window and quit
pygame.quit()