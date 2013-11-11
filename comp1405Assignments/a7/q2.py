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

        self.width = 1024
        self.height = 768
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
        dog_image = pygame.image.load("pygameAssignmentMagnet.png")
        
        tracker_radius = tracker_image.get_width()/2*images_scale
        
        tracker_pos_x = 200
        tracker_pos_y = 200
        
        max_tracker_pos_x = self.width - tracker_radius
        max_tracker_pos_y = self.height - tracker_radius
        
        magnet_pos_x = 500
        magnet_pos_y = 500
        
        dog_pos_x = 100
        dog_pos_y = 100
        
        #so, there's a problem. this is way to fast for 120 fps, so it's gonna get scaled down
        #to around where it would be at 30fps.
        accel_rate = 10.0/16.0
        tracker_velocity_scalar = 0.9**(1.0/4.0)
        
        dog_accel_rate = 10.0/16.0
        dog_velocity_scalar = 0.8**(1.0/4.0)
        
        dog_velocity_x = 0.0
        dog_velocity_y = 0.0
        
        tracker_velocity_x = 0.0
        tracker_velocity_y = 0.0
        
        tracker_magnitude = 0.0
        
        dog_angle = 0.0
        tracker_angle = 0.0
        magnet_angle = 0.0
        
        tracker_sideways_velocity_x = 0.0
        tracker_sideways_velocity_y = 0.0
        
        sideways_tracker_angle = 0.0
        velocity_angle = 0.0

        rad_to_deg = 180/3.14159265
        two_pi = 2*3.14159265
        pi_over_two = 3.141592653/2
        
        debug = 0
        
        collision_dist = tracker_image.get_width()*images_scale
        
        game_over_times = 0
        tracker_immortal = False
        tracker_immortal_counter = 0.0
        tracker_immortal_time = 5.0
        tracker_immortal_time_increment = tracker_immortal_time/self.FPS/2
        
        render_tracker = True
        tracker_immortal_blink_time = 0.100
        tracker_immortal_blink_timer = 0.0
        
        #initial sprite scaledown:
        tracker_scaled = pygame.transform.scale(tracker_image,(int(tracker_image.get_width()*images_scale),int(tracker_image.get_height()*images_scale)))
        dog_scaled = pygame.transform.scale(dog_image,(int(dog_image.get_width()*images_scale),int(dog_image.get_height()*images_scale)))
        
        bg_colour = [128,128,128]
        
        
        debug_info = dict()
        
        # create font for printing stuff:
        myfont = pygame.font.SysFont("courier", 15)
        
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
                #if mouse_buttons_pressed[0]:
                #    magnet_pos_x = mouse_pos[0]
                #    magnet_pos_y = mouse_pos[1]
                magnet_pos_x = mouse_pos[0]
                magnet_pos_y = mouse_pos[1]
                
                # Do calculations to make sure magnet and tracker are always facing eachother.
                # first we want the angle between them.
                dif_x = tracker_pos_x-magnet_pos_x
                dif_y = tracker_pos_y-magnet_pos_y
                dog_dif_x = dog_pos_x - tracker_pos_x
                dog_dif_y = dog_pos_y - tracker_pos_y
                dist = math.sqrt((dif_x**2.0)+(dif_y**2.0))
                dog_dist = math.sqrt((dog_dif_x**2.0)+(dog_dif_y**2.0))
                if dist > 0: #don't want to mess up our angle of hit...
                    angle_radians = math.atan2(-dif_y,dif_x) # we make y negative because of pygame's weird inverted y-axis.
                    angle_radians = (angle_radians - pi_over_two) % two_pi # we don't want it ending up more than 360 degrees.
                    angle_degrees = angle_radians * rad_to_deg
                    dog_angle_radians = math.atan2(-dog_dif_y,dog_dif_x) # we make y negative because of pygame's weird inverted y-axis.
                    dog_angle_radians = (dog_angle_radians - pi_over_two) % two_pi # we don't want it ending up more than 360 degrees.
                    dog_angle_degrees = dog_angle_radians * rad_to_deg
                
                #check for collisions and apply gameover:
                if tracker_immortal == False:
                    if math.fabs(dog_dist) < collision_dist:
                        game_over_times += 1
                        tracker_immortal_counter = 0.0
                        tracker_immortal = True
                else:
                    tracker_immortal_counter += tracker_immortal_time_increment
                    if tracker_immortal_counter >= tracker_immortal_time:
                        tracker_immortal_counter = 0.0
                        tracker_immortal = False
                
                #about immortal:
                debug_info["immortal_stuff"] = myfont.render("immortal_increment: " + str(tracker_immortal_time_increment), 1, [0,255,0])
                debug_info["immortal_blink_timer"] = myfont.render("immortal_blink_timer: " + str(tracker_immortal_blink_timer), 1, [0,255,0])
                debug_info["immortal_true"] = myfont.render("Immortal?: " + str(tracker_immortal), 1, [0,255,0])
                debug_info["render_tracker"] = myfont.render("Render tracker?: " + str(render_tracker), 1, [0,255,0])
                debug_info["immortal_counter"] = myfont.render("immortal_timer_counter: " + str(tracker_immortal_counter), 1, [0,255,0])
                
                game_over_text = myfont.render("game over times: " + str(game_over_times), 1, [255,0,0])
                
                # Now we can do the calculations for the movement of the tracker:
                tracker_accel_x = accel_rate * math.sin(angle_radians)
                tracker_accel_y = accel_rate * math.cos(angle_radians)
                
                dog_accel_x = dog_accel_rate * math.sin(dog_angle_radians)
                dog_accel_y = dog_accel_rate * math.cos(dog_angle_radians)
                
                #debug_info["accel_info_x"] = myfont.render("A_x:" + str(tracker_accel_x), 1, [0,255,0])
                #debug_info["accel_info_y"] = myfont.render("A_y:" + str(tracker_accel_y), 1, [0,255,0])
                
                
                
                # make changes to velocity:
                tracker_velocity_x = tracker_velocity_x*tracker_velocity_scalar + tracker_accel_x
                tracker_velocity_y = tracker_velocity_y*tracker_velocity_scalar + tracker_accel_y
                
                dog_velocity_x = dog_velocity_x*dog_velocity_scalar + dog_accel_x
                dog_velocity_y = dog_velocity_y*dog_velocity_scalar + dog_accel_y
                
                # add angular friction to the ball/tracker:
                #changed so that we are merely calculating this stuff...
                tracker_magnitude = math.sqrt(tracker_velocity_x**2.0 + tracker_velocity_y**2.0)
                velocity_angle = math.atan2(-tracker_velocity_y, tracker_velocity_x)
                sideways_tracker_angle = (angle_radians - pi_over_two)
                
                tracker_sideways_velocity_magnitude = tracker_magnitude * math.sin(velocity_angle - sideways_tracker_angle)
                
                #tracker_sideways_velocity_x = -tracker_sideways_velocity_magnitude * math.sin(sideways_tracker_angle)
                #tracker_sideways_velocity_y = -tracker_sideways_velocity_magnitude * math.cos(sideways_tracker_angle)
                #if dist > 0:
                #    tracker_velocity_x -= (tracker_sideways_velocity_x * (10 / dist))
                #    tracker_velocity_y -= (tracker_sideways_velocity_y * (10 / dist)) 
                
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
                # limit velocity, but we don't want this for a7 so...
                """if tracker_velocity_x > tracker_max_vel:
                    tracker_velocity_x = tracker_max_vel
                if tracker_velocity_x < -tracker_max_vel:
                    tracker_velocity_x = -tracker_max_vel
                if tracker_velocity_y > tracker_max_vel:
                    tracker_velocity_y = tracker_max_vel
                if tracker_velocity_y < -tracker_max_vel:
                    tracker_velocity_y = -tracker_max_vel"""
                
                #debug_info["velocity_info_x"] = myfont.render("V_x: " + str(tracker_velocity_x), 1, [0,255,0])
                #debug_info["velocity_info_y"] = myfont.render("V_y: " + str(tracker_velocity_y), 1, [0,255,0])
                
                
                # apply velocity
                tracker_pos_x += tracker_velocity_x
                tracker_pos_y += tracker_velocity_y
                
                dog_pos_x += dog_velocity_x
                dog_pos_y += dog_velocity_y
                
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
                dog_image_render = pygame.transform.rotate(dog_scaled, dog_angle_degrees)
                
                tracker_new_pos_x =  tracker_pos_x - (tracker_image_render.get_width()/2)
                tracker_new_pos_y =  tracker_pos_y - (tracker_image_render.get_height()/2)
                
                dog_new_pos_x = dog_pos_x - (dog_image_render.get_width()/2)
                dog_new_pos_y = dog_pos_y - (dog_image_render.get_height()/2)
                
                if tracker_immortal == True:
                    tracker_immortal_blink_timer += tracker_immortal_time_increment
                    if tracker_immortal_blink_timer >= tracker_immortal_blink_time:
                        render_tracker = (not render_tracker)
                        tracker_immortal_blink_timer = 0
                        
                else:
                    render_tracker = True
                if render_tracker:
                    self.screen.blit(tracker_image_render,(tracker_new_pos_x,tracker_new_pos_y))
                self.screen.blit(dog_image_render,(dog_new_pos_x,dog_new_pos_y))
                self.screen.blit(game_over_text, (5,5))
                #debug info:
                
                if debug == 1:
                
                    counter=0
                    for i in debug_info:
                        counter += 1
                        self.screen.blit(debug_info[i], (5,counter*15+5))
                    
                    #pygame.draw.line(self.screen, [255,255,0], [tracker_pos_x, tracker_pos_y], [(tracker_pos_x + (tracker_sideways_velocity_x*20)), (tracker_pos_y + (tracker_sideways_velocity_y*20))], 2)
                    #pygame.draw.line(self.screen, [255,255,0], [tracker_pos_x, tracker_pos_y], [(tracker_pos_x + (tracker_forwards_velocity_x*20)), (tracker_pos_y + (tracker_forwards_velocity_y*20))], 3)
                    pygame.draw.line(self.screen, [0,0,255], [tracker_pos_x, tracker_pos_y], [(tracker_pos_x + (tracker_velocity_x*20)), (tracker_pos_y + (tracker_velocity_y*20))], 1)    
                    pygame.draw.line(self.screen, [0,0,0],[tracker_pos_x,tracker_pos_y], [tracker_pos_x + tracker_accel_x,tracker_pos_y + tracker_accel_y])
                    
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

