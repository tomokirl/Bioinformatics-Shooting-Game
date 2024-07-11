import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen size settings
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Game title
pygame.display.set_caption("Bioinformatics Shooting Game")

# Player settings
player_width = 50
player_height = 50
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy settings
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

# DNA bases and their colors
dna_fragments = ['A', 'T', 'C', 'G']
dna_colors = {'A': (255, 0, 0), 'T': (0, 255, 0), 'C': (0, 0, 255), 'G': (255, 0, 255)}

# Current problem
current_problem = ''.join(random.choice(dna_fragments) for _ in range(10))

# Font settings
font = pygame.font.Font(None, 36)

# Main game loop control
running = True
game_over = False

# Game start time
start_time = time.time()
elapsed_time = 0

def reset_game():
    global player_x, bullets, enemies, current_problem, game_over, start_time, elapsed_time
    player_x = screen_width // 2 - player_width // 2
    bullets = []
    enemies = []
    current_problem = ''.join(random.choice(dna_fragments) for _ in range(10))
    game_over = False
    start_time = time.time()
    elapsed_time = 0

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_r:
                    reset_game()
            else:
                if event.key == pygame.K_SPACE:
                    bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])
    
    if not game_over:
        # Key state detection
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Bullet movement
        for bullet in bullets:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
        
        # Enemy generation
        if random.randint(1, 20) == 1:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemies.append([enemy_x, 0, random.choice(dna_fragments)])
        
        # Enemy movement
        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > screen_height:
                enemies.remove(enemy)
        
        # Collision detection
        for bullet in bullets:
            for enemy in enemies:
                if bullet[0] < enemy[0] + enemy_width and bullet[0] + bullet_width > enemy[0] and bullet[1] < enemy[1] + enemy_height and bullet[1] + bullet_height > enemy[1]:
                    if enemy[2] in current_problem:
                        current_problem = current_problem.replace(enemy[2], '', 1)
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

        # Clear check
        if not current_problem:
            game_over = True
            elapsed_time = time.time() - start_time

    # Screen drawing
    screen.fill((0, 0, 0))
    pygame.draw.polygon(screen, (0, 255, 0), [(player_x, player_y), (player_x + player_width // 2, player_y - player_height), (player_x + player_width, player_y)])
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), (bullet[0], bullet[1], bullet_width, bullet_height))
    for enemy in enemies:
        color = dna_colors[enemy[2]]
        if enemy[2] == 'A':
            pygame.draw.rect(screen, color, (enemy[0], enemy[1], enemy_width, enemy_height))
        elif enemy[2] == 'T':
            pygame.draw.ellipse(screen, color, (enemy[0], enemy[1], enemy_width, enemy_height))
        elif enemy[2] == 'C':
            pygame.draw.polygon(screen, color, [(enemy[0], enemy[1]), (enemy[0] + enemy_width // 2, enemy[1] + enemy_height), (enemy[0] + enemy_width, enemy[1])])
        elif enemy[2] == 'G':
            pygame.draw.polygon(screen, color, [(enemy[0], enemy[1] + enemy_height), (enemy[0] + enemy_width // 2, enemy[1]), (enemy[0] + enemy_width, enemy[1] + enemy_height)])
        text = font.render(enemy[2], True, (255, 255, 255))
        screen.blit(text, (enemy[0] + 10, enemy[1] + 10))
    
    # Problem display
    problem_text = font.render("Problem: " + current_problem, True, (255, 255, 255))
    screen.blit(problem_text, (10, 10))
    
    # Time display
    if not game_over:
        current_time = time.time() - start_time
        time_text = font.render(f"Time: {current_time:.2f} sec", True, (255, 255, 255))
    else:
        time_text = font.render(f"Clear Time: {elapsed_time:.2f} sec", True, (255, 255, 255))
    screen.blit(time_text, (10, 50))
    
    # Game over display
    if game_over:
        game_over_text = font.render("Game Clear!", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
        restart_text = font.render("Press 'R' to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
