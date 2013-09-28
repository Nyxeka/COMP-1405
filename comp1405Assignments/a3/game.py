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
import ConfigParser

# end imports #######################

global direction = ["north", "south", "east", "west"] #we reference to this...

class player:
    lives_left = 10 #defaults to ten...

class world:
    lives_left = 10
    levels = []
    
    def add_level(self,level_to_add):
        self.levels += level

        
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
    
    def __init__(self, portal_index_list):
        self.room_num = index_num
       self.portal_index = portal_index_list
       
    def clear_room_info(self):
        self.room_info = []

class level:
    #collection of rooms.
    rooms = []
    portals = []
    end_room_index = 0
    
    def __init__(self, endRoomNum):
        self.end_room_index = endRoomNum
    
    def add_room(self,room_num, portal_list):
        self.rooms += [room(room_num, portal_list )]
    
    def add_portal(self, portal_num, portal_type, connected_rooms):
        portals += [portal(portal_num,portal_type,connected_rooms)]
    
    def room_intro(self,room_num):
        print "You look around."
        for i in range(4):
            if self.portal_index[i] == None:
                print "to the " + direction[i] + " is a wall"
            elif self.portal_index[i] == 0:
                print "to the " + direction[i] + " there is a barrier."
            elif self.portal_index[i] == 1:
                print "to the " + direction[i] + " there is a barrier with a desktop computer in front of it, on a desk."
                print "the computer screen has some text on it that says 'if you go in this direction, you must play my game.'"
            
        print "you may go in the direction(s):"
        for i in range(4):
            if portal_index[i] is not None:
                print direction[i]
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

def main():
    # main function
    
    
    
















