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
        msg = message(get_message())

        if msg.type == 'max_plus'  # message == m_j_i // max_plus_message:

            for j in spanning_tree.neighbours(agent):

                m_i_j = compute_m_i_j(agent, j)

                if m_i_j != m_i_j_last:
                    send_message(m_i_j_a_j):

        if use_anytime_excpetion:

            if evaluate_heuristic_global():

                send_message(agent, 'evaluate')

            else:

                a_star = find_a_star()

        if msg.type == 'evaluate':  # received evaluate message from j

            lock
            a_star_candidate = find_a_star(agent, spanning_tree)
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
    return False
