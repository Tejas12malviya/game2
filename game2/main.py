import pygame
import sys
import threading
from player import Player, Enemy

# Initialize Pygame
pygame.init()

# Screen Settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle Arena")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (50, 50, 200)
PURPLE = (120, 0, 200)

# Load Assets
font = pygame.font.Font(None, 36)

# Try to load assets safely
try:
    background = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
    player_img = pygame.transform.scale(pygame.image.load("player.png"), (150, 150))
    enemy_img = pygame.transform.scale(pygame.image.load("enemy.png"), (150, 150))
    attack_sound = pygame.mixer.Sound("attack.wav")
except pygame.error as e:
    print(f"Error loading assets: {e}")
    sys.exit()

# Game Variables
def reset_game():
    global player, enemy, game_running
    player = Player()
    enemy = Enemy()
    player.name = "Hero"
    enemy.name = "Villain"
    game_running = True

reset_game()

def draw_health_bar(health, x, y):
    pygame.draw.rect(screen, RED, (x, y, 200, 20))  # Full bar
    pygame.draw.rect(screen, GREEN, (x, y, max(0, health * 2), 20))  # Health

def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def animate_attack():
    for i in range(10):
        screen.fill(BLUE)
        screen.blit(background, (0, 0))
        draw_health_bar(player.health, 100, 100)
        draw_health_bar(enemy.health, 600, 100)
        screen.blit(player_img, (100 + i * 5, 200))
        screen.blit(enemy_img, (600, 200))
        pygame.display.flip()
        pygame.time.delay(30)

def enemy_auto_attack():
    while game_running:
        pygame.time.delay(2000)  # Enemy attacks every 2 seconds
        if enemy.health > 0 and player.health > 0:
            attack_sound.play()
            player.health -= 10

def check_winner():
    if player.health <= 0:
        return "Villain Wins!"
    elif enemy.health <= 0:
        return "Hero Wins!"
    return None

def game_over_screen(winner):
    global game_running
    screen.fill(BLUE)
    draw_text(winner, 350, 250, WHITE)
    pygame.draw.rect(screen, PURPLE, (300, 350, 200, 50))
    draw_text("Play Again", 340, 365, WHITE)
    pygame.draw.rect(screen, RED, (300, 420, 200, 50))
    draw_text("Exit", 370, 435, WHITE)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 300 <= mouse_x <= 500 and 350 <= mouse_y <= 400:
                    reset_game()
                    main()
                elif 300 <= mouse_x <= 500 and 420 <= mouse_y <= 470:
                    pygame.quit()
                    sys.exit()

def main():
    global game_running
    game_running = True
    threading.Thread(target=enemy_auto_attack, daemon=True).start()
    
    running = True
    while running:
        screen.fill(BLUE)
        screen.blit(background, (0, 0))
        
        # Display Names
        draw_text(f"{player.name}", 100, 50, WHITE)
        draw_text(f"{enemy.name}", 600, 50, WHITE)
        
        # Draw Health Bars
        draw_health_bar(player.health, 100, 100)
        draw_health_bar(enemy.health, 600, 100)
        
        # Draw Characters
        screen.blit(player_img, (100, 200))
        screen.blit(enemy_img, (600, 200))
        
        # Check for Winner
        winner = check_winner()
        if winner:
            game_running = False
            game_over_screen(winner)
            return
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 300 <= mouse_x <= 500 and 400 <= mouse_y <= 450:
                    attack_sound.play()
                    animate_attack()
                    player.attack_enemy(enemy)
        
        # Attack Button
        pygame.draw.rect(screen, PURPLE, (300, 400, 200, 50))
        draw_text("Attack", 370, 415, WHITE)
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
