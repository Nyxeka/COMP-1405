"""
Assignment 4: Music Library
By Nicholas Hylands
https://www.github.com/Nyxeka/

NOTE: since it was made explicitly clear in the assignment page that everything should be
case INSENSITIVE, there will be no "S" function, only an "s" function.

"""
import os
import sys
#all of the mutagen files for the bonus question:
from mutagen.mp3 import MP3
from mutagen.ogg import OggFileType
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.asf import ASF
from mutagen.apev2 import APEv2

#since we use it twice, we'll stick it here.
help_message = """
Search through the music library with these commands:
st [SEARCH TERM] <- search for track's with [SEARCH TERM] in them
sa [SEARCH TERM] <- search for artists with [SEARCH TERM] in them
s [SEARCH TERM] <- search for albums with [SEARCH TERM] in them
exit <- exit the search function
"""

class Track:
    #track class, has simple info about each music file
    #also has a string representation, in case we want to print it
    artist = ""
    title = ""
    album = None
    def __init__(self, artist, title, album=None):
        self.artist = artist
        self.title = title
        self.album = album
    
    def __str__(self):
        return "Track: " + self.title + ", by: " + self.artist
    
    def set_album(self, album):
        self.album = album
    
class Album:
    #album class, has simple info and a list of its tracks
    #also has a string representation, incase we want to print it
    artist = ""
    title = ""
    year = ""
    list_of_tracks = []
    genre = ""
    #tracks2 because testing error...
    def __init__(self, artist, title, year='',genre='',tracks2=None):
        self.artist= artist
        self.title = title
        self.year = year
        self.genre = genre
        #THIS WAS THE PROBLEM RIGHT HERE:
        #used to be a +=, now it's an =
        self.list_of_tracks = tracks2
    
    def add_track(self, track):
        self.list_of_tracks += track
    
    def __str__(self):
        return "Album: " + self.title + ", by: " + self.artist
    
    def print_tracks(self):
        print self.__str__() + ":"
        for i in self.list_of_tracks:
            print "    " + i

def music_library(tracks, albums):
    #this is our search function. We use this to search through our media library
    command_origin = ""
    global help_message
    while not command_origin.lower() == "exit":
        try:
            command_origin = raw_input("Enter a command (s, sa, st, help, or exit): ")
            command = command_origin.lower()
            
            if command_origin[:2] == "S ":
                print "All tracks and albums with '" + command[2:] + "' in them:"
                for i in albums:
                    if command[2:] in i.title.lower():
                        print "  " + i.__str__()
                for i in tracks:
                    if command[2:] in i.title.lower():
                        print "  " + i.__str__()
                print ""
                continue
            elif command[:2] == "s ":
                print "All albums with '" + command[2:] + "' in them:"
                for i in albums:
                    if command[2:] in i.title.lower():
                        print "  " + i.__str__()
                print ""
                continue
            elif command[:2] == "sa":
                print "All artists with '" + command[3:] + "' in them:"
                for i in albums:
                    if command[3:] in i.artist.lower():
                        print "  " + i.artist
                print ""
                continue
            elif command[:2] == "st":
                print "All songs with '" + command[3:] + "' in them:"
                for i in tracks:
                    if command[3:] in i.title.lower():
                        print "  " + i.__str__()
                print ""
                continue
            elif command[:4] == "exit":
                break
            elif command[:4] == "help":
                print help_message
                continue
            else:
                print help_message
        except:
            print "There was an Error: " + str(sys.exc_info()[0])

# some code in the load_library function was taken from the assignment page:
"""
ORIGINAL CODE:

import os
from mutagen.mp3 import MP3

for root, dirs, files in os.walk("."):
    for filename in files:
        if filename.lower().endswith(".mp3"):
            fullname = os.path.join(root, filename)
            print "\n%s" % fullname
            try:
                audio = MP3(fullname)
                for key in audio:
                    print "  %s: %s" % (key, str(audio[key]))
            except:
                print "Error on %s" % fullname

"""
def load_library(dir="."):
    #this function will basically search through all the music files in a directory
    #and return the albums and tracks.
    failed = False
    tracks = []
    albums = {}
    albums2 = []
    album_title = ""
    track_title = ""
    track_year = ""
    track_genre = ""
    track_artist = ""
    for root, dirs, files in os.walk(dir):
        
        for filename in files:
            fullname = os.path.join(root, filename)#put this up here...
            
            try:
                #check for file-type...
                if filename.lower().endswith(".mp3"):
                    audio = MP3(fullname)
                elif filename.lower().endswith(".ogg"):
                    audio = OggFileType(fullname)
                elif filename.lower().endswith(".flac"):
                    audio = FLAC(fullname)
                elif filename.lower().endswith(".apev2"):
                    audio = APEv2(fullname)
                elif filename.lower().endswith(".mp4"):
                    audio = MP4(fullname)
                elif filename.lower().endswith(".asf"):
                    audio = ASF(fullname)
                else:
                    continue
                
                #now since some of the mp3's given don't have certain ID3 tags...
                #if they don't, they won't end up in the dictionary, so we will
                #just set them to be empty
                #really what I should be doing here is saying:
                #if 'TALB' in audio:
                #but whatever.
                try:
                    album_title = str(audio['TALB'])
                except KeyError:
                    album_title = ""
                try:
                    track_title = str(audio['TIT2'])
                except KeyError:
                    track_title = ""
                try:
                    track_year = str(audio['TDRC'])
                except KeyError:
                    track_year = ""
                try:
                    track_genre = str(audio['TCON'])
                except KeyError:
                    track_genre = ""
                try:
                    track_artist = str(audio['TPE1'])
                except KeyError:
                    track_artist = ""
                
                track_to_add = [Track(track_artist, track_title, album_title)]
                
                tracks += track_to_add
                # here we are going to check for when something is empty...
                
                #we are using a dictionary for album because it makes it easier to check and 
                #see if an album already exists.
                if not album_title in albums:
                    albums[album_title] = Album(track_artist, album_title, track_year, track_genre,track_to_add)
                    print str(len(albums[album_title].list_of_tracks))
                elif album_title in albums:
                    albums[album_title].list_of_tracks += track_to_add
            except:
                #print "Error on " + fullname + ": " + str(sys.exc_info()[0])
                pass
    #since we are done with searching for album names, we can convert albums to a list:
    for i,c in albums.items():
        albums2 += [c]
    return [tracks, albums2]