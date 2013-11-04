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
        self.bg_color = 0, 0, 0
        
        self.colour_dict = {"black"  : 0,
                            "red"    : 1,
                            "green"  : 2,
                            "blue"   : 3,
                            "orange" : 4,
                            "yellow" : 5,
                            "brown"  : 6}
        self.colour_list = [[0  ,  0,  0],
                            [255,  0,  0],
                            [0  ,255,  0],
                            [0  ,  0,255],
                            [255,175,  0],
                            [255,255,  0],
                            [ 75, 35,  0]]

        # Setup a timer to refresh the display FPS times per second
        self.FPS = 30
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)
        
        
    def run(self):
        """Loop forever processing events"""
        running = True
        old_time = pygame.time.get_ticks()
        new_time = pygame.time.get_ticks()
        current_colour = 0
        while running:
            event = pygame.event.wait()
            new_time = pygame.time.get_ticks()
            # player is asking to quit
            if event.type == pygame.QUIT:
                running = False
            if new_time > (old_time + 1000):
                old_time = new_time
                current_colour = (current_colour + 1) % 7
                self.bg_color = self.colour_list[current_colour]
            
            
            # time to draw a new frame
            elif event.type == self.REFRESH:
                self.draw()

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

