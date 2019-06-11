;  GPSS/PC Traffic Light Simulation

GENERATE ,,,1
ADVANCE 3600
TERMINATE 1

;GREENTIME EQU        10
;REDTIME EQU          10

PASS_TIME EQU 7
GAP_TIME EQU  3
BTN_PRESSS_DELAY EQU 10

CAR_INTENSE equ 60/25
MAN_INTENSE equ 60/2

wait_time VARIABLE  C1 - X$car_start_time
CarsPassSpeed  FUNCTION wait_time,D2
10,10/11,50

GENERATE 0,0,0,1
LOGIC R man_sem
LOGIC R btn
MARK_HANDLER LOGIC S car_sem
SAVEVALUE car_start_time,C1

GATE LS btn
ADVANCE BTN_PRESSS_DELAY
LOGIC R car_sem
LOGIC S man_sem
LOGIC R btn
ADVANCE PASS_TIME
LOGIC R man_sem
ADVANCE GAP_TIME
TRANSFER ,MARK_HANDLER


GENERATE                MAN_INTENSE;Create people queue
QUEUE q_people

   GATE LS car_sem,CARS_NOT_MOVE
GATE LR btn,CARS_NOT_MOVE
LOGIC S btn ; # PUSH_THE_BUTTON

CARS_NOT_MOVE GATE LS man_sem
PASS_THE_ROAD DEPART q_people
TERMINATE


GENERATE     CAR_INTENSE                ;Create next automobile.
QUEUE q_cars
SEIZE cross
ADVANCE (Exponential(2,0,60/FN$CarsPassSpeed))
GATE LS car_sem
DEPART q_cars
RELEASE cross

TERMINATE; INCOMING CARS

START 1
