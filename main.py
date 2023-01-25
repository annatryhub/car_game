import pgzrun
import math
import random

from pgzero.actor import Actor

from pgzero.keyboard import keyboard

WIDTH = 800
HEIGHT = 600

class Car:
    def __init__(self, min_speed=10):
        self.actor = Actor('car.png', center=(WIDTH // 2, HEIGHT - 150)) # на початку гри машинка стоїть посередині  внизу
        self.min_speed = min_speed # при першому запуску мінімальна швидкість дорівнює 10
        self.speed = min_speed
        self.crashed = False # машинка ще не розбилась і гра триває
        self.finished = False

    def check_crash(self, obs): # функція перевіряє, чи машинка знаходиться в полі для гри
        if self.actor.left < 0 or self.actor.right > WIDTH or self.actor.colliderect(obs.actor): # поки актор.машинка не зʼїхала за межі вправо чи вліво і поки не вдарилась в перешкоду
            self.crashed = True

    def check_finish(self, finish): # функція перевіряє, чи машинка на фініші
        if self.actor.y <= finish.actor.y: # якщо значення по Y у машинки менше, ніж у фінішу або дорівнює йому
            self.finished = True

    def update(self): # функція для натиску різних кнопок
        if keyboard.w: # при натисканні на W
            if self.actor.top <= 0: # якщо вехня межа машинки вже дісталась до верху екрану, то вона умовно переміщується вниз. Такий прийом я використала для того, щоб було відчуття дороги, яка рухається
                self.actor.top = 0
            else:
                self.actor.y -= 3.25
            self.speed += 4 # при натисканні на W швидкість машинки збільшується на 4 і програма повертає це значення
        elif keyboard.s: # при натисканні на S швидкість машинки зменшується
            if self.actor.bottom > HEIGHT: # якщо координата нижньої межі машинки більша за висоту, то нижня межа приймає значення висоти. Це потрібно для того, щоб машинка могла гальмувати
                self.actor.bottom = HEIGHT
            else:
                self.actor.y += 2.5
            if self.speed > self.min_speed:
                self.speed -= 2 # швидкість зменшується на 2
        else:
            if self.actor.bottom >= HEIGHT: # якщо нижня межа машинки більша за значення по Y за розмір екрану, то нижня межа приймає значення висоти екрану. Використовується, щоб машинка не виходила за межі поля
                self.actor.bottom = HEIGHT
            else:
                self.actor.y += 1.25 # поки машинка не знаходиться на нижній межі поля, то координата по Y збільшується на 1.25
            if self.speed > self.min_speed:
                self.speed -= 1
        if keyboard.a: # при натисканні на A машинка повертає ліворуч
            self.actor.x -= 5 # для повороту значення координати X зменшується на 5
            self.actor.angle = 10 # значення кута повороту 10. Це використовується для плавного повороту
        elif keyboard.d:
            self.actor.x += 5 # при натисканні на D машинка повертає праворуч
            self.actor.angle = -10 # значення кута -10
        else:
            self.actor.angle = 0 # якщо не викликають повороти, то машина їде прямо і кут 0

    def draw(self):
        self.actor.draw()

    def draw_speed(self):
        screen.draw.text("Speed: " + str(self.speed), (700, 575), color=(0, 0, 0))

    def reset(self, min_speed=10):
        self.__init__(min_speed)


class Obstacle:
    def __init__(self):
        self.actor = Actor('obs.png', center=(random.randrange(0, WIDTH), -150))
        self.count = 0 # використовується для підрахунку успішно подоланих перешкод

    def update(self, speed):
        self.actor.y += 2 + speed // 10 # координата Y збільшується на 2 одиниці і додається поділена на 10 швидкість. Використовується для руху дороги, перешкоди стають рухомими
        if self.actor.y > HEIGHT + 50:
            self.actor.x = random.randrange(0, WIDTH)
            self.actor.y = -150 # якщо координата Y приймає значення -150, це означає, що машина успішно подолала перешкоду і ми додаємо один до кількості подоланих перешкод. Використовуємо, щоб виводити на екран кількість перешкод
            self.count += 1

    def draw(self):
        self.actor.draw()

    def reset(self):
        self.__init__()


class Finish:
    def __init__(self, pos=-10000):
        self.actor = Actor('finish.png', (WIDTH // 2, pos))

    def update(self, speed):
        self.actor.y += 2 + speed // 10

    def draw(self):
        self.actor.draw()

    def reset(self, pos=-10000):
        self.__init__(pos)


class GameMode:
    def __init__(self):
        self.bg = 'game_bg.png'
        self.paused = False
        self.scores = 0

    def update(self, passed):
        self.scores = passed * 100 # за кожну подолану перешкоду, кількість очок множиться на 100, тобто якщо машина проїхала 1 перешкоду, то це 100 очок

    def draw(self):
        screen.blit(self.bg, (0, 0)) # blit використовує зображення як фон

    def draw_crash(self):
        screen.draw.text("Game Over!", center=(WIDTH // 2, 100), color=(0, 0, 0), fontsize=75)

    def draw_finish(self):
        screen.draw.text("Finish!", center=(WIDTH // 2, 100), color=(255, 255, 255), fontsize=75)

    def draw_scores(self):
        screen.draw.text("Scores: " + str(self.scores), (20, 25), color=(0, 0, 0))

    def pause(self, car, obs, finish):
        self.paused = True
        if keyboard.r: # при натисканні на R гра починається спочатку
            car.reset()
            obs.reset()
            finish.reset()
            self.paused = False
        if keyboard.z: # при натисканні на Z фініш переноситься на координату -10000 і швидкість машини є 10
            car.reset(10)
            obs.reset()
            finish.reset(-10000)
            self.paused = False
        if keyboard.x: # при натисканні на X фініш стає вдвічі довшим і переноситься на -20000 і мінімальна швидкість 20
            car.reset(20)
            obs.reset()
            finish.reset(-20000)
            self.paused = False
        if keyboard.c: # С викликає найважчий рівень гри. Мінімальна швидкість 35 і гра стає ще довшою
            car.reset(35)
            obs.reset()
            finish.reset(-30000)
            self.paused = False

# викликаємо класи
car = Car()
obs = Obstacle()
finish = Finish()
gamemode = GameMode()


def update():
    if car.crashed or car.finished:
        gamemode.pause(car, obs, finish)
    if not gamemode.paused:
        obs.update(car.speed)
        finish.update(car.speed)
        car.update()
        car.check_crash(obs)
        car.check_finish(finish)
        gamemode.update(obs.count)


def draw():
    screen.clear()
    if not gamemode.paused:
        gamemode.draw()
        car.draw()
        obs.draw()
        finish.draw()
        gamemode.draw_scores()
        car.draw_speed()
    else:
        screen.fill((150, 150, 150))
        if car.crashed:
            gamemode.draw_crash()
        if car.finished:
            gamemode.draw_finish()
        screen.draw.text("Easy = (Z)", (100, 250), color=(255, 255, 255), fontsize=75)
        screen.draw.text("Medium = (X)", (100, 350), color=(255, 255, 255), fontsize=75)
        screen.draw.text("Hard = (C)", (100, 450), color=(255, 255, 255), fontsize=75)


pgzrun.go()
