# TODO Take Bach MIDI files and get them in a usable format
# TODO Create initial random population
# TODO while (not done)
# TODO   Evaluate individuals
# TODO   Crossover elite individuals and generate next population
# TODO   Mutate (if needed)

import midiutil
import mido
import pygame

'''
The game plan:
  Jeremy will be in charge of finding out how to do evaluation
  Alex will work on midi util and all that
  Dustin will decide on note representation and individuals representation, and crossover, etc. reproduction

  We will meet in 2 days to confirm
'''


# note = [pitch (48-84), time(0-16), duration]
# individual = [16 notes]
# an individual is 16 beats, each beat can contain zero or more notes
# a note consists of a pitch and a duration




#_____________BASE FOR HOW TO ADD NOTES AND CREATE A MIDIFILE_________________#
"""
#Import the library
from midiutil.MidiFile import MIDIFile
 

# Create the MIDIFile Object with 1 track
MyMIDI = MIDIFile(1)
 

# Tracks are numbered from zero. Times are measured in beats.
track = 0   
time = 0
 

# Add track name and tempo.
MyMIDI.addTrackName(track,time,"Sample Track")
MyMIDI.addTempo(track,time,120)
 

# Add a note. addNote expects the following information:
track = 0
channel = 0
pitch = 60
time = 0
duration = 1
volume = 100
 

# Now add the note.
MyMIDI.addNote(track,channel,pitch,time,duration,volume)
 

# And write it to disk.
binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()
"""

#__________________HOW TO READ A MIDI FILE_____________#
'''
file = mido.MidiFile("bwv906a.mid")
for msg in file.play():
    print(msg)
'''

#___________________HOW TO PLAY A MIDI FILE_____________#
'''
pygame.init()
pygame.mixer.music.load("bwv906a.mid")
pygame.mixer.music.play(0)

while pygame.mixer.music.get_busy():
    pygame.event.poll()
'''