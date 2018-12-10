#import msg_parser as msg
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
import requests
import json
import gp_estimator as gpe


#URL = 'http://127.0.0.1:1994/'
URL = 'http://192.168.0.22:1994/'

def main():

    global agent_id

    dict = requests.get(URL + 'get_aid').json()

    agent_id = int(dict['your_aid'])
    print('Agent ID: ' , agent_id)

    dqn = DQNAgent(7, 2)
    action = np.array([0])

    for i in range(500):
        done = False

        """get observation"""
        while True:
            dicto = requests.get(URL + 'observe/%d' % (agent_id,)).json()
            #print(dicto)
            if dicto['obs_ready'] == True and dicto['episode'] == i:
                break
            time.sleep(0.04)
        #print("Env: ", dict["environment"])
        #print(dicto)
        #print(dicto["environment"])
        state = np.fromstring(dicto["environment"],dtype=float, sep=',')
        #print("Test state: ",state)

        """load ts, load mand, load opt, ts , tsprice, tsaggr """
        state = state[[[agent_id,agent_id+1,agent_id+2,-4,-3,-2,-1]]].reshape(1,7)
        tot_reward = 0
        #print("got_observation with state: ", state)
        #print("Before learn")
        while not done:
            #print(state)
            action = dqn.act(state)

            #print("Send Action")
            """ Send action """
            while True:
                #print("Make action:")
                dicto = requests.get(URL + 'make_action/%d/%d' % (agent_id,action,)).json()
                #print(dict["ready"])
                if dicto["aid"] == agent_id :
                    break
                time.sleep(0.04)

            #print("Loop State:")
            # act and wait for env feedback
            #time.sleep(0.5)
            #print("Timeslot Ready")
            """ Timeslot Ready"""
            retry_count = 0
            while True:
                if retry_count == 10:
                    requests.get(URL + 'make_action/%d/%d' % (agent_id, action,)).json()
                    retry_count
                dicto = requests.get(URL + 'ts_ready/%d' % (agent_id,)).json()
                #print("Sending ready request")
                if dicto != None:
                    if dicto["ready"]  :
                        break
                time.sleep(0.04)

                retry_count += 1


            """Then  get reward observation and done from environment"""
            #print("TST: ", dicto)
            #print("Test error: ", np.fromstring(dicto["environment"],dtype=np.float, sep=','))
            n_state = np.fromstring(dicto["environment"],dtype=np.float, sep=',')
            next_state, reward, done, _ =  n_state[[[agent_id,agent_id+1,agent_id+2,-4,-3,-2,-1]]].reshape(1,7), dicto["reward"], dicto["done"], 0

            #print("Shape: ", next_state.shape)
            #next_state = next_state.reshape(-1,1)
            #print("Shape: ", next_state.shape)

            dqn.remember(state, action, reward, next_state, done)
            state = next_state
            tot_reward += reward
            dqn.replay(96)

        print("Episode %d, Agent %d, Last {Action : %d , Reward : %.10f }" %(i,agent_id,action,tot_reward,))



if __name__ == '__main__':
    main()