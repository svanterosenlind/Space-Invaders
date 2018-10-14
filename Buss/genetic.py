from BusSimulator2018 import *
import math

class Element:
    def __init__(self):
        self.DNA = []
        for i in range(0,8):
            self.DNA.append(random.uniform(0, 1))

    def calc_fitness(self):
        tests = []
        tests.append(run_test(0.8052851667301792, self.DNA))
        tests.append(run_test(0.6644829848107292, self.DNA))
        #tests.append(run_test(0.11961149616900346, self.DNA))
        tests.append(run_test(0.782542161415102, self.DNA))
        return 100000 / sum(tests)


def run_test(seed, params):
    random.seed(seed)
    world = World(params)

    t = 0
    while t < Simulation_Length*86400:
        t += 1
        world.create_passengers(seed)
        world.happen()

    world.waited_time += world.waited_time_of_existing_people()
    return world.waited_time
