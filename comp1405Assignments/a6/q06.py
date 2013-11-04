"""Some simple skeleton code for a pygame game/animation

This skeleton sets up a basic 800x600 window, an event loop, and a
redraw timer to redraw at 30 frames per second.
"""
from __future__ import division
import math
import sys
import pygame


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
        self.bg_color = 255,255,255

        # Setup a timer to refresh the display FPS times per second
        self.FPS = 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)
        

    def run(self):
        """Loop forever processing events"""
        running = True
        
        #image is 256x256 pixels, made by Nicholas Hylands
        my_image = pygame.image.load("pygameAssignmentBall.png")
        image_pos_x = 0
        image_pos_y = self.height - my_image.get_height()
        movement_increment = self.width/30/2 #screen width divided by thirty frames divided by 2 seconds.
        ball_radius = my_image.get_width()/2
        
        ball_roll_times = self.width - (ball_radius * 3.14159265) - ball_radius*2
        
        ball_roll_increment = -ball_roll_times/30/2 #number of rolls / thirty drames / two seconds
        
        max_right = self.width - my_image.get_width()
        
        image_angle = 0
        
        while running:
            event = pygame.event.wait()

            # player is asking to quit
            if event.type == pygame.QUIT:
                running = False

            # time to draw a new frame
            elif event.type == self.REFRESH:
                self.screen.fill([255,255,255])
                
                rotated_image = pygame.transform.rotate(my_image, image_angle)
                
                image_angle = (image_angle + ball_roll_increment) % 360
                
                image_pos_x += movement_increment
                if image_pos_x > max_right:
                    image_pos_x = max_right
                    movement_increment *= -1
                    ball_roll_increment *= -1
                if image_pos_x < 0:
                    image_pos_x = 0
                    movement_increment *= -1
                    ball_roll_increment *= -1
                
                self.screen.blit(rotated_image,(image_pos_x - (rotated_image.get_width()/2 - ball_radius), image_pos_y - (rotated_image.get_height()/2 - ball_radius)))
                pygame.display.flip()
                #self.draw()

            else:
                pass # an event type we don't handle            

    def draw(self):
        """Update the display"""
        # everything we draw now is to a buffer that is not displayed
        self.screen.fill(self.bg_color)

        # flip buffers so that everything we have drawn gets displayed
        pygame.display.flip()


MyGame().run()
pygame.quit()
sys.exit()

