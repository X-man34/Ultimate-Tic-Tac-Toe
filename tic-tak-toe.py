# Import Packages
import pygame
import random
from enum import Enum
from PIL import Image
#this game was kickstarted with this guys code
#https://github.com/bishwamitre/Tic-Tac-Toe/tree/main
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
TIEL = (47,183,160)
FONT_COLOR = (255, 0, 0)

# Define board size
WIDTH = 800
HEIGHT = 800
BOARD_ROWS = 3
BUTTON_WIDTH = 110
SUB_BOARD_BUFFER = 10
X_TILE_IMG = None
O_TILE_IMG = None
X_WON_IMG = None
O_WON_IMG = None
class Players(Enum):
    X_PLR = "X",
    O_PLR = "O",
    EMPTY = " "
CURRENT_PLAYER = random.choice([Players.X_PLR, Players.O_PLR])
def resize():
    global BUTTON_HEIGHT, SUB_WIDTH, SUB_HEIGHT, X_TILE_IMG, X_WON_IMG, O_TILE_IMG, O_WON_IMG
    BUTTON_HEIGHT = HEIGHT // 7
    SUB_WIDTH = (WIDTH - (6 * SUB_BOARD_BUFFER)) // 3
    SUB_HEIGHT = (HEIGHT - BUTTON_HEIGHT - (6 * SUB_BOARD_BUFFER)) // 3
    try:
        X_TILE_IMG = pygame.image.load("assets/cancel.png")
        X_TILE_IMG = pygame.transform.smoothscale(X_TILE_IMG, (SUB_WIDTH // BOARD_ROWS, SUB_HEIGHT // BOARD_ROWS))
        O_TILE_IMG = pygame.image.load("assets/check.png")
        O_TILE_IMG = pygame.transform.smoothscale(O_TILE_IMG, (SUB_WIDTH // BOARD_ROWS, SUB_HEIGHT // BOARD_ROWS))
        X_WON_IMG = pygame.transform.smoothscale(pygame.image.load("assets/cancel.png"), (SUB_WIDTH, SUB_HEIGHT))
        O_WON_IMG = pygame.transform.smoothscale(pygame.image.load("assets/check.png"), (SUB_WIDTH, SUB_HEIGHT))

    except pygame.error as e:
        print(f"Error loading images: {e}")

def switch_turn():
    global CURRENT_PLAYER
    if CURRENT_PLAYER == Players.X_PLR:
        CURRENT_PLAYER = Players.O_PLR
        pygame.display.set_caption("O's Turn") 
    else:
        CURRENT_PLAYER = Players.X_PLR
        pygame.display.set_caption("X's Turn")

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

class sub_board:
    def __init__(self,row, col, board_rows):
        self.board = [Players.EMPTY for _ in range(board_rows * board_rows)]
        self.winner = None
        self.is_won = False
        self.origin_x = 0
        self.origin_y = 0
        self.board_rows = board_rows
        self.width = 0
        self.height = 0
        self.active = True
        self.resize(row, col)
        # Globalize Images
        global X_TILE_IMG, O_TILE_IMG

    def draw(self, screen):
        if self.is_won:
            if self.winner == Players.X_PLR:
                screen.blit(X_WON_IMG, (self.origin_x, self.origin_y))
            else:
                screen.blit(O_WON_IMG, (self.origin_x, self.origin_y))
        else:
            # Draw lines for the board
            line_size = 3
            for i in range(1, self.board_rows):
                #X line
                curr_height = self.origin_y + (i * self.height / self.board_rows)
                pygame.draw.line(screen, BLACK, (self.origin_x, curr_height), (self.origin_x + self.width, curr_height), line_size)
                #Y line
                curr_width = self.origin_x + (i * self.width/self.board_rows)
                pygame.draw.line(screen, BLACK, (curr_width, self.origin_y), (curr_width, self.origin_y + self.height), line_size)

            # Draw X or O on each space based on the board
            for row in range(self.board_rows):
                for col in range(self.board_rows):
                    x = col * self.width / self.board_rows + (self.width / self.board_rows - X_TILE_IMG.get_width()) / 2 + self.origin_x
                    y = row * self.height / self.board_rows + (self.height / self.board_rows - X_TILE_IMG.get_height()) / 2 + self.origin_y
                    if self.board[row * self.board_rows + col] == Players.X_PLR:
                        screen.blit(X_TILE_IMG, (x, y))
                    elif self.board[row * self.board_rows + col] == Players.O_PLR:
                        screen.blit(O_TILE_IMG, (x, y))
    def make_move(self, row, col)-> bool:#returns whether this move won the board
        index = row * self.board_rows + col
        if self.board[index] == Players.EMPTY:
            self.board[index] = CURRENT_PLAYER
            return self.check_winner()
    def is_valid_move(self, row, col):
        index = row * self.board_rows + col
        return self.board[index] == Players.EMPTY
    def check_winner(self):
        # Check rows
        for row in range(self.board_rows):
            if all(self.board[row * self.board_rows + i] == CURRENT_PLAYER for i in range(self.board_rows)):
                self.winner = CURRENT_PLAYER.value
                return True
        # Check columns
        for col in range(self.board_rows):
            if all(self.board[i * self.board_rows + col] == CURRENT_PLAYER for i in range(self.board_rows)):
                self.winner = CURRENT_PLAYER
                return True
        # Check diagonals
        if all(self.board[i * self.board_rows + i] == CURRENT_PLAYER for i in range(self.board_rows)):
            self.winner = CURRENT_PLAYER
            return True
        if all(
            self.board[i * self.board_rows + self.board_rows - 1 - i] == CURRENT_PLAYER
            for i in range(self.board_rows)):
            self.winner = CURRENT_PLAYER
            return True
        # Check for draw
        if all(x != Players.EMPTY for x in self.board):
            self.winner = Players.EMPTY
            return True

        return False
    def reset(self):
        self.board = [Players.EMPTY for _ in range(self.board_rows * self.board_rows)]
        self.current_player = Players.X_PLR
        self.winner = None
        self.active = True
        self.is_won = False
    def resize(self, row, col):
        self.origin_x = ((col + 1) * SUB_BOARD_BUFFER) + (col * SUB_BOARD_BUFFER) + (col * SUB_WIDTH)
        self.origin_y =((row + 1) * SUB_BOARD_BUFFER) + (row * SUB_BOARD_BUFFER) + (row * SUB_HEIGHT)
        self.width = SUB_WIDTH
        self.height = SUB_HEIGHT

class RoundRectButton:
    def __init__(self, color, text):
        self.color = color
        self.text = text
        self.rect = None
        self.resize()
    def resize(self):
        self.rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT)  
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)  # Adjust the border_radius as needed
        font = pygame.font.SysFont(None, 32)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


class MasterBoard():
    def __init__(self, width, height, board_rows):
        self.board_rows = board_rows
        self.width = width
        self.height = height
        self.boards = []
        self.winning_line = None
        self.winner = None
        for row in range(board_rows):
            for col in range(board_rows):
                self.boards.append(sub_board(row, col,board_rows))
    def draw(self, surface):
        surface.fill(WHITE)
        for i in range(len(self.boards)):
            board = self.boards[i]
            if board.active and self.winner == None:
                pygame.draw.rect(surface, TIEL, (board.origin_x, board.origin_y, board.width, board.height))
            board.draw(surface)
        if self.winner != None:
            # Draw winning line if there is a winner
            pygame.draw.line(surface, GREEN, self.winning_line[0], self.winning_line[1], 6)



    def handle_board_click(self, x, y):
        #takes in x and y coords on the window
        #first have to figure out which board is active 
        if self.winner != None:
            return
        currnet_board = None
        for i in range(len(self.boards)):
            board = self.boards[i]
            if board.origin_x <= x and x <= (board.origin_x + board.width) and  board.origin_y <= y and y <= (board.origin_y + board.height) and board.active:
                currnet_board = board
                break
        if currnet_board == None:
            return
        #so the click was on the active board, now we need to see if the click was clicked on a valid place
        col = (x - currnet_board.origin_x) // (currnet_board.width // currnet_board.board_rows)
        row = (y - currnet_board.origin_y) // (currnet_board.height // currnet_board.board_rows)
        if currnet_board.is_valid_move(row, col):
            index = row * self.board_rows + col
            if currnet_board.make_move(row, col):
                currnet_board.winner = CURRENT_PLAYER   
                currnet_board.is_won = True    
            #if the move points to a won board then all non-won boards are active
            if self.boards[index].is_won:
                self.setAllOpenBoardsActive()
            else:self.setActiveBoard(index)
            self.check_winner()
            switch_turn()

    def check_winner(self):
        # Check rows
        for row in range(self.board_rows):
            if all(self.boards[row * self.board_rows + i].winner == CURRENT_PLAYER for i in range(self.board_rows)):
                self.winner = CURRENT_PLAYER
                self.winning_line = (
                    (0, row * self.height / self.board_rows + self.height / self.board_rows / 2),
                    (self.width, row * self.height / self.board_rows + self.height / self.board_rows / 2)
                )
                return True

        # Check columns
        for col in range(self.board_rows):
            if all(self.boards[i * self.board_rows + col].winner == CURRENT_PLAYER for i in range(self.board_rows)):
                self.winner = CURRENT_PLAYER
                self.winning_line = (
                    (col * self.width / self.board_rows + self.width / self.board_rows / 2, 0),
                    (col * self.width / self.board_rows + self.width / self.board_rows / 2, self.height)
                )
                return True

        # Check diagonals
        if all(self.boards[i * self.board_rows + i].winner == CURRENT_PLAYER for i in range(self.board_rows)):
            self.winner = CURRENT_PLAYER
            self.winning_line = (
                (0,0),
                (self.width, self.height)
            )
            return True
        if all(
            self.boards[i * self.board_rows + self.board_rows - 1 - i].winner == CURRENT_PLAYER
            for i in range(self.board_rows)
        ):
            self.winner = CURRENT_PLAYER
            self.winning_line = (
                (self.width, 0),
                (0, self.height)
            )
            return True
        
        # Check for draw
        if all(x.winner != None for x in self.boards):
            self.winner = Players.EMPTY
            return True

        return False

    def reset(self):
        for board in self.boards:
            board.reset()
        self.winning_line = None
        self.winner = None
    def setActiveBoard(self, index):
        for i in range(len(self.boards)):
            if i == index:
                self.boards[i].active = True
            else:
                self.boards[i].active = False
    def setAllOpenBoardsActive(self):
        for i in range(len(self.boards)):
            if self.boards[i].is_won:
                self.boards[i].active = False
            else:
                self.boards[i].active = True
    def resize(self):
        #By the time this gets called the global constants have been updated. 
        self.width = WIDTH
        self.height = HEIGHT - BUTTON_HEIGHT
        for row in range(self.board_rows):
            for col in range(self.board_rows):
                self.boards[row * self.board_rows + col].resize(row, col)

def main():
    # initialize all imported pygame modules
    global WIDTH, HEIGHT
    pygame.init()
    resize()
    surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Tic Tac Toe")
    board = MasterBoard(WIDTH, HEIGHT - BUTTON_HEIGHT, BOARD_ROWS)

    restart_button = RoundRectButton(GREEN, "RESTART")

    # creating a bool value which checks 
    # if game is running 
    running = True

    # keep game running while running is true
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.size
                resize()
                board.resize()
                restart_button.resize()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.rect.collidepoint(event.pos):
                    board.reset()
                elif board.winner is None:
                    x, y = event.pos
                    board.handle_board_click(x,y)


        board.draw(surface)
        restart_button.draw(surface)
        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
