import pygame
import random

pygame.init()

# Screen (FIXED SIZE)
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooter 🚀")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
DARK = (10, 10, 30)
GREEN = (0, 200, 0)
LIGHT_GREEN = (0, 255, 0)
RED = (200, 0, 0)

# Fonts
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 60)

# Load Images
player_img = pygame.image.load('player.png')
enemy_img = pygame.image.load('enemy.png')
bullet_img = pygame.image.load('bullet.png')

player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Sounds
try:
    start_sound = pygame.mixer.Sound("gamestart.mp3")
    shoot_sound = pygame.mixer.Sound("laser.mp3")
    hit_sound = pygame.mixer.Sound("explosion.mp3")
    game_over_sound = pygame.mixer.Sound("gameover.mp3")

    start_sound.set_volume(0.5)
    shoot_sound.set_volume(0.4)
    hit_sound.set_volume(0.5)
    game_over_sound.set_volume(0.5)

except:
    start_sound = None
    shoot_sound = None
    hit_sound = None
    game_over_sound = None

# Stars
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(40)]

# Game states
START, PLAYING, GAME_OVER = 0, 1, 2
game_state = START

# Player
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 70
player_speed = 5
lives = 3

# SINGLE Enemy
enemy_x = random.randint(0, WIDTH - 50)
enemy_y = 50
enemy_speed = 2

# Bullet
bullet_x = 0
bullet_y = player_y
bullet_speed = 7
bullet_state = "ready"

# Score
score = 0
level = 1


def reset_game():
    global player_x, lives, enemy_x, enemy_y, enemy_speed
    global bullet_y, bullet_state, score, level

    player_x = WIDTH // 2 - 25
    lives = 3
    enemy_x = random.randint(0, WIDTH - 50)
    enemy_y = 50
    enemy_speed = 2
    bullet_y = player_y
    bullet_state = "ready"
    score = 0
    level = 1


def draw_button(text, rect):
    mouse = pygame.mouse.get_pos()
    color = LIGHT_GREEN if rect.collidepoint(mouse) else GREEN

    pygame.draw.rect(screen, color, rect, border_radius=10)

    txt = font.render(text, True, WHITE)
    text_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, text_rect)


def draw_stars():
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 2)
        star[1] += 1

        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0


def draw_player(x, y):
    screen.blit(player_img, (x, y))


def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 20, y))


def is_collision(ex, ey, bx, by):
    return abs(ex - bx) < 25 and abs(ey - by) < 25


def show_info():
    text = font.render(
        f"Score: {score}   Level: {level}   Lives: {lives}",
        True,
        WHITE
    )
    screen.blit(text, (10, 10))


running = True

while running:
    screen.fill(DARK)
    draw_stars()

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # START BUTTON
            if game_state == START:
                if start_btn.collidepoint(mouse_pos):

                    if start_sound:
                        start_sound.play()

                    game_state = PLAYING

            # RESTART BUTTON
            elif game_state == GAME_OVER:
                if restart_btn.collidepoint(mouse_pos):

                    if start_sound:
                        start_sound.play()

                    reset_game()
                    game_state = PLAYING

    # ================= START SCREEN =================
    if game_state == START:

        title = big_font.render("Alien Shooter", True, WHITE)

        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 120)
        )

        start_btn = pygame.Rect(
            WIDTH // 2 - 100,
            220,
            200,
            50
        )

        draw_button("START", start_btn)

    # ================= GAME PLAY =================
    elif game_state == PLAYING:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed

        # SHOOT BULLET
        if keys[pygame.K_SPACE] and bullet_state == "ready":

            bullet_x = player_x
            bullet_y = player_y

            fire_bullet(bullet_x, bullet_y)

            if shoot_sound:
                shoot_sound.play()

        # Enemy movement
        enemy_y += enemy_speed

        # Enemy missed
        if enemy_y > HEIGHT:

            lives -= 1

            enemy_x = random.randint(0, WIDTH - 50)
            enemy_y = 50

            if lives <= 0:

                if game_over_sound:
                    game_over_sound.play()

                game_state = GAME_OVER

        # Bullet movement
        if bullet_state == "fire":

            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_speed

        if bullet_y <= 0:

            bullet_y = player_y
            bullet_state = "ready"

        # Collision
        if is_collision(enemy_x, enemy_y, bullet_x, bullet_y):

            score += 1

            if hit_sound:
                hit_sound.play()

            # Increase level every 5 points
            if score % 5 == 0:
                level += 1
                enemy_speed += 0.5

            enemy_x = random.randint(0, WIDTH - 50)
            enemy_y = 50

            bullet_y = player_y
            bullet_state = "ready"

        draw_enemy(enemy_x, enemy_y)
        draw_player(player_x, player_y)

        show_info()

    # ================= GAME OVER =================
    elif game_state == GAME_OVER:

        over_text = big_font.render("GAME OVER", True, RED)

        screen.blit(
            over_text,
            (WIDTH // 2 - over_text.get_width() // 2, 120)
        )

        score_text = font.render(
            f"Final Score: {score}",
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (WIDTH // 2 - score_text.get_width() // 2, 200)
        )

        restart_btn = pygame.Rect(
            WIDTH // 2 - 100,
            260,
            200,
            50
        )

        draw_button("RESTART", restart_btn)

    pygame.display.update()
    clock.tick(60)