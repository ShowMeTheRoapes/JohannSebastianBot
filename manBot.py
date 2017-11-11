# TODO Take Bach MIDI files and get them in a usable format
# TODO Create initial random population
# TODO while (not done)
# TODO   Evaluate individuals
# TODO   Crossover elite individuals and generate next population
# TODO   Mutate (if needed)

# Creating midi files
from midiutil.MidiFile import MIDIFile
# Reading midi files
import mido
# Playing midi files
import pygame
from random import randint
from random import uniform

INDIVIDUAL_SIZE = 32


#_____________________REPRODUCTION AND MUTATION INFO_________________________#
"""
Reproduction/Next Gen:
  Top scoring individuals will reproduce for next round.
  Bottom individuals will be replaced with a new randomized individual
  A few of the other tops will stay with a few mutations
  Proportions of new gen assuming 10 per gen: 2/10 top reproducers, 1/10 bottom one re-randomized, 2/10 lesser tops with definite mutations, 5/10 new children with possible mutations
  1
Crossover:
  Cross over will be a random assignment that should be about 50%
    INDIVIDUAL_SIZE = ???
    ...
    parent0 = [...]
    parent1 = [...]
    child = []
    for i in range(INDIVIDUAL_SIZE):
        if randint(0,1) == 0:
            child.append(parent0[i])
        else:
            child.append(parent1[i])

Mutation:
  Mutation will be a lowish percentage that just completely randomizes the note that is being mutated...maybe like 5-10% chance for new children
  
"""


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
track = 0    (constant)
channel = 0  (constant)
pitch = 60
time = 0
duration = 1
volume = 100 (constant)
 

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


def play_midi_file(songfile):
    pygame.init()
    pygame.mixer.music.load(songfile)
    pygame.mixer.music.play(0)

    while pygame.mixer.music.get_busy():
        pygame.event.poll()


def generate_random_individual():
    new_individual = []

    for beat in range(INDIVIDUAL_SIZE):
        new_individual.append([randint(48, 84), beat, uniform(.5, 4)])
    return new_individual


def write_midi_file(song, file_name):
    # Create the MIDIFile Object with 1 track
    my_midi = MIDIFile(1)

    # Tracks are numbered from zero. Times are measured in beats.
    track = 0
    time = 0

    # Add track name and tempo.
    my_midi.addTrackName(track, time, "Main")
    my_midi.addTempo(track, time, 120)

    # Add a note. addNote expects the following information:
    track = 0 # (constant)
    channel = 0 # (constant)
    volume = 100 # (constant)

    # Now add the notes
    for beat in song:
        pitch, time, duration = beat
        my_midi.addNote(track, channel, pitch, time, duration, volume)

    # And write it to disk.
    bin_file = open(file_name, 'wb')
    my_midi.writeFile(bin_file)
    bin_file.close()


# filename = "new_test.mid"
# individual = generate_random_individual()
# write_midi_file(individual, filename)
# play_midi_file(filename)

# file = mido.MidiFile("test.mid")
# for msg in file.play():
#     print(msg)
