import pygame
import random
import tkinter as tk
from tkinter import messagebox


pygame.init()
root = tk.Tk()
root.withdraw()  

screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Dodge Master')

player_image = pygame.image.load('player.png')
enemy_image = pygame.image.load('enemy.png')

pygame.mixer.music.load('background.mp3')
collision_sound = pygame.mixer.Sound('collision.mp3')

pygame.mixer.music.play(-1)  

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

player_size = 50
player_pos = [screen_width // 2, screen_height - 7 * player_size]

enemy_size = 50
enemy_pos = [random.randint(0, screen_width ), 0]
enemy_list = [enemy_pos]

speed = 10

# clock = pygame.time.Clock()

score = 0
font = pygame.font.SysFont("monospace", 40)

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, screen_width - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def update_enemy_positions(enemy_list, speed):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < screen_height:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            return 1
    return 0

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

def show_game_over(score):
    pygame.mixer.music.stop()  
    collision_sound.play()  
    messagebox.showinfo("Game Over", f"You Dodged {score} Corona Virus")


game_over = False
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_pos[0] -= speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += speed
    if keys[pygame.K_UP]:
        player_pos[1] -= speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += speed

    player_pos[0] = max(0, min(screen_width - player_size, player_pos[0]))
    player_pos[1] = max(0, min(screen_height - player_size, player_pos[1]))

    screen.fill(BLACK)

    drop_enemies(enemy_list)
    score += update_enemy_positions(enemy_list, speed)

    if collision_check(enemy_list, player_pos):
        show_game_over(score)
        game_over = True

    screen.blit(player_image, (player_pos[0], player_pos[1]))

    for enemy_pos in enemy_list:
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))

    score_text = font.render("Virus Dodged: {}".format(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    clock.tick(30)

    pygame.display.update()

pygame.quit()
