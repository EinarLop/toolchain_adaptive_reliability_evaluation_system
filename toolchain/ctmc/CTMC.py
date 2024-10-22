import networkx as nx

from generatectmc import *
from constants import *
from classes import *

from itertools import combinations

import time
import os

NUM_SWITCHES = 2
NUM_SLAVES = 3

NUM_ILINKS = 1
NUM_REQ_SLAVES = 2

OPTIONAL_OUTPUT_ENABLED = False
OUTPUT_DIR = "..\\prism\\ctmc\\"

failure_rate_vector = {}


################################################################################
## Global variables
################################################################################

# Nodes
slaves = []
ports = []
links = []
guardians = []
switches = []

# Edges
slave_to_port_edges = []
port_to_slave_edges = []
port_to_link_edges = []
link_to_port_edges = []
link_to_guardian_edges = []
guardian_to_link_edges = []
guardian_to_switch_edges = []
switch_to_guardian_edges = []
switch_to_port_edges = []
port_to_switch_edges = []

# Graph
G = nx.DiGraph()
ctmc = nx.DiGraph()


################################################################################
## Auxiliary functions 
################################################################################

def init_elements():
    global slaves
    global ports
    global links
    global guardians
    global switches

    global slave_to_port_edges
    global port_to_slave_edges
    global port_to_link_edges
    global link_to_port_edges
    global link_to_guardian_edges
    global guardian_to_link_edges
    global guardian_to_switch_edges
    global switch_to_guardian_edges
    global switch_to_port_edges
    global port_to_switch_edges

    slaves = tuple(Slave() for i in range(NUM_SLAVES))
    switches = tuple(Switch() for i in range(NUM_SWITCHES))

    for slave in slaves:
        for switch in switches:
            new_slave_port = Port()
            ports.append(new_slave_port)
            slave_to_port_edges.append((slave, new_slave_port))
            port_to_slave_edges.append((new_slave_port, slave))

            new_slavelink = Link()
            links.append(new_slavelink)
            port_to_link_edges.append((new_slave_port, new_slavelink))
            link_to_port_edges.append((new_slavelink, new_slave_port))

            new_guardian = Guardian()
            guardians.append(new_guardian)
            link_to_guardian_edges.append((new_slavelink, new_guardian))
            guardian_to_link_edges.append((new_guardian, new_slavelink))

            guardian_to_switch_edges.append((new_guardian, switch))
            switch_to_guardian_edges.append((switch, new_guardian))

    # Create clique of switches interconnected by interlinks
    i = 0
    for switch1, switch2 in combinations(switches, 2):
        for j in range(NUM_ILINKS):
            new_interlink_port = Port()
            ports.append(new_interlink_port)
            switch_to_port_edges.append((switch1, new_interlink_port))
            port_to_switch_edges.append((new_interlink_port, switch1))

            new_interlink = Link()
            links.append(new_interlink)
            port_to_link_edges.append((new_interlink_port, new_interlink))
            link_to_port_edges.append((new_interlink, new_interlink_port))

            new_interlink_port2 = Port()
            ports.append(new_interlink_port2)
            link_to_port_edges.append((new_interlink, new_interlink_port2))
            port_to_link_edges.append((new_interlink_port2, new_interlink))
            switch_to_port_edges.append((switch2, new_interlink_port2))
            port_to_switch_edges.append((new_interlink_port2, switch2))
        i += NUM_ILINKS

    ports = tuple(ports)
    links = tuple(links)
    guardians = tuple(guardians)

    failure_rate_vector.update({s: 0.00001 for s in slaves})
    failure_rate_vector.update({p: 0.00000125537 for p in ports})
    failure_rate_vector.update({l: 0.0000001 for l in links})
    failure_rate_vector.update({g: 0.00000125537 for g in guardians})
    failure_rate_vector.update({b: 0.000001 for b in switches})

    print("SYSTEM - Number of switches: " + str(NUM_SWITCHES))
    print("SYSTEM - Number of slaves: " + str(NUM_SLAVES))


def create_system_graph():
    global G

    G.add_edges_from(slave_to_port_edges, coverage_vector={'crash': 0, 'byzantine': 0}, matrix=failure_mode_mutation_probabilities['slaves']['ports'])
    G.add_edges_from(port_to_slave_edges, coverage_vector={'crash': 1, 'byzantine': 0}, matrix=failure_mode_mutation_probabilities['ports']['slaves'])

    G.add_edges_from(port_to_link_edges,  coverage_vector={'crash': 0, 'byzantine': 0}, matrix=failure_mode_mutation_probabilities['ports']['links'])
    G.add_edges_from(link_to_port_edges,  coverage_vector={'crash': 1, 'byzantine': 0.1}, matrix=failure_mode_mutation_probabilities['links']['ports'])

    G.add_edges_from(link_to_guardian_edges, coverage_vector={'crash': 1, 'byzantine': 0.8}, matrix=failure_mode_mutation_probabilities['links']['guardians'])
    G.add_edges_from(guardian_to_link_edges, coverage_vector={'crash': 0, 'byzantine': 0}, matrix=failure_mode_mutation_probabilities['guardians']['links'])

    G.add_edges_from(guardian_to_switch_edges, coverage_vector={'crash': 1, 'byzantine': 0}, matrix=failure_mode_mutation_probabilities['guardians']['switches'])
    G.add_edges_from(switch_to_guardian_edges, coverage_vector={'crash': 0, 'byzantine': 0}, matrix=failure_mode_mutation_probabilities['switches']['guardians'])

    G.add_edges_from(switch_to_port_edges, coverage_vector={'crash': 0, 'byzantine': 0}, matrix=failure_mode_mutation_probabilities['switches']['ports'])
    G.add_edges_from(port_to_switch_edges, coverage_vector={'crash': 1, 'byzantine': 0}, matrix=failure_mode_mutation_probabilities['ports']['switches'])

    class_to_color = {
        slaves: 'green',
        switches: 'yellow',
        links: 'blue',
        ports: 'red',
        guardians: 'cyan',
    }

    colorize_graph(G, class_to_color)

    save_graph_drawing(G, OUTPUT_DIR + 'system.png')


def create_ctmc_graph():
    global G
    global ctmc

    start = time.time()
    generate_ctmc(G, ctmc, is_correct, slaves, switches, NUM_REQ_SLAVES)
    stop = time.time()

    print("CTMC - Number of states: " + str(len(ctmc.nodes())))
    print("CTMC - Number of transitions: " + str(len(ctmc.edges())))
    print("Elapsed time: " + str(round(stop - start, 2)) + " secs")
    print("")

    if os.path.exists(OUTPUT_DIR + 'ctmc.png'):
        os.remove(OUTPUT_DIR + 'ctmc.png')

    if os.path.exists(OUTPUT_DIR + 'ctmc.graphml'):
        os.remove(OUTPUT_DIR + 'ctmc.graphml')

    if OPTIONAL_OUTPUT_ENABLED:
        save_ctmc_drawing(ctmc, OUTPUT_DIR + 'ctmc.png')

        # The E vector contains a enumeration of states and their transitions.
        # It is organized as a tuple of the elements that compose a initial state,
        # a tuple of elements that compose a final state and a tuple with the
        # the elements that failed between both states. A simple example would be:
        # A state that has one switch, one guard, one link, one port and one slave,
        # a state that has one switch, one guard, one link, one port and NO slave,
        # the element that failed, i.e., the slave:
        # "['b1', 'g1', 'l1', 'p1', 's1']", "['b1', 'g1', 'l1', 'p1']", {'Label': '[s1]'}
        #         FIRST STATE                     SECOND STATE           FAILING ELEMENT
        E = []
        for u, v in ctmc.edges():
            E.append(
                #(str(sorted([str(w) for w in u.nodes()])),
                #str(sorted([str(w) for w in v.nodes()])),
                #{'Label': str(sorted(ctmc[u][v]['failed_element']))}
                (
                    str(u.nodes()),
                    str(u.nodes()),
                    {'Label': str(ctmc[u][v]['failed_element'])}
                )
            )

        ctmc_with_strings = nx.DiGraph()
        ctmc_with_strings.add_edges_from(E)
        nx.write_graphml(ctmc_with_strings, OUTPUT_DIR + 'ctmc.graphml')


def write_ctmc_matrix():
    global ctmc

    # Register state names
    states = []
    for node in ctmc.nodes():
        s_name = str(node.nodes())
        states.append(s_name)
    
    #states.sort(reverse=True)

    # Create/open file
    f = open(OUTPUT_DIR + "ctmc.tra", "w")

    # Write first line
    num_states = len(ctmc.nodes())
    num_trans = len(ctmc.edges())
    f.write(str(num_states) + " " + str(num_trans) + "\n")

    # Write transitions (s1, s2 and probability)
    for u, v in ctmc.edges():
        s1_name = str(u.nodes())
        s2_name = str(v.nodes())

        s1_idx = states.index(s1_name)
        s2_idx = states.index(s2_name)

        if OPTIONAL_OUTPUT_ENABLED:
            print(
                "s" + str(s1_idx) + ": " + s1_name +
                " => " +
                str(ctmc[u][v]['failed_element']) +
                " => " +
                "s" + str(s2_idx) + ": " + s2_name
            )

        fail_rate = 0
        for fail_elem in ctmc[u][v]['failed_element']:
            fail_rate += failure_rate_vector[fail_elem]

        f.write(str(s1_idx) + " " + str(s2_idx) + " " + str(fail_rate) + "\n")
    
    f.close()

    if OPTIONAL_OUTPUT_ENABLED:
        print("")


def is_correct(G, slaves, masters, num_necessary_slaves):
    """
    num_necessary_slaves: minimum number of slaves that must be connected to
    each other in graph G for G not to be faulty.
    """
    H = nx.Graph(G)
    num_non_faulty_cc = 0
    for cc_vertices in nx.connected_components(H):
        num_slaves_in_cc = len(set(cc_vertices) & set(slaves))
        num_masters_in_cc = len(set(cc_vertices) & set(masters))
        if num_slaves_in_cc >= num_necessary_slaves and num_masters_in_cc >= 1:
            # Check that the slaves are not a vertex cut in the connected
            # component.
            H2 = nx.Graph(H)
            H2.remove_nodes_from(slaves)
            # We check that order > 0 because nx.is_connected() is not defined
            # for the null graph.
            if H2.order() > 0 and nx.is_connected(H2):
                num_non_faulty_cc += 1

    # G is correct (non-faulty) if it has exactly 1 non-faulty connected
    # component. Having more than 1 correct component is considered a failure
    # because we assume that if the system is split into more than one
    # functioning subsystem, this is a failure.
    if num_non_faulty_cc == 1:
        return True
    else:
        return False


################################################################################
## Main function
################################################################################

if __name__ == "__main__":
    print("CTMC generator")
    print("==============")
    print("")

    init_elements()
    create_system_graph()
    create_ctmc_graph()
    write_ctmc_matrix()
