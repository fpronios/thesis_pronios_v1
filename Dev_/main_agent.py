import os
from multiprocessing import Pool

agents = 4

processes = ['alpha_agent.py' for i in range(agents)]

#processes = ('alpha_agent.py')


def run_process(process):
    os.system('python3 {}'.format(process))


pool = Pool(processes=agents)
pool.map(run_process, processes)