# setup pong special with the pygame library
import pygame
import random # randomize initial ball direction

pygame.init()
scene = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong Special 2024")
clock = pygame.time.Clock() # gamespeed

# load sounds
pygame.mixer.init()  # Initialize Pygame's sound mixer
bounce_sound = pygame.mixer.Sound("bounce.mp3")
error_sound = pygame.mixer.Sound("error.mp3")

def play_bounce_sound():
    bounce_sound.play()

def play_error_sound():
    error_sound.play()


# create Sprites
class Paddle(pygame.sprite.Sprite):
    # constructor of the class Paddle, initial properties and super constructor
    def __init__(self, x, color):
        super().__init__()
        self.width = 20
        self.height = 80
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)
        self.rect = self.image.get_rect(center = (x, 300))
        self.speed = 6 # adjust the paddle responsiveness

    # methods of the class Paddle
    def move_up(self):
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0
    
    def move_down(self):
        self.rect.y += self.speed
        if self.rect.bottom > 600:
            self.rect.bottom = 600

class Ball(pygame.sprite.Sprite):
    # constuctor of the class Ball, initial properties and super constructor
    def __init__(self, x, y, color):
        super().__init__()
        self.radius = 12
        self.image = pygame.Surface([2 * self.radius, 2 * self.radius])
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center = (x, y))

        self.dx = 0.6  # Initial horizontal speed
        if random.randint(0, 1) == 0:
           self.dx *= -1  # Randomize initial direction (horizontal)

        self.dy = 0.6  # Initial vertical speed
        if random.randint(0, 1) == 0:
           self.dy *= -1  # Randomize initial direction  (vertical)

    # update of the ball movements, collisions, and points admin
    def update(self):
        global score_1
        global score_2

        # boundery checks with the top and bottom
        if self.rect.top <= 0:
            self.dy *= -1 # reverse vertical direction of the ball
            play_bounce_sound()
        if self.rect.bottom >= 600:
            self.dy *= -1
            play_bounce_sound()
            
        # collision with the paddles
        if pygame.sprite.collide_rect(self, paddle_1):
            self.dx *= -1
            play_bounce_sound()
            
            third_height = paddle_1.height / 3

            if self.rect.bottom <= paddle_1.rect.top + third_height:  # Top edge hit
                self.dy = -abs(self.dy)  # Bounce upwards 
            if self.rect.top >= paddle_1.rect.bottom - third_height:  # Bottom edge hit
                self.dy = abs(self.dy)  # Bounce downwards

        if pygame.sprite.collide_rect(self, paddle_2):
            self.dx *= -1
            play_bounce_sound()

            third_height = paddle_2.height / 3

            if self.rect.bottom <= paddle_2.rect.top + third_height:  # Top edge hit
                self.dy = -abs(self.dy)  # Bounce upwards 
            if self.rect.top >= paddle_2.rect.bottom - third_height:  # Bottom edge hit
                self.dy = abs(self.dy)  # Bounce downwards

        # score left and right
        if self.rect.left < 0:
            score_2 += 1
            self.dx *= -1 # ball touch the left wall and bounce back
            play_error_sound()

        if self.rect.right > 800:
            score_1 += 1
            self.dx *= -1
            play_error_sound() 

        # movement
        self.rect.x += self.dx
        self.rect.y += self.dy       


# scoreboard on display
font = pygame.font.Font(None, 36)
def update_score(score_a, score_b):
    text1 = font.render(str(score_a), True, "purple" if score_a > score_b
                        else "red" if score_a < score_b else "black")
    text2 = font.render(str(score_b), True, "purple" if score_a < score_b
                        else "red" if score_a > score_b else "black")
    
    scene.blit(text1, (300 - text1.get_width() // 2,10))
    scene.blit(text2, (500 + text2.get_width() // 2,10))

# game loop, create instances of the classes Paddle and Ball
paddle_1 = Paddle(50, "black")
paddle_2 = Paddle(750, "black")
ball = Ball(400, 300, "brown")
score_1 = score_2 = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ball.update()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle_1.move_up()
    if keys[pygame.K_s]:
        paddle_1.move_down()
    if keys[pygame.K_UP]:
        paddle_2.move_up()
    if keys[pygame.K_DOWN]:
        paddle_2.move_down()

    # draw everything
    scene.fill("light blue")
    scene.blit(paddle_1.image, paddle_1.rect)
    scene.blit(paddle_2.image, paddle_2.rect)
    scene.blit(ball.image, ball.rect)
    
    update_score(score_1, score_2)

    pygame.display.flip()
    #clock.tick(60) # limit to 60 fps

pygame.quit()
