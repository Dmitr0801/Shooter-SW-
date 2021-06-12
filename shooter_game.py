from pygame import *
from random import randint
#фоновая музыка
mixer.init()
mixer.music.load('msc.mp3')
mixer.music.play()
fire_sound = mixer.Sound('Shoot.wav')

 
#нам нужны такие картинки:
img_back = "fone.png" #фон игры
img_hero = "ship-removebg-preview.png" #герой

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
 
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
        bullet = Bullet("12323-removebg-preview.png",self.rect.centerx,self.rect.top,10,20,20)
        bullets.add(bullet)




lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y>=500:
            lost += 1
            self.rect.y=0
monsters = sprite.Group()
bullets = sprite.Group()
class Bullet (GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y<0:
            self.kill()


for i in range(6):
    monsters.add(Enemy("enemy"+ str(i+1)+".png",randint(1,650),0,50,50,randint(1,5)))


#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 20)
 
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна

font,init()
font1 = font.SysFont("Times New Roman",36)
win = font1.render("You Won!!!!",True,(255,215,0))
lose = font1.render("You lose!!!!",True,(200,200,0))


score = 0


while run:
   #событие нажатия на кнопку Закрыть

   for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()  
   sprites_list = sprite.groupcollide(monsters,bullets,True,True) 
   for c in sprites_list:
       score += 1 
       monsters.add(Enemy("enemy"+ str(i+1)+".png",randint(1,650),0,50,50,randint(1,5)))
   if score >= 10:
        window.blit(win,(300,200))
        display.update()
        time.wait(1000)
        run = false
   if lost>=5 or sprite.spritecollide(ship,monsters,False):
       window.blit(lose,(300,200))
       display.update()
       time.wait(3000)
       run = false

   if not finish:
       #обновляем фон
       window.blit(background,(0,0))
 
       #производим движения спрайтов
       ship.update()
       bullets.update()
       bullets.draw(window)
       #обновляем их в новом местоположении при каждой итерации цикла
       ship.reset()
       monsters.draw(window)
       monsters.update()
       text_lose = font1.render("Пропущено: " + str(lost),1,(225,225,225))
       window.blit(text_lose, (0,0))
       text_score = font1.render("Уничтожено: " + str(score),1,(225,225,225))
       window.blit(text_score, (0,30))
 
   display.update()
   #цикл срабатывает каждые 0.05 секунд
   time.delay(30)
    
