import pygame
import random
from threading import Timer
from BFS import *

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Initialize pygame and open new window
# WIDTH = 1900
# HEIGHT = 1500
WIDTH = 1000
HEIGHT = 1000
FPS = 30 # frames per second

dam = True

pygame.init() #initialize pygame
pygame.mixer.init(frequency = 22050, size = -16, channels = 2, buffer = 4096) # initialize sound


screen = pygame.display.set_mode((WIDTH, HEIGHT)) # sets size of window
pygame.display.set_caption("Box Head")
clock = pygame.time.Clock()
'''
def damage():
    print('in damage function, dam = True')
    dam = True
'''
# health bar of player
def life_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


def health_bar(surface, x, y, pct):
    if pct < 0:
        pct = 0
    bar_length = 70
    bar_height = 10
    fill = (pct / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)


font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):  # location is an array
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file).convert()
        self.rect = self.image.get_rect()    # pygame object position,left, top, width, height
        self.rect.left, self.rect.top = location

BackGround = Background('background.png', [0,0])

# Sprite for the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        width = 108.75
        height = 150
        sheet = pygame.image.load('Character.png').convert_alpha()  #so the backround is transparent
        # scale(Surface, (width, height), DestSurface
        # this is constantly changing when the zombie image changes
        self.image = pygame.transform.scale(sheet, (100, 150))  # the size of each of the zombies moving as a 100 by 150
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.centerx = random.randint(1, WIDTH)    #center of rectangle
        self.rect.bottom = random.randint(1, HEIGHT)#screen_height  #pixels up from the bottom

        self.life = 100

        self.walkingDown = [] #1st image
        self.walkingLeft = [] #2nd imag
        self.walkingNorthEast = [] #3rd image
        self.walkingNorthWest = [] #4th image
        self.walkingRight = []  #5th image
        self.walkingSouthEast = [] #6th image
        self.walkingSouthWest = [] #7th image
        self.walkingUp = [] # 8th image (last)
        self.direction = 'R'

        sprite_sheet = SpriteSheet('Character.png')

        #Facing Down (1)
        # (corner locationx, corner locationy, width and height).
        image = sprite_sheet.get_image(0,0,100,150)
        self.walkingDown.append(image)

        #Facing Left(2)
        image = sprite_sheet.get_image(108.75,0,100,150)
        self.walkingLeft.append(image)

        #Facing NorthEast(3)
        image = sprite_sheet.get_image(217,.50,100,150)
        self.walkingNorthEast.append(image)

        #Facing NorthWest(4)
        image = sprite_sheet.get_image(326.25,0,100,150)
        self.walkingNorthWest.append(image)

        #Facing Right(5)
        # (corner locationx, corner locationy, width and height).
        image = sprite_sheet.get_image(435,0,100,150)
        self.walkingRight.append(image)

        #Facing SouthEast(6)
        image = sprite_sheet.get_image(543.75,0,100,150)
        self.walkingSouthEast.append(image)

        #Facing SouthWest(7)
        image = sprite_sheet.get_image(652.5,0,100,150)
        self.walkingSouthWest.append(image)

        #Facing Up(8)
        image = sprite_sheet.get_image(761.25,0,100,150)
        self.walkingUp.append(image)

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
            #i have added BFS now so thety move along a path
        self.speedx = 0 # Need these to make sure
        self.speedy = 0 # Sprite stops moving on keyup

        keystate = pygame.key.get_pressed()

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
            self.speedy =10
            self.speedx = 10
            self.direction = 'DR'

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        #Set edges for Width and Height
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT -5:
            self.rect.bottom = HEIGHT -5

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)
        pygame.mixer.Sound.play(bullet_sound)
        # bullet_sound.play

    def position(self):
        return [self.rect.x, self.rect.y]

class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load('White_Zombie.png').convert_alpha()  #so the backround is transparent
        self.image = pygame.transform.scale(self.sheet, (100, 150))  # the size of each of the zombies moving as a 100 by 150
        self.image.set_colorkey(BLACK) # extra  becase my images wewre aslready tranparent
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.width)
        self.speedx = 0
        self.speedy = 0
        self.pathfinder = SEARCH()  # this is the BFS
        self.walkingDown = [] #1st image
        self.walkingLeft = [] #2nd imag
        self.walkingNorthEast = [] #3rd image
        self.walkingNorthWest = [] #4th image
        self.walkingRight = []  #5th image
        self.walkingSouthEast = [] #6th image
        self.walkingSouthWest = [] #7th image
        self.walkingUp = [] # 8th image (last)
        self.direction = 'R'

        self.health = 100


        self.sprite_sheet = SpriteSheet('White_Zombie.png')
        #Facing Down (1)
        # (corner locationx, corner locationy, width and height).
        image = self.sprite_sheet.get_image(0,0,100,150)
        self.walkingDown.append(image)
        #Facing Left(2)
        image = self.sprite_sheet.get_image(108.75,0,100,150)
        self.walkingLeft.append(image)
        #Facing NorthEast(3)
        image = self.sprite_sheet.get_image(217,.50,100,150)
        self.walkingNorthEast.append(image)
        #Facing NorthWest(4)
        image = self.sprite_sheet.get_image(326.25,0,100,150)
        self.walkingNorthWest.append(image)
        #Facing Right(5)
        # (corner locationx, corner locationy, width and height).
        image = self.sprite_sheet.get_image(435,0,100,150)
        self.walkingRight.append(image)
        #Facing SouthEast(6)
        image = self.sprite_sheet.get_image(543.75,0,100,150)
        self.walkingSouthEast.append(image)
        #Facing SouthWest(7)
        image = self.sprite_sheet.get_image(652.5,0,100,150)
        self.walkingSouthWest.append(image)
        #Facing Up(8)
        image = self.sprite_sheet.get_image(761.25,0,100,150)
        self.walkingUp.append(image)

        self.path = [(0,0)]
        # self.zombie_position = [self.rect.x, self.rect.y]


    def update(self):
        # self.rect.x += self.speedx
        # self.rect.y += self.speedy

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
        if len(self.path) <= 1:
            # print("len")
            # print(len(self.path))
            player_position = player.position()
            self.zombie_position = [self.rect.x, self.rect.y]
            # print("player position, " ,player_position)
            # print(player_position)
            self.path = self.pathfinder.update_bfs(player_position, self.zombie_position)  # this returns a list of a path
            #Collition****************
            # print(" my",self.path)


        elif len(self.path) > 1:
            # print(">1")
            x,y = self.path[0][0], self.path[0][1]
            # print("x and y:, ",x,y)
            #x,y = self.zombie_position
            self.path.remove(self.path[0])
            nx,ny = self.path[0][0], self.path[0][1]   #first zombie point
            # print("nx and ny:, ",nx,ny)
            # self.end = 0 #* deal with collition if it collides do something else end = 1

            #Zombies move acording to a grid so they dont travel diagonaly :(
            #but this is a good if there are walls which i will add later (maybe)

            if x == nx and y == nx:
                # print(1)
                self.speedx = 0
                self.speedy = 0
                self.path.remove((nx,ny))
                # print(self.path)
            elif nx == x and ny > y:
                # print(2)
                self.speedy = height_grid
                self.direction = 'D'
                self.speedx = 0

            elif nx == x and ny < y:
                #print(3)
                self.speedy = -height_grid  # going up
                self.speedx = 0
                self.direction = 'U'

            elif ny == y and nx > x:
                # print(4)
                self.speedx = width_grid   #movinf right
                self.direction = 'R'
                self.speedy = 0

            elif ny == y and nx < x:
                # print(5)
                self.speedx = -width_grid   # moving left
                self.speedy = 0
                self.direction = 'L'

            # print("self.rect.x,self.rect.xy = ", self.rect.x,self.rect.y)
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

    def bleed(self):
        blood = Blood(self.rect.x, self.rect.centery)
        all_sprites.add(blood)
        bloods.add(blood)


class SpriteSheet(object):
    def __init__(self, file_name):
        # You have to call `convert_alpha`, so that the background of
        # the surface is transparent.
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def get_image(self, x, y, width, height):
        # Use a transparent surface as the base image (pass pygame.SRCALPHA).
        image = pygame.Surface([width, height], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # blit(source, dest, area=None, special_flags = 0)
        return image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
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
        sheet = pygame.image.load('boxheadBlood.gif').convert_alpha()  # so the background is transparent
        # scale(Surface, (width, height), DestSurface
        # this is constantly changing when the zombie image changes
        self.image = pygame.transform.scale(sheet, (100, 150))  # the size of each of the zombies moving as a 100 by 150
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x


def gameover_screen():
    screen.fill(BLACK)
    draw_text(screen, 'Box Head', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, 'Arrow keys move, Space to shoot', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, 'Press a key to begin', 18, WIDTH / 2, HEIGHT*3/4)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# load all sounds
bullet_sound = pygame.mixer.Sound('gun.wav')
zombie_sound = pygame.mixer.Sound('zombie.wav')
grunt_sound = pygame.mixer.Sound('gruntsound.wav')

all_sprites = pygame.sprite.Group()
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bloods = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(4):
    z = Zombie()
    all_sprites.add(z)
    zombies.add(z)

# Game loop
game_over = True
running = True
while running:
    if game_over:
        score = 0
        gameover_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        zombies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bloods = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        for i in range(4):
            z = Zombie()
            all_sprites.add(z)
            zombies.add(z)

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    screen.fill(WHITE)
    screen.blit(BackGround.image, BackGround.rect)
    life_bar(screen, 5, 5, player.life)

    all_sprites.update()
    # check if bullet hit zombie, returns list
    hits = pygame.sprite.groupcollide(zombies, bullets, False, True)
    for hit in hits:
        score += 10
        pygame.mixer.Sound.play(zombie_sound)

        if score < 50:
            zombies.update()
            hit.bleed()
            hit.kill()
            z = Zombie()
            all_sprites.add(z)
            zombies.add(z)

        elif score <= 100:
            for i in range(2):
                zombies.update()
                hit.bleed()
                hit.kill()
                z = Zombie()
                all_sprites.add(z)
                zombies.add(z)

        elif score <= 150:
            for i in range(3):
                zombies.update()
                hit.bleed()
                hit.kill()
                z = Zombie()
                all_sprites.add(z)
                zombies.add(z)


  # check if zombies attacks player, returns list

    attacks = pygame.sprite.spritecollide(player, zombies, True)
    for attack in attacks:
        pygame.mixer.Sound.play(grunt_sound)
        if player.direction == 'U':
            player.speedy = 50
            player.speedx = 0
            print('here')
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
        player.life -= 25
        if player.life == 0:
            #running = False
            game_over = True

    # Draw / render
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)

    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
