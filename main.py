import pygame
import random
import os


FPS = 60
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

global game_start_time
global score
global highest_score
global check_time
global chance

# initialize the game and make the screen
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("石帥華做的遊戲")
clock = pygame.time.Clock()
highest_score = 0
check_time = 0


# load image
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
ending_backgroung_img = pygame.image.load(os.path.join("img", "daddy.png")).convert()
bullet_img_first = pygame.image.load(os.path.join("img", "bullet.png")).convert()
player_img = pygame.image.load(os.path.join("img", "dad1.png")).convert()
dad_life_img = pygame.image.load(os.path.join("img", "dad_life.png")).convert()
player_mini_img = pygame.transform.scale(dad_life_img, (50*1.5,67.5*1.5))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.transform.scale(bullet_img_first, (13, 54*1.5))
pygame.display.set_icon(dad_life_img)
player_imgs = []
for i in range(3):
    img = pygame.image.load(os.path.join("img", f"dad{i}.png")).convert()
    img = pygame.transform.scale(img, (77, 137))
    img.set_colorkey(BLACK)
    player_imgs.append(img)

for i in range(3):
    img = pygame.transform.flip(player_imgs[i], True, False)
    player_imgs.append(img)

rock_imgs = []
for i in range(7):
    ball_size = random.randrange(40, 110)
    ball_img = pygame.image.load(os.path.join("img", f"ball{i}.png")).convert()
    if i ==2:
        rock_imgs.append(pygame.transform.scale(ball_img, (130, 130)))
    else:
        rock_imgs.append(pygame.transform.scale(ball_img, (ball_size, ball_size)))



expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)

power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()
# load music
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.4)

#  choose font
font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

# make new rock
def new_rock():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# display player's health
def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)  # 2是外框的像素

# display player's lives
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 80 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_level(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, ORANGE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "老爸戰爭", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "← →移動老爸 空白鍵發射", 22, WIDTH / 2, HEIGHT / 2)
    screen.blit(power_imgs['shield'], (WIDTH / 2-60, HEIGHT / 2+50))
    draw_text(screen, ": 補血", 22, WIDTH / 2, HEIGHT / 2+50)
    screen.blit(power_imgs['gun'], (WIDTH / 2-90, HEIGHT / 2+100))
    draw_text(screen, ": 子彈double", 22, WIDTH / 2, HEIGHT / 2+100)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)  # The number of times this loop can be executed in one second
        # get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

def draw_end():
    waiting = True
    while waiting:
        screen.blit(background_img, (0, 0))
        screen.blit(ending_backgroung_img, (237, 100))
        draw_text(screen, "父親節快樂!", 64, WIDTH / 2, HEIGHT / 5)
        draw_text(screen, "重新開始: 按 a", 24, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, f"你的分數是:{score}", 24, WIDTH/2, HEIGHT / 2 +30)
        global highest_score
        if score >= highest_score:
            highest_score = score
        draw_text(screen, f"最高分是:{highest_score}", 24, WIDTH / 2, HEIGHT / 2 + 60)
        pygame.display.update()
        clock.tick(FPS)  # The number of times this loop can be executed in one second
        # get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    waiting = False
                    return False
# define the characters in the game
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_imgs[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 將其定位，框起來
        self.radius = 19.5+26
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT - 58
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
        self.lastTick = pygame.time.get_ticks()
        self.i = 0
        self.trans = 0
        self.game_time = pygame.time.get_ticks()
        self.level = 1

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.lastTick > 100:
            self.i += 1
            self.image = player_imgs[self.i%3+self.trans]
            self.lastTick = now

        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.centery = HEIGHT -58

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.trans = 0
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.trans = 3
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if now - self.game_time >= 5000 and now - self.game_time < 10000:
            self.level = 2
        if now - self.game_time >= 10000 and now - self.game_time < 15000:
            self.level = 3
        if now - self.game_time >= 15000 and now - self.game_time < 20000:
            self.level = 4
        if now - self.game_time >= 20000:
            self.level = 5


    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()  # 將其定位，框起來
        self.radius = int(self.rect.width  / 2)
        #test
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-5, 5)
        self.game_time = 0
        self.level_time = pygame.time.get_ticks()

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image  = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center


    def update(self):
        now = pygame.time.get_ticks()
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)
            if now - game_start_time >= 5000 and now - game_start_time < 10000:
                self.speedy = random.randrange(5, 15)
                self.speedx = random.randrange(-3, 3)
            if now - game_start_time >= 10000 and now - game_start_time < 15000:
                self.speedy = random.randrange(25, 30)
                self.speedx = random.randrange(-4, 4)
            if now - game_start_time >= 15000 and now - game_start_time < 20000:
                self.speedy = random.randrange(40, 50)
                self.speedx = random.randrange(-5, 5)
            if now - game_start_time >= 20000:
                self.speedy = random.randrange(65, 75)
                self.speedx = random.randrange(-8, 8)
            global check_time
            check_time = now - game_start_time



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 將其定位，框起來
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()  # 將其定位，框起來
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame  == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center


class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()  # 將其定位，框起來
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()



# turn the music on (repeat)
pygame.mixer.music.play(-1)

# game loop
show_init = True
running = True
show_end = False
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        game_start_time = pygame.time.get_ticks()
        show_init = False
        # define sprite
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        # Reset the rock
        for i in range(8):
            new_rock()
        score = 0

    if show_end:
        show_end = False
        close = draw_end()
        if close:
            break
        # define sprite
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        player.level = 1
        all_sprites.add(player)
        # Reset the rock
        for i in range(8):
            new_rock()
        score = 0
        game_start_time = pygame.time.get_ticks()
    clock.tick(FPS)  # The number of times this loop can be executed in one second
    # get input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # update the game
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if check_time>20000:
            if random.random() > 0.95:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powers.add(pow)
        else:
            if random.random() > 0.9:
                pow = Power(hit.rect.center)
                all_sprites.add(pow)
                powers.add(pow)
        new_rock()

    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)

    for hit in hits:
        new_rock()
        player.health -= 35 #hit.radius*2(原設定值)
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            die = Explosion(player.rect.center, 'player')
            all_sprites.add(die)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()

    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            shield_sound.play()
            player.health += 35
            if player.health > 100:
                player.health = 100
        elif hit.type == 'gun':
            gun_sound.play()
            player.gunup()


    if player.lives == 0 and not (die.alive()):
        show_end = True
        # show_init = True

    # screen display
    screen.fill(BLACK)  # (R, G, B)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, "score: " + str(score), 20, WIDTH/2, 10)
    if player.level <=4:
        draw_level(screen,"level: " + str(player.level),20, WIDTH/2-100, 10)
    if player.level == 5:
        draw_level(screen, "level: impossible", 25, WIDTH / 2 , 70)
    draw_text(screen, "blood: ", 22, WIDTH-200, 118)
    draw_health(screen, player.health, WIDTH-160, 130)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 250, 10)
    pygame.display.update()

pygame.quit()
