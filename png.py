
import pygame,random
from pygame.locals import *
from sys import exit

SCREEN_SIZE = (700,500)

class Paddle(pygame.sprite.Sprite):

    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect((x,y),(self.image.get_width(),self.image.get_height()))

    def update(self,key,speed,time):
	direction = 0
        if self.rect.y < 0: self.rect.y = 0
        elif self.rect.y > 380: self.rect.y = 380

        if self.rect.y < 0: self.rect.y = 0
        elif self.rect.y > 380: self.rect.y = 380

        if key == "UP":
            direction = -1
        elif key == "DOWN":
            direction = 1

        self.rect.move_ip(0,direction*speed*time)


class Ball(pygame.sprite.Sprite):

    def __init__(self,x,y,image,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect((x,y),(self.image.get_width(),self.image.get_height()))
        self.speed = speed
        self.player_score = 0
        self.computer_score = 0

    def update(self,time):
        if self.rect.x > 640 - self.image.get_width():
            self.into_screen = False
            self.player_score +=1
            self.reset()
        elif self.rect.x < 0:
            self.into_screen = False
            self.computer_score +=1
            self.reset()
 
        if self.rect.y > 480 - self.image.get_height():
            self.speed[1] = -self.speed[1]
            self.rect.y = 480 - self.image.get_height()
        elif self.rect.y < 0:
            self.speed[1] = -self.speed[1]
            self.rect.y = 0
        
        self.rect.move_ip(self.speed[0]*time,self.speed[1]*time)

    def detect_collision(self,group):
        collision = pygame.sprite.spritecollide(self,group,False)
        if len(collision) == 1:
            self.speed[0] = -self.speed[0]
	    if self.speed[0] >= 100:
            	self.speed[0] += 200
	    elif self.speed[0] < 100:
		self.speed[0] -= 200

	    if self.speed[0] > 400: self.speed[0] = 400
	    elif self.speed[0] < -400: self.speed[0] = -400
	  
    def reset(self):
        self.rect.x = 200
        self.rect.y = 150
        self.speed[0] = random.randint(50,100)
        self.speed[1] = random.randint(100,200)
        if self.speed[0] == 0: self.speed[0] = 500
        if self.speed[1] == 0: self.speed[1] = 500
#I know where you live...

class Computer:

    def __init__(self,paddle,ball):
        self.paddle = paddle
        self.ball = ball

    def update(self,speed,time):
	if self.ball.rect.x > 320:
            if self.ball.rect.y > self.paddle.rect.y: self.paddle.update("DOWN",speed,time)
            elif self.ball.rect.y < self.paddle.rect.y: self.paddle.update("UP",speed,time)

def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
    pygame.display.set_caption("Pong")
    paddle_image = pygame.Surface((20,100))
    ball_image = pygame.Surface((21,21))
    pygame.draw.rect(paddle_image,(255,255,255,),((1,0),(19,99)))
    pygame.draw.circle(ball_image,(255,255,255,),(10,10),10)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial",20)
    
    player_paddle = Paddle(0,230,paddle_image)
    computer_paddle = Paddle(630,230,paddle_image)
    ball = Ball(200,150,ball_image,[150,100])

    paddle_group = pygame.sprite.Group()
    paddle_group.add(player_paddle)
    paddle_group.add(computer_paddle)

    CPU = Computer(computer_paddle,ball)
    pygame.mouse.set_visible(False)
    
    while 1:
        screen.fill((0,0,0))
        screen.blit(font.render(str(ball.player_score)+" - " + str(ball.computer_score),True,(255,255,255)),(280,30))
        paddle_group.draw(screen)
        screen.blit(ball.image,(ball.rect.x,ball.rect.y))

        time_passed_seconds = clock.tick(70) / 600.0

        ball.detect_collision(paddle_group)
            
        ball.update(time_passed_seconds)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()

        pressed_keys = pygame.key.get_pressed()
        pressed_mouse = pygame.mouse.get_pressed()
        if pressed_keys[K_UP] or pressed_mouse[0]: player_paddle.update("UP",200.0,time_passed_seconds)
        elif pressed_keys[K_DOWN] or pressed_mouse[2]: player_paddle.update("DOWN",200.0,time_passed_seconds)
        
        CPU.update(200.0,time_passed_seconds)
        
        pygame.display.update()

if __name__ == "__main__": run()
            
