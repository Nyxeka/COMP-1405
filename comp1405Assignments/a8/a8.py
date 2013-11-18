"""

"""



from __future__ import division
import math
import sys
import pygame
from random import randint

rad_to_deg = 180/3.14159265
two_pi = 2*3.14159265
pi_over_two = 3.141592653/2

def Pass():
    pass

class Vector():
    """simple x/y vector class"""
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    
    def getAngle():
        return math.atan((-self.y)/self.x) #-self.y because pygame's y axis is messed...
        
class Animation():
    def __init__(self, image, anim_width, anim_height, framerate = 0.1, first_frame = 1):
        self.image = image
        self.anim_width = anim_width
        self.anim_height = anim_height
        self.num_frames = 0
        self.frame_locations = dict()
        self.current_frame = first_frame
        self.anim_timer = 0
        self.anim_framerate = framerate
        self.first_frame = first_frame
        
    def add_frame(self,frame_number,x,y):
        self.frame_locations[frame_number] = Vector(x,y)
        if frame_number > 0:
            self.num_frames += 1
    
    def get_current_frame(self):
        return self.image.subsurface(pygame.Rect(self.frame_locations[self.current_frame].x,self.frame_locations[self.current_frame].y,self.anim_width,self.anim_height))
    
    def nextFrame(self):
        self.current_frame += 1
        if self.current_frame > self.num_frames:
            self.current_frame = 1
    
    
class Entity():
    def __init__(self, name, x=0, y=0, vel_x=0,vel_y=0):
        """initializes an entity"""
        #set intial location and velocity
        self.location = Vector(x,y)
        self.velocity = Vector(vel_x,vel_y)
        self.animation = dict()
        self.animation_state = ""
        self.direction = "right"
        self.run_speed = 4.8
    
    def change_animation_state(self, new_animation):
        self.animation_state = new_animation
        self.animation[new_animation].current_frame = self.animation[new_animation].first_frame
    
    def update_location(self):
        self.location.x += self.velocity.x
        self.location.y += self.velocity.y
    
    def add_animation(self, name, animation):
        self.animation[name] = animation
    
    def loop_animation(self,increment):
        self.animation[self.animation_state].anim_timer += increment
        if self.animation[self.animation_state].anim_timer > self.animation[self.animation_state].anim_framerate:
            self.animation[self.animation_state].anim_timer = 0.0
            self.animation[self.animation_state].nextFrame()
            
    def current_image(self):
        if self.direction == "right":
            return self.animation[self.animation_state].get_current_frame()
        else:
            return pygame.transform.flip(self.animation[self.animation_state].get_current_frame(),True,False)

        
class State():
    def __init__(self, state_function, enter_state_function = Pass, exit_state_function = Pass, enter_state_first_time = Pass):
        
        self.state_function = state_function
        
        self.enter_state_function = enter_state_function
        
        self.exit_state_function = exit_state_function
        
        self.enter_state_first_time = enter_state_first_time
        
        self.ran = False # has it been run for the first time yet?
        
    def run():
        self.state_function()
    
    #think about adding game events into individual states.
        
class Game_Event():
    def __init__(self, interval_time, event_function, increment, loop_type = -1):
        self.interval_time = interval_time
        self.event_function = event_function
        self.timer = 0.0
        self.increment = increment
    def loopMe(self):
        self.timer += self.increment
        if self.timer >= self.interval_time:
            self.timer = 0.0
            self.event_function()
        
class Button():
    def __init__(self, text, event_function, font, priority = 0, def_colour = (255,255,255), hover_colour = (255,255,0)):
        """text is the button text, event_function is the function to be called
           when the button is pressed, and priority decides how high up it is on
           the menu screen, (what order)"""
        self.text = text
        self.event_function = event_function
        self.priority = priority
        self.def_colour = def_colour
        self.hover_colour = hover_colour
        self.font = font
        self.image = None
        self.create_render()
        
    def create_render(self, colour = (255,255,255)):
        #new_game = self.myfont.render("New Game", 1, [255,255,255])
        self.image = self.font.render(self.text, 1, colour)
        
class Platform():
    def __init__(self,x,y,width,height,speed = 1,colour = (0,0,75)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.speed = speed
        self.next_width = width
        
    def get_rect(self):
        #changed to be thinner cause I don't feel like fixing the collision box.
        return pygame.Rect(self.x,self.y,self.width,self.height)
    
    def get_rect_next_width(self):
        #changed to be thinner cause I don't feel like fixing the collision box.
        return pygame.Rect(self.x,self.y,self.next_width,self.height)
    
class My_Game(object):
    def __init__(self):
        """Initialize a new game"""
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        # use a black background
        
        
        #_____________________________________________
        # Setup a timer to refresh the display FPS times per second
        self.FPS = 60
        #---
        self.game_counter_increment = 1/self.FPS
        #---
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)
        #=============================================
        
        
        
        #_____________________________________________
        #FSM: init different states
        #init states for our finite state machine.
        self.states = dict()
        self.states["main_menu"] = State(self.state_main_menu)
        self.states["run_game"] = State(self.state_run_game, self.enter_state_run_game, self.exit_state_run_game, self.enter_state_first_time_run_game)
        self.states["game_over"] = State(self.state_game_over)
        #=============================================
        
        #_____________________________________________
        #Set up for the main_menu state
        #---
        #set up our font renderer
        self.myfont = pygame.font.SysFont("courier", 25)
        
        #---
        self.menu_buttons = dict()
        self.menu_buttons["New_game"] = Button("New Game", self.button_event_play_game,self.myfont,1)
        self.menu_buttons["Continue_Game"] = Button("Continue Game", self.button_event_continue_game,self.myfont, 2)
        self.menu_buttons["Options"] = Button("Options", self.button_event_options,self.myfont, 3)
        self.menu_buttons["Exit"] = Button("Exit", sys.exit,self.myfont, 4)
        #=============================================
        
        #_____________________________________________
        #Set up our game events
        #basically, these happen every <interval> amount of time.
        #---
        self.game_events = dict()
        self.game_time = 0.0
        #for each of the following, the index will be the amount of time it takes for 
        #each event to happen (the interval), and the element in the array it points to 
        #will be a counter that goes up to this, so should always be set to zero.
        #the second element in the array will be the function it calls every interval.
        self.game_events["add_score"] = Game_Event(1.0, self.game_event_add_score,self.game_counter_increment)
        self.game_events["change_platforms"] = Game_Event(1.0, self.game_event_change_platform,self.game_counter_increment)
        #=============================================
        
        #_____________________________________________
        #Init stuff
        #---
        #debug?
        self.debug_log = False
        #---
        #background colour:
        self.bg_color = 25,25,25
        #font for debug info stuff
        self.myfont_info = pygame.font.SysFont("courier", 15)
        #---
        self.score = 0.0
        #---
        self.current_state = "main_menu"
        self.pause = False
        self.pause_timer = 3.0
        #-1 to play the loop indefinitely. 
        #self.channel_1 = self.sound_music.play(-1)
        self.update_mouse_location()
        self.old_button_down = False
        self.button_down = False
        self.game_over_counter = 0.0
        #---
        self.sound_music = pygame.mixer.Sound("SpaceAmbiance.ogg")
        self.channel_1 = self.sound_music.play(-1)
        self.channel_1.pause()
        self.sound_game_over = pygame.mixer.Sound("smb_gameover.wav")
        #=============================================
        
    def game_event_add_score(self):
        self.score += 100
    
    def game_event_change_platform(self):
        x = randint(1,3)
        for i in self.platform:
            if not self.platform[i].width == self.platform[i].next_width:
                self.platform[i].width = self.platform[i].next_width
        if x == 2:
            for i in self.platform:
                self.platform[i].next_width *= (float(randint(5,11))/10)
                if self.platform[i].next_width < 10:
                    self.platform = {key:value for key,value in self.platform.items() if value != self.platform[i]}
        if x == 3:
            self.platform[randint(500,1000)] = Platform(randint(0,750),randint(0,599),randint(10,175),randint(8,30),float(randint(2,17)/10))
        
    def update_mouse_location(self):
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_location = Vector(mouse_pos[0],mouse_pos[1])
        self.mouse_buttons_pressed = pygame.mouse.get_pressed()
    
    def mouse_is_colliding(self,x,y,width,height):
        if self.mouse_location.x > x and self.mouse_location.y > y and self.mouse_location.x < x+width and self.mouse_location.y < y+height:
            return True
        else:
            return False
            
    def button_event_continue_game(self):
        self.change_state("run_game")
    
    def button_event_options(self):
        pass
        
    def button_event_play_game(self):
        self.change_state("run_game",True)
    
    def change_state(self,new_state,reset = False):
        if reset:
            self.states[new_state].ran = False
        if new_state in self.states:
            self.states[self.current_state].exit_state_function()
            if not self.states[new_state].ran:
                self.states[new_state].enter_state_first_time()
            self.states[new_state].enter_state_function()
            self.current_state = new_state
        else:
            print "ERROR: STATE '" + str(new_state) + "' DOES NOT EXIST."
    
    def state_game_over(self):
        self.screen.fill([0,0,0])
        
        self.score = 0.0
        game_over_texts = dict()
        if self.game_over_counter == 0:
            self.sound_game_over.play()
        self.game_over_counter += self.game_counter_increment
        if self.game_over_counter >= 3.0:
            self.game_over_counter = 0.0
            self.states["run_game"].ran = False
            self.change_state("main_menu")
        for i in range(20):
            game_over_texts[i] = self.myfont.render("GAME OVER", 1,(randint(1,255),randint(1,255),randint(1,255)))
        
        for i,j in game_over_texts.items():
            self.screen.blit(j,(randint(1,800),randint(1,600)))
        
    def state_main_menu(self):
        #the main menu state. This is where we hit playgame, options, view scores, exit, etc~
        #if I get time, I'll implement a list/dictionary of options that point to functions
        #and probably a button class and stuff...
        """re-write this."""
        self.screen.fill([0,0,0])
        self.update_mouse_location()
        
        
        if self.mouse_buttons_pressed[0]:
            self.button_down = True
        else:
            self.button_down = False
        
        changed = False
        clicked = False
        
        if not self.old_button_down == self.button_down:
            self.old_button_down = self.button_down
            changed = True
            if not self.button_down:
                clicked = True
            
        
        for i,j in self.menu_buttons.items():
            if self.mouse_is_colliding((self.width/2-self.menu_buttons[i].image.get_width()/2),165+35*self.menu_buttons[i].priority,self.menu_buttons[i].image.get_width(),self.menu_buttons[i].image.get_height()):
                self.menu_buttons[i].create_render(self.menu_buttons[i].hover_colour)
                if clicked:
                    self.menu_buttons[i].event_function()
                if self.button_down:
                    self.menu_buttons[i].create_render((128,128,0))
            else:
                self.menu_buttons[i].create_render()
            
            if not self.states["run_game"].ran:
                self.menu_buttons["Continue_Game"].create_render((128,128,128))
            
        for i,j in self.menu_buttons.items():
            self.screen.blit(self.menu_buttons[i].image, ((self.width/2-self.menu_buttons[i].image.get_width()/2),165+35*self.menu_buttons[i].priority))
    
    def enter_state_run_game(self):
        """function to call when entering the run_game state
           basically all we're gonna do here is unthaw the VM
           which means we are going to make sure everything is "unpaused" """
        self.channel_1.unpause()
        pass
    
    def enter_state_first_time_run_game(self):
        """function to call when running run_game for the first time..."""
        
        #first, initiate entities.
        #Entity(self, name, x=0, y=0, vel_x=0,vel_y=0):
        self.player_sprite_sheet = pygame.image.load("qb7e6.png")
        self.player_sprite_sheet.set_colorkey((0,128,128))
        self.player = Entity("Player",200,200)
        self.player.add_animation("running",Animation(self.player_sprite_sheet,52,65,0.04,-1))
        self.player.add_animation("standing",Animation(self.player_sprite_sheet,40,74,0.1))
        #_____________________________________________________
        #start adding where the frames are on the sprite sheet for the player
        self.player.animation["running"].add_frame(4,7,106)
        self.player.animation["running"].add_frame(5,80,106)
        self.player.animation["running"].add_frame(6,150,106)
        self.player.animation["running"].add_frame(1,217,106)
        self.player.animation["running"].add_frame(2,286,106)
        self.player.animation["running"].add_frame(3,346,106)
        self.player.animation["running"].add_frame(-1,58,550)
        self.player.animation["running"].add_frame(0,358,546)
        #
        self.player.animation["standing"].add_frame(1,12,20)
        self.player.animation["standing"].add_frame(2,57,20)
        self.player.animation["standing"].add_frame(3,102,20)
        self.player.animation["standing"].add_frame(4,147,20)
        #=====================================================
        
        #Init the platforms:
        
        self.platform = dict()
        #x,y,width,height,fallspeed
        self.platform[0] = Platform(10,300,400,10,0.5) # starting platform. Don't want to start off
                                                       # with a game over do we? 
        for i in range(25):
            self.platform[i] = Platform(randint(0,750),randint(0,599),randint(50,250),randint(8,30),float(randint(2,17)/10))
        
        """self.platform[1] = Platform(10 ,500,225,15,0.1)
        self.platform[2] = Platform(60 ,400,150,10,1.0)
        self.platform[3] = Platform(300,300,200,12,0.5)
        self.platform[4] = Platform(200,200,100,30,2.0)
        self.platform[5] = Platform(50 ,100,50 ,15,0.2)
        self.platform[6] = Platform(600,0  ,150,10,1.0)
        self.platform[7] = Platform(400,0  ,150,20,0.5)
        self.platform[8] = Platform(200,150,150,20,0.3)"""
        
        
        self.old_key = None
        self.current_key = "none"
        self.player_jumpheight = -8.5
        
        self.states["run_game"].ran = True
        
    def state_run_game(self):
        
        #so, each of the entities will be targetting the appropriate 'thing'
        #we will split this up into a few parts:
        self.screen.fill(self.bg_color)
        dog_collided = False
        #update keys and mouse
        self.update_mouse_location()
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            self.change_state("main_menu")
        
        self.score_info = self.myfont_info.render("Score: " + str(self.score), 1, (255,255,255))
        
        if self.score < 0:
            self.change_state("game_over")
        
        for i in self.game_events:
            self.game_events[i].loopMe()
        
        if self.player.location.y > self.height-2:
            grounded = True
        else:
            grounded = False
        
        for i in self.platform:
            if i in self.platform:
                if self.player.location.y < self.platform[i].y+2:
                    if self.player.location.x > self.platform[i].x and self.player.location.x < self.platform[i].x + self.platform[i].width:
                        if self.player.location.y + self.player.velocity.y > self.platform[i].y:
                            self.player.velocity.y = 0
                            self.player.location.y = self.platform[i].y
                            grounded = True
                        if self.player.location.y > self.platform[i].y-1 and self.player.location.y < self.platform[i].y+self.platform[i].speed:
                            grounded = True
                            self.player.location.y = self.platform[i].y
                
                self.platform[i].y += self.platform[i].speed
                if self.platform[i].y > self.height:
                    self.platform[i].y = -self.platform[i].height
        
        if grounded and not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]):
            self.player.velocity.x = 0
            self.current_key = "none"
        
        if keys[pygame.K_RIGHT]:
            self.player.direction = "right"
            self.player.velocity.x = self.player.run_speed
            if grounded:
                self.current_key = "leftright"
        elif keys[pygame.K_LEFT]:
            self.player.direction = "left"
            self.player.velocity.x = -self.player.run_speed
            if grounded:
                self.current_key = "leftright"
        else:
            self.player.velocity.x = 0
        
        if keys[pygame.K_UP]:
            if grounded:
                self.player.velocity.y = self.player_jumpheight
                
        if grounded and keys[pygame.K_DOWN]:
            self.player.location.y += 5
        
        if not grounded:
            self.player.velocity.y += 0.3
        
        if not self.old_key == self.current_key:
            self.old_key = self.current_key
            if self.current_key == "leftright":
                self.player.change_animation_state("running")
            elif self.current_key == "up":
                #self.player.change_animation_state("jumping")
                
                pass
            else:
                self.player.change_animation_state("standing")
                
        if self.player.location.y < 0:
            self.score += 0.5
            
        if self.player.location.y > self.height:
            self.player.location.y = self.height
            self.player.velocity.y = 0
        
        if self.player.location.y > self.height - 2:
            self.score -= 100
        
        if self.player.location.x > self.width:
            self.player.location.x = self.width
        
        if self.player.location.x < 0:
            self.player.location.x = 0
        
        self.player.update_location()
        
        #check for collision with platforms:
        
        self.player.loop_animation(self.game_counter_increment)
        
        player_image = self.player.current_image()
        self.screen.blit(player_image, ((self.player.location.x-player_image.get_width()/2,self.player.location.y-player_image.get_height())))
        self.screen.blit(self.score_info,(10,10))
        for i in self.platform:
            if i in self.platform:
                pygame.draw.rect(self.screen, self.platform[i].colour,self.platform[i].get_rect())
                pygame.draw.rect(self.screen, (0,75,120),self.platform[i].get_rect_next_width(),1)
                if not self.platform[i].next_width == self.platform[i].width:
                    pygame.draw.rect(self.screen, (255,0,0),pygame.Rect(self.platform[i].x+self.platform[i].next_width,self.platform[i].y,self.platform[i].width-self.platform[i].next_width,self.platform[i].height),1)
                
        
    def exit_state_run_game(self):
        """function to call when changing FROM run_game state"""
        self.channel_1.pause()
        
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
                
                #FSM: run our current state
                self.states[self.current_state].state_function()
                
                pygame.display.flip()

            else:
                pass # an event type we don't handle            


My_Game().run()
pygame.quit()
sys.exit()

