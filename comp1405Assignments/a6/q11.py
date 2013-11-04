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
        self.FPS = 120
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)
        

    def run(self):
        """Loop forever processing events"""
        running = True
        
        images_scale = 0.5
        
        #image is 256x256 pixels, made by Nicholas Hylands
        tracker_image = pygame.image.load("pygameAssignmentTracker.png")
        magnet_image = pygame.image.load("pygameAssignmentMagnet.png")
        
        tracker_radius = tracker_image.get_width()/2*images_scale
        
        tracker_pos_x = 200
        tracker_pos_y = 200
        
        max_tracker_pos_x = self.width - tracker_radius
        max_tracker_pos_y = self.height - tracker_radius
        
        magnet_pos_x = 500
        magnet_pos_y = 500
        
        max_accel_rate = 1.0
        accel_rate = 0.01
        tracker_accel_x = 0.0
        tracker_accel_y = 0.0
        
        tracker_velocity_x = 0.0
        tracker_velocity_y = 0.0
        
        tracker_max_vel = 2.0
        
        tracker_magnitude = 0.0
        
        tracker_angle = 0.0
        magnet_angle = 0.0
        
        tracker_sideways_velocity_x = 0.0
        tracker_sideways_velocity_y = 0.0
        
        sideways_tracker_angle = 0.0
        velocity_angle = 0.0
        
        rad_to_deg = 180/3.14159265
        two_pi = 2*3.14159265
        pi_over_two = 3.141592653/2
        
        debug = 1
        
        #close enough for us to decide the two things are together.
        close_enough = 2
        
        #initial sprite scaledown:
        tracker_scaled = pygame.transform.scale(tracker_image,(int(tracker_image.get_width()*images_scale),int(tracker_image.get_height()*images_scale)))
        magnet_scaled = pygame.transform.scale(magnet_image,(int(magnet_image.get_width()*images_scale),int(magnet_image.get_height()*images_scale)))
        
        bg_colour = [128,128,128]
        
        debug_info = dict()
        
        while running:
            event = pygame.event.wait()

            # player is asking to quit
            if event.type == pygame.QUIT:
                running = False

            # time to draw a new frame
            elif event.type == self.REFRESH:
                self.screen.fill(bg_colour)
                mouse_pos = pygame.mouse.get_pos()
                mouse_buttons_pressed = pygame.mouse.get_pressed()
                 
                #change location of magnet:
                #if LMB is pressed
                if mouse_buttons_pressed[0]:
                    magnet_pos_x = mouse_pos[0]
                    magnet_pos_y = mouse_pos[1]
                    
                    
                # Do calculations to make sure magnet and tracker are always facing eachother.
                # first we want the angle between them.
                dif_x = tracker_pos_x-magnet_pos_x
                dif_y = tracker_pos_y-magnet_pos_y
                dist = math.sqrt((dif_x**2.0)+(dif_y**2.0))
                if dist > 0: #don't want to mess up our angle of hit...
                    angle_radians = math.atan2(-dif_y,dif_x) # we make y negative because of pygame's weird inverted y-axis.
                    angle_radians = (angle_radians - pi_over_two) % two_pi # we don't want it ending up more than 360 degrees.
                    angle_degrees = angle_radians * rad_to_deg
                
                if math.fabs(dist) < close_enough:
                    accel_rate = 0
                    tracker_velocity_x = 0
                    tracker_velocity_y = 0
                    tracker_pos_x = magnet_pos_x
                    tracker_pos_y = magnet_pos_y
                else:
                    accel_rate = 0.01
                
                # Now we can do the calculations for the movement of the tracker:
                tracker_accel_x = accel_rate * math.sin(angle_radians)
                tracker_accel_y = accel_rate * math.cos(angle_radians)
                
                # create font for printing stuff:
                myfont = pygame.font.SysFont("courier", 15)
                
                debug_info["accel_info_x"] = myfont.render("A_x:" + str(tracker_accel_x), 1, [0,255,0])
                debug_info["accel_info_y"] = myfont.render("A_y:" + str(tracker_accel_y), 1, [0,255,0])
                
                # apply acceleration to velocity:
                tracker_velocity_x += tracker_accel_x
                tracker_velocity_y += tracker_accel_y 
                
                # add angular friction to the ball/tracker:
                tracker_magnitude = math.sqrt(tracker_velocity_x**2.0 + tracker_velocity_y**2.0)
                velocity_angle = math.atan2(-tracker_velocity_y, tracker_velocity_x)
                sideways_tracker_angle = (angle_radians - pi_over_two)
                
                tracker_sideways_velocity_magnitude = tracker_magnitude * math.sin(velocity_angle - sideways_tracker_angle)
                
                tracker_sideways_velocity_x = -tracker_sideways_velocity_magnitude * math.sin(sideways_tracker_angle)
                tracker_sideways_velocity_y = -tracker_sideways_velocity_magnitude * math.cos(sideways_tracker_angle)
                if dist > 0:
                    tracker_velocity_x -= (tracker_sideways_velocity_x * (10 / dist))
                    tracker_velocity_y -= (tracker_sideways_velocity_y * (10 / dist)) 
                
                # add linear propulsion:
                tracker_forwards_velocity_magnitude = tracker_magnitude * math.sin(velocity_angle - angle_radians)
                
                tracker_forwards_velocity_x = -tracker_forwards_velocity_magnitude * math.sin(angle_radians)
                tracker_forwards_velocity_y = -tracker_forwards_velocity_magnitude * math.cos(angle_radians)
                
                
                """ not working right now:
                #magnitude_sign = (tracker_forwards_velocity_magnitude * (1/math.fabs(tracker_forwards_velocity_magnitude)))
                
                #if dist > 0:
                #    tracker_velocity_x += (math.fabs(tracker_forwards_velocity_x * (10 / dist)) * magnitude_sign)
                #    tracker_velocity_y += (math.fabs(tracker_forwards_velocity_y * (10 / dist)) * magnitude_sign)
                """
                # limit velocity
                if tracker_velocity_x > tracker_max_vel:
                    tracker_velocity_x = tracker_max_vel
                if tracker_velocity_x < -tracker_max_vel:
                    tracker_velocity_x = -tracker_max_vel
                if tracker_velocity_y > tracker_max_vel:
                    tracker_velocity_y = tracker_max_vel
                if tracker_velocity_y < -tracker_max_vel:
                    tracker_velocity_y = -tracker_max_vel
                
                debug_info["velocity_info_x"] = myfont.render("V_x: " + str(tracker_velocity_x), 1, [0,255,0])
                debug_info["velocity_info_y"] = myfont.render("V_y: " + str(tracker_velocity_y), 1, [0,255,0])
                
                # apply velocity
                tracker_pos_x += tracker_velocity_x
                tracker_pos_y += tracker_velocity_y
                
                # make sure we don't go off-screen:
                if tracker_pos_x > max_tracker_pos_x:
                    tracker_pos_x = max_tracker_pos_x
                    tracker_velocity_x *= -1
                if tracker_pos_y > max_tracker_pos_y:
                    tracker_pos_y = max_tracker_pos_y
                    tracker_velocity_y *= -1
                if tracker_pos_x < tracker_radius:
                    tracker_pos_x = tracker_radius
                    tracker_velocity_x *= -1
                if tracker_pos_y < tracker_radius:
                    tracker_pos_y = tracker_radius
                    tracker_velocity_y *= -1
                
                # calculate renders:
                tracker_image_render = pygame.transform.rotate(tracker_scaled, angle_degrees)
                magnet_image_render = pygame.transform.rotate(magnet_scaled, angle_degrees)
                
                tracker_new_pos_x =  tracker_pos_x - (tracker_image_render.get_width()/2)
                tracker_new_pos_y =  tracker_pos_y - (tracker_image_render.get_height()/2)
                
                magnet_new_pos_x = magnet_pos_x - (magnet_image_render.get_width()/2)
                magnet_new_pos_y = magnet_pos_y - (magnet_image_render.get_height()/2)
                
                self.screen.blit(tracker_image_render,(tracker_new_pos_x,tracker_new_pos_y))
                self.screen.blit(magnet_image_render,(magnet_new_pos_x,magnet_new_pos_y))
                
                #debug info:
                
                if debug == 1:
                
                    counter=0
                    for i in debug_info:
                        counter += 1
                        self.screen.blit(debug_info[i], (5,counter*15+5))
                    
                    pygame.draw.line(self.screen, [255,255,0], [tracker_pos_x, tracker_pos_y], [(tracker_pos_x + (tracker_sideways_velocity_x*20)), (tracker_pos_y + (tracker_sideways_velocity_y*20))], 2)
                    pygame.draw.line(self.screen, [255,255,0], [tracker_pos_x, tracker_pos_y], [(tracker_pos_x + (tracker_forwards_velocity_x*20)), (tracker_pos_y + (tracker_forwards_velocity_y*20))], 3)
                    pygame.draw.line(self.screen, [0,0,255], [tracker_pos_x, tracker_pos_y], [(tracker_pos_x + (tracker_velocity_x*20)), (tracker_pos_y + (tracker_velocity_y*20))], 1)    
                
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

