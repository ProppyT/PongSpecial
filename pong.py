
import turtle # game pong made with the library turtle
import pygame


# create screen
scene = turtle.Screen()
scene.title("Pong Special 2024, made by proppytfixitall@gmail.com")
scene.bgcolor("light blue")
scene.setup(width = 800, height = 600)
scene.tracer(0)

# the score
score_1 = 0
score_2 = 0

# make the paddles
# make the first peddle of the game, peddle_1
paddle_1 = turtle.Turtle()
paddle_1.speed(0) # animation speed (max)
paddle_1.shape("square")
paddle_1.color("grey")
paddle_1.shapesize(stretch_wid = 4, stretch_len = 1)
paddle_1.penup()
paddle_1.goto(-350, 0)

# make the second peddle of the game, peddle_2
paddle_2 = turtle.Turtle()
paddle_2.speed(0)
paddle_2.shape("square")
paddle_2.color("grey")
paddle_2.shapesize(stretch_wid = 4, stretch_len = 1)
paddle_2.penup()
paddle_2.goto(350, 0)

# make the ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("brown")
ball.penup()
ball.goto(0, 0) # starts in the middle of the centre
# behaviour of the ball
ball.dx = 0.1 # ball speed (horizontal)
ball.dy = 0.1 # ball speed (vertical)

# make the score digits
digit_1 = turtle.Turtle()
digit_1.speed(0)
digit_1.penup()
digit_1.goto(-100, 0)
digit_1.hideturtle()
digit_1.write("{}".format(score_1), align = "center", font = ("Courier", 24, "bold"))
digit_2 = turtle.Turtle()
digit_2.speed(0)
digit_2.penup()
digit_2.goto(100, 0)
digit_2.hideturtle()
digit_2.write("{}".format(score_2), align = "center", font = ("Courier", 24, "bold"))

# function to print the score digits, and update it every time it's called
def score_update(score_a, score_b):
    if score_a < score_b:
        digit_1.color("red")
        digit_1.clear()
        digit_1.write("{}".format(score_a), align = "center", font = ("Courier", 24, "bold"))
        digit_2.color("green")
        digit_2.clear()
        digit_2.write("{}".format(score_b), align = "center", font = ("Courier", 24, "bold"))
    elif score_a > score_b:
        digit_1.color("green")
        digit_1.clear()
        digit_1.write("{}".format(score_a), align = "center", font = ("Courier", 24, "bold"))
        digit_2.color("red")
        digit_2.clear()
        digit_2.write("{}".format(score_b), align = "center", font = ("Courier", 24, "bold"))
    else:
        digit_1.color("grey")
        digit_1.clear()
        digit_1.write("{}".format(score_a), align = "center", font = ("Courier", 24, "bold"))
        digit_2.color("grey")
        digit_2.clear()
        digit_2.write("{}".format(score_b), align = "center", font = ("Courier", 24, "bold"))


# sound part of the game
pygame.mixer.init()  # Initialize Pygame's sound mixer
bounce_sound = pygame.mixer.Sound("bounce.mp3")
error_sound = pygame.mixer.Sound("error.mp3")

def play_bounce_sound():
    bounce_sound.play()

def play_error_sound():
    error_sound.play()

# update the movement of the ball
def ball_update():
    global score_1 # make score_1 accessible from this function
    global score_2 # make score_2 accessible from this function

    # move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    
    # border bouncing
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        play_bounce_sound()
    
    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        play_bounce_sound()

    if ball.xcor() > 390:
        play_error_sound()
        ball.dx *= -1
        score_1 += 1
        score_update(score_1, score_2)

    if ball.xcor() < -390:
        play_error_sound()
        ball.dx *= -1
        score_2 += 1
        score_update(score_1, score_2)

    # bouncing against the paddles
    if (-340 > ball.xcor() > -350) and (ball.ycor() < paddle_1.ycor()+50 and ball.ycor() > paddle_1.ycor()-50):
        ball.setx(-340)
        ball.dx *= -1
        play_bounce_sound()

    if (350 > ball.xcor() > 340) and (ball.ycor() < paddle_2.ycor()+50 and ball.ycor() > paddle_2.ycor()-50):
        ball.setx(340)
        ball.dx *= -1
        play_bounce_sound()

# paddle movement functions, for paddle_1, up, and down
def paddle_1_up():
    y = paddle_1.ycor()
    if not(y > 258): # don't move the paddle if it's against the top wall
        y += 30
    paddle_1.sety(y)

def paddle_1_down():
    y = paddle_1.ycor()
    if not(y < -258): # don't move the paddle if it's against the bottom wall
        y -= 30
    paddle_1.sety(y)

# paddle movement functions, for paddle_2, up, and down
def paddle_2_up():
    y = paddle_2.ycor()
    if not(y > 258): # don't move the paddle if it's against the top wall
        y += 30
    paddle_2.sety(y)

def paddle_2_down():
    y = paddle_2.ycor()
    if not(y < -258): # don't move the paddle if it's against the bottom wall
        y -= 30
    paddle_2.sety(y)

# flag that checks if the user want to break the game loop
break_flag = False # initially don't break the loop

def quit_game():
  """Function to change the break_flag, to break the game loop."""
  global break_flag
  if break_flag == False:
      break_flag = True # set break flag to break the game loop

# keyboard controls
scene.listen() # listen to key press
scene.onkeypress(quit_game, "q")  # call screen.bye() on "q" press
scene.onkeypress(paddle_1_up, "w") # "w" key calls paddle_1_up function
scene.onkeypress(paddle_1_down, "s") # "s" key calls paddle_1_down function
scene.onkeypress(paddle_2_up, "Up") # "Up" arrow-key calls paddle_2_up function
scene.onkeypress(paddle_2_down, "Down") # "Down" arrow-key calls paddle_2_down function


# game loop
while True:
    if break_flag == True:
        break # the break flag is set to True if the user press "q" on the keyboard
    ball_update()  # always run first the game logic
    scene.update() # then update the screen
    
