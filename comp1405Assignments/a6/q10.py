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
        self.bg_color = 10, 0, 0

        # Setup a timer to refresh the display FPS times per second
        self.FPS = 120 #increased due to lag in key pressing.
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)
        

    def run(self):
        """Loop forever processing events"""
        running = True
        
        key_string = ""
        counter = 0
        sound_a= pygame.mixer.Sound("8whip.wav")
        sound_s= pygame.mixer.Sound("nantucket.wav")
        sound_d= pygame.mixer.Sound("RedtailHawkA.wav")
        sound_f= pygame.mixer.Sound("ShotgunFire.wav")
        sound_default = pygame.mixer.Sound("")
        current_sound = sound_default
        old_sound = sound_default
        
        currently_busy = False
        
        
        while running:
            event = pygame.event.wait()
            # player is asking to quit
            if event.type == pygame.QUIT:
                running = False
            
            # time to draw a new frame
            elif event.type == self.REFRESH:
                
                self.screen.fill(self.bg_color)
                key_string = ""
                keys = pygame.key.get_pressed()
                #I could probably think of a better way to do this but for now I'm tired.
                
                if keys[pygame.K_a]:
                    key_string += "a"
                    current_sound = sound_a
                elif keys[pygame.K_s]:
                    key_string += "s"
                    current_sound = sound_s
                elif keys[pygame.K_d]:
                    key_string += "d"
                    current_sound = sound_d
                elif keys[pygame.K_f]:
                    key_string += "f"
                    current_sound = sound_f
                else:
                    current_sound = sound_default
                if len(key_string) > 1:
                    key_string += " <--- PLEASE ONLY PRESS ONE LETTER AT A TIME, THANKS."
                
                if not current_sound == old_sound:
                    if not current_sound == sound_default:
                        pygame.mixer.stop()
                        old_sound = current_sound
                        old_sound.play()
                    else:
                        old_sound = current_sound
                    
                
                myfont = pygame.font.Font("CALLIGRA.TTF", 15)
                my_text = myfont.render(key_string, 1, (0,255,255))
                self.screen.blit(my_text, (5,5))
                
                # flip buffers so that everything we have drawn gets displayed
                pygame.display.flip()
                
                #self.draw()
            else:
                pass # an event type we don't handle            

    def draw(self):
        """Update the display"""
        # everything we draw now is to a buffer that is not displayed
        


MyGame().run()
pygame.quit()
sys.exit()

