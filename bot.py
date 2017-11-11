# TODO Take Bach MIDI files and get them in a usable format
# TODO Create initial random population
# TODO while (not done)
# TODO   Evaluate individuals
# TODO   Crossover elite individuals and generate next population
# TODO   Mutate (if needed)

from midiutil.MidiFile import MIDIFile #  creating midi files
import mido     #  reading in midi files
import pygame   #  playing midi files
from random import randint

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


def play_midi_file(filename):
    pygame.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(0)

    while pygame.mixer.music.get_busy():
        pygame.event.poll()


def generate_random_individual():
    new_individual = []

    for beat in range(16):
        new_individual.append([randint(48, 84), beat, randint(0, 4)])

    return new_individual


def write_midi_file(individual, filename):
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
    for beat in individual:
        pitch, time, duration = beat
        my_midi.addNote(track, channel, pitch, time, duration, volume)

    # And write it to disk.
    bin_file = open(filename, 'wb')
    my_midi.writeFile(bin_file)
    bin_file.close()


filename = "test.mid"
# individual = generate_random_individual()
# write_midi_file(individual, filename)
play_midi_file(filename)
