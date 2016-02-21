# Genetic Algorithm for solving the Traveling Salesman problem
# Authors: Mihaela Stoycheva, Vukan Turkulov

# Includes
import configparser
import math
import matplotlib.pyplot as plt
import numpy
import random
import sys
from operator import itemgetter

#Global variables(yay!)
#    Configuration variables(read from config.txt)
mutation_rate = 0;
population_size = 0;
elitism_rate = 0;
tournament_rate = 0;
max_iterations = 0;
input_file_name = "";
parent_rate = 0;

#    General global variables
cities = {};
number_of_cities = 0;
parent_number = 0;
tournament_size = 0;
elite_number = 0;
crossover_number = 0;

def read_config():
    global mutation_rate;
    global elitism_rate;
    global tournament_rate;
    global population_size;
    global input_file_name;
    global max_iterations;
    global parent_rate;
    global parent_number;
    global tournament_size;
    global elite_number;
    global crossover_number;

    config = configparser.ConfigParser();
    config.read("config.txt");

    mutation_rate = float(config['general']['mutation_rate']);
    population_size = int(config['general']['population_size']);
    elitism_rate = float(config['general']['elitism_rate']);
    tournament_rate = float(config['general']['tournament_rate']);
    max_iterations = int(config['general']['max_iterations']);
    parent_rate = float(config['general']['parent_rate']);
    input_file_name = config['general']['input_file_name'];

    parent_number = int(population_size * parent_rate);
    elite_number = int(population_size * elitism_rate);
    tournament_size = int(population_size * tournament_rate);
    crossover_number = population_size - elite_number;

def print_config():
    print("***** CONFIGURATION *****");
    print_var("Population size", population_size);
    print_var("Elitism rate", elitism_rate);
    print_var("Tournament rate", tournament_rate);
    print_var("Mutation rate", mutation_rate);
    print_var("Parent rate", parent_rate);
    print_var("Iteration number", max_iterations);
    print("");
    print_var("Tournament size", tournament_size);
    print_var("Parent number", parent_number);
    print_var("Elite number", elite_number);
    print_var("Crossover number", crossover_number);
    print("");

def read_input_file():
    global number_of_cities;

    file = open(input_file_name, "r");
    file_lines = file.readlines();
    file.close();

    for file_line in file_lines:
        temp = file_line.split();        
        cities[int(temp[0])] = {'x' : float(temp[1]), 'y' : float(temp[2])};

    number_of_cities = len(cities);

def get_distance(city1, city2):
    return math.sqrt( ((city1['x']-city2['x'])**2) +
                      ((city1['y']-city2['y'])**2));

def print_cities():
    print("***** CITIES *****");

    for key, city in cities.items():
        print("#" + "%2s" % str(key) + ": (" +
              "%6s" % str(city['x']) + ', '  +
              "%6s" % str(city['y']) + ')');

    print("");

def print_var(name, var):
    print(name + ":" + " "*(17-len(name)) + str(var));

def init():
    read_config();
    read_input_file(); 
    print_config();

def create_random_individual():
    individual = [];

    # We must begin at first city
    individual.append(1);

    # Create list of city indexes
    indexes = list(range(2,number_of_cities+1));

    while len(indexes) > 0:
        picked_index = random.choice(indexes);
        indexes.remove(picked_index);
        individual.append(picked_index);

    # We must end at first city
    individual.append(1);

    return individual;

def print_population(population, name):
    print("***** POPULATION: " + name + " *****");

    print("Population size = " + str(len(population)));

    i = 0;
    for individual in population:
        print("IND #" + str(i) + ": " + str(individual));
        i += 1;

def print_population_2(population, name):
    print("***** POPULATION: " + name + " *****");

    print("Population size = " + str(len(population)));
    i = 0;
    for individual in population:
        print("IND #" + str(i) + " distance = " +
              str(evaluate_individual(individual)));
        i += 1;

    print("");

def print_population_3(population, name):
    print("***** POPULATION: " + name + " *****");

    print("Population size = " + str(len(population)));
    for individual in population:
        print(str(individual) + ": distance = " +
              str(evaluate_individual(individual)));

    print("");

def create_random_population(population_size):
    population = [];

    for i in range(0, population_size):
        population.append(create_random_individual());

    return population;

def evaluate_individual(individual):
    distance_traveled = 0;
   
    for i in range(0, len(individual)-1):    
        distance_traveled = (distance_traveled +
            get_distance(cities[individual[i]], cities[individual[i+1]]));

    return distance_traveled;

def evaluate_population(population):
    evaluations = [];

    for individual in population:
        evaluations.append(evaluate_individual(individual));

    return evaluations;

def select_tournament_pool(data):
    tournament_pool = [];

    indexes = list(range(0, len(data)));

    for i in range(0, tournament_size):
        chosen_index = random.choice(indexes);
        tournament_pool.append(data[chosen_index]);
        indexes.remove(chosen_index);

    return tournament_pool;

def best_solution(pool):
    best_individual = {'eval' : sys.float_info.max};

    for individual in pool:
        if individual['eval'] < best_individual['eval']:
            best_individual = individual; 
    
    return best_individual;

def run_tournament(pool):
    return best_solution(pool);

def merge_popul_and_eval(population, evaluations):
    data = [];
    for i in range(0, len(population)):
        data.append({'ind' : population[i],
                     'eval' : evaluations[i]});

    return data;

def select_parent_pool(population, evaluations):
    parent_pool = [];
    data = merge_popul_and_eval(population, evaluations);

    for i in range(0, parent_number):
        tournament_pool = select_tournament_pool(data);
        parent = run_tournament(tournament_pool);
        parent_pool.append(parent['ind']);
        data.remove(parent);

    return parent_pool;

def is_individual_valid(individual):

    if(len(individual) != (number_of_cities+1)):
        print("INVALID " + str(individual));
        return False;

    if(individual[0] != 1):
        print("INVALID " + str(individual));
        return False;

    if(individual[-1] != 1):
        print("INVALID " + str(individual));
        return False;

    for city in individual:
        if city == 1:
            if individual.count(city) != 2:
                print("INVALID " + str(individual));
                return False;
        else:
            if individual.count(city) != 1:
                print("INVALID " + str(individual));
                return False;

    return True;

def is_population_valid(population):
    for individual in population:
        if is_individual_valid(individual) == False:
            return False;

    return True;

def create_child(parent1, parent2):
    l = len(parent1);
    x = random.randint(1, l-1);
    y = random.randint(x, l-1);

    child = [];
    extract = parent1[x:y];
    """print_var("P1", parent1);
    print_var("P2", parent2);
    print_var("x", x);
    print_var("y", y);
    print_var("Extract", extract);"""

    i = 0;

    for j in range(0, x):

        while(parent2[i] in extract):
            i += 1;

        child.append(parent2[i]);
        i += 1;

    child.extend(extract);

    for j in range(y, l):

        while(parent2[i] in extract):
            i += 1;

        child.append(parent2[i]);
        i += 1;

    return child;

def generate_children(parent_pool, child_num):
    children = [];

    for i in range(0, child_num):
        parent1 = random.choice(parent_pool);
        parent_pool.remove(parent1);
        parent2 = random.choice(parent_pool);
        parent_pool.append(parent1);
        new_child = create_child(parent1, parent2);
        children.append(new_child);

    return children;

def generate_elites(population, evaluations, number):
    data = merge_popul_and_eval(population, evaluations);
    elites = [];

    for i in range(0, number):
        best = best_solution(data);
        elites.append(best['ind']);
        data.remove(best);

    return elites;

def mutate_individual(individual):

    i = random.randint(1, len(individual)-2);
    j = i;

    while j == i:
        j = random.randint(1, len(individual)-2);

    individual[i], individual[j] = individual[j], individual[i];

def mutate_population(population):
    for individual in population:
        if random.random() < mutation_rate:
            mutate_individual(individual);

def test_stuff():
    """
    p1 = "abcdefg";
    p2 = "1234567";
    for i in range(0,10):
        print(create_child(p1,p2));
    

    ind = [1,2,3,4,5,6];
    print("Before", ind);
    mutate_individual(ind);
    print("After", ind);
    exit();"""

def perform_GA():
    best_solutions = [];

    #print("***** ALGORITHM START *****");

    population = create_random_population(population_size);

    iteration_counter = 1;

    while True:
        #print("Running iteration " + str(iteration_counter) + ":");

        evaluations = evaluate_population(population);

        best_solutions.append(min(evaluations));

        if iteration_counter == max_iterations:
            break;   

        parent_pool = select_parent_pool(population, evaluations);
        children = generate_children(parent_pool, crossover_number);
        mutate_population(children);

        elites = generate_elites(population, evaluations, elite_number);
        
        # Prepare population for the next iteration
        population = children + elites;
        iteration_counter += 1;

        if is_population_valid(population) == False:
            break;

    return best_solutions;

def do_what_needs_to_be_done():
    results = [];
    bests = [];

    print("***** ALGORITHM START *****");
    sys.stdout.flush()

    for i in range(0, 10):
        print("Starting cycle " + str(i+1));
        results.append(perform_GA());
        bests.append(results[i][-1]);

    best_ind = bests.index(min(bests));

    print("");
    print("***** RESULTS *****");
    print("Best result is " + str(min(bests)));

    plt.plot(results[best_ind]);
    plt.show();

    


#main
init();
do_what_needs_to_be_done()
