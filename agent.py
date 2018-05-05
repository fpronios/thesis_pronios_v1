import msg_parser as msg
#import keras
#import theano
#import tensorflow as tf
#import mdptoolbox
from mpi4py import MPI

import asyncio
import time
from functools import wraps

import zmq
import pandas
import igraph

agent_id = 1

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1-t0))
               )
        return result
    return function_timer


#
#   A function to set the initial parameters for the
#   learning processes, load the graph and wait
#
def initialize():

    return 2

#
#   Start the learning process, this should be the decentralized-ready implementation
#
#
def start_agent():

    return 3

#
#   Reporting of stats (cpu time, msgs/second, RAM alloc )
#
#
def per_agent_stats():

    return 4


#
# Load the Graph and tree files
#
#
#@fn_timer
def load_tree(filepath):
    st = igraph.Graph.Read_Pickle(filepath)

    #igraph.Graph.Read_Edgelist(st)
    print(st.degree(agent_id))
    print("Children:")
    print(st.neighbors(agent_id , mode="OUT"))
    print("Parent:")
    print(st.neighbors(agent_id, mode="IN"))
    #st.degree()

    return st


def main(agent_idd,filepath, server_push_port = "5556", server_pub_port = "5558"):
    global agent_id
    agent_id = agent_idd

    print('Agent ID: ' , agent_id)

    # Load the spaaning tree from the file as object
    st = load_tree(filepath)
    children = list(set(st.neighbors(agent_id , mode="OUT")))
    parent = list(set(st.neighbors(agent_id , mode="IN")))

    msg.main(agent_id, server_push_port, server_pub_port, parent, children)