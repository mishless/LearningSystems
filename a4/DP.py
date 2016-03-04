# encoding: utf-8
'''
Implementation of value iteration algorithm for finding the optimal value for all states in a graph;
Using the optimal value the optimal policy can be easily constrcuted and thus the shortest path is found;
Results are validated using Bellman-Ford shortest path algorithm;

Authors: Mihaela Stoycheva <mihaela.stoycheva@gmail.com> & Vukan Turkulov <vukant@gmail.com>

'''

import sys
import random
from argparse import ArgumentParser

def value_iterate_algorithm(graph, destination, eps):
    optimal_values = dict()
    d = dict()
    for node in graph:
        optimal_values[node] = 0
        d[node] = 0
    search = True 
    while search:
        for node in graph:
            if node == destination:
                continue
            old_optimal_value = optimal_values[node]
            optimal_values[node] = max([optimal_values[dest] - int(graph[node][dest]) for dest in graph[node]])
            d[node] = abs(old_optimal_value - optimal_values[node])
        search = False
        for node in graph:
            if (d[node] > eps):
                search = True
    return optimal_values

def calculate_policy(graph, optimal_values):
    policy = dict()
    for node in graph:
        policy[node] = max([(optimal_values[dest] - int(graph[node][dest]), dest) for dest in graph[node]], key=lambda e:e[0])[1]
    return policy

def find_shortest_paths(graph, destination, policy):
    shortest_paths = dict()
    for node in graph:
        shortest_paths[node] = 0
        current_node = node;
        while current_node is not destination:
            random_policy = random.choice(policy[current_node])
            shortest_paths[node] += int(graph[current_node][random_policy])
            current_node = random_policy
    return shortest_paths

def bellman_ford(graph, destination):
    shortest_paths = dict()
    edges = 0;
    for node in graph:
        shortest_paths[node] = sys.maxsize
    shortest_paths[destination] = 0
    for i in range(0, len(graph)):
        for node in graph:
            for edge in graph[node]:
                if (shortest_paths[node] + int(graph[node][edge]) < shortest_paths[edge]):
                    shortest_paths[edge] = shortest_paths[node] + int(graph[node][edge])
    return shortest_paths

def compare_shortest_paths(bellman_ford_shortest_path, value_iteration_shorest_path):
    for path in bellman_ford_shortest_path:
        if (bellman_ford_shortest_path[path] != value_iteration_shorest_path[path]):
            raise Exception("The two distances are not the same: Bellman-Ford shortest path for {} is {} and value iteration shortest path for {} is {}."
                            .format(path, bellman_ford_shortest_path[path], path, value_iteration_shorest_path[path]))

def create_graph(paths):
    graph = dict()
    for path in paths:
        path = path.split(" ")
        if path[0] not in graph:
            graph[path[0]] = dict()
        if path[1] not in graph:
            graph[path[1]] = dict()
        graph[path[0]][path[1]] = path[2]
        graph[path[1]][path[0]] = path[2]
    return graph

def process_input(argv=None):
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
        # Setup argument parser
    parser = ArgumentParser()
    parser.add_argument("-f", "--cities-file", dest="file", help="the file containing the cities information", required=True)

    # Process arguments
    args = parser.parse_args()

    file = args.file
    paths = []
    with open(file, 'r') as f:
        paths = f.read().splitlines()
    f.closed
    return paths

def main(argv=None):
    try:
        paths = process_input(argv)
        graph = create_graph(paths)
        optimal_values = value_iterate_algorithm(graph, "F", 00.1)
        policy = calculate_policy(graph, optimal_values)
        shortest_paths = find_shortest_paths(graph, "F", policy)
        bellman_ford_shortest_paths = bellman_ford(graph, "F")
        compare_shortest_paths(bellman_ford_shortest_paths, shortest_paths)
        print("Optimal values: {}".format(optimal_values))
        print("Shortest paths from every node to F: {}".format(shortest_paths))
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        sys.stderr.write(repr(e))
        return 2

if __name__ == "__main__":
    sys.exit(main())
