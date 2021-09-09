# Creating midi files
from midiutil.MidiFile import MIDIFile
# Playing midi files
import pygame
import math as Math
import statistics as Stats
import textwrap
import os
from random import randint
from random import uniform

# !!!! CONSTANT FIELDS !!!! #
# !!!! TWEAK THESE FOR FUN !!!! #
MIDI_TEMPO = 220
INDIVIDUAL_SIZE = 24
PARENT_PERCENT = 0.10
RANDOM_PERCENT = 0.25
MUTANT_PERCENT = 0.55
DEFAULT_MUTATE_NUM = 8
MUTATE_NUM = DEFAULT_MUTATE_NUM
MAX_NOTE_LEN = 4
MIN_NOTE_LEN = .5


def play_midi_file(songfile):
    """
    Function to play a written MIDI file using
    pygame
    :param songfile: the name of the MIDI file
    """
    pygame.init()
    pygame.mixer.music.load(songfile)
    pygame.mixer.music.play(0)

    while pygame.mixer.music.get_busy():
        pygame.event.poll()


def generate_random_individual():
    """
    Function to generate a random musical phrase
    :return: the randomly generated phrase
    """
    new_individual = []

    for beat in range(INDIVIDUAL_SIZE):
        # Generate a random note between 48 and 84 and random note duration
        new_individual.append([randint(48, 84), beat, uniform(MIN_NOTE_LEN, MAX_NOTE_LEN)])

    return new_individual


def write_midi_file(song, file_name):
    """
    Write a musical phrase to a MIDI file in the same directory.
    Uses MIDIUtil.
    :param song: the musical phrase to write to a file
    :param file_name: the name of the MIDI file
    """
    # Create the MIDIFile Object with 1 track
    my_midi = MIDIFile(1)

    # Tracks are numbered from zero. Times are measured in beats.
    track = 0
    time = 0

    # Add track name and tempo.
    my_midi.addTrackName(track, time, "Main")
    my_midi.addTempo(track, time, MIDI_TEMPO)

    # Add a note. addNote expects the following information:
    track = 0  # (constant)
    channel = 0  # (constant)
    volume = 100  # (constant)

    # Now add the notes
    for beat in song:
        pitch, time, duration = beat
        my_midi.addNote(track, channel, pitch, time, duration, volume)

    # And write it to disk.
    if not os.path.exists('./currentRun'):
        os.mkdir('./currentRun')

    bin_file = open(file_name, 'wb')
    my_midi.writeFile(bin_file)
    bin_file.close()


def generate_initial_population(size):
    """
    Function to generate the initial random population
    :param size: the desired size of the population
    :return: the newly generated population of phrases
    """
    population = []
    for i in range(size):
        population.append(generate_random_individual())

    return population


def create_next_generation(population, ratings):
    """
    Creates the next generation using the old population
    and their individual ratings
    :param population: the previous population
    :param ratings: the array of the ratings of the musical phrases
    :return: the newly generated population
    """
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
        index_of_max = ratings.index(max(ratings))
        parents.append(population[index_of_max])
        ratings.pop(index_of_max)
        population.pop(index_of_max)

    # Create the children
    children.extend(crossover_parents(parents, parent_num))

    # Mutate the next best of the previous population
    for i in range(mutant_num):
        index_of_max = ratings.index(max(ratings))
        mutated.append(mutate_individual(population[index_of_max], MUTATE_NUM))
        ratings.pop(index_of_max)
        population.pop(index_of_max)

    # Generate the randoms
    for i in range(random_num):
        randoms.append(generate_random_individual())

    # Add each group to the next generation
    next_generation.extend(parents)
    next_generation.extend(children)
    next_generation.extend(mutated)
    next_generation.extend(randoms)

    return next_generation


def crossover_parents(parents, child_num):
    """
    Randomly chooses parents and crosses them over to create
    as many children as child_num specifies.
    Uses one-point crossover, with the point randomly chosen.
    :param parents: the array of parent phrases
    :param child_num: the number of children to be generated
    :return: the array of generated children
    """
    children = []
    crossover_point = randint(0, INDIVIDUAL_SIZE)

    for i in range(child_num):
        parent_1 = parents[randint(0, len(parents) - 1)]
        parent_2 = parents[randint(0, len(parents) - 1)]

        # Ensure different parents
        while parent_2 is parent_1:
            parent_2 = parents[randint(0, len(parents) - 1)]

        # Get the first half from one parent
        child = []
        for note in range(crossover_point):
            child.append(parent_1[note])

        # Get the second half from the other parent
        for note in range(crossover_point, INDIVIDUAL_SIZE):
            child.append(parent_2[note])

        children.append(child)

    return children


def mutate_individual(mutant, num_mutations):
    """
    Mutate a musical phrase as many times as num_mutations
    specifies.
    Each mutation chooses a random note and gives it a random new
    tone and a random new duration.
    :param mutant: the musical phrase to be mutated
    :param num_mutations: the number of mutations to perform
    :return: the mutated phrase
    """
    for i in range(num_mutations):
        note_index = randint(0, len(mutant) - 1)
        mutant[note_index] = [randint(48, 84), mutant[note_index][1], uniform(.5, 4)]

    return mutant


def evaluate_individual(individual):
    """
    Evaluates a musical phrase using various characteristics
    we found that make notes sound pleasant together.
    :param individual: the musical phrase to be evaluated
    :return: the score given to the phrase
    """
    good_diffs = [3, 4, 5, 7, 9]
    neutral_diffs = [0, 2, 6, 8]
    score = 0

    for i in range(len(individual)-1):
        diff_first = individual[0][0] - individual[i][0]
        diff_prev = individual[i][0] - individual[i + 1][0]

        # Compare each note to the first note
        if diff_first % 12 in good_diffs:
            score += 2
        elif diff_first % 12 in neutral_diffs:
            score += 1
        else:
            score -= 1

        # Compare each note to its neighbor
        if diff_prev % 12 in good_diffs:
            score += 2
        elif diff_prev % 12 in neutral_diffs:
            score += 1
        else:
            score -= 2

        # Penalize notes next to each other in different octaves
        if diff_prev > 12:
            score -= 3
        if diff_prev > 8:
            score -= 2

    diff_last = individual[0][0] - individual[INDIVIDUAL_SIZE - 1][0]

    # Compare the first note to the last note
    if diff_last % 12 in good_diffs:
        score += 2
    elif diff_last % 12 in neutral_diffs:
        score += 1
    else:
        score -= 1

    # Penalize the last note if it is too short
    if individual[-1][2] < 1.5:
        score -= 3

    return score


def main(size=10, toSave=True, toPlay=True):
    """
    The main program.
    Maintains the algorithm and writes the best MIDI file on
    specified generation.
    :param size: the desired size of the population
    """
    global MUTATE_NUM
    global MUTANT_PERCENT
    global RANDOM_PERCENT
    done = False
    generation = 0
    population = generate_initial_population(size)
    lastMaxRating = 0
    runsStuckAtSameMaxRating = 0
    stabilizeMutation = True

    def printCurrentStats(title='None'):
        ratingsSort = ratings.copy()
        ratingsSort.sort()
        body = textwrap.dedent(f"""
        :{":" * len(title)}:
        :{title}:
        :{":" * len(title)}:
            Generation: {str(generation)}
            Current Max score: {str(currentMaxRating)}
            Lowest score: {str(min(ratings))}
            Mean of scores: {str(Stats.mean(ratings))}
            Ratings: {ratingsSort}
            Consistent Score Runs: {runsStuckAtSameMaxRating}
            Population size: {len(population)}
            Mutations strenght: {MUTATE_NUM}
            New population random/mutate: {RANDOM_PERCENT}/{MUTANT_PERCENT}
        """)
        print(body)
    
    while not done:
        ratings = []
        for individual in population:
            ratings.append(evaluate_individual(individual))
        
        if generation % 1000 == 0:
            # print(generation)
            index_of_best = ratings.index(max(ratings))
            best_song = population[index_of_best]
            currentMaxRating = int(ratings[index_of_best])

            # Deal with saving files and reseting stats after a successful new bump up.
            if(lastMaxRating < currentMaxRating):
                filename = f"currentRun/{str(generation)}.mid"
                if toSave:
                    printCurrentStats(f"S A V I N G -- {filename}")
                    write_midi_file(best_song, filename)
                
                lastMaxRating = currentMaxRating
                runsStuckAtSameMaxRating = 0
                MUTATE_NUM = DEFAULT_MUTATE_NUM                    
                
                if toPlay:
                    print("Playing " + filename + " with a score of: " + str(ratings[index_of_best]))
                    play_midi_file(filename)

        if generation % 4000 == 0 and generation != 0:
            if runsStuckAtSameMaxRating >= 4000:
                printCurrentStats("C H E C K  I N  O N L Y")
                # print("\nC H E C K  I N  O N L Y  \n" + printCurrentStats())
            # Slows down mutation amount to fine tune the randomness
            if stabilizeMutation and MUTATE_NUM > 1:
                MUTATE_NUM -= 1



        # Massive radiation causes increased mutation chance if life is too stagnant.
        if runsStuckAtSameMaxRating >= 20000:
            if runsStuckAtSameMaxRating == 20000:
                print(f"We are stuck at: {currentMaxRating}...")
                print(f"Reactor meltdown initated....")
                stabilizeMutation = False
            if not stabilizeMutation and runsStuckAtSameMaxRating % 4000 == 0 and MUTATE_NUM < INDIVIDUAL_SIZE:
                MUTATE_NUM += 1
                print(f"Radiation leak causing higher than average mutations! Number of mutations now at {str(MUTATE_NUM)}.")
                if MUTATE_NUM == INDIVIDUAL_SIZE:
                    print("Radiation Declining")
                    stabilizeMutation = True

        if runsStuckAtSameMaxRating % 100000 == 0 and runsStuckAtSameMaxRating != 0:
            # Change mutation to highest
            if(MUTANT_PERCENT != .75):
                MUTANT_PERCENT = .75
                RANDOM_PERCENT = .05

        population = create_next_generation(population, ratings)
        generation += 1
        runsStuckAtSameMaxRating += 1

        

main(size=100, toPlay=False)
