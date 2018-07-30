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
import requests
import json

URL = 'http://127.0.0.1:1994/'

def main():

    global agent_id

    dict = requests.get(URL + 'get_aid').json()

    agent_id = int(dict['your_aid'])
    print('Agent ID: ' , agent_id)

    dqn = DQNAgent(4, 2)
    action = np.array([0])

    for i in range(500):
        done = False

        """get observation"""
        dict = requests.get(URL + 'observe/%d' % (agent_id,)).json()
        #print("Env: ", dict["environment"])

        state = np.fromstring(dict["environment"],dtype=float)
        state = state[[[agent_id,agent_id+1,-3,-2]]].reshape(1,4)
        tot_reward = 0
        while not done:
            action = dqn.act(state)

            """ Send action """
            requests.get(URL + 'make_action/%d/%d' % (agent_id,action,)).json()

            # act and wait for env feedback
            """ Timeslot Ready"""
            while True:
                dict = requests.get(URL + 'ts_ready/%d' % (agent_id,)).json()
                #print(dict["ready"])
                if dict["ready"] :
                    break
                time.sleep(0.04)

            """Then  get reward observation and done from environment"""
            #print(dict["environment"])
            #print(np.fromstring(dict["environment"],dtype=float))
            n_state = np.fromstring(dict["environment"],dtype=float)
            next_state, reward, done, _ =  n_state[[[agent_id,agent_id+1,-3,-2]]].reshape(1,4), dict["reward"], dict["done"], 0

            #print("Shape: ", next_state.shape)
            #next_state = next_state.reshape(-1,1)
            #print("Shape: ", next_state.shape)

            dqn.remember(state, action, reward, next_state, done)
            state = next_state
            tot_reward += reward
            dqn.replay(16)

        print("Episode %d, Agent %d, Last {Action : %d , Reward : %d }" %(i,agent_id,action,tot_reward,))


if __name__ == '__main__':
    main()