import random
from math import log


class car:
    def __init__(self, time, direction):
        self.time = time
        self.arrived = 0
        self.direction = direction
        self.already_on_line = False

        # 0 - left , 1 - straight ,2 - right

    def transit(self, time):
        self.arrived = 1
        self.time = time
        return self.time


#====================================================================
direction_counter = 0
#====================================================================


def car_generator(cur_time, arrival_speed):
    car_t = cur_time - log(1 - random.random()) * arrival_speed
    global direction_counter
    direction_counter = car_direction = (direction_counter + 1) % 4

    if direction_counter == 3:
        car_direction = 1

    return car(round(car_t, 1), car_direction)

#====================================================================
#====================================================================


def timer_correction(queue, future):
    min_t = future[0].time
    to_current = []

    for itm in future:
        if itm.time < min_t:
            min_t = itm.time
            to_current = [itm]
        elif itm.time == min_t:
            to_current.append(itm)

    for itm in to_current:
        direct = itm.direction

        if itm.arrived == 1:
            queue[direct].insert(0, itm)
        else:
            queue[direct].append(itm)

    for itm in to_current:
        future.pop(future.index(itm))

    cur_time = min_t

    return cur_time, queue, future

#====================================================================
#====================================================================


def scan_phase(queue, direction_is_busy, future, stop, cur_time, speed):

    for car_direction, queue_direct in enumerate(queue):
        if len(queue_direct):
            if queue_direct[0].arrived and not stop:
                direction_is_busy[car_direction] = 0
                queue_direct.pop(0)

                if len(queue_direct):
                    direction_is_busy[car_direction] = 1
                    car_arr = queue_direct[0]
                    car_arr.transit(
                        cur_time + round(-log(1 - random.random())*speed[car_direction], 1))
                    future = future + [car_arr]
                    queue_direct.pop(0)

            elif not direction_is_busy[car_direction]:
                direction_is_busy[car_direction] = 1
                car_arr = queue_direct[0]
                car_arr.transit(
                    cur_time + round(-log(1 - random.random())*speed[car_direction], 1))
                future = future + [car_arr]
                queue_direct.pop(0)

    return queue, direction_is_busy, future

#====================================================================
#====================================================================


random.seed(0)

cur_time = 0
arrival_speed = 3.
queue = [[], [], []]
sum_queue = [0, 0, 0]
direction_is_busy = [0, 0, 0]
direction_car = [0, 0, 0]
future = [car_generator(cur_time, arrival_speed)]
last_car_time = future[0].time
speed = [3., 3., 3.]
#print("time = ", last_car_time)
k = 1
i = 0

while cur_time < 3600:
    i += 1
    speed[1] = 3
    stop = 0

    cur_time, queue, future = timer_correction(queue, future)

    sum_queue[0] += len(queue[0])
    sum_queue[1] += len(queue[1])
    sum_queue[2] += len(queue[2])

    if cur_time % 240 >= 60:
        stop = 1
    elif cur_time % 240 >= 10:
        speed[2] = 1.2

   # print("==================================")
   # print("  time = ", cur_time)
   # print("  speed = ", speed)
   # print("  stop = ", stop)
 #   print("  queue:")
 #   print("      0: ", queue[0])
 #   print("      1: ", queue[1])
 #   print("      2: ", queue[2])
 #   print("  future: ", future)

    if cur_time == last_car_time:
        car_gen = car_generator(cur_time, arrival_speed)
        direction_car[car_gen.direction] += 1
        last_car_time = car_gen.time
        future.append(car_gen)
        k += 1

 #   print("  future_2: ", future)

    queue, direction_is_busy, future = scan_phase(
        queue, direction_is_busy, future, stop, cur_time, speed)

print(k)
print(direction_car[0], direction_car[1], direction_car[2])
print(sum_queue[0]/i, sum_queue[1]/i, sum_queue[2]/i)
