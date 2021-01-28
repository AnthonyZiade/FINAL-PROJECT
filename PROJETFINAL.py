import pygame
from pygame.locals import (RLEACCEL,)
pygame.init()

screen_width = 1600 # Dimensions
screen_height = 900 # Dimensions
screen = pygame.display.set_mode([screen_width, screen_height]) # Setting the screen mode for the game

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.image = pygame.image.load("bball.jpg").convert_alpha() # Loads ball image
        self.image.set_colorkey((255, 255, 255), RLEACCEL) # Sets background transparent 
        self.size = self.image.get_size() # Gets size of image
        self.x = 1400 # Ball x coordinate
        self.y = 150 # Ball y coordinate
        self.multiplier = 1 # Defines the size multiplier of the ball initially, used to inflate ball size
        self.angle = 0 # Definines the angle of the ball initially, used to create a rotation
    def update(self):
        self.updated = pygame.transform.scale(self.image, (int(self.size[0] * self.multiplier), int(self.size[1] * self.multiplier))) # Inflates ball size by multiplier
        self.rect = self.updated.get_rect(center=[self.x, self.y]) # Sets center according to coordinates
        self.original_image = self.updated # Defines original image of ball before inflation or rotation
        self.angle -= 12 # Speed of rotation of the ball
        if ball.multiplier > 1: # If statement to stop the ball from rotating while not moving
            self.rotate()
        screen.blit(self.updated, self.rect) # Draws the ball
    def rotate(self): # Rotates ball by angle
        self.updated = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.updated.get_rect(center = self.rect.center)

# Getters and setters for attributes for Ball class
    @property  
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
    @property
    def size_multiplier(self):
        return self._size_multiplier
    @size_multiplier.setter
    def size_multiplier(self, value):
        self._size_multiplier = value
        
def image_loader(img): # Loads images to prevent lag
    return pygame.image.load(img).convert_alpha()

# Atributes
WHITE = (255, 255, 255)
score = 0
ball = Ball()
ball_moving = False # Ball is not initially moving
ballspeed_x = 0 # Speeds of ball
ballspeed_y = 0 # ""
ball_falling = False
background = image_loader("court.jpeg") # Calls image loader function
hoop = image_loader("hoop.png") # ""
myfont = pygame.font.SysFont("Comic Sans MS", 30) # Default font for upcoming text usage
bar_start_height = 0 # Charge bar default height
bar_x = 1450 # Charge bar coordinates
bar_y = 50 # ""
bar_width = 25 # Charge bar width
y_change = 0 # Length of charge bar
shots = 0 # Shots

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60) # Tick rate of the game
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and ball_moving == False and shots < 10: # If ball is not moving and a mouse button is used, the ball will begin to move toward mouse position
            y_change = 1.5
        if event.type == pygame.MOUSEBUTTONUP and ball_moving == False and shots < 10:
            ball_moving = True
            shots += 1
            mouse_x, mouse_y = pygame.mouse.get_pos() # Gets mouse (x, y) positions
            ballspeed_x = (mouse_x - ball.x)/10000 * bar_start_height # Gives horrizontal speed to the ball 
            ballspeed_y = (mouse_y - ball.y)/10000 * bar_start_height # Gives vertical speed to the ball
            y_change = 0
            
        if event.type == pygame.QUIT: # If the user wants to quit the game, this will exit out of the window
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                shots = 0
                score = 0
                ball.x = 1550
                ball.y = 150
            
    if ball_moving == True: # Increases x and y coordinates because of speed
        ball.x += ballspeed_x
        ball.y += ballspeed_y
        # Ball inflation
        if ball.multiplier > 2 and ball_falling == False: # Once the multiplier exceeds 2, ball_falling becomes True
            ball_falling = True
        if ball.multiplier <= 2 and ball_falling == False: # If the ball multiplier is smaller or equal to 2, the ball will increase in size
            ball.multiplier += 0.025
        if ball.multiplier > 1 and ball_falling == True: # If the ball multiplier is greater than 1 and ball_falling is True, the ball wil shrink toward the original size
            ball.multiplier -= 0.025
        if ball.multiplier <= 1 and ball_falling == True: # If the ball multiplier is smaller or equal to 1 and ball_falling is True, the ball will stop shrinking and moving
            ball_falling = False
            ball_moving = False
            bar_start_height = 1
            
    bar_start_height += y_change # Increases height of the bar as y_change changes
    if bar_start_height <= 0: 
        bar_start_height = 1
    
    screen.fill(WHITE) # Turns background white
    screen.blit(background, [0, 0]) # Displays the background image
    screen.blit(hoop, [600, -80]) # Displays the hoop image
    power = myfont.render("Power: " + str(bar_start_height - 1), False, (0, 0, 0)) # Power level indication
    screen.blit(power, [1400, 800]) # Power level message location
    textsurface = myfont.render("Points: " + str(score), False, (0, 0, 0)) # Lets user know how many points he has scored
    screen.blit(textsurface, [1400, 850]) # Point number location
    pygame.draw.rect(screen, [0, 0, 255], [bar_x, bar_y, bar_width, bar_start_height])
    remaining = myfont.render("Shots remaining: " + str(10 - shots), False, (0,0,0)) # Displays shots remaining
    screen.blit(remaining, [1261, 750]) # Location of shots remaining
    restart_game = myfont.render("Press R to restart the game at any time", False, (0, 0, 0)) # Lets user know they can restart the game at any time with R button
    screen.blit(restart_game, [500, 850]) # Message location
    
    if ball_moving == False:
        if ball.x < 830 and ball.x > 760 and ball.y < 207 and ball.y > 150: # Range of where the ball is considered in the hoop
            print("Nice shot, +3 points")
            score += 3
        if shots < 5: # Original location for ball when less than 5 shots have been taken
            ball.x = 1550
            ball.y = 150
        if shots >= 5 and shots < 10: # Swithes side of the ball after 5 shots have been taken, # Note, didnt have time to add different rotation for opposite side
            ball.x = 50
            ball.y = 150
        if shots >= 10:
            game_over = myfont.render("Game Over! You Scored : " + str(int(score/3)) + " out of 10 " + "Shots and Scored : " + str(score) + " Points!", False, (0, 0, 0))
            screen.blit(game_over, [350, 450]) # Displays end screen with message
            
    ball.update()
    pygame.display.flip() # Updates the screen
    
pygame.quit() # Quits the game
