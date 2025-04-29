''' ---------- GAME SETTINGS ---------- '''

import pygame as pg
import random, time
import asyncio

pg.init()
clock = pg.time.Clock()

# Add in colour variables
black = (0, 0, 0)

# Set the full window width and height
win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris')

font = pg.font.Font(None, 30)

speed = 10
capacity = 20
running = True

# Add in main game variables

player_size = 95
player_pos = [win_width / 2, win_height - player_size]

obj_size = 57
obj_data = []

# Load in and scale player image
player_image = pg.image.load('./assets/images/Bowl.png').convert_alpha()
player_image = pg.transform.scale(player_image,
                                  (player_size, player_size))

# Load in and scale object image
obj = pg.image.load('./assets/images/bread_pudding2.png').convert_alpha()
obj = pg.transform.scale(obj, (obj_size, obj_size))

heart_size = 60
heart_data = []
heart = pg.image.load('./assets/images/cute_strawberry_jelly.png').convert_alpha()
heart = pg.transform.scale(heart, (heart_size, heart_size))

# Load in and scale background image
bg_image = pg.image.load('./assets/images/kitchen_background.jpg').convert_alpha()
bg_image = pg.transform.scale(bg_image, (win_width, win_height))



''' ---------- CREATE_OBJECT FUNCTION ---------- '''

def create_object(obj_data):
    if len(obj_data) < 10 and random.random() < 0.1:
        x = random.randint(0, win_width - obj_size)
        y = 0
        obj_data.append([x, y, obj])

def create_heart(heart_data):
    if len(heart_data) < 2 and random.random() < 0.01:
        x = random.randint(0, win_width - heart_size)
        y = 0
        heart_data.append([x, y, heart])        



''' ---------- UPDATE_OBJECTS FUNCTION ---------- '''

def update_objects(obj_data):
    global capacity

    for object in obj_data:
        x, y, image_data = object
        if y < win_height:
            y += speed
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            

def update_hearts(heart_data):

    for heart in heart_data:
        x, y, image_data = heart
        if y < win_height:
            y += speed
            heart[1] = y
            screen.blit(image_data, (x, y))
        else:
            heart_data.remove(heart)





''' ---------- COLLISION_CHECK FUNCTION ---------- '''

def collision_check(obj_data, player_pos):
    global running, capacity
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y,
                              player_size, player_size)
        if player_rect.colliderect(obj_rect):
            capacity -= 1
            obj_data.remove(object)
            if capacity == 0:
                time.sleep(2)
                running = False
                break

def heart_check(heart_data, player_pos):
    global capacity
    for heart in heart_data:
        x, y, image_data = heart
        player_x, player_y = player_pos[0], player_pos[1]
        heart_rect = pg.Rect(x, y, heart_size, heart_size)
        player_rect = pg.Rect(player_x, player_y,
                              player_size, player_size)
        if player_rect.colliderect(heart_rect):
            capacity += 2
            heart_data.remove(heart)

        



''' ---------- EVENT HANDLERS ---------- '''

async def main():
    global player_pos, running

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                x, y = player_pos[0], player_pos[1]
                if event.key == pg.K_a:
                    x -= 20
                elif event.key == pg.K_d:
                    x += 20
                player_pos = [x, y]


        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))



        text = f'Capacity: {capacity}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 150, win_height - 20))

        create_object(obj_data)
        create_heart(heart_data)
        update_objects(obj_data)
        update_hearts(heart_data)
        collision_check(obj_data, player_pos)
        heart_check(heart_data, player_pos)

        clock.tick(30)
        pg.display.update()
        await asyncio.sleep(0)

asyncio.run(main())
