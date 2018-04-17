# Team Members: Madeeha Anjum 1514645,

import pygame
import random
from threading import Timer
from BFS import *        # this is not good practice but we know whats in the file

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Initialize pygame and open new window
# WIDTH = 1900
# HEIGHT = height
WIDTH = 1000        # heigh and width of the window
HEIGHT = 1000
FPS = 30        # updateing frames per second


pygame.init()           # initialize pygame

screen = pygame.display.set_mode((WIDTH, HEIGHT))          # set size of window + tittle
pygame.display.set_caption("Box Head")

# load all sounds
bullet_sound = pygame.mixer.Sound('gun.wav')
zombie_sound = pygame.mixer.Sound('zombie.wav')
grunt_sound = pygame.mixer.Sound('gruntsound.wav')

pygame.mixer.init(frequency = 22050, size = -16, channels = 2, buffer = 4096)       # initialize sound

font_name = pygame.font.match_font('arial')     # chosing font

clock = pygame.time.Clock()
zombies_last_tick = pygame.time.get_ticks()
spawn_interval = 7000       # Zombies spawn every 7 seconds

# drawing and updating the life bar of player
def life_bar(surface, x, y, points):

    bar_length = 100
    bar_height = 10

    if points < 0:
        points = 0

    fill = (points / 100) * bar_length      # filling the bar depending on the points
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

# drawing and updating the health bar of player
def health_bar(surface, x, y, points):

    bar_length = 70
    bar_height = 10

    if points < 0:
        points = 0

    fill = (points / 100) * bar_length      # filling the bar depending on the points
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)



def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):       # location is an array
        pygame.sprite.Sprite.__init__(self)         # call Sprite initializer
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()       # pygame object position,left, top, width, height
        self.rect.left, self.rect.top = location

BackGround = Background('background.png', [0,0])


#******************************PLAYER SPRITE***********************************#
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width = 108.75      # height and width of the sprite player
        height = 150
        sheet = pygame.image.load('Character.png').convert_alpha()      # convert_alpha so the backround is transparent

        #  updating with the zombie player sprites(1-8) used
        self.image = pygame.transform.scale(sheet, (100, 150))      # the size of each of the zombies moving as a 100X150
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.centerx = random.randint(1, WIDTH)         # center of rectangle
        self.rect.bottom = random.randint(1, HEIGHT)        # screen_height  #pixels up from the bottom
        self.life = 100

        self.walkingDown = []            #1st image
        self.walkingLeft = []        #2nd imag
        self.walkingNorthEast = []       #3rd image
        self.walkingNorthWest = []       #4th image
        self.walkingRight = []          #5th image
        self.walkingSouthEast = []       #6th image
        self.walkingSouthWest = []       #7th image
        self.walkingUp = []         # 8th image (last)
        self.direction = 'R'

        sprite_sheet = SpriteSheet('Character.png')

        #Facing Down (1)
        image = sprite_sheet.get_image(0, 0, width, height)
        self.walkingDown.append(image)

        #Facing Left(2)
        image = sprite_sheet.get_image(1*width, 0, 100, height)
        self.walkingLeft.append(image)

        #Facing NorthEast(3)
        image = sprite_sheet.get_image(2*width, 0, 100, height)
        self.walkingNorthEast.append(image)

        #Facing NorthWest(4)
        image = sprite_sheet.get_image(3*width, 0, 100, height)
        self.walkingNorthWest.append(image)

        #Facing Right(5)
        image = sprite_sheet.get_image(4*width, 0, 100, height)
        self.walkingRight.append(image)

        #Facing SouthEast(6)
        image = sprite_sheet.get_image(5*width, 0, 100, height)
        self.walkingSouthEast.append(image)

        #Facing SouthWest(7)
        image = sprite_sheet.get_image(6*width, 0, 100, height)
        self.walkingSouthWest.append(image)

        #Facing Up(8)
        image = sprite_sheet.get_image(7*width, 0, 100, height)
        self.walkingUp.append(image)

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)
        pygame.mixer.Sound.play(bullet_sound)
        # bullet_sound.play

    def position(self):
        return [self.rect.x, self.rect.y]

    def update(self):
        # update the image depending on the direction
        if self.direction == "R":
            self.image = self.walkingRight[0]
        if self.direction == "L":
            self.image = self.walkingLeft[0]
        if self.direction == "U":
            self.image = self.walkingUp[0]
        if self.direction == "D":
            self.image = self.walkingDown[0]
        if self.direction == "UR":
            self.image = self.walkingNorthEast[0]
        if self.direction == "UL":
            self.image = self.walkingNorthWest[0]
        if self.direction == "DR":
            self.image = self.walkingSouthEast[0]
        if self.direction == "DL":
            self.image = self.walkingSouthWest[0]

        self.speedx = 0         # Need these to make sure
        self.speedy = 0         # Sprite stops moving on keyup

        keystate = pygame.key.get_pressed()
        # moving thr player coresponding to the speed
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
            self.direction = 'L'
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
            self.direction = 'R'
        if keystate[pygame.K_UP]:
            self.speedy = -10
            self.direction = 'U'
        if keystate[pygame.K_DOWN]:
            self.speedy = 10
            self.direction = 'D'

        if keystate[pygame.K_LEFT] and keystate[pygame.K_UP]:
            self.speedx = -10
            self.speedy = -10
            self.direction = 'UL'
        if keystate[pygame.K_RIGHT] and keystate[pygame.K_UP]:
            self.speedx = 10
            self.speedy = -10
            self.direction = 'UR'
        if keystate[pygame.K_DOWN] and keystate[pygame.K_LEFT]:
            self.speedy = 10
            self.speedx = -10
            self.direction = 'DL'
        if keystate[pygame.K_DOWN] and keystate[pygame.K_RIGHT]:
            self.speedy = 10
            self.speedx = 10
            self.direction = 'DR'

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # cases for when player hits the edge of the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5


# ******************************ZOMBIE SPRITE******************************#
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width = 108.75      # height and width of the sprite player
        height = 150

        self.sheet = pygame.image.load('White_Zombie.png').convert_alpha()          # so the backround is transparent
        self.image = pygame.transform.scale(self.sheet, (100, 150))          # the size of each of the zombies moving as a 100 by height
        self.image.set_colorkey(BLACK)      # extra  becase the images were aslready tranparent
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.width)
        self.direction = 'R'
        self.health = 100
        self.speedx = 0
        self.speedy = 0

        self.pathfinder = SEARCH()      # this is the BFS class
        self.path = [(0,0)]         #initalizing a path

        self.walkingDown = []       #1st image
        self.walkingLeft = []       #2nd imag
        self.walkingNorthEast = []      #3rd image
        self.walkingNorthWest = []      #4th image
        self.walkingRight = []          #5th image
        self.walkingSouthEast = []      #6th image
        self.walkingSouthWest = []      #7th image
        self.walkingUp = []      # 8th image (last)

        self.sprite_sheet = SpriteSheet('White_Zombie.png')         #intializing the sprite sheet class

        #Facing Down (1)
        image = self.sprite_sheet.get_image(0,0,width,height)
        self.walkingDown.append(image)

        #Facing Left(2)
        image = self.sprite_sheet.get_image(width,0,100,height)
        self.walkingLeft.append(image)

        #Facing NorthEast(3)
        image = self.sprite_sheet.get_image(2*width,0,100,height)
        self.walkingNorthEast.append(image)

        #Facing NorthWest(4)
        image = self.sprite_sheet.get_image(3*width,0,100,height)
        self.walkingNorthWest.append(image)

        #Facing Right(5)
        image = self.sprite_sheet.get_image(4*width,0,100,height)
        self.walkingRight.append(image)

        #Facing SouthEast(6)
        image = self.sprite_sheet.get_image(5*width,0,100,height)
        self.walkingSouthEast.append(image)

        #Facing SouthWest(7)
        image = self.sprite_sheet.get_image(6*width,0,100,height)
        self.walkingSouthWest.append(image)

        #Facing Up(8)
        image = self.sprite_sheet.get_image(7*width,0,100,height)
        self.walkingUp.append(image)

    def bleed(self):

        blood = Blood(self.rect.x, self.rect.centery)
        all_sprites.add(blood)
        bloods.add(blood)


    def update(self):

        if self.direction == "R":
            self.image = self.walkingRight[0]
        if self.direction == "L":
            self.image = self.walkingLeft[0]
        if self.direction == "U":
            self.image = self.walkingUp[0]
        if self.direction == "D":
            self.image = self.walkingDown[0]
        if self.direction == "UR":
            self.image = self.walkingNorthEast[0]
        if self.direction == "UL":
            self.image = self.walkingNorthWest[0]
        if self.direction == "DR":
            self.image = self.walkingSouthEast[0]
        if self.direction == "DL":
            self.image = self.walkingSouthWest[0]

        # Note: the zombies get a new path once they reach the end of the current path

        #if the path is empty: find a new path using bfs
        if len(self.path) <= 1:

            player_position = player.position()
            self.zombie_position = [self.rect.x, self.rect.y]
            # this returns a list of a path
            self.path = self.pathfinder.update_bfs(player_position, self.zombie_position)

        # if we have a path we want to follow the path
        elif len(self.path) > 1:

            prevgridcord_x, prevgridcord_y = self.path[0][0], self.path[0][1]

            self.path.remove(self.path[0])
            nextgridcord_x,nextgridcord_y = self.path[0][0], self.path[0][1]         # first zombie point

            # Zombies move acording to a grid so they dont travel diagonaly :(
            # this is a good search if there were walls

            if prevgridcord_x == nextgridcord_x and prevgridcord_y == nextgridcord_x:

                self.speedx = 0
                self.speedy = 0
                self.path.remove((nextgridcord_x, nextgridcord_y))       # always keep removing from the path once point is reached

            elif nextgridcord_x == prevgridcord_x and nextgridcord_y > prevgridcord_y:
                self.speedy = height_grid
                self.direction = 'D'
                self.speedx = 0

            elif nextgridcord_x == prevgridcord_x and nextgridcord_y < prevgridcord_y:
                self.speedy = -height_grid  # going up
                self.speedx = 0
                self.direction = 'U'

            elif nextgridcord_y == prevgridcord_y and nextgridcord_x > prevgridcord_x:
                self.speedx = width_grid   #moving right
                self.direction = 'R'
                self.speedy = 0

            elif nextgridcord_y == prevgridcord_y and nextgridcord_x < prevgridcord_x:
                self.speedx = -width_grid   # moving left
                self.speedy = 0
                self.direction = 'L'

            self.rect.x += self.speedx
            self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT -5:
            self.rect.bottom = HEIGHT -5


class SpriteSheet(object):
    def __init__(self, file_name):

        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()         # convert_alpha, so that the background is transparent

    def get_image(self, x, y, width, height):

        image = pygame.Surface([width, height], pygame.SRCALPHA)            # Use a transparent surface as the base image (pass pygame.SRCALPHA).
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))        # blit(source, dest, area=None, special_flags = 0)

        return image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        # bullet directions
        if player.direction == "R":
            self.speedy = 0
            self.speedx = 100
        if player.direction == "L":
            self.speedy = 0
            self.speedx = -100
        if player.direction == "U":
            self.speedy = -100
            self.speedx = 0
        if player.direction == "D":
            self.speedy = 100
            self.speedx = 0
        if player.direction == "UR":
            self.speedy = -100
            self.speedx = 100
        if player.direction == "UL":
            self.speedy = -100
            self.speedx = -100
        if player.direction == "DR":
            self.speedy = 100
            self.speedx = 100
        if player.direction == "DL":
            self.speedy = 100
            self.speedx = -100

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.kill()

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()


class Blood(pygame.sprite.Sprite):
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        blood_image = pygame.image.load('boxheadBlood.gif').convert_alpha()  # so the background is transparent
        self.image = pygame.transform.scale(blood_image, (100, 100))  # the size of each of the zombies moving as a 100X100
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x



# This GAME OVER screen also acts as a Starting Screen
def gameover_screen():
    screen.fill(BLACK)
    draw_text(screen, 'Box Head', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, 'Arrow keys move, Space to shoot', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, 'Press up key to begin', 18, WIDTH / 2, HEIGHT*3/4)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#************************ MAIN  GAME LOOP*******************************************#
game_over = True
running = True

while running:

    if game_over:       # this acts as a game over and a start
        score = 0
        gameover_screen()
        game_over = False   # restarting
        #***********INITALIZING ALL SPRITE GRUOPS *************#
        all_sprites = pygame.sprite.Group()
        zombies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bloods = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)

 # creating 4 zombies every 7 seconds

    zombies_current_tick = pygame.time.get_ticks()     # getting the current time ticks
    if zombies_current_tick - zombies_last_tick >= spawn_interval:
        zombies_last_tick = zombies_current_tick

        for i in range(4):
            z = Zombie()
            all_sprites.add(z)
            zombies.add(z)


    for event in pygame.event.get():        # event handaling
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # check for player shooting
            if event.key == pygame.K_SPACE:
                player.shoot()


    #******************UPDATING******************************#
    screen.fill(WHITE)
    screen.blit(BackGround.image, BackGround.rect)
    life_bar(screen, 5, 5, player.life)

    all_sprites.update()

    hits = pygame.sprite.groupcollide(zombies, bullets, False, True)        # checking if bullet hit zombie

    for hit in hits:        # iterating through to see if a zombie was hit
        score += 10
        pygame.mixer.Sound.play(zombie_sound)
        zombies.update()
        hit.bleed()     # if a zombie was hit it leaves behind blood and dies
        hit.kill()

    attacks = pygame.sprite.spritecollide(player, zombies, True)        # check if zombies attacks player

    for attack in attacks:
        pygame.mixer.Sound.play(grunt_sound)
        # the following makes the player move back when hit by the zombie
        if player.direction == 'U':
            player.speedy = 50
            player.speedx = 0

        if player.direction == 'D':
            player.speedy = -50
            player.speedx = 0

        if player.direction == 'R':
            player.speedx = -50
            player.speedy = 0

        if player.direction == 'L':
            player.speedx = 50
            player.speedy = 0

        player.rect.x += player.speedx
        player.rect.y += player.speedy

        player.life -= 25       # updaing the players life

        if player.life == 0:
            game_over = True

    # Draw / render
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    clock.tick(FPS)     # keep loop running at the right speed
    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
