from __future__ import division
import math
import sys
import pygame

rad_to_deg = 180/3.14159265
two_pi = 2*3.14159265
pi_over_two = 3.141592653/2

class vector():
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        
class Entity():
    def __init__(self, name, image_filename = None, image_scale = 1.0, x=0, y=0, velocity_scalar=1.0, accel_rate=1.0,vel_x=0,vel_y=0,rotation = 0):
        """initializes an entity"""
        #if we want an image for it:
        if not image_filename is None:
            self.image_unscaled = pygame.image.load(image_filename)
            self.image_scaled = pygame.transform.scale(self.image_unscaled,(int(self.image_unscaled.get_width()*image_scale),int(self.image_unscaled.get_height()*image_scale)))
        #set intial location and velocity
        self.location = vector(x,y)
        self.velocity = vector(vel_x,vel_y)
        
        self.image_rotated = self.image_scaled
        
        self.rotation = 0
        
        self.name = name
        
        self.acceleration = accel_rate
        
        self.velocity_scalar = velocity_scalar
        
        self.render_location = vector()
        
    def update(self):
        """updates the location of entity, applying velocity etc~"""
        
        self.location.x += self.velocity.x
        self.location.y += self.velocity.y
        
        self.image_rotated = pygame.transform.rotate(self.image_scaled,self.rotation)
        
        self.render_location.x = self.location.x - (self.image_rotated.get_width()/2)
        self.render_location.y = self.location.y - (self.image_rotated.get_width()/2)
        
        
    
    def target(self,x,y,velocity_scalar,collision_distance):
        """have the entity target/chase down a location"""
        global rad_to_deg
        #difference between entity and target
        difference = vector(self.location.x - x,self.location.y - y)
        
        
        if difference.y > 0:
            self.rotation = math.atan(difference.x/difference.y) * rad_to_deg + 180
        elif difference.y < 0:
            self.rotation = math.atan(difference.x/difference.y) * rad_to_deg
        #distance between entity and target:
        distance = math.sqrt(difference.x**2.0 + difference.y**2.0)
        
        #for if we ever want to debug this stuff
        self.distance_from_target = distance
        
        #set up the acceleration scalar for our normalized vector.
        scalar = self.acceleration/distance
        
        #set up our normalized vector for acceleration:
        accel_target = vector(-scalar*difference.x,-scalar*difference.y)
        
        #apply acceleration towards target to entities velocity
        self.velocity.x = (self.velocity.x * self.velocity_scalar) + accel_target.x
        self.velocity.y = (self.velocity.y * self.velocity_scalar) + accel_target.y
        
        if distance < collision_distance:
            return True
        else:
            return False
        #apply changes to acceleration:
        
        
        
class MyGame(object):
    def __init__(self):
        """Initialize a new game"""
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        # use a black background
        self.bg_color = 128,128,128
        
        # Setup a timer to refresh the display FPS times per second
        self.FPS = 60
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)
        
        #init sound:
        self.sound_music = pygame.mixer.Sound("SpaceAmbiance.ogg")
        self.sound_immortal = pygame.mixer.Sound("smb_warning.wav")
        self.sound_gameover = pygame.mixer.Sound("smb_gameover.wav")
        
        #set up our font renderer
        self.myfont = pygame.font.SysFont("courier", 25)
        
        self.myfont_info = pygame.font.SysFont("courier", 15)
        
        #Game part:
        self.lives = 3
        self.game_over = False
        self.game_over_timer = 0.0
        self.game_over_time = self.sound_gameover.get_length()
        self.game_over_sound_played = False
        
        self.score = 0
        self.cat_caught = False
        self.entities = dict()
        
        #when the cat gets caught
        self.cat_immortal = False
        self.render_cat = True
        self.immortal_cat_timer = 0.0
        self.immortal_cat_time = 5.0
        
        self.standard_image_scale = 0.25
        
        self.min_collision_distance = 60
        
        #Entity(name, image_filename = None, image_scale = 1.0, x=0, y=0, velocity_scalar, accel_rate,vel_x=0,vel_y=0,rotation = 0)
        
        self.entities["cat"] = Entity("cat","pygameAssignmentTracker.png",self.standard_image_scale,0,0,0.9**(1.0/4.0),10.0/16.0)
        
        #since we will be checking to see if it's a list of entities
        self.entities["dogs"] = []
        
        self.game_event_add_dog()
        
        self.states = dict()
        self.states["main_menu"] = self.state_main_menu
        self.states["run_game"] = self.state_run_game
        
        
        
        self.game_counters_increment = 1/self.FPS
        
        self.game_events = dict()
        self.game_time = 0.0
        #for each of the following, the index will be the amount of time it takes for each event to happen
        #and the the element in the array it points to will be a counter that goes up to this.
        #the second element in the array will be the function it calls.
        self.game_events[1.0] = [0.0, self.game_event_add_score]
        self.game_events[30.0] = [0.0, self.game_event_add_dog]
        self.game_events[0.05] = [0.0, self.game_event_cat_immortal_check]
        #self.game_events[self.sound_music.get_length()] = [0.0, self.game_event_play_sound]
        
        self.current_state = "main_menu"
        self.pause = False
        self.pause_timer = 3.0
        
        #-1 to play the loop indefinitely. 
        self.channel_1 = self.sound_music.play(-1)
    
    def game_event_add_dog(self):
        #adds a dog to the game
        new_dog_location_x = -100
        new_dog_location_y = -100
        self.entities["dogs"].append(Entity("dog","pygameAssignmentMagnet.png",self.standard_image_scale,new_dog_location_x,new_dog_location_y,0.9**(1.0/4.0),((float(len(self.entities["dogs"]))*3.0) + 8.0)/16.0))
    
    def game_event_add_score(self):
        self.score += 100
        
    def game_event_cat_immortal_check(self):
        if self.cat_immortal:
            self.render_cat = not self.render_cat
        else:
            self.render_cat = True
            
    
    def update_mouse_location(self):
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_location = vector(mouse_pos[0],mouse_pos[1])
        self.mouse_buttons_pressed = pygame.mouse.get_pressed()
    
    def mouse_is_colliding(self,x,y,width,height):
        if self.mouse_location.x > x and self.mouse_location.y > y and self.mouse_location.x < x+width and self.mouse_location.y < y+height:
            return True
        else:
            return False
    
    def reset_game(self):
        self.lives = 3
        self.score = 0
        self.cat_caught = False
        self.game_over = False
        self.entities = dict()
        
        #when the cat gets caught
        self.cat_immortal = False
        self.render_cat = True
        #Entity(name, image_filename = None, image_scale = 1.0, x=0, y=0, velocity_scalar, accel_rate,vel_x=0,vel_y=0,rotation = 0)
        self.entities["cat"] = Entity("cat","pygameAssignmentTracker.png",self.standard_image_scale,0,0,0.9**(1.0/4.0),10.0/16.0)
        
        #since we will be checking to see if it's a list of entities
        self.entities["dogs"] = []
        
        self.game_event_add_dog()
        self.game_time = 0.0
        self.current_state = "run_game"
        
        self.game_events[1.0] = [0.0, self.game_event_add_score]
        self.game_events[30.0] = [0.0, self.game_event_add_dog]
        self.game_events[0.05] = [0.0, self.game_event_cat_immortal_check]
        self.channel_1.unpause()
    
    def state_main_menu(self):
        #the main menu state. This is where we hit playgame, options, view scores, exit, etc~
        #if I get time, I'll implement a list/dictionary of options that point to functions
        #and probably a button class and stuff...
        self.screen.fill([0,0,0])
        self.update_mouse_location()
        self.channel_1.pause()
        new_game = self.myfont.render("New Game", 1, [255,255,255])
        continue_game = self.myfont.render("Continue Game", 1, [128,128,128])
        options = self.myfont.render("Options", 1, [128,128,128])
        exit = self.myfont.render("Exit", 1, [255,255,255])
        
        if self.mouse_is_colliding((self.width/2-new_game.get_width()/2),200,new_game.get_width(),new_game.get_height()):
            new_game = self.myfont.render("New Game", 1, [255,255,0])
            if self.mouse_buttons_pressed[0]:
                self.reset_game()
                self.pause = False
        
        if self.mouse_is_colliding((self.width/2-new_game.get_width()/2),305,new_game.get_width(),new_game.get_height()):
            exit = self.myfont.render("Exit", 1, [255,0,0])
            if self.mouse_buttons_pressed[0]:
                sys.exit()
        
        if self.pause:
            continue_game = self.myfont.render("Continue Game", 1, [255,255,255])
            if self.mouse_is_colliding((self.width/2-continue_game.get_width()/2),235,continue_game.get_width(),continue_game.get_height()):
                if self.mouse_buttons_pressed[0]:
                    self.current_state = "run_game"
        self.screen.blit(new_game, ((self.width/2-new_game.get_width()/2),200))
        self.screen.blit(continue_game, ((self.width/2-continue_game.get_width()/2),235))
        self.screen.blit(options, ((self.width/2-options.get_width()/2),270))
        self.screen.blit(exit, ((self.width/2-exit.get_width()/2),305))
        
    def state_run_game(self):
        
        #so, each of the entities will be targetting the appropriate 'thing'
        #we will split this up into a few parts:
        self.screen.fill(self.bg_color)
        dog_collided = False
        #update keys and mouse
        self.update_mouse_location()
        keys = pygame.key.get_pressed()
        
        #if the p key is pressed...
        if not self.game_over:
            if keys[pygame.K_p]:
                self.pause = True
                self.current_state = "main_menu"
        
        if self.cat_caught:
            if not self.pause and not self.game_over:
                if self.immortal_cat_timer == 0.0:
                    self.channel_1.pause()
                    self.sound_immortal.play()
                if self.immortal_cat_timer > self.sound_immortal.get_length() and self.immortal_cat_timer < self.sound_immortal.get_length()+self.game_counters_increment:
                    self.sound_immortal.stop()
                    self.channel_1.unpause()
                self.immortal_cat_timer += self.game_counters_increment
            if self.immortal_cat_timer > self.immortal_cat_time:
                self.immortal_cat_timer = 0.0
                self.cat_immortal = False
                self.cat_caught = False
        
        if not self.pause and not self.game_over:
            #check for and run any game events..
            for index,event in self.game_events.items():
                self.game_events[index][0] += self.game_counters_increment
                if self.game_events[index][0] > float(index):
                    self.game_events[index][0] = 0.0
                    self.game_events[index][1]()
        
        #go through all of the entities...
        for index, entity in self.entities.items():
            #first check to see if it's a list of entities
            if type(self.entities[index]) is list:
                #we know it's a list of entities
                if index == "dogs":
                    #we are dealing with the dogs:
                    for i in range(len(entity)):
                        if not self.pause and not self.game_over:
                            dog_collided = self.entities[index][i].target(self.entities["cat"].location.x,self.entities["cat"].location.y,self.entities[index][i].velocity_scalar,self.min_collision_distance)
                            self.entities[index][i].update()
                        self.screen.blit(self.entities[index][i].image_rotated, (self.entities[index][i].render_location.x,self.entities[index][i].render_location.y))
                        if dog_collided == True and not self.cat_immortal:
                            self.cat_caught = True
                            self.cat_immortal = True
                            self.lives -= 1
                            self.score -= 500
            else:
                if index == "cat":
                    if not self.pause and not self.game_over:
                        self.entities[index].target(self.mouse_location.x,self.mouse_location.y,self.entities["cat"].velocity_scalar,self.min_collision_distance)
                        self.entities[index].update()
                    if self.render_cat:
                        self.screen.blit(self.entities[index].image_rotated, (self.entities[index].render_location.x,self.entities[index].render_location.y))
        
        if self.pause:
            self.pause_timer -= self.game_counters_increment
            pause_time_left = self.myfont_info.render("Unpausing in: " + str(self.pause_timer), 1, [0,0,0])
            self.screen.blit(pause_time_left,(200,300))
            if self.pause_timer <= 0:
                self.pause_timer = 3.0
                self.pause = False
                self.channel_1.unpause()
        
        #part 3: set up game info:
        score_info = self.myfont_info.render("Score: " + str(self.score), 1, [0,0,0])
        immortal_info = self.myfont_info.render("Immortal: " + str(self.cat_immortal), 1, [0,0,0])
        lives_info = self.myfont_info.render("lives left: " + str(self.lives), 1, [0,0,0])
        self.screen.blit(score_info,(5,5))
        self.screen.blit(immortal_info,(5,25))
        self.screen.blit(lives_info,(self.width-200,5))
        
        if self.lives < 0:
            self.game_over = True
        
        if self.game_over:
            self.channel_1.pause()
            game_over_msg = self.myfont_info.render("GAME OVER", 1, [0,0,0])
            self.screen.blit(game_over_msg,((self.width/2) - (game_over_msg.get_width()/2),300))
            
            if not self.game_over_sound_played:
                self.sound_gameover.play()
                self.game_over_sound_played = True
            
            if self.game_over_timer >= self.game_over_time:
                self.game_over_sound_played = False
                self.current_state = "main_menu"
            else:
                self.game_over_timer += self.game_counters_increment
        
        
        
        
    def run(self):
        """Loop forever processing events"""
        running = True
        
        while running:
            event = pygame.event.wait()

            # player is asking to quit
            if event.type == pygame.QUIT:
                running = False

            # time to draw a new frame
            elif event.type == self.REFRESH:
                self.screen.fill([0,0,0])
                
                self.states[self.current_state]()
                
                pygame.display.flip()

            else:
                pass # an event type we don't handle            


MyGame().run()
pygame.quit()
sys.exit()

