import os
import sys
import random
from math import log

import matplotlib.pyplot as plt

from sim import Color, semaphore
from sim import Sim as simulation
from sim import queue

simulation_time = 3600

simul = simulation(simulation_time)

car_queue = queue()
man_queue = queue()

def exp_generator(mean):
    return -log(1 - random.random()) * mean


class semaphore_w_button():
    def __init__(self):
        self.button_active = True

        self.car_sem = semaphore(start_color= Color.RED)
        self.people_sem = semaphore(start_color=Color.RED)
        self.press_button_event = None
        self.change_state_time = 0

        self.btn_delay_time = 0

    def press_button(self):
        if sem.button_active == True:
            sem.button_active = False
            simul.new_event(self.allow_people_pass, 10)

    def button_activate(self):
        self.button_active = True

    def deprecate_car_pass(self):
        self.car_sem.value = Color.RED
        simul.new_event(self.button_activate, self.btn_delay_time)

    def allow_people_pass(self):
        self.deprecate_car_pass()
        self.people_sem.value = Color.GREEN

        global man_queue
        man_queue.free(simul.time)

        simul.new_event(self.deprecate_people_pass, 7)
        simul.new_event(self.allow_car_pass, 10)

    def deprecate_people_pass(self):
        self.people_sem.value = Color.RED

    def car_generator_pass(self):
        if self.car_sem.value != Color.GREEN:
            return

        global car_queue
        car_queue.sub(simul.time)

        if simul.time - self.change_state_time > 10:
            mean = 60. / 50.
        else:
            mean = 60. / 10.
        simul.new_event(self.car_generator_pass, exp_generator(mean))

    def allow_car_pass(self):
        if self.people_sem.value == Color.GREEN:
            raise BaseException
        self.car_sem.value = Color.GREEN

        self.change_state_time = simul.time

        simul.new_event(self.car_generator_pass, 0)


sem = semaphore_w_button()

def car_generator():
    simul.new_event(car_generator, exp_generator(60. / 25.))
    global car_queue
    car_queue.add(simul.time)

def people_generator():
    if sem.people_sem.value == Color.RED:
        sem.press_button()

        global man_queue
        man_queue.add(simul.time)

    simul.new_event(people_generator, exp_generator(60. / 2.))


def plot_results():
    fig, axes = plt.subplots(2, 1, figsize=(12, 9), sharex=True)
    fig.set_dpi(100)
    axes[0].plot(car_queue.times, car_queue.vals, linewidth=2.0, linestyle="-")
    axes[0].set_xlabel("time", fontsize=16)
    axes[0].set_ylabel("car queue size", fontsize=16)
    axes[0].grid()

    axes[1].plot(man_queue.times, man_queue.vals, linewidth=2.0, linestyle="-")
    axes[1].set_xlabel("time", fontsize=16)
    axes[1].set_ylabel("man queue", fontsize=16)
    axes[1].grid()


    # axes[0].plot([0, car_queue.time], [car_queue.get_mean_val(),
    #                                    car_queue.get_mean_val()], linewidth=1.0, linestyle="--")
    # axes[1].plot([0, man_queue.time], [man_queue.get_mean_val(),
    #                                    man_queue.get_mean_val()], linewidth=1.0, linestyle="--")

    plt.tight_layout()
    plt.show()

def main():
    sem.btn_delay_time = 100

    car_generator()
    people_generator()

    sem.allow_people_pass()

    while simul.pop_event() != None:
        if simul.time > simul.sim_time:
            break

        # print("time:", simul.time)
        simul.event.action()

    print("mean queue len: ",car_queue.get_mean_val(), man_queue.get_mean_val())

    plot_results()

if __name__ == "__main__":
    main()
