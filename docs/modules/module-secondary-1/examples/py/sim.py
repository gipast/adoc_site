import os
import sys
import math
import numpy as np

from enum import IntEnum, auto
from itertools import cycle
from operator import attrgetter

class Color(IntEnum):
    _order_ = 'GREEN RED'
    GREEN = 1
    RED = 2


class queue():
    def __init__(self):
        self.size = 0
        self.times = []
        self.vals = []
        self.time = 0
        self.sum = 0

    def plot_update(self, time, next_val):
        self.vals.append(self.size)
        self.times.append(time)
        self.sum += self.size * (time - self.time)

        self.vals.append(next_val)
        self.times.append(time)

        self.time = time
        self.size = next_val

    def add(self, time):
        self.plot_update(time, self.size + 1)

    def sub(self, time):
        if self.size > 0:
            self.plot_update(time, self.size - 1)

    def free(self, time):
        self.plot_update(time, 0)

    def get_mean_val(self):
        return self.sum / self.time


class semaphore():

    colors = ['GREEN', 'RED']

    def __init__(self, start_color=Color.RED):
        self.sem = cycle(enumerate(semaphore.colors, start=start_color))
        self.value = next(self.sem)

    def turn_ligth(self):
        self.value = next(self.sem)
        pass


class sim_event():

    def __init__(self, action, sys_time, time):
        self.time = sys_time + time
        self.action = action


class Sim(sim_event):
    next_evets_queue = []
    time = 0

    def finished(self):
        print("sim done")

    def new_event(self, action, time):
        event = sim_event(action, self.time, time)
        self.next_evets_queue.append(event)

    def __init__(self, sim_time):
        self.sim_time = sim_time
        self.event = sim_event(None, 0, 0)
        self.new_event(self.finished, sim_time)

    def pop_event(self):
        '''
        pops event with min time from queue self.event
        '''
        if len(self.next_evets_queue) == 0:
            return None
        min_val = min(self.next_evets_queue, key=attrgetter('time'))
        minpos = self.next_evets_queue.index(min_val)
        self.event = self.next_evets_queue[minpos]
        self.time = min_val.time

        self.next_evets_queue.remove(self.event)
        return 0

if __name__ == "__main__":
    pass
