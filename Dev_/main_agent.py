import os
from multiprocessing import Pool

agents = 20

processes = ['/home/filippos/PycharmProjects/thesis_pronios_v1/Dev_/alpha_agent.py' for i in range(agents)]

#processes = ('alpha_agent.py')


def run_process(process):
    print("STARTING AGENTS")
    os.system('python3 {}'.format(process))


pool = Pool(processes=agents)
pool.map(run_process, processes)