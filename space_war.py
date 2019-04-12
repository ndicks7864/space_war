# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1800
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)
bg = pygame.image.load("alien_assets/images/space_background.jpg").convert_alpha()


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("alien_assets/fonts/star_wars/star_jedi_rounded.ttf", 76)
FONT_SCORE = pygame.font.Font("alien_assets/fonts/star_wars/star_jedi_rounded.ttf", 16)

# Images
ship_img = pygame.image.load('alien_assets/images/shipBeige_manned.png').convert_alpha()
laser_img = pygame.image.load('alien_assets/images/laserBeige1.png').convert_alpha() 
enemy_img = pygame.image.load('alien_assets/images/shipYellow_manned.png').convert_alpha()
bomb_img = pygame.image.load('alien_assets/images/laserYellowTranR.png').convert_alpha()
sheild_img = pygame.image.load('alien_assets/images/dome.png').convert_alpha()


# Sounds
pygame.mixer.music.load("alien_assets/sounds/star_wars.wav")
EXPLOSION = pygame.mixer.Sound('alien_assets/sounds/explosion.ogg')
LASER = pygame.mixer.Sound('alien_assets/sounds/shoot.wav')


# Stages
START = 0
PLAYING = 1
WIN = 2
LOSE = 3


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def move_down(self):
        self.rect.y += self.speed
        
    def move_up(self):
        self.rect.y -= self.speed

    def shoot(self):
        print("PEW!")
        LASER.play()

        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.left
        laser.rect.centery = self.rect.centery
        lasers.add(laser)
        
    def update(self):
        '''check screen edges'''
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.left < 800:
            self.rect.left = 800
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        '''check bombs'''
        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)
        if len(hit_list) > 0:
            player.life -= 1
            player.score -= 2
            EXPLOSION.play()
            print("Oof")

        if player.life == 0:
            self.kill()
            stage = LOSE

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def drop_bomb(self):
        print("Bwwap!")

        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.right
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        mob_list = mobs.sprites()
        
        if len(hit_list) > 0:
            player.score += 1
            EXPLOSION.play()
            self.kill()
            
        if self.rect.left >= WIDTH:
            hits_edge = True

            if hits_edge:
                player.score -= 2
                self.kill()

        #if len(mob_list) < 10 and len(mob_list) > 6:
            #self.speed = 5

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 3

    def update(self):
        self.rect.x += self.speed

        if self.rect.left > WIDTH:
            self.kill()

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 1
        self.bomb_rate = 60
        self.moving_right = True

    def move(self):
        for m in mobs:
            m.rect.x += self.speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()

    def update(self):
        mob_list = mobs.sprites()
        
        self.move()
        self.choose_bomber()

        if len(mob_list) == 0:
            stage = WIN

# Game helper functions
def show_title_screen():
    title_text = FONT_XL.render("The Alien invasion!", 1, WHITE)
    w = title_text.get_width()
    h = title_text.get_height()
    screen.blit(title_text, [WIDTH/2 - w/2, HEIGHT/2 - h/2])

def draw_background():
    screen.blit(bg, [0,0])

def draw_score():
    score_txt1 = FONT_SCORE.render(str(player.score), 1, WHITE)
    screen.blit(score_txt1, [10,15])

def draw_life():
    if player.life == 5:
        pygame.draw.rect(screen, WHITE, [1590, 15, 200, 25])
        pygame.draw.rect(screen, GREEN, [1592, 17, 196, 21])
    elif player.life == 4:
        pygame.draw.rect(screen, WHITE, [1590, 15, 200, 25])
        pygame.draw.rect(screen, GREEN, [1592, 17, 157, 21])
    elif player.life == 3:
        pygame.draw.rect(screen, WHITE, [1590, 15, 200, 25])
        pygame.draw.rect(screen, YELLOW, [1592, 17, 118, 21])
    elif player.life == 2:
        pygame.draw.rect(screen, WHITE, [1590, 15, 200, 25])
        pygame.draw.rect(screen, YELLOW, [1592, 17, 79, 21])
    elif player.life == 1:
        pygame.draw.rect(screen, WHITE, [1590, 15, 200, 25])
        pygame.draw.rect(screen, RED, [1592, 17, 40, 21])
    elif player.life == 0:
        pygame.draw.rect(screen, WHITE, [1590, 15, 200, 25])
        
    score_txt1 = FONT_SCORE.render(str(player.life), 1, WHITE)
    screen.blit(score_txt1, [1080,15])

def draw_end():
    title_text = FONT_XL.render("Game over", 1, WHITE)
    w = title_text.get_width()
    h = title_text.get_height()
    screen.blit(title_text, [WIDTH/2 - w/2, HEIGHT/2 - h/2])
    title_text = FONT_SCORE.render("press space to restart", 1, WHITE)
    w = title_text.get_width()
    h = title_text.get_height()
    screen.blit(title_text, [WIDTH/2 - w/2, 650])

def show_stats(player):
    pass

def check_end():
    global stage

    if len(mobs) == 0:
        stage = WIN
    elif len(player) == 0:
        stage = LOSE

def setup():
    global stage, done
    global player, ship, lasers, mobs, fleet, bombs
    global score
    
    ''' Make game objects '''
    ship = Ship(1670, 300, ship_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0
    player.life = 5

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    mob1 = Mob(20, 30, enemy_img)
    mob2 = Mob(20, 160, enemy_img)
    mob3 = Mob(20, 290, enemy_img)
    mob4 = Mob(20, 420, enemy_img)
    mob5 = Mob(20, 550, enemy_img)
    mob6 = Mob(170, 105, enemy_img)
    mob7 = Mob(170, 235, enemy_img)
    mob8 = Mob(170, 365, enemy_img)
    mob9 = Mob(170, 495, enemy_img)
    mob10 = Mob(320, 30, enemy_img)
    mob11= Mob(320, 160, enemy_img)
    mob12= Mob(320, 290, enemy_img)
    mob13= Mob(320, 420, enemy_img)
    mob14= Mob(320, 550, enemy_img)

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10,
             mob11, mob12, mob13, mob14)

    fleet = Fleet(mobs)
    
    ''' set stage '''
    stage = START
    done = False

    '''score'''
    score = 0

    
# Game loop
pygame.mixer.music.play(-1)

setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
                
            elif stage == WIN or LOSE:
                if event.key == pygame.K_SPACE:
                    setup()
                

    pressed = pygame.key.get_pressed()
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        if pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()

        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()

        check_end()
        
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    draw_background()
    mobs.draw(screen)
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    draw_score()
    draw_life()

    
    if stage == START:
        show_title_screen()
    elif stage == WIN:
        draw_end()
    elif stage == LOSE:
        draw_end()

        
    # Update screen (Actually draw the picture in the window.)
    #screen.blit(bg, [0,0])
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
