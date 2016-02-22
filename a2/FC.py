#!/usr/local/bin/python2.7
# encoding: utf-8
'''
mdh.FC is a fuzzy classifier that classifies iris data into three classes provided with membership 
functions for all terms of linguistic variables and a database of fuzzy rules.

It defines classes_and_methods

@author:    Vukan Turkolov <vukant@gmail.com>
            Mihaela Stoycheva <mihaela.stoycheva@gmail.com

@copyright:  2016 IDT, Mälardalen Högskola. All rights reserved.
'''

import sys
import os
import re
from operator import itemgetter
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

def normalize_formula(x, min, max):
    normalized = [((x[i] - min[i]) / (max[i] - min[i])) for i in range(0, len(x) - 1)]
    normalized += (x[4],)
    return normalized

def normalize_data(data_set):
    maximum_tuples = (max(data_set, key=itemgetter(0))[0],
                      max(data_set, key=itemgetter(1))[1],
                      max(data_set, key=itemgetter(2))[2],
                      max(data_set, key=itemgetter(3))[3])
    minimum_tuples = (min(data_set, key=itemgetter(0))[0],
                      min(data_set, key=itemgetter(1))[1],
                      min(data_set, key=itemgetter(2))[2],
                      min(data_set, key=itemgetter(3))[3])
    data_set = [normalize_formula(item, minimum_tuples, maximum_tuples) for item in data_set]
    return data_set

def short(value):
    return abs((1 - (value / 0.6)) * (value < 0.6))

def middle(value):
    return abs((value / 0.6) * (value <= 0.6) + (2.5 - 2.5 * value) * (value > 0.6));

def calc_long(value):
    return abs((value * 2.5 - 1.5) * (value > 0.6));

def rule_one(sho, mid, lon, union_op, intersecion_op):
    result = intersecion_op(union_op(sho[0], lon[0]), union_op(mid[1], lon[1]),
             union_op(mid[2], lon[2]), mid[3]);
    return (result, 'Iris-versicolor');

def rule_two(sho, mid, lon, union_op, intersecion_op):
    result = intersecion_op(union_op(sho[2], mid[2]), sho[3]);
    return (result, 'Iris-setosa');

def rule_three(sho, mid, lon, union_op, intersecion_op):
    result = intersecion_op(union_op(sho[1], mid[1]),
                lon[2], lon[3])
    return (result, 'Iris-virginica')

def rule_four(sho, mid, lon, union_op, intersecion_op):
    result = intersecion_op(mid[0], union_op(sho[1],
                mid[1]), sho[2],
                lon[3])
    return (result, 'Iris-versicolor')

def probor(*args):
    if (len(args) == 2):
        return ((args[0] + args[1]) - (args[0] * args[1]))
    else:
        sys.exit("Probor operator works only with two arguments. ;)")

def prod(*args):
    result = 1
    for arg in args:
        result *= arg
    return result;

def classify(short, middle, calc_long, union_op, intersection_op):
    result = []
    result.append(rule_one(short, middle, calc_long, union_op, intersection_op))
    result.append(rule_two(short, middle, calc_long, union_op, intersection_op))
    result.append(rule_three(short, middle, calc_long, union_op, intersection_op))
    result.append(rule_four(short, middle, calc_long, union_op, intersection_op))
    return max(result, key=lambda item:item[0])[1]

def fuzzify_and_eval(data_set, union_op, intersection_op):
    correct = 0;
    for data_item in data_set:
        membership_short = list([short(data_item[i]) for i in range(0, len(data_item) - 1)])
        membership_middle = list([middle(data_item[i]) for i in range(0, len(data_item) - 1)])
        membership_long = list([calc_long(data_item[i]) for i in range(0, len(data_item) - 1)])
        if (data_item[4] == classify(membership_short, membership_middle, membership_long, union_op, intersection_op)):
            correct += 1
    return correct / len(data_set);

def process_input(argv=None):
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
        # Setup argument parser
    parser = ArgumentParser()
    parser.add_argument("-d", "--data-set", dest="data_set", help="the file containing the data set", required=True)
    parser.add_argument("-u", "--union-operator", dest="union_operator", choices=['max', 'probor'],
                        help="specify the operator to be used for union; possible values: max, probors", required=True)
    parser.add_argument("-i", "--intersection-operator", dest="intersection_operator", choices=['min', 'prod'],
                        help="specify the operator to be used for intersection; possible values: min, prod", required=True)

    # Process arguments
    args = parser.parse_args()

    data_set_path = args.data_set
    union_operator = args.union_operator
    intersection_operator = args.intersection_operator
    
    with open(data_set_path, 'r') as f:
        data_set = [(float(value[0]),
                     float(value[1]),
                     float(value[2]),
                     float(value[3]),
                     value[4]) for value in [line.split(',') for line in [re.sub('\s+', ' ', line).strip() for line in f.read().splitlines()]]]
    f.closed
    return {'data-set': data_set, 'union-op': union_operator, 'intersection-op': intersection_operator}

def main():
    try:
        input_data = process_input()
        data_set = normalize_data(input_data['data-set'])
        result = fuzzify_and_eval(data_set, eval(input_data['union-op']), eval(input_data['intersection-op']))
        print("CORRECTLY CLASSIFIED: {}%".format(result))
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        sys.stderr.write(repr(e))
        return 2

if __name__ == "__main__":
    sys.exit(main())
