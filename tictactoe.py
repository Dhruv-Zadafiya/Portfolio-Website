import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TTT")

X_IMG = pygame.transform.scale(
    pygame.image.load("Tic-Tac-Toe/assets/X.png"), (150, 150)
)
O_IMG = pygame.transform.scale(
    pygame.image.load("Tic-Tac-Toe/assets/O.jpg"), (150, 150)
)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 120, 255)

board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False
winner_line = None
celebration_particles = []
flash_alpha = 0
winner_text = ""  

font = pygame.font.SysFont("calibri", 32)
big_font = pygame.font.SysFont("calibri", 48, bold=True)   


def reset_game():
    global board, current_player, game_over, winner_line
    global celebration_particles, flash_alpha, winner_text

    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    winner_line = None
    celebration_particles = []
    flash_alpha = 0
    winner_text = ""


def create_confetti():
    for _ in range(50):
        celebration_particles.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(-20, -5),
            "speed": random.uniform(2, 5),
            "color": (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            ),
            "size": random.randint(4, 8)
        })


def update_confetti():
    for p in celebration_particles:
        p["y"] += p["speed"]
        if p["y"] > HEIGHT:
            p["y"] = random.randint(-20, -5)
            p["x"] = random.randint(0, WIDTH)


def draw_confetti():
    for p in celebration_particles:
        pygame.draw.rect(WIN, p["color"], (p["x"], p["y"], p["size"], p["size"]))


def screen_flash():
    global flash_alpha
    if flash_alpha > 0:
        flash = pygame.Surface((WIDTH, HEIGHT))
        flash.set_alpha(flash_alpha)
        flash.fill((255, 255, 255))
        WIN.blit(flash, (0, 0))
        flash_alpha -= 4


def draw_restart_button():
    button_rect = pygame.Rect(200, 520, 200, 50)
    pygame.draw.rect(WIN, BLUE, button_rect, border_radius=10)

    text = font.render("Play Again", True, WHITE)
    WIN.blit(text, (button_rect.x + 35, button_rect.y + 10))

    return button_rect


def draw_board():
    WIN.fill(WHITE)

  
    pygame.draw.line(WIN, BLACK, (200, 0), (200, 600), 5)
    pygame.draw.line(WIN, BLACK, (400, 0), (400, 600), 5)
    pygame.draw.line(WIN, BLACK, (0, 200), (600, 200), 5)
    pygame.draw.line(WIN, BLACK, (0, 400), (600, 400), 5)

    for r in range(3):
        for c in range(3):
            x, y = c * 200 + 25, r * 200 + 25
            if board[r][c] == "X":
                WIN.blit(X_IMG, (x, y))
            elif board[r][c] == "O":
                WIN.blit(O_IMG, (x, y))

   
    if winner_line:
        thickness = 10 + int(abs(pygame.time.get_ticks() % 800 - 400) / 40)
        start, end = winner_line
        pygame.draw.line(WIN, RED, start, end, thickness)
        pygame.draw.line(WIN, YELLOW, start, end, 4)

        if winner_text != "":
            text_surface = big_font.render(winner_text, True, (0, 0, 180))
            WIN.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, 10))

        draw_confetti()
        screen_flash()

        return draw_restart_button()

    pygame.display.update()
    return None


def check_winner(player):
    global winner_line, flash_alpha, winner_text

    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] == player:
            winner_line = ((0, r * 200 + 100), (600, r * 200 + 100))
            flash_alpha = 200
            create_confetti()
            winner_text = f"{player} Wins!"
            return True

    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] == player:
            winner_line = ((c * 200 + 100, 0), (c * 200 + 100, 600))
            flash_alpha = 200
            create_confetti()
            winner_text = f"{player} Wins!"
            return True

    if board[0][0] == board[1][1] == board[2][2] == player:
        winner_line = ((0, 0), (600, 600))
        flash_alpha = 200
        create_confetti()
        winner_text = f"{player} Wins!"
        return True

    if board[0][2] == board[1][1] == board[2][0] == player:
        winner_line = ((600, 0), (0, 600))
        flash_alpha = 200
        create_confetti()
        winner_text = f"{player} Wins!"
        return True

    return False


def check_tie():
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                return False
    return True


def main():
    global current_player, game_over, winner_text

    while True:
        update_confetti()
        restart_button = draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if game_over and restart_button and restart_button.collidepoint(event.pos):
                    reset_game()
                    continue

                if not game_over:
                    x, y = event.pos
                    row, col = y // 200, x // 200

                    if board[row][col] == "":
                        board[row][col] = current_player

                        if check_winner(current_player):
                            game_over = True

                        elif check_tie():
                            winner_text = "Match Tie!"
                            game_over = True

                        current_player = "O" if current_player == "X" else "X"

        pygame.display.update()


if __name__ == "__main__":
    main()
