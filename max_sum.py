import time
import datetime
from itertools import starmap
import numpy as np
from sqlite_messenger import *
import random
from numpy import  inf
from DQNAgent import DQNAgent

class message():
    def __init__(self, mtype, mfrom, mto, mdat, t_slot):
        self.type = mtype
        self.mfrom = int(mfrom)
        self.mto = int(mto)
        self.mdat = mdat
        self.t_slot = int(t_slot)

def message_encoder(mtype, mfrom, mto, mdat, t_slot):
    msg = message(mtype, mfrom, mto, mdat, t_slot)

    return msg

def message_decoder(msg):
    sep = ','
    msg_str = str(msg.type) + sep + str(msg.mfrom) + sep + str(msg.mto) + sep + str(msg.mdat) + sep + str(msg.t_slot)

    return msg_str

def distributed_max_sum(agent, graph, spanning_tree):
    """Initialize message variables"""

    m_i_j = 0
    m_j_i = 0
    # j subset Gamma(i) == Neighbour nodes

    g_i = 0
    p_i = 0
    m = -inf

    """Awating for decision deadline"""

    while deadline_to_send_not_arrived:

        # wait for message
        msg = poll_for_incoming(agent)

        if msg.type == 'max_plus'  # message == m_j_i // max_plus_message:

            for j in spanning_tree.neighbours(agent):

                m_i_j = compute_m_i_j(agent, j)

                if m_i_j != m_i_j_last:
                    send_message(m_i_j_a_j):

        if use_anytime_excpetion:

            if evaluate_heuristic_global():

                send_message(agent, 'evaluate', 1 , action)

            else:

                a_star = find_a_star()

        if msg.type == 'evaluate':  # received evaluate message from j

            lock (a_star_candidate = find_a_star(agent, spanning_tree))
            p_i = 0

            if a_star_candidate != 'locked':

                for j in spanning_tree.neighbours(agent).remove(msg.mfrom):

                    send_message(agent, j, 'evaluate')

                    if spanning_tree.is_leaf(agent):
                        send_message(agent, agent, 0.0, 'accumulate_payoff')

        if msg.type == 'accumulate_payoff':

            p_i = p_i + msg.data

            # Add child node list

            if received_payoff_from_all_children:

                get_actions
                a_j_candidate =
                from j in Gamma(agent) in CG

                g_i = calculate_g_i()

                if spanning_tree.is_root(agent):

                    for j in spanning_tree.children(agent):

                        send_message(agent, j, g_i + p_i, 'global_payoff')

                    else:

                        send_message(agent, spanning_tree.parent(agent), p_i + g + i, 'accumulate_payoff')

        if msg.type == 'accumulate_payoff':

            if msg.data > m:
                a_star = a_star_candidate
                m = g

            for j in spanning_tree.children(agent):
                send_message(agent, j, g, 'global_payoff')
            # unlock a_star_candidate


    return a_star

def calcualte_g_i():
    return

def find_a_star():
    return 'a_star'

def compute_m_i_j():
    return

def evaluate_heuristic_global():
    return True
    #return False

class load_state():
    def __init__(self, on_state, submitted):

        self.on = on_state
        self.submitted_req = submitted

    def set_submitted(self, val):
        self.submitted_req = val

    def set_on_state(self, val):
        self.on = val

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

def request_state(lstate):

    if lstate.submitted_req == False:
        rnd = random.random()
        if rnd > 0.9 :
           on = True
        else:
           on = False
    else:
        on = True

    return on

def main(agent_id , spanning_tree):

    #-------------------#
    m_i_j = 0
    m_j_i = 0
    # j subset Gamma(i) == Neighbour nodes
    g_i = 0
    p_i = 0
    m = -inf
    # -------------------#

    l_state = load_state(False, False)
    episodes = 1000
    start_tslot = time.time()

    lock_list = []
    payoff_list = []

    dqn = DQNAgent(6 , 2)

    for i in range(episodes):

        ## State Variables for NN
        l_state.set_on_state(request_state(l_state))
        now = datetime.datetime.now()
        day, month, hour = now.day, now.month, now.hour
        state = np.array([day, month, hour, l_state.get_on_state()])
        ##


        # MAX PLUS Goes HERE
        while time.time() - start_tslot > 15.0:

            # wait for message
            msg = message_decoder(poll_for_incoming(agent_id)[0])

            if msg.type == 'max_plus':  # message == m_j_i // max_plus_message:

                for j in spanning_tree.neighbours(agent_id):

                    m_i_j = compute_m_i_j(agent_id, j)
                    # m_i_j =

                    if m_i_j != m_i_j_last:
                        send_message(m_i_j_a_j):

                if use_anytime_extension:

                    if evaluate_heuristic_global():

                        send_message(agent_id, 'evaluate', 1, action)

                    else:

                        a_star = find_a_star()

            if msg.type == 'evaluate':  # received evaluate message from j _ send eval
                # to all in ST =/= j

                #lock(a_star_candidate=find_a_star(agent_id, spanning_tree))
                lock_list.append("argmax a star")
                p_i = 0

                if a_star_candidate != 'locked':

                    for j in spanning_tree.neighbours(agent_id).remove(msg.mfrom):

                        send_message(agent_id, j, 'evaluate')

                        if spanning_tree.is_leaf(agent_id):
                            send_message(agent_id, agent_id, 0.0, "null",'accumulate_payoff')

            if msg.type == 'accumulate_payoff':

                p_i = p_i + msg.data

                # Add child node list
                payoff_list

                if received_payoff_from_all_children:

                    get_actions
                    a_j_candidate =
                    from j in Gamma(agent_id) in CG

                    g_i = calculate_g_i()

                    if spanning_tree.is_root(agent_id):

                        for j in spanning_tree.children(agent_id):

                            send_message(agent_id, j, g_i + p_i, 'global_payoff')

                        else:

                            send_message(agent_id, spanning_tree.parent(agent_id), p_i + g + i, 'accumulate_payoff')

            if msg.type == 'accumulate_payoff':

                if msg.data > m:
                    a_star = a_star_candidate
                    m = g

                for j in spanning_tree.children(agent):
                    send_message(agent, j, g, 'global_payoff')
                # unlock a_star_candidate
            action = dqn.act(state)

            # act and wait for env feedback
            next_state, reward, done , _ = 0,0,0,0

            dqn.remember(state, action, reward, next_state, done)

            state = next_state

            if done == True:
                print("Agent %d, performed action %d, at timeslot %d, with reward %0.2f" % (agent_id, action, 10 , reward))
                break


        dqn.replay(16)


