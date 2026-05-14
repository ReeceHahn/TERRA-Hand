"""
************************************************************************************************************************
Libraries:
    [1] aakmsk, serial_bus_servo_controller_python_module. Python module for controlling Hiwonder serial bus servos
    through the Hiwonder serial bus servo controller.
************************************************************************************************************************
"""

import time
from lib import serial_bus_servo_controller as sbsc

# global constants
port = "COM3"
neutral_position = 500
number_of_servos = 16
default_move_time = 2000

# servo index constants
middle_mcp_flexion = 1 # 300 to 660
middle_pip_dip_flexion = 2 # 300 to 600
thumb_cmc_flexion = 3 # 300 to 720
thumb_cmc_abduction = 4 # 400 to 650
middle_mcp_abduction = 5 # 350 to 650
ring_mcp_abduction = 6 # 350 to 650
pinky_pip_dip_flexion = 7 # 280 to 570
pinky_mcp_flexion = 8 # 280 to 610
index_mcp_flexion = 9 # 340 to 680
ring_pip_dip_flexion = 10 # 440 to 750
ring_mcp_flexion = 11 # 360 to 660
pinky_mcp_abduction = 12 # 350 to 650
index_pip_dip_flexion = 13 # 400 to 700
thumb_mp_flexion = 14 # 390 to 780
thumb_ip_flexion = 15 # 400 to 680
index_mcp_abduction = 16 # 350 to 650

# global servo limits, experimentally determined values, since the spool design is currently limiting these are quite conservative until a superior design is made
servo_limits = {
    1:  (300, 660),
    2:  (300, 600),
    3:  (300, 720),
    4:  (430, 740),
    5:  (350, 650),
    6:  (350, 650),
    7:  (280, 570),
    8:  (280, 610),
    9:  (340, 680),
    10: (440, 750),
    11: (360, 660),
    12: (350, 650),
    13: (400, 700),
    14: (390, 780),
    15: (400, 680),
    16: (350, 650),
}

# global variable to store servo controller object
controller = None

# motors setup function to initialise connection to the bus servo controller
def motors_setup():
    global controller

    controller = sbsc.SBS_Controller(port)

# function to constrain servo position within experimentally defined hard limits
def constrain_servo_position(servo_id, position):
    position = int(position)

    min_position = servo_limits[servo_id][0]
    max_position = servo_limits[servo_id][1]

    if position < min_position:
        return min_position

    if position > max_position:
        return max_position

    return position

# function to move a single servo to a specified position
def move_servo(servo_id, position, move_time=default_move_time):
    safe_position = constrain_servo_position(servo_id, position)

    controller.cmd_servo_move([servo_id], [safe_position], move_time)

# function to move multiple servos using a dictionary of servo ids and positions
def move_servos(servo_positions, move_time=default_move_time):
    servo_ids = []
    safe_positions = []

    for servo_id, position in servo_positions.items():
        servo_ids.append(servo_id)
        safe_positions.append(constrain_servo_position(servo_id, position))

    controller.cmd_servo_move(servo_ids, safe_positions, move_time)

# function to move all servos to the neutral position
def neutral_all(move_time=default_move_time):
    servo_positions = {}

    for servo_id in range(1, number_of_servos + 1):
        servo_positions[servo_id] = neutral_position

    move_servos(servo_positions, move_time)

# function to move the index finger
def move_index_finger(mcp_abduction, mcp_flexion, pip_dip_flexion, move_time=default_move_time):
    move_servos({
        index_mcp_abduction: mcp_abduction,
        index_mcp_flexion: mcp_flexion,
        index_pip_dip_flexion: pip_dip_flexion,
    }, move_time)

# function to move the middle finger
def move_middle_finger(mcp_abduction, mcp_flexion, pip_dip_flexion, move_time=default_move_time):
    move_servos({
        middle_mcp_abduction: mcp_abduction,
        middle_mcp_flexion: mcp_flexion,
        middle_pip_dip_flexion: pip_dip_flexion,
    }, move_time)

# function to move the ring finger
def move_ring_finger(mcp_abduction, mcp_flexion, pip_dip_flexion, move_time=default_move_time):
    move_servos({
        ring_mcp_abduction: mcp_abduction,
        ring_mcp_flexion: mcp_flexion,
        ring_pip_dip_flexion: pip_dip_flexion,
    }, move_time)

# function to move the pinky finger
def move_pinky_finger(mcp_abduction, mcp_flexion, pip_dip_flexion, move_time=default_move_time):
    move_servos({
        pinky_mcp_abduction: mcp_abduction,
        pinky_mcp_flexion: mcp_flexion,
        pinky_pip_dip_flexion: pip_dip_flexion,
    }, move_time)

# function to move the thumb
def move_thumb(cmc_abduction, cmc_flexion, mp_flexion, ip_flexion, move_time=default_move_time):
    move_servos({
        thumb_cmc_abduction: cmc_abduction,
        thumb_cmc_flexion: cmc_flexion,
        thumb_mp_flexion: mp_flexion,
        thumb_ip_flexion: ip_flexion,
    }, move_time)

def open_hand(move_time=default_move_time):
    move_servos({
        index_mcp_abduction: 560,
        index_mcp_flexion: 420,
        index_pip_dip_flexion: 565,

        middle_mcp_abduction: 590,
        middle_mcp_flexion: 510,
        middle_pip_dip_flexion: 415,

        ring_mcp_abduction: 490,
        ring_mcp_flexion: 490,
        ring_pip_dip_flexion: 630,

        pinky_mcp_abduction: 475,
        pinky_mcp_flexion: 470,
        pinky_pip_dip_flexion: 425,
        
        thumb_cmc_abduction: 555,
        thumb_cmc_flexion: 565,
        thumb_mp_flexion: 670,
        thumb_ip_flexion: 610,
    }, move_time)

# function to move the hand to the power grasp pose
def power_grasp(move_time=default_move_time):
    move_servos({
        index_mcp_abduction: 615,
        index_mcp_flexion: 640,
        index_pip_dip_flexion: 650,

        middle_mcp_abduction: 590,
        middle_mcp_flexion: 350,
        middle_pip_dip_flexion: 300,

        ring_mcp_abduction: 490,
        ring_mcp_flexion: 660,
        ring_pip_dip_flexion: 740,

        pinky_mcp_abduction: 440,
        pinky_mcp_flexion: 300,
        pinky_pip_dip_flexion: 300,
        
        thumb_cmc_abduction: 550,
        thumb_cmc_flexion: 575,
        thumb_mp_flexion: 760,
        thumb_ip_flexion: 470,
    }, move_time)

# function to move the hand to the single finger pinch pose
def single_finger_pinch(move_time=default_move_time):
    move_servos({
        index_mcp_abduction: 560,
        index_mcp_flexion: 670,
        index_pip_dip_flexion: 690,

        middle_mcp_abduction: 590,
        middle_mcp_flexion: 510,
        middle_pip_dip_flexion: 415,

        ring_mcp_abduction: 490,
        ring_mcp_flexion: 490,
        ring_pip_dip_flexion: 630,

        pinky_mcp_abduction: 475,
        pinky_mcp_flexion: 470,
        pinky_pip_dip_flexion: 425,
        
        thumb_cmc_abduction: 720,
        thumb_cmc_flexion: 445,
        thumb_mp_flexion: 780,
        thumb_ip_flexion: 470,
    }, move_time)

# function to move the hand to the double finger pinch pose
def double_finger_pinch(move_time=default_move_time):
    move_servos({
        index_mcp_abduction: 615,
        index_mcp_flexion: 670,
        index_pip_dip_flexion: 690,

        middle_mcp_abduction: 590,
        middle_mcp_flexion: 310,
        middle_pip_dip_flexion: 300,

        ring_mcp_abduction: 490,
        ring_mcp_flexion: 490,
        ring_pip_dip_flexion: 630,

        pinky_mcp_abduction: 475,
        pinky_mcp_flexion: 470,
        pinky_pip_dip_flexion: 425,
        
        thumb_cmc_abduction: 700,
        thumb_cmc_flexion: 400,
        thumb_mp_flexion: 760,
        thumb_ip_flexion: 470,
    }, move_time)

def finger_tip_sequence_1(move_time=default_move_time):
    move_servos({
        index_mcp_abduction: 560,
        index_mcp_flexion: 670,
        index_pip_dip_flexion: 690,

        middle_mcp_abduction: 590,
        middle_mcp_flexion: 510,
        middle_pip_dip_flexion: 415,

        ring_mcp_abduction: 490,
        ring_mcp_flexion: 490,
        ring_pip_dip_flexion: 630,

        pinky_mcp_abduction: 475,
        pinky_mcp_flexion: 470,
        pinky_pip_dip_flexion: 425,
        
        thumb_cmc_abduction: 720,
        thumb_cmc_flexion: 445,
        thumb_mp_flexion: 780,
        thumb_ip_flexion: 470,
    }, move_time)

def finger_tip_sequence_2(move_time=default_move_time):
    move_servos({
        index_mcp_abduction: 560,
        index_mcp_flexion: 420,
        index_pip_dip_flexion: 565,

        middle_mcp_abduction: 590,
        middle_mcp_flexion: 310,
        middle_pip_dip_flexion: 310,

        ring_mcp_abduction: 490,
        ring_mcp_flexion: 490,
        ring_pip_dip_flexion: 630,

        pinky_mcp_abduction: 475,
        pinky_mcp_flexion: 470,
        pinky_pip_dip_flexion: 425,
        
        thumb_cmc_abduction: 695,
        thumb_cmc_flexion: 310,
        thumb_mp_flexion: 705,
        thumb_ip_flexion: 470,
    }, move_time)

def finger_tip_sequence_3(move_time=default_move_time):
    move_servos({
        index_mcp_abduction: 560,
        index_mcp_flexion: 420,
        index_pip_dip_flexion: 565,

        middle_mcp_abduction: 590,
        middle_mcp_flexion: 510,
        middle_pip_dip_flexion: 415,

        ring_mcp_abduction: 490,
        ring_mcp_flexion: 650,
        ring_pip_dip_flexion: 740,

        pinky_mcp_abduction: 475,
        pinky_mcp_flexion: 470,
        pinky_pip_dip_flexion: 425,
        
        thumb_cmc_abduction: 620,
        thumb_cmc_flexion: 310,
        thumb_mp_flexion: 705,
        thumb_ip_flexion: 505,
    }, move_time)

def finger_tip_sequence_4(move_time=default_move_time):
    move_servos({
        index_mcp_abduction: 560,
        index_mcp_flexion: 420,
        index_pip_dip_flexion: 565,

        middle_mcp_abduction: 590,
        middle_mcp_flexion: 510,
        middle_pip_dip_flexion: 415,

        ring_mcp_abduction: 490,
        ring_mcp_flexion: 490,
        ring_pip_dip_flexion: 630,

        pinky_mcp_abduction: 475,
        pinky_mcp_flexion: 280,
        pinky_pip_dip_flexion: 280,
        
        thumb_cmc_abduction: 575,
        thumb_cmc_flexion: 330,
        thumb_mp_flexion: 685,
        thumb_ip_flexion: 570,
    }, move_time)

# function to unload torque from all servos
def unload_all():
    servo_ids = []

    for servo_id in range(1, number_of_servos + 1):
        servo_ids.append(servo_id)

    controller.cmd_mult_servo_unload(servo_ids)

# test example to see the current draw of 2 motors simul operation, gradually increase until confident all 16 can operate at once
if __name__ == "__main__":

    # initialise motor controller connection
    motors_setup()

    # test simultaneous movement of two servos
    move_servos({
        index_mcp_flexion: 600,
        middle_mcp_flexion: 600,
    }, 2000)

    time.sleep(2)

    move_servos({
        index_mcp_flexion: 400,
        middle_mcp_flexion: 400,
    }, 2000)