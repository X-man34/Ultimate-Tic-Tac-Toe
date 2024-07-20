# Import Packages
import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
FONT_COLOR = (255, 0, 0)

# Define board size
WIDTH = 300
HEIGHT = 300
BOARD_ROWS = 3

# Define X and O images (replace with your image files)
IMAGE_X = "assets/cancel.png"
IMAGE_O = "assets/check.png"
try:
    X_IMG = pygame.image.load(IMAGE_X)
    O_IMG = pygame.image.load(IMAGE_O)
except pygame.error as e:
    print(f"Error loading images: {e}")

class Board:
    def __init__(self):
        self.board = [" " for _ in range(BOARD_ROWS * BOARD_ROWS)]
        self.current_player = random.choice(["X", "O"])
        self.winner = None
        self.winning_line = None

        # Globalize Images
        global X_IMG, O_IMG

    def draw(self, screen):
        # Fill the board with white background
        screen.fill(WHITE)

        # Draw lines for the board
        line_size = 3
        pygame.draw.line(screen, BLACK, (WIDTH / 3, 0), (WIDTH / 3, HEIGHT), line_size)
        pygame.draw.line(screen, BLACK, (2 * WIDTH / 3, 0), (2 * WIDTH / 3, HEIGHT), line_size)
        pygame.draw.line(screen, BLACK, (0, HEIGHT / 3), (WIDTH, HEIGHT / 3), line_size)
        pygame.draw.line(screen, BLACK, (0, 2 * HEIGHT / 3), (WIDTH, 2 * HEIGHT / 3), line_size)

        # Draw X or O on each space based on the board
        for row in range(BOARD_ROWS):
            for col in range(BOARD_ROWS):
                x = col * WIDTH / 3 + (WIDTH / 3 - X_IMG.get_width()) / 2
                y = row * HEIGHT / 3 + (HEIGHT / 3 - X_IMG.get_height()) / 2
                if self.board[row * BOARD_ROWS + col] == "X":
                    screen.blit(X_IMG, (x, y))
                elif self.board[row * BOARD_ROWS + col] == "O":
                    screen.blit(O_IMG, (x, y))

        # Draw winning line if there is a winner
        if self.winning_line:
            pygame.draw.line(screen, GREEN, self.winning_line[0], self.winning_line[1], 6)

        # Add text for the winner
        if self.winner:
            font = pygame.font.SysFont(None, 52)
            if self.winner == "Draw":
                text = font.render("It's a Draw!", True, FONT_COLOR)
            else:
                text = font.render(f"winner: {self.winner}", True, FONT_COLOR)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 32))  # Adjust vertical position
            screen.blit(text, text_rect)

    def make_move(self, row, col):
        index = row * BOARD_ROWS + col
        if self.board[index] == " ":
            self.board[index] = self.current_player
            if not self.check_winner():
                self.switch_turn()

    def is_valid_move(self, row, col):
        index = row * BOARD_ROWS + col
        return self.board[index] == " "

    def switch_turn(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        # Check rows
        for row in range(BOARD_ROWS):
            if all(self.board[row * BOARD_ROWS + i] == self.current_player for i in range(BOARD_ROWS)):
                self.winner = self.current_player
                self.winning_line = (
                    (0, row * HEIGHT / 3 + HEIGHT / 6),
                    (WIDTH, row * HEIGHT / 3 + HEIGHT / 6)
                )
                return True

        # Check columns
        for col in range(BOARD_ROWS):
            if all(self.board[i * BOARD_ROWS + col] == self.current_player for i in range(BOARD_ROWS)):
                self.winner = self.current_player
                self.winning_line = (
                    (col * WIDTH / 3 + WIDTH / 6, 0),
                    (col * WIDTH / 3 + WIDTH / 6, HEIGHT)
                )
                return True

        # Check diagonals
        if all(self.board[i * BOARD_ROWS + i] == self.current_player for i in range(BOARD_ROWS)):
            self.winner = self.current_player
            self.winning_line = (
                (0, 0),
                (WIDTH, HEIGHT)
            )
            return True
        if all(
            self.board[i * BOARD_ROWS + BOARD_ROWS - 1 - i] == self.current_player
            for i in range(BOARD_ROWS)
        ):
            self.winner = self.current_player
            self.winning_line = (
                (WIDTH, 0),
                (0, HEIGHT)
            )
            return True
        
        # Check for draw
        if all(x != " " for x in self.board):
            self.winner = "Draw"
            return True

        return False

    def reset(self):
        self.board = [" " for _ in range(BOARD_ROWS * BOARD_ROWS)]
        self.current_player = "X"
        self.winner = None
        self.winning_line = None

    def draw_button(self, screen, button):
        button.draw(screen)

class RoundRectButton:
    def __init__(self, color, rect, text):
        self.color = color
        self.rect = rect
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)  # Adjust the border_radius as needed
        font = pygame.font.SysFont(None, 32)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


def main():
    # initialize all imported pygame modules
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
    pygame.display.set_caption("Tic Tac Toe")

    # Define object of class
    board = Board()

    button_rect = pygame.Rect(WIDTH // 2 - 55, HEIGHT + 60, 115, 48)  
    restart_button = RoundRectButton(GREEN, button_rect, "RESTART")

    # creating a bool value which checks 
    # if game is running 
    running = True

    # keep game running till running is true
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    board.reset()
                elif board.winner is None:
                    x, y = event.pos
                    if y < HEIGHT:
                        col = x // (WIDTH // BOARD_ROWS)
                        row = y // (HEIGHT // BOARD_ROWS)
                        if board.is_valid_move(row, col):
                            board.make_move(row, col)

        board.draw(screen)
        board.draw_button(screen, restart_button)
        pygame.display.flip()

        if board.winner:
            print(f"Winner: {board.winner}")

    # uninitialize all pygame modules
    pygame.quit()

if __name__ == "__main__":
    main()
