'''
Imported Libraries
-----------------
pygame --> provides visual and auditory libraries to bring the game to life!
We use 'from pygame.locals import *' to make our coding more efficient and easier.
If we didn't include this line, everything we wanted to access a pygame method we would have to do .pygame.method()

Pickle is a library that allows one to convert objects such as lists into character streams. This allows us to store our
levels in files such as level1_data, rather than having 10 large lists in our main.py file as it would be very messy.

The line 'from os import path' imports a library that allows us to verify that a level actually exists as a file before
pickle calls on it to use in the game. This is important because if we call a nonexistant level, there will be no data
for that level causing the game to crash.
'''

import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

'''
Loading music settings in pygame
--------------------------------
We run mixer.init() to initializes the mixer module which is how pygame supports the playback of audio
The pre_init() method defines the frequency, volume, channels, and buffer settings as pygame requires this
We use the default values for the pre_init() method as they run perfectly for this game 
Finally, run pygame.init() which initializes all pygame modules, many of which we'll be using later on in the program! 
'''

mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Setting up Frames-Per-Second limiter for the game
clock = pygame.time.Clock()  # define variable clock to equal pygame's Clock() module to let our program recognize time.
frame_rate = 60  # define variable frame_rate to equal 60 as this is a good frame rate for most games.

# Setting up screen
screen_width = 1000  # set screen width to equal 1000 pixels
screen_height = 1000  # set screen height to equal 1000 pixels
screen = pygame.display.set_mode((screen_width, screen_height))  # create the display window and stores it in var screen
pygame.display.set_caption('Platformer')  # sets a title for our game window

'''
Function to load images + convert them to the same pixel format as the screen. The images are loaded with .load()
And converted to the screen format by .convert_alpha(). This prevents lag as images are pre-loaded and converted.
This is very helpful as we load 20+ images in this game, and typing out 'pygame.image.load(imgname).convert_alpha()'
everytime is inefficient coding, so this function helps us modularize our code saving a lot of time!
'''


def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha()


# load fonts
font_score = pygame.font.SysFont('Bauhaus 93', 30)  # store Bauhaus 93 font in size 30 in variable 'font_score'
font = pygame.font.SysFont('Bauhaus 93', 70)  # store Bauhaus 93 font in size 70 in variable 'font_score'

# define global variables
tile_size = 50  # define variable tile_size as 50
game_over = 0  # define variable game_over as 0
main_menu = True  # define variable main_menu as True
level = 1  # define variable level as 1
max_levels = 10  # define variable max_levels as 10
score = 0  # # define variable score as 0
display = 'original'  # define variable display as 'original'
current_music = 'forest'  # define variable current_music as 'forest'

# define colors for efficiency
blue = (0, 0, 255)  # define variable blue as the color's RGB values
red = (255, 0, 0)  # define variable red as the color's RGB values
black = (0, 0, 0)  # define variable black as the color's RGB values

# load images
forest_img = loadify('images/forest3.png')  # pre-load and convert the forest levels' background image
bg_img = loadify('Assets/Base_pack/bg.png')  # pre-load and convert the default sky background image
restart_img = loadify('images/restart_btn.png')  # pre-load and convert the restart button image
start_img = loadify('images/start_btn.png')  # pre-load and convert the start button image
exit_img = loadify('images/exit_btn.png')  # pre-load and convert the exit button image
arctic_img = loadify('images/arctic2.png')  # pre-load and convert the arctic levels' background image
cake_img = loadify('images/cake-bg.jpg')  # pre-load and convert the cake levels' background image
final_img = loadify('images/final_background.png')  # pre-load and convert the final level's background image


# load sounds

def change_music():  # define function change_music()
    global current_music  # make the current_music variable used in this function a global variable

    if level < 5 and current_music != 'forest':  # if the level is less than 5 and the music is not already 'forest':
        pygame.mixer.music.load('sounds/Forest_Music.wav')  # load the forest music file
        pygame.mixer.music.set_volume(1)  # set the forest music to max volume (1)
        pygame.mixer.music.play(-1, 0.0, 5000)  # play the forest music infinitely with a 5000 millisecond fade-in
        current_music = 'forest'  # set variable 'current_music' to forest

    elif 4 < level < 8 and current_music != 'arctic':  # if the level between 4-8 and the music is not already 'arctic':
        pygame.mixer.music.load('sounds/Arctic_Music.mp3')  # load the forest music file
        pygame.mixer.music.set_volume(1)  # set the forest music to max volume (1)
        pygame.mixer.music.play(-1, 0.0, 5000)  # play the forest music infinitely with a 5000 millisecond fade-in
        current_music = 'arctic'  # set variable 'current_music' to arctic

    elif 7 < level < 9 and current_music != 'cake':  # if the level between 7-9 and the music is not already 'arctic':
        pygame.mixer.music.load('sounds/cake_sound.mp3')
        pygame.mixer.music.set_volume(0.8)  # set the forest music to 80% volume (0.8)
        pygame.mixer.music.play(-1, 0.0, 5000)  # play the forest music infinitely with a 5000 millisecond fade-in
        current_music = 'cake'  # set variable 'current_music' to cake

    elif level == 10 and current_music != 'final':
        pygame.mixer.music.load('sounds/Final_Music.mp3')
        pygame.mixer.music.set_volume(1)  # set the forest music to max volume (1)
        pygame.mixer.music.play(-1, 0.0, 5000)  # play the forest music infinitely with a 5000 millisecond fade-in
        current_music = 'final'  # set variable 'current_music' to final


# Set default music (in start menu)
pygame.mixer.music.load('sounds/Forest_Music.wav')  # load the forest music file
pygame.mixer.music.set_volume(1)  # set the forest music to max volume (1)
pygame.mixer.music.play(-1, 0.0, 5000)  # play the forest music infinitely with a 5000 millisecond fade-in

coin_fx = pygame.mixer.Sound('sounds/coin.wav')  # load the coin sound effect file
coin_fx.set_volume(0.5)  # set the volume to half (0.5)
jump_fx = pygame.mixer.Sound('sounds/jump.wav')  # load the jump sound effect file
jump_fx.set_volume(0.5)  # set the volume to half (0.5)
game_over_fx = pygame.mixer.Sound('sounds/game_over.wav')  # load the game over sound effect file
game_over_fx.set_volume(0.5)  # set the volume to half (0.5)

# Scale background images to fit the screen
forest_img = pygame.transform.scale(forest_img, (screen_width, screen_height))  # scale forest background image
arctic_img = pygame.transform.scale(arctic_img, (screen_width, screen_height))  # scale arctic background image
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))  # scale sky background image
cake_img = pygame.transform.scale(cake_img, (screen_width, screen_height))  # scale cake background image
final_img = pygame.transform.scale(final_img, (screen_width, screen_height))  # scale final background image


# Create function to draw text on screen
def draw_text(text, font, text_col, x, y):  # take in multiple parameters for the text
    img = font.render(text, True, text_col)  # render the font as an image based on the parameters given
    screen.blit(img, (x, y))  # blit the image onto the screen at the given coordinate parameters


# resetting level function
def reset_level(level):  # take in the current level as a parameter
    global current_music  # set current_music as a global variable when used inside this function
    player.reset(100, screen_height - 130)  # reset the player by calling the Player() class' reset() function
    blob_group.empty()  # delete all instances of enemy slimes
    lava_group.empty()  # delete all instances of lava
    exit_group.empty()  # delete all instances of exit gates
    platform_group.empty()  # delete all instances of platforms
    ice_platform_group.empty()  # delete all instances of ice platforms
    coin_group.empty()  # delete all instances of coins
    water_group.empty()  # delete all instances of water

    # loading data for the levels / world
    if path.exists(f'level{level}_data'):  # verify if the data file for the level exists
        pickle_in = open(f'level{level}_data', 'rb')  # process the data file | 'rb' stands for read binary
        world_data = pickle.load(pickle_in)  # save the processed data in variable 'world_data'
    world = World(world_data)  # process world_data through class World() and store in variable 'world'.

    return world  # return the world_data inside variable 'world'


# class for button
class Button():
    def __init__(self, x, y, image):  # create constructor function with coordinate parameters (x, y) + image
        self.image = image  # store the value of parameter 'image' inside local variable 'image'
        self.rect = self.image.get_rect()  # create a collision rectangle around the image
        self.rect.x = x  # set the rectangles x coordinate to the x coordinate of the image
        self.rect.y = y  # set the rectangles y coordinate to the y coordinate of the image
        self.clicked = False  # set variable 'self.clicked' to False

    # draw function
    def draw(self):
        action = False  # set action to false

        # getting position of cursor
        pos = pygame.mouse.get_pos()

        # check if mouse is over the button and if it is clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        # if it is not clicked then set self.clicked to False
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)  # drawing the button

        return action  # return the action (clicked or not)


# player class
class Player():
    def __init__(self, x, y):  # constructor function with coordinate parameters (x, y)
        self.reset(x, y)  # run the reset function with the coordinate parameters (x, y)

    def update(self, game_over):  # update function with 'game_over' parameter (global variable)

        # defining delta values
        dx = 0  # delta x = 0
        dy = 0  # delta y = 0
        walk_cooldown = 3  # walk animation speed limiter
        collision_threshold = 20  # collision predictor for platform movement

        if game_over == 0:  # when the game is NOT over

            # get key inputs
            key = pygame.key.get_pressed()

            '''
            Player Jumping Movement: 
            If the spacebar is pressed while the player is not currently jumping or in air, play the jump sound effect
            And change the player's 'jumped' status to True as well as set their vertical velocity to -15 which will
            make them jump! If they are not pressing the spacebar, then set their 'jumped' status to False.
            '''
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True

            if not key[pygame.K_SPACE]:
                self.jumped = False

            '''
            Player Walkikng Movement: 
            If the left arrow-key is pressed then change the player's predicted x-axis position by -5
            Increase the counter by 1 (for walk animation)
            Set the direction to -1 (left)
            
            If the right arrow-key is pressed then change the player's predicted x-axis position by +5
            Increase the counter by 1 (for walk animation)
            Set the direction to 1 (right)
            
            If neither arrow-keys are being pressed, reset the counter and animation index to 0.
            Set the character to face left or right depending on if the direction is equal to -1 or 1 respectfully.
            '''
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # player animation
            '''
            If the counter is greater than the walk_cooldown (limiting the speed of animation) then reset the counter
            to 0 and increase the index by 1. Then check if the index is greater than or equal to the length of the
            images_right list, and if it is then reset the index to 0. This prevents the animation from looking for
            an image in the list that doesn't exist, and loops the animaton. 
            
            If the direction is 1 then set the player's image to the current index image in the images_right[] list of
            sprites. If the direction is -1 then set the player's image to the current index image in the images_left[] 
            list of sprites. This creates an animation as the game loops through the list of walking images quickly.
            '''
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # gravity + jumping mechanic
            self.vel_y += 1  # increase the vertical velocity by 1
            if self.vel_y > 10:  # if the vertical velocity is greater than 10
                self.vel_y = 10  # set it to 10 (this effectively limits it at 10)
            dy += self.vel_y  # self the predicted player movement (delta y) to equal delta y + vel_y

            self.in_air = True  # set the player's 'in_air' status to True

            # checking collisions

            '''
            iterate through all the tiles, and access their collision rectangles (tile[1]) and see if there would be
            a collision with the player and the tile on either the x or y axis at the player's current velocity and 
            projected movement.
            '''
            for tile in world.tile_list:

                # check for x-axis collisions
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # check for y-axis collisions
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    '''
                    If there is a vertical collision, determine if it is from above or below and restrict player
                    movement so that the player stops at the collision point.
                    '''
                    # check if the player is jumping or resting on a block
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0

                    # check if the player is falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # if there is a collision between the player and an enemy slime:
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1  # set var game_over to -1 as the player dies and loses temporarily
                game_over_fx.play()  # play the game_over sound effect

            # if there is a collision between the player and lava:
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1  # set var game_over to -1 as the player dies and loses temporarily
                game_over_fx.play()  # play the game_over sound effect

            # if there is a collision between the player and water:
            if pygame.sprite.spritecollide(self, water_group, False):
                game_over = -1  # set var game_over to -1 as the player dies and loses temporarily
                game_over_fx.play()  # play the game_over sound effect

            # checking for collisions with exit door (next level)
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1  # set var game_over to 1 meaning the player 'wins' that level

            # checking for collisions with platforms
            for platform in platform_group:
                # collision on the x-axis
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # collision on the y-axis
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # collision if player is BELOW platform
                    '''
                    (When player is BELOW platform) 
                    Check if the players predicted position will overlap with the platforms predicted position, and if 
                    it will then there will be a collision so stop player movement in that direction at the collision
                    point. 
                    
                                    
                    (When player is BELOW platform) 
                    Check if the players predicted position will overlap with the platforms predicted position, and if 
                    it will then there will be a collision so stop player movement in that direction at the collision
                    point. 
                    '''
                    if abs((self.rect.top + dy) - platform.rect.bottom) < collision_threshold:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top + 1
                        if platform.rect.bottom > (tile_size + self.height):
                            dy = 0

                    # collision if player is ABOVE platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < collision_threshold:
                        dy = 0
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False

                    # make player move with platform
                    if platform.move_x != 0:  # if the platform is moving
                        self.rect.x += platform.move_direction  # add platform movement to player movement

            # checking for collisions with ice-platforms
            for ice_platform in ice_platform_group:
                # collision on the x-axis
                if ice_platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # collision on the y-axis
                if ice_platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # collision if player is BELOW platform
                    '''
                    (When player is BELOW platform) 
                    Check if the players predicted position will overlap with the platforms predicted position, and if 
                    it will then there will be a collision so stop player movement in that direction at the collision
                    point. 


                    (When player is BELOW platform) 
                    Check if the players predicted position will overlap with the platforms predicted position, and if 
                    it will then there will be a collision so stop player movement in that direction at the collision
                    point. 
                    '''
                    if abs((self.rect.top + dy) - ice_platform.rect.bottom) < collision_threshold:
                        self.vel_y = 0
                        dy = ice_platform.rect.bottom - self.rect.top + 1
                        if ice_platform.rect.bottom > (tile_size + self.height):
                            dy = 0

                    # collision if player is ABOVE platform
                    elif abs((self.rect.bottom + dy) - ice_platform.rect.top) < collision_threshold:
                        dy = 0
                        self.rect.bottom = ice_platform.rect.top - 1
                        self.in_air = False

                    # make player move with ice platform
                    if ice_platform.move_x != 0:  # if the ice platform is moving
                        self.rect.x += ice_platform.move_direction  # add ice platform movement to player movement

            # moving player
            self.rect.x += dx  # move the player's collision rectangle with the predicted delta x movement value
            self.rect.y += dy  # move the player's collision rectangle with the predicted delta y movement value

        elif game_over == -1:  # else if the game_over var is equal to -1 (aka player dead)
            self.image = self.dead_image  # replace the player image with the dead image file
            draw_text('GAME OVER', font, red, (screen_width // 2) - 200, screen_height // 2)  # write GAME OVER screen
            if self.rect.y > 200:  # if the player is not 200 pixels off the ground
                self.rect.y -= 5  # decrease their dead ghost's image position by 5 on the y-axis to make them float

        screen.blit(self.image, self.rect)  # displaying player

        # return the game_over parameter's new value
        return game_over

    def reset(self, x, y):  # player reset function
        self.images_right = []  # reset player right-facing sprites
        self.images_left = []  # reset player left-facing sprites
        self.index = 0  # reset index to 0
        self.counter = 0  # reset counter to 0
        for picture in range(1, 12):  # looping 11 times, starting at 1:
            img_right = loadify(f'Assets/Base_pack/Player/p1_walk/PNG/p1_walk{picture}.png')  # load facing-right image
            img_right = pygame.transform.scale(img_right, (45, 70))  # scale image to desired player size
            img_left = pygame.transform.flip(img_right, True, False)  # flip image at y-axis and store as facing-left
            self.images_right.append(img_right)  # append the image to the image_right list
            self.images_left.append(img_left)  # append the image to the image_left list
        self.dead_image = loadify('images/ghost.png')  # load the player's death image
        self.image = self.images_right[self.index]  # set the player's default image to facing right
        self.rect = self.image.get_rect()  # create a collision rectangle around player
        self.rect.x = x  # set x coordinate of rectangle to x coordinate of player
        self.rect.y = y  # set y coordinate of rectangle to y coordinate of player
        self.width = self.image.get_width()  # get the width of the player
        self.height = self.image.get_height()  # get the height of the player
        self.vel_y = 0  # set player's vertical velocity to 0
        self.jumped = False  # set the player's 'jumped' status to False
        self.direction = 0  # set player's direction to 0
        self.in_air = True  # set the player's 'in_air' status to True


# World class
class World():
    def __init__(self, data):  # constructor function that takes parameter 'data'
        self.tile_list = []  # create an empty list

        # load world images
        dirt_img = loadify('images/dirt.png')  # load dirt image
        grass_img = loadify('images/grass.png')  # load grass image
        tundra_img = loadify('images/tundra.png')  # load tundra image
        blank_tundra_img = loadify('images/tundra_blank.png')  # load tundra_blank image
        cake_img = loadify('images/cake.png')  # load cake image
        blank_cake_img = loadify('images/cake_blank.png')  # load cake_blank image
        choco_cake_img = loadify('images/choco_cake.png')  # load choco_cake image
        blank_choco_cake_img = loadify('images/choco_cake_blank.png')  # load choco_cake_blank image

        rows = 0  # create a rows variable and set to 0

        '''
        This part of the code repeats 22 times. Instead of commenting each part individually, this block-comment will 
        feature an explanation of all repetitions that are not individually commented below (anything but tiles)
        This runs off a nested for loop as the world_data is contained within a nested list.
        
        if tile == x: --> depending on what the number in the tile_list is:
            object = Class(columns * width, rows * height, 'parameter') --> generate an instance of an object with
            a specified size and any parameters (such as color)
            object_group.add(object) --> add this object to a group of other identical objects
        
        '''
        for row in data:  # iterating as many values in the variable 'data':
            columns = 0  # set columns to equal 0
            for tile in row:  # iterating for every tile per value in 'data':
                if tile == 1:  # if the tile has a value of 1
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))  # scale the image to tile_size
                    img_rect = img.get_rect()  # create a collision rectangle around the image
                    img_rect.x = columns * tile_size  # set the rectangle's x coordinate to be at the column * tile_size
                    img_rect.y = rows * tile_size  # set the rectangle's x coordinate to be at the row * tile_size
                    tile = (img, img_rect)  # create the tile object with the image and the rectangle in a tuple
                    self.tile_list.append(tile)  # append this tile to a list of tiles
                if tile == 2:  # if the tile has a value of 2
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))  # scale the image to tile_size
                    img_rect = img.get_rect()  # create a collision rectangle around the image
                    img_rect.x = columns * tile_size  # set the rectangle's x coordinate to be at the column * tile_size
                    img_rect.y = rows * tile_size  # set the rectangle's x coordinate to be at the row * tile_size
                    tile = (img, img_rect)  # create the tile object with the image and the rectangle in a tuple
                    self.tile_list.append(tile)  # append this tile to a list of tiles
                if tile == 3:
                    blob = Enemy(columns * tile_size, rows * tile_size + 15, 'green')
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(columns * tile_size, rows * tile_size, 1, 0, 'dirt')
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(columns * tile_size, rows * tile_size, 0, 1, 'dirt')
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(columns * tile_size, rows * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(columns * tile_size + (tile_size // 2), rows * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit = Exit(columns * tile_size, rows * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == 9:
                    img = pygame.transform.scale(tundra_img, (tile_size, tile_size))  # scale the image to tile_size
                    img_rect = img.get_rect()  # create a collision rectangle around the image
                    img_rect.x = columns * tile_size  # set the rectangle's x coordinate to be at the column * tile_size
                    img_rect.y = rows * tile_size  # set the rectangle's x coordinate to be at the row * tile_size
                    tile = (img, img_rect)  # create the tile object with the image and the rectangle in a tuple
                    self.tile_list.append(tile)  # append this tile to a list of tiles
                if tile == 10:
                    img = pygame.transform.scale(blank_tundra_img, (tile_size, tile_size))  # scale the image to tile_size
                    img_rect = img.get_rect()  # create a collision rectangle around the image
                    img_rect.x = columns * tile_size  # set the rectangle's x coordinate to be at the column * tile_size
                    img_rect.y = rows * tile_size  # set the rectangle's x coordinate to be at the row * tile_size
                    tile = (img, img_rect)  # create the tile object with the image and the rectangle in a tuple
                    self.tile_list.append(tile)  # append this tile to a list of tiles
                if tile == 11:
                    ice_platform = IcePlatform(columns * tile_size, rows * tile_size, 1, 0)
                    ice_platform_group.add(ice_platform)
                if tile == 12:
                    ice_platform = IcePlatform(columns * tile_size, rows * tile_size, 0, 1)
                    ice_platform_group.add(ice_platform)
                if tile == 13:
                    water = Water(columns * tile_size, rows * tile_size + (tile_size // 2))
                    water_group.add(water)
                if tile == 14:
                    img = pygame.transform.scale(cake_img, (tile_size, tile_size))  # scale the image to tile_size
                    img_rect = img.get_rect()  # create a collision rectangle around the image
                    img_rect.x = columns * tile_size  # set the rectangle's x coordinate to be at the column * tile_size
                    img_rect.y = rows * tile_size  # set the rectangle's x coordinate to be at the row * tile_size
                    tile = (img, img_rect)  # create the tile object with the image and the rectangle in a tuple
                    self.tile_list.append(tile)  # append this tile to a list of tiles
                if tile == 15:
                    img = pygame.transform.scale(blank_cake_img, (tile_size, tile_size))  # scale the image to tile_size
                    img_rect = img.get_rect()  # create a collision rectangle around the image
                    img_rect.x = columns * tile_size  # set the rectangle's x coordinate to be at the column * tile_size
                    img_rect.y = rows * tile_size  # set the rectangle's x coordinate to be at the row * tile_size
                    tile = (img, img_rect)  # create the tile object with the image and the rectangle in a tuple
                    self.tile_list.append(tile)  # append this tile to a list of tiles
                if tile == 16:
                    img = pygame.transform.scale(choco_cake_img, (tile_size, tile_size))  # scale the image to tile_size
                    img_rect = img.get_rect()  # create a collision rectangle around the image
                    img_rect.x = columns * tile_size  # set the rectangle's x coordinate to be at the column * tile_size
                    img_rect.y = rows * tile_size  # set the rectangle's x coordinate to be at the row * tile_size
                    tile = (img, img_rect)  # create the tile object with the image and the rectangle in a tuple
                    self.tile_list.append(tile)  # append this tile to a list of tiles
                if tile == 17:
                    img = pygame.transform.scale(blank_choco_cake_img, (tile_size, tile_size))  # scale the image to tile_size
                    img_rect = img.get_rect()  # create a collision rectangle around the image
                    img_rect.x = columns * tile_size  # set the rectangle's x coordinate to be at the column * tile_size
                    img_rect.y = rows * tile_size  # set the rectangle's x coordinate to be at the row * tile_size
                    tile = (img, img_rect)  # create the tile object with the image and the rectangle in a tuple
                    self.tile_list.append(tile)  # append this tile to a list of tiles
                if tile == 18:
                    blob = Enemy(columns * tile_size, rows * tile_size + 15, 'blue')
                    blob_group.add(blob)
                if tile == 19:
                    blob = Enemy(columns * tile_size, rows * tile_size + 15, 'purple')
                    blob_group.add(blob)
                if tile == 20:
                    blob = Enemy(columns * tile_size, rows * tile_size + 15, 'red')
                    blob_group.add(blob)
                if tile == 21:
                    platform = Platform(columns * tile_size, rows * tile_size, 1, 0, 'cake')
                    platform_group.add(platform)
                if tile == 22:
                    platform = Platform(columns * tile_size, rows * tile_size, 0, 1, 'cake')
                    platform_group.add(platform)
                columns += 1  # every iteration, increase columns by 1
            rows += 1  # every iteration, increase rows by 1

    def draw(self): # draw() function
        for tile in self.tile_list:  # iterate through all the tiles
            screen.blit(tile[0], tile[1])  # draw all the tiles and their collision rectangles


# Enemy class (slimes)
class Enemy(pygame.sprite.Sprite):  # identify this class as a sprite (pygame method)
    def __init__(self, x, y, color):  # create constructor function with coordinate parameters (x, y)
        pygame.sprite.Sprite.__init__(self)  # create a sprite (image) for every instance of this class

        if color == 'green':  # if the color parameter is 'green':
            self.img_left = loadify('images/slimeGreen.png')  # load green slime image
        elif color == 'blue':  # if the color parameter is 'blue':
            self.img_left = loadify('images/slimeBlue.png')  # load blue slime image
        elif color == 'purple':  # if the color parameter is 'purple':
            self.img_left = loadify('images/slimePurple.png')  # load purple slime image
        elif color == 'red':  # if the color parameter is 'red':
            self.img_left = loadify('images/slimeRed.png')  # load red slime image
        # flip the image across the y-axis and save as img_right
        self.img_right = pygame.transform.flip(self.img_left, True, False)
        self.image = self.img_right  # set default image facing right
        self.rect = self.image.get_rect()  # create collision rectangle around image
        self.rect.x = x  # set rectangle x position to equal the x position of the platform
        self.rect.y = y  # set rectangle y position to equal the y position of the platform
        self.move_direction = 1  # set move_direction to 1
        self.move_counter = 0  # reset move_counter to 0
        self.facing_right = 1  # set facing_right to 1 as the slime spawns facing_right

    def update(self):  # update slime movement function
        self.rect.x += self.move_direction  # update the rectangle position in the direction the slime is moving in
        self.move_counter += 1  # increase move_counter by 1
        if abs(self.move_counter) > 50:  # if the absolute value of the move_counter is greater than 50
            self.move_direction *= -1  # move_direction = move_direction times -1 (swaps direction)
            self.move_counter *= -1  # move_counter = move_counter times - 1 (swaps counter)
            if self.facing_right == 1:  # if facing_right == 1 (face right)
                self.facing_right = 0  # facing_right = 0 (face left)
            else:
                self.facing_right = 1  # facing_right = 1 (face right)
        if self.facing_right == 1:  # if facing_right == 1 (face right)
            self.image = self.img_right  # set the slime image to face right
        else:  # else (meaning facing_right == 0 (left))
            self.image = self.img_left  # set the slime image to face left


# class for platform object
class Platform(pygame.sprite.Sprite):  # identify this class as a sprite (pygame method)
    def __init__(self, x, y, move_x, move_y, material):  # create constructor function with coordinate parameters (x, y)
        pygame.sprite.Sprite.__init__(self)  # create a sprite (image) for every instance of this class
        if material == 'dirt':  # if the material parameter is 'dirt':
            img = loadify('images/platform.png')  # load the default platform image
        elif material == 'cake':  # if the material parameter is 'cake'
            img = loadify('images/choco_platform.png')  # load the chocolate platform image
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))  # scale the platform image
        self.rect = self.image.get_rect()  # create collision rectangle around image of platform
        self.rect.x = x  # set rectangle x position to equal the x position of the platform
        self.rect.y = y  # set rectangle y position to equal the y position of the platform
        self.move_direction = 1  # set the move direction to 1 (right)
        self.move_counter = 0  # set the move counter to 0
        self.move_x = move_x  # set the move_x variable inside this function equal to the parameter given
        self.move_y = move_y  # set the move_y variable inside this function equal to the parameter given

    def update(self):  # function to update the position of the platform
        self.rect.x += self.move_direction * self.move_x  # increase collision rectangle in x direction * pixels moved
        self.rect.y += self.move_direction * self.move_y  # increase collision rectangle in y direction * pixels moved
        self.move_counter += 1  # increase the move counter by 1
        if abs(self.move_counter) > 50:  # if the absolute value of the move_counter is above 50
            self.move_direction *= - 1  # set move_direction to move_direction * -1
            self.move_counter *= -1  # set move_counter to move_counter * -1


# class for ice platform
class IcePlatform(pygame.sprite.Sprite):  # identify this class as a sprite (pygame method)
    def __init__(self, x, y, move_x, move_y):  # create constructor function with coordinate parameters + movement
        pygame.sprite.Sprite.__init__(self)  # create a sprite (image) for every instance of this class
        img = loadify('images/ice_platform.png')  # load the ice platform image
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))  # scale the ice platform image
        self.rect = self.image.get_rect()  # create collision rectangle around image of ice platform
        self.rect.x = x  # set rectangle x position to equal the x position of the ice platform
        self.rect.y = y  # set rectangle y position to equal the y position of the ice platform
        self.move_direction = 1  # set the move direction to 1 (right)
        self.move_counter = 0  # set the move counter to 0
        self.move_x = move_x  # set the move_x variable inside this function equal to the parameter given
        self.move_y = move_y  # set the move_y variable inside this function equal to the parameter given

    def update(self):  # function to update the position of the ice platform
        self.rect.x += self.move_direction * self.move_x  # increase collision rectangle in x direction * pixels moved
        self.rect.y += self.move_direction * self.move_y  # increase collision rectangle in y direction * pixels moved
        self.move_counter += 1  # increase the move counter by 1
        if abs(self.move_counter) > 50:  # if the absolute value of the move_counter is above 50
            self.move_direction *= - 1  # set move_direction to move_direction * -1
            self.move_counter *= -1  # set move_counter to move_counter * -1


# class for lava
class Lava(pygame.sprite.Sprite):  # identify this class as a sprite (pygame method)
    def __init__(self, x, y):  # create constructor function with coordinate parameters (x, y)
        pygame.sprite.Sprite.__init__(self)  # create a sprite (image) for every instance of this class
        image = loadify('images/lava.png')  # load the lava image
        self.image = pygame.transform.scale(image, (tile_size, tile_size // 2))  # scale the lava image
        self.rect = self.image.get_rect()  # create a collision rectangle around the image
        self.rect.x = x  # set rectangle x position to equal the x position of the lava
        self.rect.y = y  # set rectangle y position to equal the y position of the lava


# class for water
class Water(pygame.sprite.Sprite):  # identify this class as a sprite (pygame method)
    def __init__(self, x, y):  # create constructor function with coordinate parameters (x, y)
        pygame.sprite.Sprite.__init__(self)  # create a sprite (image) for every instance of this class
        image = loadify('images/water.png')  # load the water image
        self.image = pygame.transform.scale(image, (tile_size, tile_size // 2))  # scale the water image
        self.rect = self.image.get_rect()  # create a collision rectangle around the image
        self.rect.x = x  # set rectangle x position to equal the x position of the water
        self.rect.y = y  # set rectangle y position to equal the y position of the water


# class for coins
class Coin(pygame.sprite.Sprite):  # identify this class as a sprite (pygame method)
    def __init__(self, x, y):  # create constructor function with coordinate parameters (x, y)
        pygame.sprite.Sprite.__init__(self)  # create a sprite (image) for every instance of this class
        image = loadify('images/coin.png')  # load the coin image
        self.image = pygame.transform.scale(image, (tile_size // 2, tile_size // 2))  # scale the coin image
        self.rect = self.image.get_rect()  # create a collision rectangle around the image
        self.rect.center = (x, y)  # set the rectangle's center point to be at the coordinates given in the parameters


# class for exit gates
class Exit(pygame.sprite.Sprite):  # identify this class as a sprite (pygame method)
    def __init__(self, x, y):  # create constructor function with coordinate parameters (x, y)
        pygame.sprite.Sprite.__init__(self)  # create a sprite (image) for every instance of this class
        image = loadify('images/exit.png')  # load the exit gate image
        self.image = pygame.transform.scale(image, (tile_size, int(tile_size * 1.5)))  # scale the exit door image
        self.rect = self.image.get_rect()  # create a collision rectangle around the image
        self.rect.x = x  # set rectangle x position to equal the x position of the exit gate
        self.rect.y = y  # set rectangle y position to equal the y position of the exit gate


player = Player(100, screen_height - 130)  # create player by calling the Player class with coordinates to spawn

# creating sprite groups for game objects
blob_group = pygame.sprite.Group()  # create a sprite group for slime enemies
platform_group = pygame.sprite.Group()  # create a sprite group for platforms
ice_platform_group = pygame.sprite.Group()  # create a sprite group for ice platforms
lava_group = pygame.sprite.Group()  # create a sprite group for lava
water_group = pygame.sprite.Group()  # create a sprite group for water
coin_group = pygame.sprite.Group()  # create a sprite group for coins
exit_group = pygame.sprite.Group()  # create a sprite group for exit gates

# loading data for the levels / world
if path.exists(f'level{level}_data'):  # verify if the data file for the level exists
    pickle_in = open(f'level{level}_data', 'rb')  # process the data file | 'rb' stands for read binary
    world_data = pickle.load(pickle_in)  # save the processed data in variable 'world_data'
world = World(world_data)  # process world_data through class World() and store in variable 'world'.

# create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)  # create restart button
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)  # create start button
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)  # create exit button

# Main Game Loop
run = True  # create variable run and assign it a boolean value of True

while run:  # while variable 'run' == True, run the main game loop

    clock.tick(frame_rate)  # use pygame .tick() method to limit the game at a specified frame_rate (60)

    # draw the background image(s)
    screen.blit(bg_img, (0, 0))  # blit the default background image (blue sky) onto the screen

    if level < 5:  # if level is less than 5
        screen.blit(forest_img, (0, 0))  # blit the forest background onto the screen
    elif level < 8:  # if level is less than 8
        screen.blit(arctic_img, (0, 0))  # blit the arctic background onto the screen
        change_music()  # call the change_music() function
    elif level < 10:  # if level is less than 10
        screen.blit(cake_img, (0, 0))  # blit the cake background onto the screen
        change_music()  # call the change_music() function
    elif level == 10:  # if level is equal to 10
        screen.blit(final_img, (0, 0))  # blit the final level background onto the screen
        change_music()  # call the change_music() function

    if main_menu == True:  # if variable main_menu is equal to True then run the following:
        if exit_button.draw():  # if the exit button is clicked
            run = False  # terminate the game loop, ending the program
        if start_button.draw():  # if the start button is clicked
            main_menu = False  # set variable main_menu to False which will get rid of the main menu screen
            display = 'unoriginal'  # set display to 'unoriginal' meaning the game updates the display after it starts

    else:  # else, meaning if the main_menu is not True, start the main part of the game loop
        world.draw()  # run the draw() function with the world_data stored inside variable 'world'

        if game_over == 0:  # if the game_over variable is 0, representing that the game is NOT over:
            blob_group.update()  # update the slime enemies positions on the screen as they move
            platform_group.update()  # update the platforms positions on the screen as they move
            ice_platform_group.update()  # update the ice platforms positions on the screen as they move

            # score updater which checks which coins have been collected
            if pygame.sprite.spritecollide(player, coin_group, True):  # if the player collides with a coin
                score += 1  # increase score by 1
                coin_fx.play()  # play the coin_fx sound effect

            draw_text('X ' + str(score), font_score, black, tile_size - 10, 10)  # draw the score counter in top left

        # drawing game objects to screen
        blob_group.draw(screen)  # draw the slime enemies to the screen
        platform_group.draw(screen)  # draw the platforms to the screen
        lava_group.draw(screen)  # draw the lava to the screen
        water_group.draw(screen)  # draw the water to the screen
        coin_group.draw(screen)  # draw the coins to the screen
        exit_group.draw(screen)  # draw the exit gates to the screen
        ice_platform_group.draw(screen)  # draw the ice platforms to the screen

        game_over = player.update(game_over)  # send the game_over variable to the .update() function in class Player()

        # when player dies
        if game_over == -1:  # when the player dies and the game temporarily pauses/ends
            if restart_button.draw():  # if the restart button is clicked
                world_data = []  # empty out the world_data list
                world = reset_level(level)  # reset the level and return the new world_data to variable world
                game_over = 0  # set game_over to 0, representing that the game is NOT over anymore
                score = 0  # reset player score to 0

        # when player finishes the level
        if game_over == 1:
            # go to next level
            level += 1
            if level <= max_levels:
                # clear the world of all data
                world_data = []  # empty out the world_data list
                world = reset_level(level)  # reset the level and return the new world_data to variable world
                game_over = 0  # set game_over to 0, representing that the game is NOT over anymore
            else:
                # draw winning message to the screen at the center of the screen
                draw_text(f'YOU WIN! SCORE: {score} ', font, blue, (screen_width // 2) - 280, screen_height // 2)
                # restart game
                if restart_button.draw():
                    level = 1  # set level to 1, resetting the game
                    world_data = []  # empty out the world_data list
                    world = reset_level(level)  # reset the level and return the new world_data to variable world
                    game_over = 0  # set the game_over variable to 0, representing that the game is NOT over anymore
                    score = 0  # reset score to 0
                    change_music()  # run function change_music()

    for event in pygame.event.get():  # loops through all the 'events' pygame supports
        if event.type == pygame.QUIT:  # if the x button in the top right of the game screen is pressed:
            run = False  # Set variable 'run' to False, terminating the main game loop.

    # coin beside the score for visual purposes
    if display != 'original':
        display_coin = loadify('images/coin.png')  # load and convert image 'coin' and store in new var 'display_coin'
        display_coin = pygame.transform.scale(display_coin, (tile_size // 2, tile_size // 2))  # scale the coin's image
        screen.blit(display_coin, (10, 15))  # blit the display_coin to the screen at coordinate (10, 15) from top-left.

    pygame.display.update()  # Updates the display with any new .blit() methods called

pygame.quit()  # Deactivates the initialized modules of the pygame library, terminating the program.
