from pygame import *
from random import randint

# Увімкнули текст та звуки
font.init()
mixer.init()
main_font = font.SysFont('Arial', 72)
txt_loose = main_font.render('You loose!', True, (255, 0, 0))
txt_win = main_font.render('You win!', True, (0, 255, 0))
score = 0
# Базові змінні
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
GAME_RUN, GAME_FINISHED = True, False
FPS = 60
WINDOW = display.set_mode((WINDOW_WIDTH + 350, WINDOW_HEIGHT))
display.set_caption("Арканоїд")
CLOCK = time.Clock()
mixer.music.load("music.mp3")
mixer.music.play(loops=-1)
mixer.music.set_volume(0.1)
# Базовий клас для спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, img, position, size, speed):
        super().__init__()
        # Створюємо зображення спрайта (властивість self.image).
        # transform.scale() - змінити розміри
        # image.load() - завантажити зображення
        self.image = transform.scale(
            image.load(img),
            size
        )
        # Отримали хітбокс зображення спрайта self.image
        self.rect = self.image.get_rect()
        # Ставимо хітбокс на початкові координати, томущо картинка бігає за хітбоксом, а не навпаки
        self.rect.x, self.rect.y = position
        
        # Зберегаємо інші властивості
        self.width, self.height = size
        self.speed = speed
    def draw(self):
        # Малюємо зображення self.image на координатах хітбокса
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))
#Класс для читов
class GGG(sprite.Sprite):
    def __init__(self, mr):
        super().__init__()
        self.mr = mr
# Класс для меню
class in_menu(sprite.Sprite):
    def __init__(self, img, position, size,  m):
        super().__init__()
        self.m = m
        self.image = transform.scale(
            image.load(img),
            size
        )
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.width, self.height = size
    def draw(self):
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, img, position, size, speed):
        super().__init__(img, position, size, speed)
        
        self.is_big = False
        self.is_big_timer = FPS * 5
        self.zamedlut_mac = False
        self.zamedlut_mac_timer = FPS * 5


        
    # Логіка спрайту
    def update(self):
        keys = key.get_pressed()
        if (keys[K_a] or keys[K_LEFT]) and self.rect.x > 0:
            self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < WINDOW_WIDTH - self.width:
            self.rect.x += self.speed
        
        if self.is_big:
            if self.is_big_timer > 0:
                self.is_big_timer -= 1
            else:
                self.is_big_timer = FPS * 5
                self.is_big = False
                old_pos_y = player.rect.y
                self.image = transform.scale(
                    self.image,
                    (150, player.height)
                )
                player.width = 150
                player.rect = player.image.get_rect()
                player.rect.y = old_pos_y
        
        if self.zamedlut_mac:
            if self.zamedlut_mac_timer > 0:
                self.zamedlut_mac_timer -= 1
            else:
                old_pos_x, old_pos_y = ball.rect.x, ball.rect.y
                self.zamedlut_mac_timer = FPS * 5
                self.zamedlut_mac = False
                ball.image = transform.scale(
                    ball.image,
                    (30, 30)
                )
                ball.width, ball.height = 30, 30
                ball.rect = ball.image.get_rect()
                ball.rect.x, ball.rect.y = old_pos_x, old_pos_y

                
                    
class Enemy(GameSprite):
    # Логіка спрайту
    def update(self):
            pass
class Ball(GameSprite):
    # Логіка спрайту
    x_speed, y_speed = 3, 3
    def update(self):
        global score, GAME_FINISHED
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.x >= WINDOW_WIDTH:
            self.rect.x = WINDOW_WIDTH / 2
            self.rect.y = WINDOW_HEIGHT / 2

        if self.rect.x <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.x_speed += -1
        if self.rect.y <= 0:
            self.y_speed *= -1
        if sprite.collide_rect(self, player):
            self.y_speed *= -1
        if sprite.collide_rect(self, stenka_l):
            self.x_speed *= -1
        if sprite.collide_rect(self, stenka_r):
            self.x_speed *= -1
        if sprite.collide_rect(self, stenka_lower):
            GAME_FINISHED = True
        for enemy in enemys:
            if sprite.collide_rect(self, enemy):
                
                need_bonus = randint(1, 2)
                if need_bonus == 1:
                    new_bonus = Bonus(
                        img="bonus.png",
                        position=(enemy.rect.x, enemy.rect.y),
                        size=(32, 32),
                        speed=5
                    )
                    bonuses.append(new_bonus)
                    
                self.y_speed *= -1
                enemys.remove(enemy)
                score += 1
                if len(enemys) == 0:
                    GAME_FINISHED = True
        #Читы
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.x = (WINDOW_WIDTH / 2)
            self.rect.y = (WINDOW_HEIGHT / 2)
        #Читы
        if keys[K_e] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_r] and self.rect.x < WINDOW_WIDTH - self.width:
            self.rect.x += self.speed

class Bonus(GameSprite):
    def update(self):
        global timer
        
        self.rect.y += self.speed
        
        if sprite.collide_rect(self, player):
            bonus_type = randint(1, 3)
            
            if bonus_type == 1:
                old_pos_y = player.rect.y
                player.image = transform.scale(
                    player.image,
                    (WINDOW_WIDTH, player.height)
                )
                player.width = WINDOW_WIDTH
                player.rect = player.image.get_rect()
                player.rect.y = old_pos_y
                player.is_big = True
            
            if bonus_type == 2:
                old_pos_x, old_pos_y = ball.rect.x, ball.rect.y
                ball.image = transform.scale(
                    ball.image,
                    (100, 100)
                )
                ball.width, ball.height = 100, 100
                ball.rect = ball.image.get_rect()
                ball.rect.x, ball.rect.y = old_pos_x, old_pos_y
                player.zamedlut_mac = True
                
            if bonus_type == 3:
                timer += FPS * 10
                
            bonuses.remove(self)

#Класс для читов
rr = GGG(mr = False)
menu = in_menu(
    img = 'menu.jpg',
    position = (0, 0),
    size = (WINDOW_WIDTH + 350, WINDOW_HEIGHT),
    m = True
)
#Права стінка
stenka_r = GameSprite(
    img = 'stenka.png',
    position = (WINDOW_WIDTH - 10, 0),
    size = (10,  WINDOW_HEIGHT),
    speed = 0
)   
#Ліва стінка
stenka_l = GameSprite(
    img = 'stenka.png',
    position = (-10, 0),
    size = (10,  WINDOW_HEIGHT),
    speed = 0
)
#Стінка що знаходиться внизу
stenka_lower = GameSprite(
    img = 'stenka.png',
    position = (0, WINDOW_HEIGHT - 10),
    size = (WINDOW_WIDTH, 10),
    speed = 0
)
# Створення спрайтів
background = GameSprite(
    img="background.jpg",
    position=(0, 0),
    size=(WINDOW_WIDTH + 350, WINDOW_HEIGHT),
    speed=0
)
player = Player(
    img="player.png",
    position=(WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT - 150),
    size=(150, 25),
    speed=10
)
ball = Ball(
    img="ball.png",
    position=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
    size=(30, 30),
    speed=8    
)

bonuses = []
enemys = []
enemys_count = 50

def restart():
    global score, timer, GAME_FINISHED
    score = 0
    timer = FPS * 150
    ball.rect.x, ball.rect.y = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
    ball.x_speed, ball.y_speed = 3, 3
    player.rect.x, player.rect.y = WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT - 150
    GAME_FINISHED = False
    s1()
def s1():
    enemys.clear()
    column, row = 1, 1
    enemy_x, enemy_y = 0, 0
    enemy_width, enemy_heiight = 50, 15
    enemys_count = 50
    global score, GAME_FINISHED, timer
    timer = FPS * 150
    score = 0
    ball.x_speed, ball.y_speed = 3, 3
    for i in range(enemys_count):
        enemy_x = (enemy_width + 5) * column
        enemy_y = (enemy_heiight + 5) * row
        if enemy_x < WINDOW_WIDTH:
            new_enemy = Enemy(
                img = 'enemy.png',
                position=(enemy_x, enemy_y),
                size = (enemy_width, enemy_heiight),
                speed = 0
            )
            enemys.append(new_enemy)
            column += 1
        else:
            column = 1
            row += 1
            enemy_y = (enemy_heiight + 5) * row
def s2():
    enemys.clear()
    column, row = 1, 1
    enemy_x, enemy_y = 0, 0
    enemy_width, enemy_heiight = 50, 15
    enemys_count = 75
    global score, GAME_FINISHED, timer
    timer = FPS * 150
    score = 0
    ball.x_speed, ball.y_speed = 6, 6
    for i in range(enemys_count):
        enemy_x = (enemy_width + 5) * column
        enemy_y = (enemy_heiight + 5) * row

        if enemy_x < WINDOW_WIDTH:
            new_enemy = Enemy(
                img = 'enemy2.png',
                position=(enemy_x, enemy_y),
                size = (enemy_width, enemy_heiight),
                speed = 0
            )
            enemys.append(new_enemy)
            column += 1
        else:
            column = 1
            row += 1
            enemy_y = (enemy_heiight + 5) * row
def s3():
    enemys.clear()
    column, row = 1, 1
    enemy_x, enemy_y = 0, 0
    enemy_width, enemy_heiight = 50, 15
    enemys_count = 100
    global score, GAME_FINISHED, timer
    timer = FPS * 150
    score = 0
    ball.x_speed, ball.y_speed = 9, 9

    for i in range(enemys_count):
        enemy_x = (enemy_width + 5) * column
        enemy_y = (enemy_heiight + 5) * row

        if enemy_x < WINDOW_WIDTH:
            new_enemy = Enemy(
                img = 'enemy3.png',
                position=(enemy_x, enemy_y),
                size = (enemy_width, enemy_heiight),
                speed = 0
            )
            enemys.append(new_enemy)
            column += 1
        else:
            column = 1
            row += 1
            enemy_y = (enemy_heiight + 5) * row
#Таймер
timer = FPS * 150

s1()
# python Arcanoid.py
while GAME_RUN:
    for ev in event.get():
        if ev.type == QUIT:
            GAME_RUN = False
        if ev.type == KEYUP:
            if ev.key == K_q:
                menu.m = not menu.m
        #Читы
        if ev.type == KEYUP:
            if ev.key == K_w:
                rr.mr = not rr.mr
        #Читы
        if ev.type == KEYUP:
            if ev.key == K_p:
                enemys.clear()
                GAME_FINISHED = True
                background.draw()
                WINDOW.blit(txt_win, (WINDOW_WIDTH / 2 + 100 - txt_win.get_width() / 2, WINDOW_HEIGHT / 2 - txt_win.get_height() / 2))
        if ev.type == KEYUP:
            if ev.key == K_1:
                s1()
            if ev.key == K_2:
                s2()
            if ev.key == K_3:
                s3()
        if ev.type == KEYUP:
             if ev.key == K_9:
                restart()
        if ev.type == KEYUP:
             if ev.key == K_8:
                exit()
    if menu.m:
        menu.draw()
        menu.update()
    else:
        if not GAME_FINISHED:
            background.draw()
            player.draw()
            ball.draw()
            for enemy in enemys:
                enemy.draw()
            for bonus in bonuses:
                bonus.draw()
                bonus.update()
            stenka_l.draw()
            stenka_r.draw()
            stenka_lower.draw()
            menu.update()
            player.update()
            ball.update()
            if timer > 0:
                timer -= 1
            else:
                GAME_FINISHED = True
                WINDOW.blit(txt_loose, (WINDOW_WIDTH / 2 - txt_loose.get_width() / 2, WINDOW_HEIGHT / 2  - txt_loose.get_height() / 2))
            txt_score = main_font.render('Score= ' + str(score), True, (0, 255, 0))
            WINDOW.blit(txt_score, (WINDOW_WIDTH + 160 - txt_score.get_width() / 2, WINDOW_HEIGHT - 550 - txt_score.get_height() / 2))
            txt_time = main_font.render('Time= ' + str(round(timer / 60)), True, (0, 255, 0))
            WINDOW.blit(txt_time, (WINDOW_WIDTH + 340 - txt_time.get_width(), 150))
        else:
            if len(enemys) == 0:
                background.draw()
                WINDOW.blit(txt_win, (WINDOW_WIDTH / 2 + 100 - txt_win.get_width() / 2, WINDOW_HEIGHT / 2 - txt_win.get_height() / 2))
            else:
                background.draw()
                WINDOW.blit(txt_loose, (WINDOW_WIDTH / 2 - txt_loose.get_width() / 2, WINDOW_HEIGHT / 2 - txt_loose.get_height() / 2))
    display.update()
    CLOCK.tick(FPS)