"""
Assignment 4: Music Library
By Nicholas Hylands

"""
import os
from mutagen.mp3 import MP3

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
    command = ""
    while not command.lower() == "exit":
        try:
            command = raw_input("Enter a command (s, sa, st, help, or exit): ")
            command = command.lower()
            if command[:2] == "s ":
                print "All albums with '" + command[2:] + "' in them:"
                for i,c in albums.items():
                    if command[2:] in c.title.lower():
                        print c.__str__()
            if command[:2] == "sa":
                print "All artists with '" + command[3:] + "' in them:"
                for i,c in albums.items():
                    if command[3:] in c.artist.lower():
                        print c.artist
            if command[:2] == "st":
                print "All songs with '" + command[3:] + "' in them:"
                for i,c in tracks.items():
                    if command[3:] in c.title.lower():
                        print i
            if command[:4] == "help":
                print "Search through the music library with these commands:"
                print "st [SEARCH TERM] <- search for track's with [SEARCH TERM] in them"
                print "sa [SEARCH TERM] <- search for artists with [SEARCH TERM] in them"
                print "s [SEARCH TERM] <- search for albums with [SEARCH TERM] in them"
                print "exit <- exit the search function"
        except:
            print "error in input."

def load_library(dir="."):
    failed = False
    tracks = []
    albums = {}
    for root, dirs, files in os.walk(dir):
        
        for filename in files:
            if filename.lower().endswith(".mp3"):
                fullname = os.path.join(root, filename)
                #print "\n%s" % fullname
                
                try:
                    audio = MP3(fullname)
                    track_to_add = [Track(str(audio['TPE1']),str(audio['TIT2']),str(audio['TALB']))]
                    tracks += track_to_add
                    if not str(audio['TALB']) in albums:
                        albums.update({str(audio['TALB']): Album(str(audio['TPE1']),str(audio['TALB']),str(audio['TDRC']), str(audio['TCON']),track_to_add)})
                    elif str(audio['TALB']) in albums:
                        albums[str(audio['TALB'])].add_track(track_to_add)
                except:
                    #print "Error on %s" % fullname
                    pass
                
    return [tracks, albums]