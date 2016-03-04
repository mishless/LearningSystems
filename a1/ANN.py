#Artificial Neural Network


#includes
import configparser
import math
import matplotlib.pyplot as plt
import numpy as np
import random
from decimal import *

#global variables
weights = [];
topology = [];
data_training = [];
data_test = [];
learning_rate = 0;
weight_min = 0;
weight_max = 0;
error_terms = [];
outputs = [];
result_offset = 4.5;
partition_num = 0;
partition_size = 0;
data_sets = [];
scalings = [{'min' : 1.5*(10**9), 'max' : 2.5*(10**9)},
            {'min' : 1.5*(10**8), 'max' : 4.5*(10**8)},
            {'min' : 0, 'max' : 150}];

def read_config():
    global partition_num;
    global learning_rate;
    global weight_min;
    global weight_max;
    global iteration_num;
    
    config = configparser.ConfigParser();
    config.read("config.txt");
    temp = config["general"]["topology"];
    temp = temp.split(",");
    for s in temp:
        topology.append(int(s));
    learning_rate = float(config['general']['learning_rate']);
    weight_min = float(config['general']['weight_min']);
    weight_max = float(config['general']['weight_max']);
    partition_num = int(config['general']['partition_num']);
    
def read_input():
    read_config();

def print_weights():
    print("***** WEIGHTS *****");
    for i in range(0, len(weights)):
        print("Layer 0 (" + str(topology[i]) + " -> " + str(topology[i+1]) + "):");
        print("---------------");
        for j in range(0, len(weights[i])):
            for k in range(0, len(weights[i][j])):
                print("%.6f " % weights[i][j][k], end="");
            print();
        print("---------------");
        print();

def fill_dummy_weights():
    w = 0.1;
    for i in range(0, len(weights)):
        for j in range(0, len(weights[i])):
            for k in range(0, len(weights[i][j])):
                weights[i][j][k] = w;
                w = w + 0.1;

def fill_random_weights(min_limit, max_limit):
    for i in range(0, len(weights)):
        for j in range(0, len(weights[i])):
            for k in range(0, len(weights[i][j])):
                weights[i][j][k] = random.uniform(min_limit, max_limit);

def init_weights():
    for i in range(0, len(topology)-1):
        weights.append([]);
        for j in range(0, topology[i+1]):
            weights[i].append([]);
            for k in range(0, topology[i]):
                weights[i][j].append(0);
            weights[i][j].append(0);

def init_error_terms():
    for layer in range(0, len(topology)):        
        error_terms.append([]);
        for row in range(0, topology[layer]):
            error_terms[layer].append(0);

def init_outputs():
    for layer in range(0, len(topology)):        
        outputs.append([]);
        for row in range(0, topology[layer]):
            outputs[layer].append(0);
            
def plot_sigmoid():
    x_list = np.arange(-8, 8, 0.1);
    y_list = [];
    for x in x_list:
        y_list.append(sigmoid(x));

    plt.plot(x_list, y_list);
    plt.show();
    
def sigmoid(x):

    #avoid overflow fuckups
    if x < -100:
        x = -100;
        
    res = 1/(1+(math.exp(-x)));
    return res;
    
def output_function(x):
    return sigmoid(x) + 4.5;

def calculate_output(input_sample):
    return output_function(calculate_net(len(topology)-1, 0, input_sample));

def print_nets(input_sample):
    print("***** NETS *****");
    for layer in range(0, len(topology)):
        print("Layer " + str(layer) + ":");
        for row in range(0, topology[layer]):
            print("%0.2f   " % calculate_net(layer, row, input_sample), end = "");
        print();
        print();

def print_outputs():
    print("***** OUTPUTS *****");
    for layer in range(0, len(topology)):
        print("Layer " + str(layer) + ":");
        for row in range(0, topology[layer]):
            print("%0.20f   " % outputs[layer] [row], end = "");
        print();
        print();
        
def print_error_terms():
    print("***** ERROR TERMS *****");
    for layer in range(0, len(topology)):
        print("Layer " + str(layer) + ":");
        for row in range(0, topology[layer]):
            print("%0.6f   " % error_terms[layer] [row], end = "");
        print();
        print();
        
def read_input():
    file = open("Data_Training.txt");
    file_lines = file.readlines();
    file.close();
    
    for line in file_lines:
        temp = line.split();
        data_sample_strings = [temp[1], temp[18], temp[19], temp[21]];
        data_sample_numbers = [];
        
        for s in data_sample_strings:
            data_sample_numbers.append(float(s));
            
        data_training.append(data_sample_numbers);

    file = open("Data_Test.txt");
    file_lines = file.readlines();
    file.close();
    
    for line in file_lines:
        temp = line.split();
        data_sample_strings = [temp[1], temp[18], temp[19], temp[21]];
        data_sample_numbers = [];
        
        for s in data_sample_strings:
            data_sample_numbers.append(float(s));
            
        data_test.append(data_sample_numbers);

    random.shuffle(data_training);
    
def partition_data():
    global partition_size;
    partition_size = math.floor(len(data_training)/partition_num);

    print("Total data: " + str(len(data_training)));
    print("Partition size: " + str(partition_size));
    
    for i in range(0, partition_size*partition_num, partition_size):
        data_sets.append(data_training[i:(i+partition_size)]);

def examine_input():

    a = [];
    b = [];
    c = [];
    d = [];
    for data_sample in data_training:
        a.append(data_sample[0]);
        b.append(data_sample[1]);
        c.append(data_sample[2]);
        d.append(data_sample[3]);
        
    exit();

def scale_training_data():
    for data_sample in data_training:
        for i in range(0, topology[0]):
            data_sample[i] = (data_sample[i] - scalings[i]['min']) / (scalings[i]['max'] - scalings[i]['min']);

def scale_test_data():
    for data_sample in data_test:
        for i in range(0, topology[0]):
            data_sample[i] = (data_sample[i] - scalings[i]['min']) / (scalings[i]['max'] - scalings[i]['min']);

def scale_data():
    scale_training_data();
    scale_test_data();

def init():
    read_config();
    read_input();
    scale_data();
    init_weights();
    fill_random_weights(weight_min, weight_max);
    init_error_terms();
    init_outputs();
    partition_data();
    
def calculate_output_error_term(target_output, calculated_output):
    return (target_output - calculated_output) * calculated_output * (1 - calculated_output);

def calculate_net(layer, row):
    result = 0;
    for i in range(0, topology[layer-1]):
        result = result + outputs[layer-1][i] * weights[layer-1][row][i];
    result = result + (1 * weights[layer-1][row][-1]);
    return result;

def calculate_outputs(input_sample):
    for input_node in range(0, topology[0]):
        outputs[0][input_node] = input_sample[input_node];
        
    for layer in range(1, len(topology)):
        for row in range(0, topology[layer]):
            outputs[layer][row] = sigmoid(calculate_net(layer, row));

def calculate_error_term(layer, row):
    result = 0;
    for row_from_next_layer in range(0, topology[layer+1]):
        result = result + error_terms[layer+1][row_from_next_layer] * weights[layer][row_from_next_layer][row];
    result = result * outputs[layer][row] * (1 - outputs[layer][row]);
    return result

def calculate_error_terms(target_output):
    error_terms[-1][0] = calculate_output_error_term(target_output, outputs[-1][0]);
    for layer in reversed(range(1, len(topology)-1)):
        for row in range(0, topology[layer]):
            error_terms[layer][row] = calculate_error_term(layer, row);

def update_weights():
    for layer in range(0, len(topology)-1):
        for destination_row in range(0, topology[layer+1]):
            for source_row in range(0, topology[layer]):
                delta_weight = learning_rate * error_terms[layer+1][destination_row] * outputs[layer][source_row];
                weights[layer][destination_row][source_row] = weights[layer][destination_row][source_row] + delta_weight;
            weights[layer][destination_row][-1] = weights[layer][destination_row][-1] + learning_rate * error_terms[layer+1][destination_row] * 1;
        
    
                
def iterate_once(data_list):
    squared_errors = [];
    
    for data_sample in data_list:
        calculate_outputs(data_sample[0:3]);
        target_result = data_sample[3] - result_offset;
        squared_errors.append((target_result - outputs[-1][0])**2);
        calculate_error_terms(target_result);
        update_weights();
    
    mean_squared_error = sum(squared_errors)/float(len(squared_errors));
    return mean_squared_error;

def temp_test():
    data_sample = data_training[0];
    print_weights();
    
    for i in range(0, 10000):
        calculate_outputs(data_sample[0:3]);
        target_result = data_sample[3] - result_offset;
        calculate_error_terms(target_result);
        update_weights();
    print_weights();

def get_mean_error(data_list):
    squared_errors = [];
    
    for data_sample in data_list:
        calculate_outputs(data_sample[0:3]);
        target_result = data_sample[3] - result_offset;
        squared_errors.append((target_result - outputs[-1][0])**2);
        calculate_error_terms(target_result);
        
    mean_squared_error = sum(squared_errors)/float(len(squared_errors));
    return mean_squared_error;

def calculate_iteration_num(training, validation):

    fill_random_weights(weight_min, weight_max);
    error_old = get_mean_error(validation);

    consecutive_worse_num = 0;
    iterations = 0;
    while True:

        iterate_once(training);
        iterations = iterations + 1;
        error_new = get_mean_error(validation);
        #print("Iteration = " + str(iterations) + ", error = " + str(error_new));
        
        if error_new > error_old:
            consecutive_worse_num = consecutive_worse_num + 1;
            if consecutive_worse_num == 10:
                break;
        else:
            consecutive_worse_num = 0;
            
        error_old = error_new;
        
    return iterations;

def train_network(number_of_iterations):
    errors = []
    for i in range(0, number_of_iterations):
        errors.append(iterate_once(data_training));
    return errors;

    
def estimate_iteration_num():
    best_iterations = [];
        
    for i in range(0, partition_num):
        
        validation = data_training[ (i*partition_size) : ((i+1)*partition_size) ];
        
        if i == 0:
            training = data_training[ (i+1)*partition_size : partition_num*partition_size ];
        if i == (partition_num-1):
            training = data_training[0:partition_size*(partition_num-1)];
        else:
            training = data_training[0:i*partition_size] + data_training[(i+1)*partition_size:partition_num*partition_size];

        #print("Training = " + str(training));
        #print("Validation = " + str(validation));
        print("Performing K-fold cross validation... %2d%%" % int(i*100*partition_size/(partition_num*partition_size)));
        iteration_number = calculate_iteration_num(training, validation);
        best_iterations.append(iteration_number);

    average_iterations = int(sum(best_iterations)/len(best_iterations));
    print("Best iterations:" + str(best_iterations));
    print("Average best iterations: " + str(average_iterations));
    return average_iterations;

def estimate_and_train():

    global weights;
    
    all_errors = [];
    errors = [];
    weight_sets = [];
    
    number_of_iterations = estimate_iteration_num();
    
    for i in range(0, 10):
        print("Running training network, cycle " + str(i));
        fill_random_weights(weight_min, weight_max);
        all_errors.append(train_network(number_of_iterations));
        errors.append(get_mean_error(data_training));
        print("Error on whole training data set: " + str(errors[-1]));
        weight_sets.append(weights);

    weights = weight_sets[errors.index(min(errors))];
    plt.plot(all_errors[errors.index(min(errors))]);
    plt.show()

    test_error = get_mean_error(data_test);
    print("Test data error is " + str(test_error));

        
#main
init();
estimate_and_train();
