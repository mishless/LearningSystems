# Reinforcment learning for balancing pole on a cart system.
#
# Authors: Vukan Turkulov & Mihaela Stoycheva
# Licence: Ask Mihaela

import math
import matplotlib.pyplot as plt
import random
import sys
from matplotlib.backends.backend_pdf import PdfPages

#constants
F1 =  10
F2 = -10
initial_state = (0.0, 0.0, 0.0, 0.0);

FAIL_PENALTY = -1000;
X_BOUNDARY_LOW = -2.4;
X_BOUNDARY_HIGH = 2.4;
THETA_BOUNDARY_LOW = -0.20944;
THETA_BOUNDARY_HIGH = 0.20944;

states_info = {};
iteration_num = 10000;
coeff = 1.1025;
v_exp_guard = math.floor(math.log(sys.float_info.max/2, coeff));
v_max = 1000;
chain_states =  [initial_state];
chain_other_states = [initial_state];
chain_chances = [1.0];
max_depth = 0;
plot_graphs = False

def simulate_movement(force):
    floats = initial_state;
    xses = [0];
    xdots = [0];
    thetas = [0];
    theta_dots = [0];

    for f in force:
        floats = simulate(f, floats);
        xses.append(floats[0]);
        xdots.append(floats[1]);
        thetas.append(floats[2]);
        theta_dots.append(floats[3]);

    return (xses, thetas, xdots, theta_dots);

def simulate(force, floats):

    GRAVITY=9.8;
    MASSCART=1.0;
    MASSPOLE=0.1;
    TOTAL_MASS=MASSPOLE + MASSCART;
    LENGTH=0.5;          
    POLEMASS_LENGTH=MASSPOLE * LENGTH;
    STEP=0.02;    
    FOURTHIRDS=1.3333333333333;

    x = floats[0];
    x_dot = floats[1];
    theta = floats[2];
    theta_dot = floats[3];

    costheta = math.cos(theta);
    sintheta = math.sin(theta);

    temp = ((force + POLEMASS_LENGTH * theta_dot  *theta_dot * sintheta)/
        TOTAL_MASS);

    thetaacc = ((GRAVITY * sintheta - costheta* temp)/
        (LENGTH * (FOURTHIRDS - MASSPOLE * costheta * costheta/ TOTAL_MASS)));

    xacc  = temp - POLEMASS_LENGTH * thetaacc* costheta / TOTAL_MASS;

    y0= x+STEP*x_dot;
    y1=x_dot+STEP*xacc;
    y2=theta+STEP*theta_dot;
    y3=theta_dot+STEP*thetaacc;

    return(y0, y1, y2, y3);

def is_state_valid(s):
    x = s[0];
    theta = s[2];

    if(x < X_BOUNDARY_LOW or x > X_BOUNDARY_HIGH):
        return False;
    if(theta < THETA_BOUNDARY_LOW or theta > THETA_BOUNDARY_HIGH):
        return False;

    return True;

def get_initial_info():
    x = random.random()

    for i in reversed(range(0, len(chain_states))):
        if x < chain_chances[i]:
            starting_state = chain_other_states[i]
            path = chain_states[0:i] + [starting_state];
            return{'state':starting_state, 'path':path};

def get_next_state(s, force):

    if force != F1 and force != F2:
        print("Invalid force! Terminating.");
        exit();

    return simulate(force, s);

def chances_add(state):
    global_chances

def calculate_chance(v1, v2):
    if v1 > v_exp_guard:
        v1 = v_exp_guard;
    if v2 > v_exp_guard:
        v2 = v_exp_guard;

    if v1 >= v_max:
        return 1;
    if v2 >= v_max:
        return 0;

    return coeff**v1/(coeff**v1 + coeff**v2);

def get_v(state):
    global states_info;
    if state in states_info:
        return states_info[state]['v'];
    else:
        return 0;

def update_states_info(path):
    global states_info;

    i = -1;

    # Update v function backwards
    for state in reversed(path[0:-1]):
        if states_info[state]['v'] >= v_max:
            break;
        v1 = get_v(states_info[state]['s1']);
        v2 = get_v(states_info[state]['s2']);

        if states_info[state]['v'] == 1 + max(v1, v2):
           break;
        else:
           i -= 1;
           states_info[state]['v'] = min(v_max, 1 + max(v1, v2));

    # Update chances forward
    for state in path[i-1 : -1]:
        v1 = get_v(states_info[state]['s1']);
        v2 = get_v(states_info[state]['s2']);
        states_info[state]['chance'] = calculate_chance(v1, v2)

    if i == -len(path):
        i = 1;

    # If needed, update helper data structs
    if path[i-1] in chain_states:
        update_chain(path[i-1]);

def update_chain(starting_state):
    global chain_states;
    global chain_chances;

    i = chain_states.index(starting_state);
    del chain_states[i+1:];
    del chain_chances[i+1:];
    del chain_other_states[i+1:];
    s = chain_states[i];

    while True:
        if not s in states_info:
            break;

        chance = states_info[s]['chance'];

        if chance > 0.5:
            chain_states.append(states_info[s]['s1']);
            chain_other_states.append(states_info[s]['s2']);
            next_state = states_info[s]['s1'];
        else:
            chain_states.append(states_info[s]['s2']);
            chain_other_states.append(states_info[s]['s1']);
            next_state = states_info[s]['s2'];
            chance = 1 - chance;

        chain_chances.append(chain_chances[-1]*chance);

        s = next_state;

def info_add(state, prev_state):
    global states_info;

    states_info[state] = {'v' : 0,
                          'chance' : 0.5,
                          's1' : get_next_state(state, F1),
                          's2' : get_next_state(state, F2),
                          'prev' : prev_state};

def info_set_fail_state(state):
    global states_info;
    states_info[state]['v'] = FAIL_PENALTY;

def get_next_state_exp(state):

    x = random.random();
    if x < states_info[state]['chance']:
        return states_info[state]['s1'];
    else:
        return states_info[state]['s2'];

def train_system_once():
    global max_depth;

    initial_info = get_initial_info();
    state = initial_info['state'];
    chosen_states = initial_info['path'];

    depth = len(chosen_states);

    while True:

        if not state in states_info:
            info_add(state, chosen_states[-1]);

        if(is_state_valid(state) == False):
            info_set_fail_state(state);
            break;

        state = get_next_state_exp(state);
        chosen_states.append(state);

        if not state in states_info:
            info_add(state, chosen_states[-1]);

        depth += 1;

    update_states_info(chosen_states);

    if depth > max_depth:
        max_depth = depth;

def train_system(iterations):

    for i in range(0, iterations):
        if (i % 100) == 0:
            print("\n*** Running iteration %5d *** depth = %d" % (i, max_depth));
        train_system_once();

def run_system():
    state = initial_state;
    i = 0;
    f = [];

    xses = [0];
    xdots = [0];
    thetas = [0];
    theta_dots = [0];

    while True:
        if(is_state_valid(state) == False):
            break;

        if states_info[state]['chance'] > 0.5:
            state = states_info[state]['s1'];
            f.append(F1);
        else:
            state = states_info[state]['s2'];
            f.append(F2);

        xses.append(state[0]);
        xdots.append(state[1]);
        thetas.append(state[2]);
        theta_dots.append(state[3]);
        i += 1;

    print("Until fail: " + str(i));
    return {'forces': f, 'movement': (xses, xdots, thetas, theta_dots)};

def plot_results(data):

    pp = PdfPages('Movement.pdf')

    plt.figure(1);
    plt.plot(data[0]);
    plt.title("Cart Position");
    plt.xlabel("time[steps]");
    plt.ylabel("position[meters]");
    if plot_graphs == True:
        plt.show(block=False);
    pp.savefig();


    plt.figure(2);
    plt.plot(data[1]);
    plt.title("Cart Velocity");
    plt.xlabel("time[steps]");
    plt.ylabel("velocity[?]");
    pp.savefig();
    if plot_graphs == True:
        plt.show(block=False);

    plt.figure(3);
    plt.plot(data[2]);
    plt.title("Pole Angle");
    plt.xlabel("time[steps]");
    plt.ylabel("angle[radians]");
    pp.savefig();
    if plot_graphs == True:
        plt.show(block=False);

    plt.figure(4);
    plt.plot(data[3]);
    plt.title("Pole Angle Velocity");
    plt.xlabel("time[steps]");
    plt.ylabel("angle velocity[?]");
    pp.savefig();
    if plot_graphs == True:
        plt.show(block=False);

    pp.close();

def init():
    global states_info;

    states_info[initial_state] = {'v' : 0,
                          'chance' : 0.5,
                          's1' : get_next_state(initial_state, F1),
                          's2' : get_next_state(initial_state, F2),
                          'prev' : -1};

def do_what_has_to_be_done():
    train_system(iteration_num);

    run_system_results = run_system();

    forces_used = run_system_results['forces'];
    file = open("forces_used.txt", "w");
    file.write(str(forces_used));
    file.close();

    print("States encountered: " + str(len(states_info)));
    movement = run_system_results['movement'];
    print("Steps = " + str(len(forces_used)));
    plot_results(movement);

#main
init();
do_what_has_to_be_done();