import pygame
from game_elements import Paddle
from game_elements import Ball
from agent import Agent
import warnings
warnings.filterwarnings('ignore')

pygame.init()

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)

#window & misc
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong AI")
carryOn = True
clock = pygame.time.Clock()

#paddles
paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 0
paddleA.rect.y = 0
paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 690
paddleB.rect.y = 200

#ball
ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

#spritelist
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

#score
scoreA = 0
scoreB = 0

agent = Agent()
agent.load_model('model_lv4.pkl')

action = 0 

#main
while carryOn:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False

    # paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)

    state = (ball.velocity[0], ball.velocity[1], ball.rect.x, ball.rect.y, paddleB.rect.y, action)

    action = agent.predict([state[:-1]])

    if action == 0:
        paddleB.moveUp(0)
    if action == 1:
        paddleB.moveDown(5)
    if action == 2:
        paddleB.moveUp(5)

    all_sprites_list.update()

    # ball check
    if ball.rect.x >= 690:
        scoreA += 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        scoreB += 1
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()

    # drawing
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    all_sprites_list.draw(screen)

    # score display
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420, 10))

    # screen update
    pygame.display.flip()
    clock.tick(70)

#quit
pygame.quit()