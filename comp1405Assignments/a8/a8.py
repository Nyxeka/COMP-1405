"""

"""



from __future__ import division
import math
import sys
import pygame

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
    def __init__(self, image, anim_width, anim_height, framerate = 0.1):
        self.image = image
        self.anim_width = anim_width
        self.anim_height = anim_height
        self.num_frames = 0
        self.frame_locations = dict()
        self.current_frame = 1
        self.anim_timer = 0
        self.anim_framerate = framerate
        
    def add_frame_location(self,frame_number,x,y):
        self.frame_locations[frame_number] = Vector(x,y)
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
    def __init__(self, interval_time, event_function, loop_type = -1):
        self.interval_time = interval_time
        self.event_function = event_function
        self.timer = 0.0
        
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
        self.REFRESH = pygame.USEREVENT+1
        pygame.time.set_timer(self.REFRESH, 1000//self.FPS)
        #=============================================
        
        
        
        #_____________________________________________
        #FSM: init different states
        #init states for our finite state machine.
        #because I decided not to add a State object, I'm just gonna do this stuff here...
        #so, if you plan on using this, remember that you should be creating a state object
        self.states = dict()
        self.states["main_menu"] = State(self.state_main_menu)
        self.states["run_game"] = State(self.state_run_game, self.enter_state_run_game, self.exit_state_run_game, self.enter_state_first_time_run_game)
        #=============================================
        
        #_____________________________________________
        #Set up for the main_menu state
        #---
        #set up our font renderer
        self.myfont = pygame.font.SysFont("courier", 25)
        
        #---
        self.menu_buttons = dict()
        self.menu_buttons["Play_Game"] = Button("Play Game", self.button_event_play_game,self.myfont,1)
        self.menu_buttons["Continue_Game"] = Button("Continue Game", self.button_event_continue_game,self.myfont, 2)
        self.menu_buttons["Options"] = Button("Options", self.button_event_options,self.myfont, 3)
        self.menu_buttons["Exit"] = Button("Exit", sys.exit,self.myfont, 4)
        #=============================================
        
        #_____________________________________________
        #Set up our game events
        #really I should have an event object with the function set in the init but
        #don't feel like thinking about that right now....
        #so, if you plan to use this in any way, instead of doing this, just make
        #an event object and stick them in a dict or something...
        #---
        #basically, these happen every <interval> amount of time.
        #---
        self.game_events = dict()
        self.game_time = 0.0
        #for each of the following, the index will be the amount of time it takes for 
        #each event to happen (the interval), and the element in the array it points to 
        #will be a counter that goes up to this, so should always be set to zero.
        #the second element in the array will be the function it calls every interval.
        self.game_events["add_score"] = Game_Event(1.0, self.game_event_add_score)
        #=============================================
        
        #_____________________________________________
        #Init stuff
        #---
        #debug?
        self.debug_log = False
        #---
        #background colour:
        self.bg_color = 128,128,128
        #font for debug info stuff
        self.myfont_info = pygame.font.SysFont("courier", 15)
        #---
        self.game_counter_increment = 1/self.FPS
        #---
        self.current_state = "main_menu"
        self.pause = False
        self.pause_timer = 3.0
        #-1 to play the loop indefinitely. 
        #self.channel_1 = self.sound_music.play(-1)
        self.update_mouse_location()
        self.old_button_down = False
        self.button_down = False
        #=============================================
        
    def game_event_add_score(self):
        self.score += 100
        
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
        pass
    
    def button_event_options(self):
        pass
        
    def button_event_play_game(self):
        self.change_state("run_game")
    
    def change_state(self,new_state):
        if new_state in self.states:
            self.states[self.current_state].exit_state_function()
            if not self.states[new_state].ran:
                self.states[new_state].enter_state_first_time()
            self.states[new_state].enter_state_function()
            self.current_state = new_state
        else:
            print "ERROR: STATE '" + str(new_state) + "' DOES NOT EXIST."
    
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
        pass
    
    def enter_state_first_time_run_game(self):
        """function to call when running run_game for the first time..."""
        
        #first, initiate entities.
        #Entity(self, name, x=0, y=0, vel_x=0,vel_y=0):
        self.player_sprite_sheet = pygame.image.load("i8aic.png")
        self.player_sprite_sheet.set_colorkey((0,128,128))
        self.player = Entity("Player",200,200)
        self.player.add_animation("running",Animation(self.player_sprite_sheet,52,65,0.06))
        #_____________________________________________________
        #start adding where the frames are on the sprite sheet
        self.player.animation["running"].add_frame_location(1,7,106)
        self.player.animation["running"].add_frame_location(2,80,106)
        self.player.animation["running"].add_frame_location(3,150,106)
        self.player.animation["running"].add_frame_location(4,217,106)
        self.player.animation["running"].add_frame_location(5,286,106)
        self.player.animation["running"].add_frame_location(6,346,106)
        #=====================================================
        
        
        
    def state_run_game(self):
        
        #so, each of the entities will be targetting the appropriate 'thing'
        #we will split this up into a few parts:
        self.screen.fill(self.bg_color)
        dog_collided = False
        #update keys and mouse
        self.update_mouse_location()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.direction = "right"
            self.player.animation_state = "running"
        elif keys[pygame.K_LEFT]:
            self.player.direction = "left"
            self.player.animation_state = "running"
        else:
            self.player.animation_state = "running"
        
        self.player.loop_animation(self.game_counter_increment)
        
        self.screen.blit(self.player.current_image(), ((self.player.location.x,self.player.location.y)))
        
    def exit_state_run_game(self):
        """function to call when changing FROM run_game state"""
        pass
        
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

