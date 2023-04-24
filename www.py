import pygame
from random import randint
from time import time
pygame.init()
window = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
fill_color = ((200, 255, 255))
window.fill(fill_color)

class Area():
    def __init__(self,x=0,y=0,width=10, height =10, color =None):
        self.rect = pygame.Rect(x, y, width, height)                    # створення прямокутника
        self.fill_color = color
    
    def set_color(self,color):
        self.fill_color = color   
    
    def fill(self):
        pygame.draw.rect(window,self.fill_color,self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
    def colliderect (self, rect):
        return self.rect.colliderect(rect)
class Label(Area):
    
    def set_text(self, text, fsize =12, text_color = "black"):     # створення тексту
        self.text = text
        self.image = pygame.font.Font(None,fsize).render(text,True, text_color)
    
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_y,self.rect.y + shift_y))
class Picture(Area):
    def __init__(self,x,y,width, height, color, filename):
        super().__init__(x,y,width, height, color)
        self.image = pygame.transform.scale(pygame.image.load(filename),(width,height))
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_y,self.rect.y + shift_y))

ball= Picture(200,350,50,50,(200, 255, 255),"ball_V2.png")
platform = Picture(200,450,110,25,(200, 255, 255),"platform_V2.png")
start_x = 0
start_y = 0
monsters = list()
n=9
for j in range (3):
    x = start_x + (27*j)
    y = start_y + (55*j)
    for i in range (n): 
        monster = Picture(x,y,50,50,(200, 255, 255),"enemy.png")
        monsters.append(monster)
        x+=55
    n = n - 1
game_over = False
move_left = False
move_right = False
speed_x = 3
speed_y = 3
text = Label(150,150,50,50,(255,0,0))
text.set_text('GAME OVER',60, (255,0,0))
while not game_over:
    ball.fill()
    platform.fill()
#            Створення монстрів та видалення монстрів
    for monster in monsters:
        monster.draw(start_x,start_y)
        if monster.rect.colliderect(ball.rect):
            monsters.remove(monster)
            monster.fill()
            speed_y *= -1
#                    РУХ ПЛАТФОРМИ
    for event in pygame.event.get():        
        if event.type ==  pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:    
                move_left = False
    if move_right:
        platform.rect.x +=3
    elif move_left:
        platform.rect.x -=3
#----------------------------------------------- 
#               РУХ МЯЧА
    ball.rect.x += speed_x
    ball.rect.y += speed_y
    if ball.rect.y < 0 :
        speed_y *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        speed_x *= -1
    if ball.colliderect(platform.rect):
        speed_y *=-1
# -----------Система програшу--------------------
    if ball.rect.y > (platform.rect.y + 20):
        text = Label(150,200,50,50,(200, 255, 255))
        text.set_text('GAME OVER',60, (255,0,0))
        text.draw(10,10)
        game_over = True
#-----------Система виграшу-------------------
    if len(monsters) == 0:
        time_text = Label(150, 200, 200, 50, (200, 255, 255))
        time_text.set_text('GAME WIN', 60, (0, 255, 0))
        time_text.draw(10,10)
        game_over = True
    ball.draw(0,0)
    platform.draw(0,0)
    clock.tick(40)
    pygame.display.update()