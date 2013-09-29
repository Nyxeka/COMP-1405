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

import os

# end imports #######################

direction = ["north", "south", "east", "west"] #we reference to this...

class portal:
    #portals between rooms:
    portal_index = None
    barrier_type = 0
    connected_rooms = []
    
    def __init__(self, portal_index, barrier_type, room_list):
        self.portal_index = portal_index
        self.barrier_type = barrier_type
        self.connected_rooms = room_list

class room:
    room_num = None
    
    portal_index = []
    
    def __init__(self, room_num, portal_index_list):
        self.room_num = room_num
        self.portal_index = portal_index_list
       
    def clear_room_info(self):
        self.room_info = []

class level:
    #collection of rooms.
    rooms = []
    portals = []
    end_room_index = 0
    
    #player stuff:
    current_room = 0
    current_life = 100
    
    def __init__(self, endRoomNum):
        self.end_room_index = endRoomNum
    
    def add_room(self,room_num, portal_list):
        self.rooms += [room(room_num, portal_list )]
    
    def add_portal(self, portal_num, portal_type, connected_rooms):
        self.portals += [portal(portal_num,portal_type,connected_rooms)]
    
    def set_end_room_index(self, end_room_index):
        self.end_room_index = end_room_index
    
    def room_intro(self, cur_room):
        print "------------------------------------------------------------------------"
        print "You look around.\n"
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
        print "\nYou may go in the direction(s):"
        for i in range(4):
            if cur_room.portal_index[i] is not None:
                print direction[i]
    
    def change_rooms(self, new_room):
        #I know this is bad coding but I'll put the following where it's supposed to be later...
        print ("------------------------------------------------------------------------\n"
               "You step towards the barrier and it begins to fade to black faster. as you pass through, "
               "it shatters like glass, the individual pieces fading to nothingness before they hit the "
               "ground. You feel the drain on your life force")
        self.current_room = new_room
        next = raw_input("Press Enter to continue")
        self.room_intro(self.rooms[self.current_room])
#done with object stuff...

def create_level():
    newLev = level(17)
    
    #first add the rooms
    newLev.add_room(0,[1, None, None, None])
    newLev.add_room(1,[None,1,2,None])
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
    newLev.add_portal(0, 2, [100,100])
    newLev.add_portal(1, 2, [0,1])
    newLev.add_portal(2, 0, [1,2])
    newLev.add_portal(3, 0, [2,3])
    newLev.add_portal(4, 0, [3,4])
    newLev.add_portal(5, 0, [4,5])
    newLev.add_portal(6, 0, [5,6])
    newLev.add_portal(7, 1, [7,6])
    newLev.add_portal(8, 1, [2,7])
    newLev.add_portal(9, 0, [2,8])
    newLev.add_portal(10, 0, [8,9])
    newLev.add_portal(11, 0, [9,10])
    newLev.add_portal(12, 0, [10,12])
    newLev.add_portal(13, 0, [6,11])
    newLev.add_portal(14, 0, [11,12])
    newLev.add_portal(15, 0, [12,13])
    newLev.add_portal(16, 0, [10,14])
    newLev.add_portal(17, 0, [15,14])
    newLev.add_portal(18, 0, [13,16])
    newLev.add_portal(19, 0, [16,15])
    newLev.add_portal(20, 0, [14,17])
    
    newLev.set_end_room_index(17)
    
    return newLev
    

def playGame(difficulty, newLev):
    print "play game"

def showIntroMenu():
    print "intro menu c:"