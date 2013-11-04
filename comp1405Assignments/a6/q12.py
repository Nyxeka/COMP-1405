"""Some simple skeleton code for a pygame game/animation

This skeleton sets up a basic 800x600 window, an event loop, and a
redraw timer to redraw at 30 frames per second.
"""
from __future__ import division
import math
import sys
import pygame
from random import randint

class ball():
    def __init__(self, image, starting_pos_x, starting_pos_y, starting_magnitude, angle):
        self.x = starting_pos_x
        self.y = starting_pos_y
        self.vel_x = starting_magnitude * math.sin(angle)
        self.vel_y = starting_magnitude * math.cos(angle)
        self.angle = angle
        self.image_origin = pygame.transform.scale(image, (30, 30))
        self.image = self.image_origin
        self.accel_y = -0.05
        
    def moveMe(self):
        
        self.image = pygame.transform.rotate(self.image_origin,self.angle*57.2957795+180)# the * 57.2957795 part is radians to degrees...
        self.x += self.vel_x 
        self.y += self.vel_y
        self.final_x = self.x - ((self.image.get_width() - self.image_origin.get_width())/2)
        self.final_y = self.y - ((self.image.get_height() - self.image_origin.get_height())/2)
        self.angle = math.atan(self.vel_x/self.vel_y)
        if self.angle > 0 and self.vel_x > 0:
            self.angle = self.angle + 3.14159265358979
        if self.angle < 0 and self.vel_x < 0:
            self.angle = self.angle + 3.14159265358979
        self.vel_y -= self.accel_y

class MyGame(object):
    def __init__(self):
        """Initialize a new game"""
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        # set up a 640 x 480 window
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        # use a black background
        self.bg_color = 0, 0, 0

        # Setup a timer to refresh the display FPS times per second
        self.FPS = 120 # we want to get ALL the keypresses, while maintaining vertical sync, my keeping fps a multiple of 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)


    def run(self):
        """Loop forever processing events"""
        running = True
        
        random_angle = 0
        
        starting_ball_pos_x = self.width/2
        starting_ball_pos_y = self.height
        
        balls = []
        
        rad_to_deg = 180/3.14159265
        deg_to_rad = 3.14159265/180
        two_pi = 2*3.14159265
        pi_over_two = 3.141592653/2
        to_remove = []
        
        ball_starting_velocity = 6
        
        current_key = None
        last_key = None
        
        myfont = pygame.font.SysFont("courier", 15)
        
        min_angle = 45
        max_angle = 180-45
        
        while running:
            event = pygame.event.wait()

            # player is asking to quit
            if event.type == pygame.QUIT:
                running = False
            
            # time to draw a new frame
            elif event.type == self.REFRESH:
                keys = pygame.key.get_pressed()
                self.screen.fill(self.bg_color)
                
                to_remove = []
                
                if keys[pygame.K_a]:
                    balls += [ball(pygame.image.load("pygameAssignmentTracker.png"), starting_ball_pos_x, starting_ball_pos_y, ball_starting_velocity, ((randint(90+min_angle,90+max_angle))*deg_to_rad))]
                
                if keys[pygame.K_SPACE]:
                    current_key = "space"
                    #balls += [ball(pygame.image.load("pygameAssignmentTracker.png"), starting_ball_pos_x, starting_ball_pos_y, ball_starting_velocity, ((randint(90,270))*deg_to_rad))]
                else:
                    current_key = None
                    last_key = None
                
                if not current_key == last_key and current_key == "space":
                    last_key = current_key
                    balls += [ball(pygame.image.load("pygameAssignmentTracker.png"), starting_ball_pos_x, starting_ball_pos_y, ball_starting_velocity, ((randint(90+min_angle,90+max_angle))*deg_to_rad))]
                
                #go over all the balls, drawing them, as well as visibility check...
                for i in range(len(balls)):
                    balls[i].moveMe()
                    self.screen.blit(balls[i].image,(balls[i].x-(balls[i].image.get_width()/2),balls[i].y-(balls[i].image.get_height()/2)))
                    if balls[i].x > self.width or balls[i].x < 0 - balls[i].image.get_width() or balls[i].y > self.height:
                        to_remove += [balls[i]]
                
                #draw our text on the top of the screen...
                self.screen.blit(myfont.render("press 'a' for a surprise :D... also number of balls: " + str(len(balls)), 1, [0,255,255]),(0,0))        
                
                #remove the unseen balls
                if len(to_remove) > 0:
                    for i in to_remove:
                        balls.remove(i)
                        
                    #if balls location is out of screen, TERMINATE IT. balls.remove(i)
                
                pygame.display.flip()
                
            else:
                pass # an event type we don't handle            
        


MyGame().run()
pygame.quit()
sys.exit()

