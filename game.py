# Xinyu Hou (xh4eu), Mengchen Wang(mw5ew), Xinyi Yu(xy6qn)

import pygame
import gamebox
import random

"""
Game Name is LMY-7. It is weird, but the game name is LMY-7.
Required Features:
(1) User Input: The user can control the player using KEYS.
(2) Graphics/Images
(3) Start Screen: The first screen displays the name of the game,
student names (and IDs), and lets the user pick the player (2 
choices). The second screen displays the game instructions and 
lets the user pick the level (beginner, intermediate, advanced).
(4) Small Enough Window: The game window size is 800*600.
Six Features:
(1) Animation: The collectible (coins) is an animation.
(2) Enemies: Fire and stone will fall from the sky, and they can
cause damages to the player's health meter.
(3) Collectibles: The collectibles in this game are coins. The goal
of the game is for the player to collect a total number of 20 coins.
Once the player collects enough coins and its health meter is still
bigger than 0, the user wins the game.
(4) Timer: There is a count-up timer for this game. We will count
the total survival time of the player and also display it at the 
end of the game.
(5) Health Meter: The maximum health meter of the player is 5. It
decreases when the player hit by obstacles (fire and stone). When 
it gets to 0, the  user will automatically lose the game.
(6) Multiple Levels: There are three levels of this game (beginner,
intermediate, advanced). Beginner level does not have fire or stone,
but the other two levels have. Fire and stone will fall at a faster 
rate if advanced level is picked. 
"""

# game window size 800*600
camera = gamebox.Camera(800, 600)

# player list
player_1 = gamebox.from_image(200, 390, 'player_1.png')
player_2 = gamebox.from_image(600, 390, 'player_2.png')
player_1.scale_by(.25)
player_2.scale_by(.25)
player_lst = [player_1, player_2]
player_1_right = gamebox.from_image(200, 390, 'player_1_right.png')
player_2_right = gamebox.from_image(600, 390, 'player_2_right.png')
player_1_right.scale_by(.2)
player_2_right.scale_by(.2)

# Start Screen
game_created_by = gamebox.from_text(600, 15, 'This game is created by:', 25, 'white')
student1 = gamebox.from_text(600, 30, 'Xinyu Hou (xh4eu)', 20, 'white')
student2 = gamebox.from_text(600, 45, 'Mengchen Wang(mw5ew)', 20, 'white')
student3 = gamebox.from_text(600, 60, 'Xinyi Yu(xy6qn)', 20, 'white')
game_name = gamebox.from_text(400, 210, 'LMY-7', 50, 'orange', bold=True)
first_line = gamebox.from_text(400, 250, 'Press 1 for Player 1.', 40, 'white')
second_line = gamebox.from_text(400, 280, 'Press 2 for Player 2.', 40, 'white')
choice_1 = gamebox.from_text(210, 485, 'Player 1', 40, 'orange')
choice_2 = gamebox.from_text(610, 485, 'Player 2', 40, 'orange')
start_screen = [game_created_by, student1, student2, student3, game_name, first_line, second_line, choice_1, choice_2]


# background
background = gamebox.from_image(400, 300, 'background.png')
background.scale_by(1.57)

# three levels
beginner = gamebox.from_text(400, 210, 'Beginner', 40, 'white')
intermediate = gamebox.from_text(400, 240, 'Intermediate', 40, 'white')
advanced = gamebox.from_text(400, 270, 'Advanced', 40, 'white')
line_1 = gamebox.from_text(400, 20, 'Instruction:', 30, 'black')
line_2 = gamebox.from_text(400, 45, 'The ultimate goal for you is to collect 20 coins', 25, 'black')
line_3 = gamebox.from_text(400, 65, 'Use the UP DOWN LEFT RIGHT keys to control the player', 25, 'black')
line_4 = gamebox.from_text(400, 85, 'Beware of the falling Fire and Stone', 25, 'black')
line_5 = gamebox.from_text(400, 105, "And don't get pushed off the screen", 25, 'black')
level_lst = [beginner, intermediate, advanced, line_1, line_2, line_3, line_4, line_5]
pick_level = gamebox.from_text(400, 485, 'Press B, I, or A for level', 40, 'orange')

# obstacles (fire, stone, rect) and boundary (floor)
fire = gamebox.from_image(random.randint(100, 700), -100, 'fire.png')
stone = gamebox.from_image(random.randint(100, 700), -100, 'stone.png')
rect = gamebox.from_image(random.randint(900, 1000), random.randint(100, 400), 'rect.png')
floor = gamebox.from_color(400, 510, 'brown', 800, 5)
fire.scale_by(0.08)
rect.scale_by(0.2)
stone.scale_by(0.08)
obs = [rect]
falling = [fire, stone]

# coin (Credit to one of the CS professors: Craig Dill. Xinyu adopted his idea of using coins as collectibles and
# altered some codes to make the coin an animation.)
number_of_frames = 6
sheet = gamebox.load_sprite_sheet("coin.png", 1, number_of_frames)
frame = 0
counter = 0
coin = gamebox.from_image(400, 300, sheet[frame])
coin.scale_by(.5)
coin_lst = [coin]
time1 = 0

# score
score = 0

# timer
survival_time = 0

# health meter
health_meter = 5

# other variables
game_on = False
game_b = False
game_i = False
game_a = False
player_speed = 15
gravity = 7
time = 0
ticks = 0


def no1_screen(keys):
    # Start Screen: The user can pick one of the two players.
    global player_1, player_2, player_lst, start_screen, level_lst
    camera.draw(background)
    player = player_lst[0]
    for player in player_lst:
        camera.draw(player)
    for thing in start_screen:
        camera.draw(thing)
    if pygame.K_1 in keys and game_on == False:
        player_lst = [player_1_right]
        start_screen = [pick_level]
        player.x = 400
        for level in level_lst:
            start_screen.append(level)
    if pygame.K_2 in keys and game_on == False:
        player_lst = [player_2_right]
        start_screen = [pick_level]
        player.x = 400
        for level in level_lst:
            start_screen.append(level)


def coin_collectibles(keys):
    global counter, frame, sheet, coin_lst, time1, player_lst, score
    player = player_lst[0]
    # coin
    for coin in coin_lst:
        if player.touches(coin):
            score += 1
            coin_lst.remove(coin)
        camera.draw(coin)
        if frame >= number_of_frames:
            frame = 0
        if counter % 1 == 0:  # control coin spinning speed by changing 1
            coin.image = sheet[frame]
    frame += 1
    counter += 1
    time1 += 1
    if time1 % 60 == 0:
        coin_x = random.randint(50, 750)
        coin_y = random.randint(200, 480)
        for coin in coin_lst:
            if coin_x == coin.x:
                coin_x -= 100
            if coin_y == coin.y:
                coin_y -= 100
        new_coin = gamebox.from_image(coin_x, coin_y, sheet[0])
        new_coin.scale_by(.5)
        coin_lst.append(new_coin)


def player_control(keys):
    # move player
    global time, player_lst, gravity
    player = player_lst[0]
    if pygame.K_RIGHT in keys:
        player.x += player_speed
    if pygame.K_LEFT in keys:
        player.x -= player_speed
    if pygame.K_UP in keys or pygame.K_SPACE in keys:
        # Like the Flappybird assignment, there is no rocketing up.
        player.y -= 50
        keys.clear()
        time = 0
    if pygame.K_DOWN in keys:
        player.y += player_speed
    player.y += gravity * time
    time += 0.1


def b_level_game(keys):
    """
    This is the beginner level of the game. There is no fire
    or stone falling from the sky. Don't get pushed off the
    screen by the obstacles. Once the player collects 20 coins,
    the user will win the game.
    """
    global time, player_lst, health_meter
    player = player_lst[0]
    if game_on and game_b:
        coin_collectibles(keys)
        player_control(keys)

        # obstacle
        if player.touches(floor):
            time = 0
            player.move_to_stop_overlapping(floor)
        for thing in obs:
            if player.touches(thing):
                time = 0
                player.move_to_stop_overlapping(thing)
                if player.right == thing.left or player.top == thing.bottom:
                    player.y += gravity * 0.5

        for thing in obs:
            thing.x -= 5

        if player.x < 0 or player.x > 800 or player.y < 0 or player.y > 600:
            health_meter -= 1
            player.x = 400
            player.y = 300


def i_level_game(keys):
    """
    This is the intermediate level of the game. There is fire
    or stone falling from the sky. Don't get pushed off the
    screen by the obstacles. Once the player collects 20 coins,
    the user will win the game.
    """
    global time, player_lst, level_lst, falling, obs
    global health_meter
    player = player_lst[0]
    if game_on and game_i:
        coin_collectibles(keys)
        player_control(keys)

        # obstacle
        if player.touches(floor):
            time = 0
            player.move_to_stop_overlapping(floor)
        for thing in obs:
            if player.touches(thing):
                time = 0
                player.move_to_stop_overlapping(thing)
                if player.right == thing.left or player.top == thing.bottom:
                    player.y += gravity * 0.5

        for thing in falling:
            thing.y += 10
        for thing in obs:
            thing.x -= 5
        # health meter
        for thing in falling:
            if player.touches(thing):
                health_meter -= 1
                thing.y = 700
        if player.x < 0 or player.x > 800 or player.y < 0 or player.y > 600:
            health_meter -= 1
            player.x = 400
            player.y = 300


def a_level_game(keys):
    """
    This is the advanced level of the game. There is fire
    or stone falling from the sky. They are also falling at
    a faster rate. Don't get pushed off the screen by the
    obstacles. Once the player collects 20 coins, the user
    will win the game.
    """
    global time, player_lst, falling, obs
    global health_meter
    player = player_lst[0]
    if game_on and game_a:
        coin_collectibles(keys)
        player_control(keys)

        # obstacle
        if player.touches(floor):
            time = 0
            player.move_to_stop_overlapping(floor)
        for thing in obs:
            if player.touches(thing):
                time = 0
                player.move_to_stop_overlapping(thing)
                if player.right == thing.left or player.top == thing.bottom:
                    player.y += gravity * 0.5

        for thing in falling:
            thing.y += 20
        for thing in obs:
            thing.x -= 10

        # health meter
        for thing in falling:
            if player.touches(thing):
                health_meter -= 1
                thing.y = 700
        if player.x < 0 or player.x > 800 or player.y < 0 or player.y > 600:
            health_meter -= 1
            player.x = 400
            player.y = 300


def tick(keys):
    global player_lst, game_on, game_i, game_a, game_b, level_lst, health_meter, ticks, score
    global survival_time
    no1_screen(keys)
    if pygame.K_b in keys and game_on == False:
        for level in level_lst:
            level.y -= 1000
        pick_level.y -= 1000
        for player in player_lst:
            player.scale_by(.7)
        game_on, game_b = True, True

    if pygame.K_i in keys and game_on == False:
        for level in level_lst:
            level.y -= 1000
        pick_level.y -= 1000
        for player in player_lst:
            player.scale_by(.7)
        game_on, game_i = True, True

    if pygame.K_a in keys and game_on == False:
        for level in level_lst:
            level.y -= 1000
        pick_level.y -= 1000
        for player in player_lst:
            player.scale_by(.7)
        game_on, game_a = True, True

    ticks += 1
    if game_b:
        if ticks % 100 == 0:
            new_rect = gamebox.from_image(random.randint(900, 1000), random.randint(100, 400), 'rect.png')
            new_rect.scale_by(0.2)
            obs.append(new_rect)

    if game_i:
        if ticks % 70 == 0:
            new_rect = gamebox.from_image(random.randint(900, 1000), random.randint(100, 400), 'rect.png')
            new_rect.scale_by(0.2)
            obs.append(new_rect)

        if ticks % 40 == 0:
            new_fire = gamebox.from_image(random.randint(100, 700), -100, 'fire.png')
            new_stone = gamebox.from_image(random.randint(100, 700), -100, 'stone.png')
            new_fire.scale_by(0.08)
            new_stone.scale_by(0.08)
            falling.append(new_fire)
            falling.append(new_stone)
    if game_a:
        if ticks % 80 == 0:
            new_rect = gamebox.from_image(random.randint(900, 1000), random.randint(100, 400), 'rect.png')
            new_rect.scale_by(0.2)
            obs.append(new_rect)

        if ticks % 30 == 0:
            new_fire = gamebox.from_image(random.randint(100, 700), -40, 'fire.png')
            new_stone = gamebox.from_image(random.randint(100, 700), -40, 'stone.png')
            new_fire.scale_by(0.08)
            new_stone.scale_by(0.08)
            falling.append(new_fire)
            falling.append(new_stone)

    b_level_game(keys)
    i_level_game(keys)
    a_level_game(keys)

    survival = int(float(survival_time / ticks_per_second))
    if game_on:
        survival_time += 1

    if health_meter <= 0:
        game_on = False
        end = gamebox.from_text(400, 300, 'Game Over!', 180, 'black')
        survival_time_box = gamebox.from_text(400, 370, "You've survived " + str(survival) + " seconds!", 40, 'white')
        # remove extra obs from screen
        for thing in obs:
            thing.y -= 10000
        camera.draw(survival_time_box)
        camera.draw(end)
        gamebox.pause()
    life = gamebox.from_text(100, 30, "Health Meter: " + str(health_meter), 30, 'green')
    final_score = gamebox.from_text(135, 50, "Score: " + str(score), 30, 'green')
    # NOTE: When the score reaches 20, the user will win the game. The ending shows the 'Mission Complete!' Sign and
    # gives the total survival time.
    if score >= 20:
        game_on = False
        gamebox.pause()
        win = gamebox.from_text(400, 300, 'Mission Complete!', 120, 'orange')
        survival_time_box = gamebox.from_text(400, 370, "You've survived " + str(survival) + " seconds!", 40, 'white')
        # remove extra obs from screen
        for thing in obs:
            thing.y = 10000
        camera.draw(win)
        camera.draw(survival_time_box)

    camera.draw(floor)
    for thing in obs:
        camera.draw(thing)
    for thing in falling:
        camera.draw(thing)
    camera.draw(life)
    camera.draw(final_score)
    camera.display()


ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, tick)

'''
Citation:
coin image from 'https://www.pixilart.com/art/coin-sprite-sheet-c7f297523ce57fc'
background image from 'http://armyblog.ru/mario-game-backgrounds'
rect image from 'https://www.fotolia.com/tag/%22cartoon%20ruler%22'
fire image from 'http://www.stickpng.com/img/nature/fire/cartoon-fire-flames'
stone image from https://clip2art.com/explore/Boulder%20clipart%20cartoon/
all the images for the players from 'weibo.com'
'''