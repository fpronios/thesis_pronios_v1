import zmq
import time
import sys
import random
from multiprocessing import Process

agent_id_loc = 0


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
    sep = '?'
    msg_str = str(msg.type) + sep + str(msg.mfrom) + sep + str(msg.mto) + sep + str(msg.mdat) + sep + str(msg.t_slot)

    return msg_str

def server_push(port, mfrom, mto , mdat, t_slot = 1):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:%s" % port)
    print ("Running server on port: ", port)
    # serves only 5 request and dies
    msg = message("type", mfrom,mto,mdat,t_slot)
    for reqnum in range(10):
        if reqnum < 6:
            socket.send_string(message_decoder(msg))
        else:
            socket.send_string("Exit")
            break
        time.sleep (1)



def server_pub(port,  mfrom, mto , mdat, t_slot = 1):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    publisher_id = agent_id_loc#random.randrange(0,9999)
    print ("Running server on port: ", port)
    # serves only 5 request and dies
    msg = message("type", mfrom, mto, mdat, t_slot)
    print("msg")
    print(message_decoder(msg))
    for reqnum in range(10):
        # Wait for next request from client
        topic = random.randrange(8,10)
        messagedata = "server#%s" % publisher_id
        print ("%s %s" % (topic, messagedata))

        socket.send_string("%d %s" % (topic,  socket.send_string(message_decoder(msg))))
        time.sleep(1)



def client(port_push, port_sub):
    context = zmq.Context()
    socket_pull = context.socket(zmq.PULL)
    socket_pull.connect ("tcp://localhost:%s" % port_push)
    print ("Connected to server with port %s" % port_push)
    socket_sub = context.socket(zmq.SUB)
    socket_sub.connect ("tcp://localhost:%s" % port_sub)
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, "9")
    print ("Connected to publisher with port %s" % port_sub)
    # Initialize poll set
    poller = zmq.Poller()
    poller.register(socket_pull, zmq.POLLIN)
    poller.register(socket_sub, zmq.POLLIN)

    # Work on requests from both server and publisher
    should_continue = True
    while should_continue:
        socks = dict(poller.poll())
        if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
            message = socket_pull.recv()
            print ("Recieved control command: %s" % message)
            if message == "Exit":
                print ("Recieved exit command, client will stop recieving messages")
                should_continue = False

        if socket_sub in socks and socks[socket_sub] == zmq.POLLIN:
            string = socket_sub.recv()
            topic, messagedata = string.split()
            print ("Processing ... ", topic, messagedata)


def client_sub(port_push, port_sub):
    context = zmq.Context()

    socket_sub = context.socket(zmq.SUB)
    socket_sub.connect ("tcp://localhost:%s" % port_sub)
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, "9")
    #socket_sub.setsockopt_string(zmq.SUBSCRIBE, "8")

    print ("Connected to publisher with port %s" % port_sub)
    # Initialize poll set
    poller = zmq.Poller()

    poller.register(socket_sub, zmq.POLLIN)

    # Work on requests from both server and publisher
    should_continue = True
    while should_continue:
        socks = dict(poller.poll())
        if socket_sub in socks and socks[socket_sub] == zmq.POLLIN:
            string = socket_sub.recv()
            print("raw string", string)
            topic, messagedata = string.split()
            print ("Processing ... Agent: ",agent_id_loc , topic, messagedata)




def push_to_parent():
    #get the parent ID from the graph and fetch a message
    #maybe parent has subbed on the children
    return 0

def poll_parent():
    #check if parent sent a new message
    #child should be subbed and poll the parent at this point
    return 0

def push_to_children():
    # children should be subs
    return 0

def poll_children():
    # check if children have sent a mesg
    # we should be subscribers to all children
    return 0

#
#   Create the publishers needed (one||two per agent )
#
def init_binds():
    return 0

#
#   Subscribe to the children and parents
#
def init_subs():

    return 0



def main(agent_id, server_push_port, server_pub_port , parent, children):

    global agent_id_loc

    agent_id_loc = agent_id
    #Process(target=server_push, args=(server_push_port,)).start()
    if agent_id == 1:
        Process(target=server_pub, args=(server_push_port, 1, 10 , "Test_data", )).start()
        Process(target=server_push, args=(server_push_port, 1, 10 , "Test_data", )).start()
    #Process(target=client_sub, args=(server_push_port, server_pub_port,)).start()
    Process(target=client, args=(server_push_port,server_pub_port,)).start()


if __name__ == "__main__":
    # Now we can run a few servers
    #server_push_port = "5556"
    #server_pub_port = "5558"
    main("5556", "5558")
