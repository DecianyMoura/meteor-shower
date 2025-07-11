import random
from pygame import Rect
from pgzero.actor import Actor

# Game Configurations
WIDTH = 800
HEIGHT = 600

# Game States and Flags
game_state = 'menu'
sound_enabled = True
menu_music_playing = True

# Player Setup
player_images = ['player', 'player2', 'player3']
player_level = 1
player_speed = 5
player = Actor(player_images[player_level - 1])
player.pos = (WIDTH // 2, HEIGHT - 70)
active_bonus = "None"

# Meteors and Shots
meteors = []
meteor_speed = 3
meteor_timer = 0

shots = []
shot_speed = 5

# Bonus Items
bonus = None
bonus_type = None
bonus_timer = 0
bonus_spawn_time = 600  # 10 seconds

# Shield
shield_active = False

# Timer para qualquer efeito de bônus
bonus_effect_timer = 0
bonus_effect_duration = 600  # 10 segundos

# Score and High Score
score = 0
high_score = 0

# Sounds and Music
bonus_sound = sounds.bonus
laser_sound = sounds.laser
explosion_sound = sounds.explosion
music.set_volume(0.5)
music.play('menu_music')


# Game Functions
def spawn_meteor():
    if player_level == 1:
        image = 'meteor'
    elif player_level == 2:
        image = 'meteor2'
    else:
        image = 'meteor3'

    meteor = Actor(image)
    meteor.x = random.randint(40, WIDTH - 40)
    meteor.y = -40
    meteors.append(meteor)


def spawn_bonus():
    global bonus, bonus_type
    bonus_type = random.choice(['upgrade', 'laser', 'shield'])

    if bonus_type == 'upgrade':
        bonus = Actor('bonus_green')
    elif bonus_type == 'laser':
        bonus = Actor('bonus_red')
    elif bonus_type == 'shield':
        bonus = Actor('bonus_blue')

    bonus.x = random.randint(40, WIDTH - 40)
    bonus.y = -40


def activate_shield():
    global shield_active
    shield_active = True
    player.image = 'player_shield'


def start_game():
    global player_level, score, meteors, shots, bonus, bonus_timer
    global meteor_timer, shield_active, active_bonus, player_speed, bonus_effect_timer

    meteors.clear()
    shots.clear()
    bonus = None
    bonus_timer = 0
    meteor_timer = 0
    bonus_effect_timer = 0
    score = 0
    player_level = 1
    player_speed = 5
    player.image = player_images[player_level - 1]
    player.pos = (WIDTH // 2, HEIGHT - 70)
    shield_active = False
    active_bonus = "None"
    change_state('playing')


def change_state(state):
    global game_state
    game_state = state


# Drawing Functions
def draw():
    screen.clear()

    if game_state == 'menu':
        draw_menu()

    elif game_state == 'playing':
        draw_game()

    elif game_state == 'game_over':
        draw_game_over()


def draw_menu():
    for x in range(0, WIDTH, 200):
        for y in range(0, HEIGHT, 200):
            screen.blit('background', (x, y))

    screen.draw.text("METEOR SHOWER", center=(WIDTH // 2, 100), fontsize=70, color="orange")

    screen.draw.filled_rect(Rect((300, 250), (200, 50)), "green")
    screen.draw.text("Start", center=(400, 275), fontsize=35, color="white")

    screen.draw.filled_rect(Rect((300, 320), (200, 50)), "orange")
    toggle_text = "Sounds: on" if sound_enabled else "Sounds: off"
    screen.draw.text(toggle_text, center=(400, 345), fontsize=35, color="white")

    screen.draw.filled_rect(Rect((300, 390), (200, 50)), "red")
    screen.draw.text("Exit", center=(400, 415), fontsize=35, color="white")

    screen.draw.text(f"Record: {high_score}", center=(WIDTH // 2, 200), fontsize=40, color="green")


def draw_game():
    for x in range(0, WIDTH, 200):
        for y in range(0, HEIGHT, 200):
            screen.blit('background', (x, y))

    player.draw()

    for meteor in meteors:
        meteor.draw()

    for shot in shots:
        shot.draw()

    if bonus:
        bonus.draw()

    screen.draw.text(f"Record: {high_score}", (WIDTH - 200, 10), fontsize=30, color="green")
    screen.draw.text(f"Points: {score}", (10, 10), fontsize=30, color="white")
    screen.draw.text(f"Bonus: {active_bonus}", (10, 40), fontsize=30, color="yellow")


def draw_game_over():
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=60, color="red")
    screen.draw.text(f"SCORE: {score}", center=(WIDTH // 2, HEIGHT // 2 + 30), fontsize=40, color="white")
    screen.draw.text(f"RECORD: {high_score}", center=(WIDTH // 2, HEIGHT // 2 + 80), fontsize=40, color="green")
    screen.draw.text("Press ENTER to return to the menu", center=(WIDTH // 2, HEIGHT // 2 + 130), fontsize=30, color="yellow")


# Game Loop
def update():
    global meteor_timer, bonus_timer, bonus, player_level
    global shield_active, score, player_speed, active_bonus, high_score, bonus_effect_timer

    if game_state != 'playing':
        return

    # Player movement
    if keyboard.left and player.left > 0:
        player.x -= player_speed
    if keyboard.right and player.right < WIDTH:
        player.x += player_speed

    # Meteors movement
    for meteor in meteors:
        meteor.y += meteor_speed

    for meteor in meteors[:]:
        if meteor.top > HEIGHT:
            meteors.remove(meteor)
            score += 1

    for meteor in meteors:
        if meteor.colliderect(player) and not shield_active:
            if score > high_score:
                high_score = score
            change_state('game_over')

    # Shots
    for shot in shots[:]:
        shot.y -= shot_speed
        if shot.top < 0:
            shots.remove(shot)
            continue
        for meteor in meteors[:]:
            if shot.colliderect(meteor):
                shots.remove(shot)
                meteors.remove(meteor)
                if sound_enabled:
                    explosion_sound.play()
                score += 5
                break

    # Bonus handling
    if bonus:
        bonus.y += meteor_speed
        if bonus.colliderect(player):
            if sound_enabled:
                bonus_sound.play()

            bonus_effect_timer = 0  # Reinicia o tempo do bônus

            if bonus_type == 'upgrade':
                player_level = 2
                player.image = player_images[1]
                player_speed = 8
                active_bonus = "Upgrade (Speed)"
                shield_active = False

            elif bonus_type == 'laser':
                player_level = 3
                player.image = player_images[2]
                player_speed = 5
                active_bonus = "Laser (Shooter)"
                shield_active = False

            elif bonus_type == 'shield':
                activate_shield()
                active_bonus = "Shield (Protection)"

            bonus = None

        elif bonus.top > HEIGHT:
            bonus = None

    # Spawn bonus
    bonus_timer += 1
    if bonus_timer >= bonus_spawn_time:
        if not bonus:
            spawn_bonus()
        bonus_timer = 0

    # Spawn meteors
    meteor_timer += 1
    if meteor_timer >= 60:
        spawn_meteor()
        meteor_timer = 0

    # Duração dos bônus
    if active_bonus != "None":
        bonus_effect_timer += 1
        if bonus_effect_timer >= bonus_effect_duration:
            bonus_effect_timer = 0
            shield_active = False
            player_level = 1
            player_speed = 5
            player.image = player_images[0]
            active_bonus = "None"


# Event Handlers
def on_key_down(key):
    global shots

    if game_state == 'playing' and key == keys.SPACE and player_level == 3:
        if len(shots) < 5:
            shot = Actor('laser')
            shot.pos = (player.x, player.y - 30)
            shots.append(shot)
        if sound_enabled:
            laser_sound.play()

    elif game_state == 'game_over' and key == keys.RETURN:
        change_state('menu')


def on_mouse_down(pos):
    global sound_enabled, menu_music_playing

    if game_state != 'menu':
        return

    if Rect((300, 250), (200, 50)).collidepoint(pos):
        start_game()
    elif Rect((300, 320), (200, 50)).collidepoint(pos):
        sound_enabled = not sound_enabled
        menu_music_playing = not menu_music_playing
        if not menu_music_playing:
            music.stop()
        else:
            music.set_volume(0.5)
            music.play('menu_music')
    elif Rect((300, 390), (200, 50)).collidepoint(pos):
        exit()
