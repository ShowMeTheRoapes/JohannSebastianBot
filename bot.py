# Creating midi files
from midiutil.MidiFile import MIDIFile
# Playing midi files
import pygame
import math as Math
from random import randint
from random import uniform

INDIVIDUAL_SIZE = 16
PARENT_PERCENT = 0.25
RANDOM_PERCENT = 0.10
MUTANT_PERCENT = 0.40
MUTATE_NUM = 8


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
    my_midi.addTempo(track, time, 160)

    # Add a note. addNote expects the following information:
    track = 0  # (constant)
    channel = 0  # (constant)
    volume = 100  # (constant)

    # Now add the notes
    for beat in song:
        pitch, time, duration = beat
        my_midi.addNote(track, channel, pitch, time, duration, volume)

    # And write it to disk.
    bin_file = open(file_name, 'wb')
    my_midi.writeFile(bin_file)
    bin_file.close()


def generate_initial_population(size):
    population = []
    for i in range(size):
        population.append(generate_random_individual())

    return population


def create_next_generation(population, ratings):
    next_generation = []
    parents = []
    children = []
    mutated = []
    randoms = []
    parent_num = int(Math.floor(len(population)*PARENT_PERCENT))
    random_num = int(Math.floor(len(population)*RANDOM_PERCENT))
    mutant_num = int(Math.floor(len(population)*MUTANT_PERCENT))

    # Get the parents
    for i in range(parent_num):
        max_index = ratings.index(max(ratings))
        parents.append(population[max_index])
        ratings.pop(max_index)
        population.pop(max_index)

    # Create the children
    children += crossover_parents(parents, parent_num)

    # Mutate some of the previous population
    for i in range(mutant_num):
        mutated.append(mutate_individual(population[randint(0, len(population)-1)], MUTATE_NUM))

    # Generate the randoms
    for i in range(random_num):
        randoms.append(generate_random_individual())

    next_generation += parents + children + mutated + randoms

    return next_generation


def crossover_parents(parents, child_num):
    children = []
    crossover_point = randint(0, INDIVIDUAL_SIZE)

    for i in range(child_num):
        parent_1 = parents[randint(0, len(parents) - 1)]
        parent_2 = parents[randint(0, len(parents) - 1)]

        # Ensure different parents
        while parent_2 is parent_1:
            parent_2 = parents[randint(0, len(parents) - 1)]

        child = []
        for note in range(crossover_point):
            child.append(parent_1[note])

        for note in range(crossover_point, INDIVIDUAL_SIZE):
            child.append(parent_2[note])

        children.append(child)

    return children


def mutate_individual(mutant, num_mutations):
    for i in range(num_mutations):
        index = randint(0, len(mutant) - 1)
        if i % 2 == 0:
            mutant[index] = [randint(48, 84), mutant[index][1], uniform(.5, 4)]
        else:
            swapper_index = randint(0, len(mutant) - 1)
            temp = mutant[swapper_index]
            mutant[swapper_index] = mutant[index]
            mutant[index] = temp

    return mutant


def evaluate_individual(individual):
    good_diffs = [0, 3, 4, 5, 7, 9]
    neutral_diffs = [2, 6, 8]
    score = 0

    for i in range(len(individual)-1):
        diff_first = individual[0][0] - individual[i][0]
        diff_prev = individual[i][0] - individual[i + 1][0]

        if diff_first % 12 in good_diffs:
            score += 2
        elif diff_first % 12 in neutral_diffs:
            score += 1
        else:
            score -= 1

        if diff_prev % 12 in good_diffs:
            score += 2
        elif diff_prev % 12 in neutral_diffs:
            score += 1
        else:
            score -= 2

        if diff_prev > 12:
            score -= 3
        if diff_prev > 8:
            score -= 2

    diff_last = individual[0][0] - individual[INDIVIDUAL_SIZE - 1][0]

    if diff_last % 12 in good_diffs:
        score += 2
    elif diff_last % 12 in neutral_diffs:
        score += 1
    else:
        score -= 1

    return score


def main(size=10):
    done = False
    generation = 0
    population = generate_initial_population(size)

    while not done:
        ratings = []
        for individual in population:
            ratings.append(evaluate_individual(individual))

        if generation % 10000 == 0:
            best_index = ratings.index(max(ratings))
            best_individual = population[best_index]
            filename = str(generation) + ".mid"
            print("Writing " + filename + " with a score of: " + str(ratings[best_index]))
            write_midi_file(best_individual, filename)
            play_midi_file(filename)

        # print("Generation: " + str(generation) + " Population size: " + str(len(population)))
        population = create_next_generation(population, ratings)
        generation += 1


main(40)
