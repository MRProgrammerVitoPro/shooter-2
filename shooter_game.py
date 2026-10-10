
#TODO Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load("D:/Python/Shooter_#2/space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("D:/Python/Shooter_#2/fire.ogg")

#TODO Фон игры
img_back = "D:/Python/Shooter_#2/galaxy.jpg"
#TODO Главный игрок ракета
img_hero = "D:/Python/Shooter_#2/rocket.png"
#TODO Враги инопланетяни
img_enemy = "D:/Python/Shooter_#2/ufo.png"
#TODO Пуля
img_bullet = "D:/Python/Shooter_#2/bullet.png"
#TODO Астеройд
img_asteroid = "D:/Python/Shooter_#2/asteroid.png"

font.init()
font_1 = font.SysFont('Arial', 80)
win = font_1.render('You Win!', True, (255,255, 255))
lose = font_1.render('You lose!', True, (180, 0, 0))
font_2 = font.SysFont('Aria', 36)

scrole = 0 #TODO сбитих кораблей
gloab = 20 #TODO столько кораблей нужно сбить для победы
lost = 0 #TODO пропущенные корабли
max_lost = 10 #TODO проиграли, если пропустили кораблей
life = 3 #TODO Количество жизней

#TODO класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        #* Каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        #* Каждый спрайт должен зранить свойство rect - прямоугольник в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    #* Метод отрисовки героя в окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#TODO Класс главного героя
class Player(GameSprite):
    #* Метод для управления главным героем стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    #* Метод выстрел
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#TODO класс спрайта-врага   
class Enemy(GameSprite):
    #* движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #* исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#TODO класс спрайта-пули   
class Bullet(GameSprite):
    #* движение врага
    def update(self):
        self.rect.y += self.speed
        #* исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()

#TODO Создание окна
win_width = 700
win_height = 500
display.set_caption("Космический шутер")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

#TODO Создаем спрайт героя игры
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_asteroid, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)

bullets = sprite.Group()

#TODO Переменная игры "Закончилась"
finish = False
#TODO Флаг сбрасывается при завершении игры при закрытии на крестик
run = True
rel_time = False #TODO флаг отвечающий за перезарядку
num_five = 0 #TODO Переменная для подсчета выстрелов

#TODO Основной цикл
while run:
    #* Событие нажатия кнопки закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #* Проверяем сколько выстрелов сделано и не происходит ли перезарядка
                if num_five < 5 and rel_time == False:
                    num_five = num_five + 1
                    fire_sound.play()
                    ship.fire()
                #* Если игрок сделал 5 выстрелов
                if num_five >= 5 and rel_time == False:
                    #* Засекаем время, когда происходит перезарядка
                    last_time = timer()
                    #* Ставит флаг перезарядки
                    rel_time = True
                
    #TODO Сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        #* Обновляем фон
        window.blit(background, (0,0))

        #* Пишем текст на экране
        text = font_2.render("Счёт:" + str(scrole), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font_2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        #* Произсводим движение спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        #* Обнавляем их в новом положении
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        #* Перезарядка
        if rel_time == True:
            now_time = timer() #* Считываем время
            #* Пока не прошло 3 секунды, высвечивать сообщение о перезарядки
            if now_time - last_time < 3:
                reloader = font_2.render('Wair, reloader....', 1, (150, 0, 0))
                window.blit(reloader, (260, 460))
            else:
                num_five = 0
                rel_time = False
            
        #* проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #* этот цикл повторится столько раз, сколько монстров подбито
            scrole = scrole + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        #* возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        #!if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            #* проиграли, ставим фон и больше не управляем спрайтами.
            #!finish = True
            #!window.blit(lose, (200, 200))

        #* Если спрайт коснулся врагаб уменьшается жизнь
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1

        #* Проверка проигрыша
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        #* проверка выигрыша: сколько очков набрали?
        if scrole >= gloab:
            finish = True
            window.blit(win, (200, 200))

        #* Задаем разный увет в зависимости от количества жизней
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font_1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()
    #TODO Автоматический перезапуск игры
    else:
        finish = False
        scrole = 0
        lost = 0
        num_five = 0
        life = 3

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        for i in range(1, 3):
            asteroid = Enemy(img_asteroid, randint(30, win_width - 30), -40, 80, 50, randint(1, 3))
            asteroids.add(asteroid)
        
        time.delay(3000)
    #* цикл срабатывает каждую 0.05 секунд
    time.delay(50)

