import msg_parser as msg
#import keras
#import theano
#import tensorflow as tf
#import mdptoolbox
#from mpi4py import MPI
import sqlite3
from DQNAgent import DQNAgent
import random
import asyncio
import datetime
import time
from functools import wraps
import argparse
import numpy as np
import sys

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

def request_state(lstate):
    print("Lstate: ", lstate.submitted_req, lstate.on)
    if lstate.submitted_req == 0:
        rnd = random.random()
        if rnd > 0.9 :
           on = True
        else:
           on = False
    else:
        on = True

    return on

class load_state():
    def __init__(self, on_state, submitted):

        self.on = on_state
        self.submitted_req = submitted

    def set_submitted(self, val):
        self.submitted_req = val

    def set_on_state(self, val):
        if val == 0:
            self.on = False
        else:
            self.on = True

    def get_submitted(self):
        if self.submitted_req:
            return 1
        else:
            return 0

    def get_on_state(self):
        if self.on:
            return 1
        else:
            return 0



def send_status(timeslot , agent):
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()
    c.execute('''INSERT INTO payoff_table VALUES (?,?)''',(agent, timeslot,))
    conn.commit()
    conn.close()

    return

def send_ok(timeslot , agent):
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()
    c.execute('''INSERT INTO all_ok VALUES (?,?)''',(timeslot, agent,))
    conn.commit()
    conn.close()

    return

def check_ok(timeslot , test_num):
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()
    out = 0
    for row in c.execute('''SELECT COUNT (agent) FROM all_ok WHERE timeslot = ? GROUP BY timeslot ''',(timeslot,)):
        out = row
    #print('OUT DB: ', out)
    if out[0] == test_num:
        return True
    else:
        return False

def wait_for_episode():
    return False

def send_load_status(timeslot , agent, on_status, request_status):
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()
    c.execute('''INSERT INTO state_table VALUES (?,?,?,?)''',(agent, timeslot,on_status,request_status,))
    conn.commit()
    conn.close()

    return

def get_payoff(timeslot,tot):
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()
    req_on = 0
    on = 0
    for row in c.execute('''SELECT COUNT (agent) FROM state_table WHERE timeslot = ? GROUP BY timeslot HAVING request_status = 1''', (timeslot,)):
        req_on = row[0]
    # print('OUT DB: ', out)
    for row in c.execute('''SELECT COUNT (agent) FROM state_table WHERE timeslot = ? GROUP BY timeslot HAVING on_status = 1''',
                         (timeslot,)):
        on = row[0]

    if on == 0 or req_on == 0:
        return 0
    return (tot / on) + (on/req_on)
#parser = argparse.ArgumentParser(description='Process some integers.')

def reset_db():
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()
    c.execute('''DELETE FROM state_table''')
    c.execute('''DELETE FROM all_ok''')
    conn.commit()
    conn.close()

def main(agent_idd):#,filepath, server_push_port = "5556", server_pub_port = "5558"):
    if agent_idd == 1:
        reset_db()
    global agent_id
    agent_id = agent_idd
    episodes = 1000000
    print('Agent ID: ' , agent_id)

    total_agents = 3
    # Load the spaaning tree from the file as object
    #st = load_tree(filepath)
    #children = list(set(st.neighbors(agent_id , mode="OUT")))
    #parent = list(set(st.neighbors(agent_id , mode="IN")))

    #print("Agent Online")
    l_state = load_state(False, False)
    l_state.set_on_state(request_state(l_state))
    now = datetime.datetime.now()
    day, month, hour = now.day, now.month, now.hour
    state = np.array([day, month, hour, l_state.get_on_state()])

    dqn = DQNAgent(4, 2)
    action = np.array([0])
    reward = 0


    for i in range(episodes):
        send_ok(i, agent_id)
        while not check_ok(i, total_agents):
            #pass
            time.sleep(0.001)

        now = now + datetime.timedelta(minutes=5)
        if l_state.get_submitted() == 1:
            action = dqn.act(state)
            l_state.set_on_state(action)
            # act and wait for env feedback
            next_state, reward, done, _ = np.array([now.day, now.month, now.hour, l_state.get_on_state()]), get_payoff(i,total_agents) , False, 0

            dqn.remember(state, action, reward, next_state, done)

            state = next_state
            #msg.main(agent_id, server_push_port, server_pub_port, parent, children)

            dqn.replay(16)
            l_state.set_on_state(0)
            l_state.submitted_req = False

        print("Episode %d, Agent %d, Load_StateS: %d, Last {Action : %d , Reward : %d }" %(i,agent_id,l_state.get_submitted(),action,reward,))
        send_load_status(i,agent_id,l_state.get_submitted(),l_state.get_on_state())
        bool_state = request_state(l_state)
        l_state.set_on_state(bool_state)
        l_state.set_submitted(bool_state)

if __name__ == '__main__':
    main(int(sys.argv[1]))