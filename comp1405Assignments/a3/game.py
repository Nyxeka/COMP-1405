"""
I want to play a game.
By Nicholas Hylands

Everything in this project was created by Nicholas Hylands,
unless otherwise stated around a block of code not created
by Nicholas Hylands.

Comp-1405-b Assignment number 3
Text-based dungeon crawler in python.

"""

# imports ###########################
from __future__ import division
import os, sys, time, random

# end imports #######################

map = """
MAP:
    03--04--05
    ||      ||
01--02--07--06--11     00:          start room
^^  ||          ||     17:          end room
00  08--09--10>>12     <<,>>,^^,vv: one-way barrier
            ||  ||     --,||:       normal barrier
        17<<14  13
            ||  ||
            15--16
"""

help_message = """
COMMANDS:
_____________________
DIRECTIONAL_COMMANDS:
NORTH: move north
SOUTH: move south
EAST: move east
WEST: move west
_____________________
OTHER_COMMANDS:
HELP: display this help message
MAP: display a map of the level
EXIT: quit the game
"""

game_over_message = """
 _____   ___  ___  ___ _____   _____  _   _ ___________ 
|  __ \ / _ \ |  \/  ||  ___| |  _  || | | |  ___| ___ \
| |  \// /_\ \| .  . || |__   | | | || | | | |__ | |_/ /
| | __ |  _  || |\/| ||  __|  | | | || | | |  __||    / 
| |_\ \| | | || |  | || |___  \ \_/ /\ \_/ / |___| |\ \ 
 \____/\_| |_/\_|  |_/\____/   \___/  \___/\____/\_| \_|
"""

win_message = """
 _    _ _____ _   _ _   _ ___________ 
| |  | |_   _| \ | | \ | |  ___| ___ \
| |  | | | | |  \| |  \| | |__ | |_/ /
| |/\| | | | | . ` | . ` |  __||    / 
\  /\  /_| |_| |\  | |\  | |___| |\ \ 
 \/  \/ \___/\_| \_|_| \_|____/\_| \_|
"""

debug = False

BARRIER_TYPE_NORMAL = 0
BARRIER_TYPE_CHALLENGE = 1
BARRIER_TYPE_ONE_WAY = 2
BARRIER_TYPE_FINISH = 3

direction = ["north", "south", "east", "west"] #we reference to this...

# come up with commands and put them here to compare with when we want the users input:
command_list = ["NORTH", "SOUTH", "EAST", "WEST", "HELP", "EXIT", "MAP"]

class portal:
    #portals between rooms:
    portal_index = None
    barrier_type = 0
    connected_rooms = [] #for checking in order.
                         #if a portal is one-way, only put the portal index in one
    
    def __init__(self, portal_index, barrier_type, room_list):
        self.portal_index = portal_index
        self.barrier_type = barrier_type
        self.connected_rooms = room_list

class room:
    #room object. has an index of portals
    room_num = None
    
    #portal_index is a NSEW list of the portals' indexes in the room.
    portal_index = []
    
    def __init__(self, room_num, portal_index_list):
        self.room_num = room_num
        self.portal_index = portal_index_list
       
    def clear_room_info(self):
        self.room_info = []

class level:
    #collection of rooms and portals, basically contains player as well.
    rooms = []
    portals = []
    end_room_index = 0
    difficulty = 5
    
    #player stuff:
    current_room = 0
    current_life = 100
    
    #life drain when switch rooms.
    life_drain = 1
    
    def __init__(self, endRoomNum, difficulty):
        self.end_room_index = endRoomNum
        self.difficulty = difficulty
        self.current_life = int(20 + (50 / difficulty))
        life_drain = int(((10 - difficulty) / 5) + 1)
        #self.difficulty = difficulty
    
    def add_room(self,room_num, portal_list):
        self.rooms += [room(room_num, portal_list )]
    
    def add_portal(self, portal_num, portal_type, connected_rooms):
        self.portals += [portal(portal_num,portal_type,connected_rooms)]
    
    def set_end_room_index(self, end_room_index):
        self.end_room_index = end_room_index
        
    def drain_life(self, amount):
        self.current_life = self.current_life - amount
    
    def room_intro(self, cur_room):
        print "\n"
        print "You look around...\n"
        time.sleep(0.8)
        #check the surrounding walls for portals.
        #we want to tell the user where they are, and what type of portal it is...
        for i in range(4):
            if cur_room.portal_index[i] == None:
                print "To the " + direction[i] + " is a wall"
            elif self.portals[cur_room.portal_index[i]].barrier_type == 0:
                print "To the " + direction[i] + " there is a barrier."
            elif self.portals[cur_room.portal_index[i]].barrier_type == 1:
                print "To the " + direction[i] + " there is a barrier with a desktop computer in front of it, on a desk."
                print "The computer screen has some text on it that says 'if you go in this direction, you must play my game.'"
            elif self.portals[cur_room.portal_index[i]].barrier_type == 2:
                print "To the " + direction[i] + " there is a one-way barrier."
            elif self.portals[cur_room.portal_index[i]].barrier_type == 3:
                print "To the " + direction[i] + " IS THE END."
            print "\n"
            time.sleep(0.5)
        print "The number on the floor says: " + str(cur_room.room_num)
        #clarify the user...
        print "\nYou may go in the direction(s):"
        for i in range(4):
            if cur_room.portal_index[i] is not None:
                print direction[i]
                time.sleep(0.5)
                
    def change_rooms(self, new_room_index): #move the player to a new room.
        time.sleep(1)
        self.drain_life(self.life_drain)
        self.current_room = new_room_index
        self.room_intro(self.rooms[self.current_room])
    
    def play_challenge(self, floor_number): #let the user run the challenge
        #lots to do here...
        #GAMES:
        #which game is layed is decided by the floor_number entered.
        #from 0 to 6, we will go for simple double-digit addition questions(get 2/3 right)
        #from 7 to 13: guess my number 2**floor_number
        #from 14 to 20: addition/subtraction triple digit. (get 3/5 right)
        print "You walk towards the computer desk and sit down. as you sit,\na console appears on the computer screen."
        print "On the console, it says:"
        time.sleep(1.5)
        if floor_number < 7:
            self.play_easy_challenge(floor_number)
        elif floor_number >= 7 and floor_number < 14:
            self.play_medium_challenge(floor_number)
        elif floor_number >= 14:
            self.play_hard_challenge(floor_number)
    
    def play_easy_challenge(self, floor_number):
        print """
This will be a simple two-digit number addition challenge.
I will ask you three questions. get two out of three to pass without losing life-points
Get three out of three correct to pass, gaining 3x life-points usually drained.
get 1/3 right and lose the usual amount of lifepoints while passing a barrier
get none right, and all of the surrounding barriers in your room will shatter.
"""
        go = raw_input("Press Enter to continue and start the challenge.")
        numCorrect = 0
        for i in range(3):
            a = random.randrange(1,100)
            b = random.randrange(1,100)
            answer = str(a+b)
            print "Question %d" % (i+1)
            guess = raw_input(str(a) + " + " + str(b) + " = ")
            if guess == answer:
                numCorrect += 1
                time.sleep(0.5)
                print "Correct!"
            else:
                print "Incorrect! The correct answer was " + str(answer)
        if numCorrect == 0:
            print "Unfortunately, you answered all of the questions wrong."
            time.sleep(1)
            print "All of the barriers around you flash to black and shatter as you"
            print "make your way to the next room"
            for i in self.rooms[self.current_room].portal_index:
                if i is not None:
                    self.drain_life(self.life_drain)
        elif numCorrect == 1:
            print ("\nYou step towards the barrier and it begins to fade to black faster. as you pass through,\n"
                               "it shatters like glass, the individual pieces fading to nothingness before they hit the\n"
                               "ground. You feel the drain on your life force.\n")
            time.sleep(1)
        elif numCorrect == 2:
            self.drain_life(-self.life_drain)
            print "You answered 2 out of 3 questions right. you will move on unpenalized."
            print "\nYou continue your journey, passing through the invisible barrier, which snaps"
            print "back into place after you step inside the room."
            time.sleep(1)
        elif numCorrect == 3:
            print "You answered all three questions correctly. Enjoy your reward."
            print "\nYou continue your journey, passing through the invisible barrier, which snaps"
            print "back into place after you step inside the room. You feel your health replenish slightly."
            self.drain_life(-3 * self.life_drain)
            time.sleep(1)
    
    def play_medium_challenge(self, floor_number):
        print """
Your challenge will be a guess my number game.
I will give you a number between 1 and x where x is 2 to the exponent <your floor number>
if you guess too low, you will be told to guess higher.
if you guess too high, you will be told to guess lower.
You have as many guesses as you do your floor number to pass this challenge and be awarded
3x the usual life points drained by passing a barrier.
If your guesses surpass your floor number, you have failed the test.
If your guesses are under your floor number, you will get a bonus.

"""
        raw_input("Press Enter to continue.")
        numGuesses = 0
        maximum = int(2.0**floor_number)
        answer = random.randrange(1,maximum)
        print "I have chosen a number between 1 and " + str(maximum)
        for i in range(floor_number+2):
            guess = raw_input("Please enter your guess: ")
            guess = int(guess)
            numGuesses += 1
            print "You guessed: " + str(guess)
            try:
                if guess == answer:
                    break
                if guess > answer:
                    print "Your guess was too high"
                if guess < answer:
                    print "Your guess was too low"
            except ValueError:
                print "Please input a number."
        if answer == guess:
            print "You got the correct answer in " + numGuesses + " guesses."
            print "You will be rewarded."
            self.drain_life((-3 * self.life_drain) + floor_number - numGuesses)
        else:
            print "You did not pass the test."
            print "The answer was: " + str(answer)
            time.sleep(1)
            print "All of the barriers around you flash to black and shatter as you"
            print "make your way to the next room"
            for i in self.rooms[self.current_room].portal_index:
                if i is not None:
                    self.drain_life(self.life_drain)
                        
    def play_hard_challenge(self, floor_number):
        print """
This will be a three-digit addition game.
get 3/5 of the answers right to pass.
Get 4/5 or 5/5 
"""
        go = raw_input("Press Enter to continue and start the challenge.")
        numCorrect = 0
        for i in range(3):
            a = random.randrange(1,1000)
            b = random.randrange(1,1000)
            answer = str(a+b)
            print "Question %d" % (i+1)
            guess = raw_input(str(a) + " + " + str(b) + " = ")
            if guess == answer:
                numCorrect += 1
                time.sleep(0.5)
                print "Correct!"
            else:
                print "Incorrect! The correct answer was " + str(answer)
        if numCorrect  == 0:
            print "Unfortunately, you answered all of the questions wrong."
            time.sleep(1)
            print "All of the barriers around you flash to black and shatter as you"
            print "make your way to the next room"
            for i in self.rooms[self.current_room].portal_index:
                if i is not None:
                    self.drain_life(self.life_drain)
        elif numCorrect <= 3 and numCorrect > 0:
            self.drain_life(-self.life_drain)
            print "You answered between 1 and 3 questions right. you will move on unpenalized."
        elif numCorrect > 3:
            print "You answered more than 3 questions correctly. Enjoy your reward."
            #default reward plus 1 if you got 5/5
            self.drain_life((-3 * self.life_drain) + ((-1 * self.life_drain * numCorrect) - 4))
                        
        
#done with class stuff...

def create_level(difficulty):
    #function to create and initialize our level
    newLev = level(17,difficulty)
    
    #first add the rooms
    newLev.add_room(0,[1, None, None, None])
    newLev.add_room(1,[None,None,2,None])
    newLev.add_room(2,[3,9,8,2])
    newLev.add_room(3,[None,3,4,None])
    newLev.add_room(4,[None,None,5,4])
    newLev.add_room(5,[None,6,None,5])
    newLev.add_room(6,[6,None,13,7])
    newLev.add_room(7,[None,None,7,8])
    newLev.add_room(8,[9,None,10,None])
    newLev.add_room(9,[None,None,11,10])
    newLev.add_room(10,[None,16,13,11])
    newLev.add_room(11,[None,14,None,13])
    newLev.add_room(12,[14,15,None,None])
    newLev.add_room(13,[15,18,None,None])
    newLev.add_room(14,[16,17,None,20])
    newLev.add_room(15,[17,None,19,None])
    newLev.add_room(16,[18,None,None,19])
    newLev.add_room(17,[None,None,None,None])
    #now add the portals:
    #add_portal(self, portal_num, portal_type: 0,1,2,3 connected_rooms: must be in order if one-way)
    #barrier types:
    #0 - normal barrier
    #1 - challenge barrier
    #2 - one-way barrier
    #3 - the barrier leading to the end game room.
    newLev.add_portal(0, BARRIER_TYPE_ONE_WAY, [100,100]) #forgot to add 0 as I drew the level map. oh well.
    newLev.add_portal(1, BARRIER_TYPE_ONE_WAY, [0,1])
    newLev.add_portal(2, BARRIER_TYPE_NORMAL, [1,2])
    newLev.add_portal(3, BARRIER_TYPE_NORMAL, [2,3])
    newLev.add_portal(4, BARRIER_TYPE_NORMAL, [3,4])
    newLev.add_portal(5, BARRIER_TYPE_NORMAL, [4,5])
    newLev.add_portal(6, BARRIER_TYPE_NORMAL, [5,6])
    newLev.add_portal(7, BARRIER_TYPE_CHALLENGE, [7,6])
    newLev.add_portal(8, BARRIER_TYPE_CHALLENGE, [2,7])
    newLev.add_portal(9, BARRIER_TYPE_NORMAL, [2,8])
    newLev.add_portal(10, BARRIER_TYPE_NORMAL, [8,9])
    newLev.add_portal(11, BARRIER_TYPE_CHALLENGE, [9,10])
    newLev.add_portal(12, BARRIER_TYPE_NORMAL, [10,12])
    newLev.add_portal(13, BARRIER_TYPE_NORMAL, [6,11])
    newLev.add_portal(14, BARRIER_TYPE_NORMAL, [11,12])
    newLev.add_portal(15, BARRIER_TYPE_NORMAL, [12,13])
    newLev.add_portal(16, BARRIER_TYPE_CHALLENGE, [10,14])
    newLev.add_portal(17, BARRIER_TYPE_NORMAL, [15,14])
    newLev.add_portal(18, BARRIER_TYPE_CHALLENGE, [13,16])
    newLev.add_portal(19, BARRIER_TYPE_NORMAL, [16,15])
    newLev.add_portal(20, BARRIER_TYPE_FINISH, [14,17])
    
    newLev.set_end_room_index(17)
    
    return newLev
    

def playGame(newLev):
    #basically the main function. 
    #the game happens in this function.
    global debug
    newLev.room_intro(newLev.rooms[newLev.current_room])
    running = True #if we ever want to stop...
    lost = False
    #a check we do in the loop. if false, it will skip through the loop and return to
    #asking for the command
    command_entered = False
    command = ""
    while running:
        command_entered = False
        command_debug = False
        print "\nYou have " + str(newLev.current_life) + " life points left"
        os.system("title " + "Current lifepoints left: " + str(newLev.current_life))
        if newLev.current_life <= 0:
            break
            lost = True
        
        try:
            command = raw_input("\nPlease enter a command: ")
            if command.upper() in command_list:
                command_entered = True
            if debug and command[0:4] == "GOTO":
                command_debug = True
                print "debuggezz"
        except ValueError: #just in case...
            print "ValueError: please type a string >_>"
        #now we want to check the command, and do stuff about it!
        if command_entered == True:
            command = command.upper()
            #if it's a directional command:
            if command_list.index(command) < 4:
                
                if newLev.rooms[newLev.current_room].portal_index[direction.index(command.lower())] is not None:
                    
                    new_portal_index = newLev.rooms[newLev.current_room].portal_index[direction.index(command.lower())]
                    newRoom = (newLev.portals[new_portal_index].connected_rooms.index(newLev.current_room)+1) % len(newLev.portals[new_portal_index].connected_rooms)
                    #check to see if barrier requires a challenge:
                    if newLev.portals[new_portal_index].barrier_type == 1:
                        #came up to a challenge!
                        newLev.play_challenge(newLev.current_room)
                    elif newLev.portals[new_portal_index].barrier_type == 3:
                        #Game over, user wins
                        print "You have found the end!"
                        print "You made it with " + str(newLev.current_life) + " lifepoints left!"
                        os.system("cls")
                        print win_message
                        raw_input("\n\nPress Enter to quit")
                        break
                    else:
                        #since nothing special, just make the move
                        print ("\nYou step towards the barrier and it begins to fade to black faster. as you pass through,\n"
                               "it shatters like glass, the individual pieces fading to nothingness before they hit the\n"
                               "ground. You feel the drain on your life force.\n")
                        time.sleep(1)
                    newLev.change_rooms(newLev.portals[new_portal_index].connected_rooms[newRoom])
                else:
                    print "\nYou may not go in that direction.\n"
            if command == "HELP":
                print help_message
            if command == "MAP":
                print map
            if command == "EXIT":
                print "Exit called, quitting."
                break
        if command_debug:
            if command[0:4] == "GOTO":
                print "changing rooms..."
                newLev.change_rooms(int(command[5:]))
    if lost:
        os.system(cls)
        print game_over_message
        raw_input("Press Enter to Quit.")
        
    

def showIntroMenu():
    global debug
    """print "I"
    time.sleep(0.4)
    os.system("cls")
    print "I want"
    time.sleep(0.2)
    os.system("cls")
    print "I want to"
    time.sleep(0.4)
    os.system("cls")
    print"I want to play"
    time.sleep(0.1)
    os.system("cls")
    print "I want to play a"
    time.sleep(0.4)
    os.system("cls")
    print "I want to play a game"
    time.sleep(0.6)
    os.system("cls")
    print "I want to play a game."
    time.sleep(0.8)
    os.system("cls")
    print "I want to play a game.."
    time.sleep(1)
    os.system("cls")
    print "I want to play a game..."
    time.sleep(2.5)"""
    print """
 _   _                _         
| \ | |              | |        
|  \| |_   ___  _____| | ____ _ 
| . ` | | | \ \/ / _ \ |/ / _` |
| |\  | |_| |>  <  __/   < (_| |
\_| \_/\__, /_/\_\___|_|\_\__,_|
        __/ |                   
       |___/                    

Welcome, and thank you for playing Nyxeka's Game!

This is a bit of a maze-exploring game. Your character is stuck
inside of a room, in a level created as some sort of test by 
some sort of overpowering diety for the fun of it.

The goal of the game is to get to the end without losing all of
your life-points. You will start with 100 life-points, in a room.

A room has four sides. each side either has a barrier or a wall.
A barrier is similar to a holographic pane of glass. As you get 
closer to a barrier, it darkens until it becomes pitch-black, then
shatters like glass, quickly fading before hitting the ground.
In order to pass some barriers, you must beat a 
challenge/game, which will be timed. 

Every time you pass through a barrier, it will
shatter. Every time you lose a challenge, all of the barriers in 
the room will shatter. If you win a challenge, you will be awarded
4 life points.

Every time a barrier shatters, it will zap back into exsistence
once there is nothing blocking the way.

To get to the end of the level, you must traverse between rooms
until you find the end room. To move between rooms, simply enter
the commands: "North", "South", "East", or "West". commands are 
not case sensitive.

Please select your difficulty level (an integer between 0 and 10:
 
 """
    difficulty = raw_input("Difficulty ranges from 0 (easiest) to 10 (hardest): ")
    if difficulty == "debug":
        debug = True
        print "debug enabled: " + str(debug)
    try: 
        newdif = int(difficulty)
    except ValueError:
        print "please enter a number between 0 and 10 >_>"
        difficulty = raw_input("Difficulty ranges from 0 (easiest) to 10 (hardest): ")
        try: 
            newdif = int(difficulty)
        except ValueError:
            print "Or whatever. defaulting to 5."
            newdif = 5
    newdif = newdif % 10
    newdif = max(1, newdif)
    print "\nYou start your journey... Opening your eyes, you realize that you are laying down."
    print "you stand."
    time.sleep(1)
    print "---------------------------------------------"
    return newdif
    
def main():
    os.system("cls")
    playGame(create_level(showIntroMenu()))

if __name__ == "__main__":
    main()