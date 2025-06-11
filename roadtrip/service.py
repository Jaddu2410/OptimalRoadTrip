import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="http")


def findbestroute(city_coordinates):
    def plot_cities(city_coordinates, annotate=True):
        """
        Makes a plot of all cities.
        Input: city_coordinates; dictionary of all cities and their coordinates in (x,y) format
        """
        names = []
        x = []
        y = []
        plt.figure(dpi=250)
        for ix, coord in city_coordinates.items():
            names.append(ix)
            x.append(coord[0])
            y.append(coord[1])
            if annotate:
                plt.annotate(ix, xy=(coord[0], coord[1]), xytext=(20, -20),
                             textcoords='offset points', ha='right', va='bottom',
                             bbox=dict(boxstyle='round,pad=0.5', fc='w', alpha=0.5),
                             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        plt.scatter(x, y, c='r', marker='o')

    plot_cities(city_coordinates)

    # In[99]:

    print(list(city_coordinates.keys()))

    # In[100]:

    from copy import copy
    def create_guess(cities):
        """
        Creates a possible path between all cities, returning to the original.
        Input: List of City IDs
        """
        guess = copy(cities)
        np.random.shuffle(guess)
        guess.append(guess[0])
        return list(guess)

    create_guess(list(city_coordinates.keys()))

    # In[101]:

    def plot_guess(city_coordinates, guess, guess_in_title=True):
        """
        Takes the coordinates of the cities and the guessed path and
        makes a plot connecting the cities in the guessed order
        Input:
        city_coordinate: dictionary of city id, (x,y)
        guess: list of ids in order
        """
        plot_cities(city_coordinates)
        for ix, current_city in enumerate(guess[:-1]):
            x = [city_coordinates[guess[ix]][0], city_coordinates[guess[ix + 1]][0]]
            y = [city_coordinates[guess[ix]][1], city_coordinates[guess[ix + 1]][1]]
            plt.plot(x, y, 'c--', lw=1)
        plt.scatter(city_coordinates[guess[0]][0], city_coordinates[guess[0]][1], marker='x', c='b')
        if guess_in_title:
            plt.title("Current Guess: [%s]" % (','.join([str(x) for x in guess])))
        else:
            print("Current Guess: [%s]" % (','.join([str(x) for x in guess])))

    path = create_guess(list(city_coordinates.keys()))
    print(path)
    plot_guess(city_coordinates, path)

    # In[102]:

    def create_generation(cities, population=100):
        """
        Makes a list of guessed city orders given a list of city IDs.
        Input:
        cities: list of city ids
        population: how many guesses to make
        """
        generation = [create_guess(cities) for _ in range(population)]
        return generation

    test_generation = create_generation(list(city_coordinates.keys()), population=10)
    print(test_generation)

    # In[103]:

    print(city_coordinates)

    # In[104]:

    def distance_between_cities(city1_id, city2_id):
        """
        Given two cities, this calculates this distance between them
        """

        c1 = city_coordinates[city1_id]
        c2 = city_coordinates[city2_id]
        distance = np.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
        return distance

    def fitness_score(guess):
        """
        Loops through the cities in the guesses order and calculates
        how much distance the path would take to complete a loop.
        Lower is better.
        """
        score = 0
        for ix, city_id in enumerate(guess[:-1]):
            score += distance_between_cities(city_id, guess[ix + 1])
        return score

    def check_fitness(guesses):
        """
        Goes through every guess and calculates the fitness score.
        Returns a list of tuples: (guess, fitness_score)
        """
        fitness_indicator = []
        for guess in guesses:
            fitness_indicator.append((guess, fitness_score(guess)))
        return fitness_indicator

    print(check_fitness(test_generation))

    # Now we need to setup a breeding program. So what does that entail? We can't take random cities from each parent, we might get the same city in there twice. So instead we'll take a random set of the cities from parent 1 and hold them in place. Then well fill in with cities from parent 2, going left to right and making sure no duplicates occur.

    # In[105]:

    def get_breeders_from_generation(guesses, take_best_N=10, take_random_N=5, verbose=False, mutation_rate=0.1):
        """
        This sets up the breeding group for the next generation. You have
        to be very careful how many breeders you take, otherwise your
        population can explode. These two, plus the "number of children per couple"
        in the make_children function must be tuned to avoid exponential growth or decline!
        """
        # First, get the top guesses from last time
        fit_scores = check_fitness(guesses)
        sorted_guesses = sorted(fit_scores, key=lambda x: x[1])  # sorts so lowest is first, which we want
        new_generation = [x[0] for x in sorted_guesses[:take_best_N]]
        best_guess = new_generation[0]

        if verbose:
            # If we want to see what the best current guess is!
            print(best_guess)

        # Second, get some random ones for genetic diversity
        for _ in range(take_random_N):
            ix = np.random.randint(len(guesses))
            new_generation.append(guesses[ix])

        # No mutations here since the order really matters.
        # If we wanted to, we could add a "swapping" mutation,
        # but in practice it doesn't seem to be necessary

        np.random.shuffle(new_generation)
        return new_generation, best_guess

    def make_child(parent1, parent2):
        """
        Take some values from parent 1 and hold them in place, then merge in values
        from parent2, filling in from left to right with cities that aren't already in
        the child.
        """
        list_of_ids_for_parent1 = list(np.random.choice(parent1, replace=False, size=len(parent1) // 2))
        child = [-99 for _ in parent1]

        for ix in list_of_ids_for_parent1:
            child[ix] = parent1[ix]
        for ix, gene in enumerate(child):
            if gene == -99:
                for gene2 in parent2:
                    if gene2 not in child:
                        child[ix] = gene2
                        break
        child[-1] = child[0]
        return child

    def make_children(old_generation, children_per_couple=1):
        """
        Pairs parents together, and makes children for each pair.
        If there are an odd number of parent possibilities, one
        will be left out.

        Pairing happens by pairing the first and last entries.
        Then the second and second from last, and so on.
        """
        mid_point = len(old_generation) // 2
        next_generation = []

        for ix, parent in enumerate(old_generation[:mid_point]):
            for _ in range(children_per_couple):
                next_generation.append(make_child(parent, old_generation[-ix - 1]))
        return next_generation

    # In[106]:

    make_child([0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11])

    # Let's look at a test cycle with our test_generation.

    # In[107]:

    breeders, _ = get_breeders_from_generation(test_generation)
    print(breeders)

    # In[108]:

    print(make_children(breeders, children_per_couple=2))

    # Sweet, it looks like our parents features are being carried on, but aren't being directly copies. So all is going how we hoped for now. Now let's try actually solving the problem by letting many generations happen and turning up how many guesses there are in the initial generation.

    # In[109]:

    current_generation = create_generation(list(city_coordinates.keys()), population=500)
    print_every_n_generations = 5

    for i in range(100):
        if not i % print_every_n_generations:
            print("Generation %i: " % i, end='')
            print(len(current_generation))
            is_verbose = True
        else:
            is_verbose = False
        breeders, best_guess = get_breeders_from_generation(current_generation,
                                                            take_best_N=250, take_random_N=100,
                                                            verbose=is_verbose)
        current_generation = make_children(breeders, children_per_couple=3)

    # Let's put this into a function so we can repeat it with different sets of stuff.

    # In[110]:

    def evolve_to_solve(current_generation, max_generations, take_best_N, take_random_N,
                        mutation_rate, children_per_couple, print_every_n_generations, verbose=False):
        """
        Takes in a generation of guesses then evolves them over time using our breeding rules.
        Continue this for "max_generations" times.
        Inputs:
        current_generation: The first generation of guesses
        max_generations: how many generations to complete
        take_best_N: how many of the top performers get selected to breed
        take_random_N: how many random guesses get brought in to keep genetic diversity
        mutation_rate: How often to mutate (currently unused)
        children_per_couple: how many children per breeding pair
        print_every_n_geneartions: how often to print in verbose mode
        verbose: Show printouts of progress
        Returns:
        fitness_tracking: a list of the fitness score at each generations
        best_guess: the best_guess at the end of evolution
        """
        fitness_tracking = []
        for i in range(max_generations):
            if verbose and not i % print_every_n_generations and i > 0:
                print("Generation %i: " % i, end='')
                print(len(current_generation))
                print("Current Best Score: ", fitness_tracking[-1])
                is_verbose = True
            else:
                is_verbose = False
            breeders, best_guess = get_breeders_from_generation(current_generation,
                                                                take_best_N=take_best_N, take_random_N=take_random_N,
                                                                verbose=is_verbose, mutation_rate=mutation_rate)
            fitness_tracking.append(fitness_score(best_guess))
            current_generation = make_children(breeders, children_per_couple=children_per_couple)

        return fitness_tracking, best_guess

    #current_generation = create_generation([0, 1, 2, 3, 4], population=500)
    fitness_tracking, best_guess = evolve_to_solve(current_generation, 100, 150, 70, 0.5, 3, 5, verbose=True)

    plot_guess(city_coordinates, best_guess)

    return best_guess