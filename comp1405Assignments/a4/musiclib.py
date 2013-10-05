"""
Assignment 4: Music Library
By Nicholas Hylands

NOTE: since it was made explicitly clear in the assignment page that everything should be
case INSENSITIVE, there will be no "S" function, only an "s" function.

"""
import os
from mutagen.mp3 import MP3

help_message = """
Search through the music library with these commands:
st [SEARCH TERM] <- search for track's with [SEARCH TERM] in them
sa [SEARCH TERM] <- search for artists with [SEARCH TERM] in them
s [SEARCH TERM] <- search for albums with [SEARCH TERM] in them
exit <- exit the search function
"""

class Track:
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
    artist = ""
    title = ""
    year = ""
    list_of_tracks = []
    genre = ""
    
    def __init__(self, artist, title, year='',genre='',tracks=None):
        self.artist= artist
        self.title = title
        self.year = year
        self.genre = genre
        self.list_of_tracks += tracks
    
    def add_track(self, track):
        self.list_of_tracks += track
    
    def __str__(self):
        return "Album: " + self.title + ", by: " + self.artist

def music_library(tracks, albums):
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
            print "There was an Error: " + sys.exc_info()[0]

def load_library(dir="."):
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
            if filename.lower().endswith(".mp3"):
                fullname = os.path.join(root, filename)
                #print "\n%s" % fullname
                
                try:
                    audio = MP3(fullname)
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
                    
                    
                    if not album_title in albums:
                        albums.update({album_title: Album(track_artist, album_title, track_year, track_genre,track_to_add)})
                    elif album_title in albums:
                        albums[album_title].add_track(track_to_add)
                except:
                    #print "Error on %s" % fullname
                    pass
    for i,c in albums.items():
        albums2 += [c]
    return [tracks, albums2]