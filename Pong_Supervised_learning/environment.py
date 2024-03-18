from game_elements import Paddle
from game_elements import Ball
import pygame
import random

BLACK = (0,0,0)
WHITE = (255,255,255)
pygame.font.init()
pygame.display.init()   
pygame.display.set_caption("Pygame Pong")
font = pygame.font.Font(None, 74)
clock = pygame.time.Clock()
limit_fps_each_step = 100

class PongEnv():
    def __init__(self):
        self.state = None
        
        self.paddleA = Paddle(WHITE, 10, 500)
        self.paddleB = Paddle(WHITE, 10, 100)
        self.ball = Ball(WHITE, 10, 10)
        self.all_sprites_list = pygame.sprite.Group()
        
        self.scoreA = 0
        self.scoreB = 0
        
    def step(self, action):
        done = False

        if action == 0:
            self.paddleB.moveUp(0)

        elif action == 1:
            self.paddleB.moveDown(5)
            
        elif action == 2:
            self.paddleB.moveUp(5)
                
        self.all_sprites_list.update()
        
        
        if self.ball.rect.y > 490: # base and top colision
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y < 0:
            self.ball.velocity[1] = -self.ball.velocity[1]
             
        if pygame.sprite.collide_mask(self.ball, self.paddleA) or pygame.sprite.collide_mask(self.ball, self.paddleB):
            self.ball.bounce()
    
        if self.ball.rect.x >= 690:  # opponent's point
            done = True
            self.ball.velocity[0] = -self.ball.velocity[0]
            
        if pygame.sprite.collide_mask(self.ball, self.paddleB): # hit the ball
            self.scoreB += 1
            done = True
            
         
        y_paddle = self.paddleB.rect.y
        y_ball = self.ball.rect.y
        
        if self.ball.velocity[0] > 0:
            atention = 1
        else:
            atention = 0
         
        self.state = (self.ball.velocity[0], self.ball.velocity[1], self.ball.rect.x, self.ball.rect.y, self.paddleB.rect.y, action) 

        return self.state, y_paddle, y_ball, done, atention
    
    def render(self, screen, nfps_each_step):
        
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
        self.all_sprites_list.draw(screen)


        #score display        
        text = font.render(str(self.scoreA), 1, WHITE)
        screen.blit(text, (250, 10))
        text = font.render(str(self.scoreB), 1, WHITE)
        screen.blit(text, (420, 10))

        #screen update
        pygame.display.flip()
        clock.tick(nfps_each_step)   # limit FPS in one step
             
    def reset(self):
        self.paddleA.rect.x = 5
        self.paddleA.rect.y = 0
        self.paddleB.rect.x = 690
        self.paddleB.rect.y = 300
        self.ball.rect.x = 345
        self.ball.rect.y = 195
        self.scoreB = 0
        self.scoreA = 0
        
        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)
        
        self.state = (self.ball.velocity[0], self.ball.velocity[1], 345, random.randint(0,400), self.paddleB.rect.y, 0) # vel_x, vel_y, pos_x, pos_y, pos_paddle, action

        return self.state
