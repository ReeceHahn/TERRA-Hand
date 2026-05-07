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
middle_mcp_flexion = 1
middle_pip_dip_flexion = 2
thumb_cmc_flexion = 3
thumb_cmc_abduction = 4
middle_mcp_abduction = 5
ring_mcp_abduction = 6
pinky_pip_dip_flexion = 7
pinky_mcp_flexion = 8
index_mcp_flexion = 9
ring_pip_dip_flexion = 10
ring_mcp_flexion = 11
pinky_mcp_abduction = 12
index_pip_dip_flexion = 13
thumb_mp_flexion = 14
thumb_ip_flexion = 15
index_mcp_abduction = 16

# global servo limits, experimentally determined values (REPLACE THESE)
servo_limits = {
    1:  (490, 510),
    2:  (490, 510),
    3:  (490, 510),
    4:  (490, 510),
    5:  (490, 510),
    6:  (490, 510),
    7:  (490, 510),
    8:  (490, 510),
    9:  (490, 510),
    10: (490, 510),
    11: (490, 510),
    12: (490, 510),
    13: (490, 510),
    14: (490, 510),
    15: (490, 510),
    16: (490, 510),
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

    controller.cmd_servo_move(
        [servo_id],
        [safe_position],
        move_time
    )

# function to move multiple servos using a dictionary of servo ids and positions
def move_servos(servo_positions, move_time=default_move_time):
    servo_ids = []
    safe_positions = []

    for servo_id, position in servo_positions.items():
        servo_ids.append(servo_id)
        safe_positions.append(constrain_servo_position(servo_id, position))

    controller.cmd_servo_move(
        servo_ids,
        safe_positions,
        move_time
    )

# function to move all servos to the neutral position
def neutral_all(move_time=default_move_time):
    servo_positions = {}

    for servo_id in range(1, number_of_servos + 1):
        servo_positions[servo_id] = neutral_position

    move_servos(servo_positions, move_time)

# emergency stop function, currently returns all servos to neutral open hand position
def emergency_stop():
    open_hand()

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

# function to move the hand to the open hand pose
def open_hand(move_time=default_move_time):
    move_index_finger(500, 500, 500, move_time)
    move_middle_finger(500, 500, 500, move_time)
    move_ring_finger(500, 500, 500, move_time)
    move_pinky_finger(500, 500, 500, move_time)
    move_thumb(500, 500, 500, 500, move_time)

# function to move the hand to the power grasp pose
def power_grasp(move_time=default_move_time):
    move_index_finger(500, 500, 500, move_time)
    move_middle_finger(500, 500, 500, move_time)
    move_ring_finger(500, 500, 500, move_time)
    move_pinky_finger(500, 500, 500, move_time)
    move_thumb(500, 500, 500, 500, move_time)

# function to move the hand to the pinch pose
def pinch(move_time=default_move_time):
    move_index_finger(500, 500, 500, move_time)
    move_middle_finger(500, 500, 500, move_time)
    move_ring_finger(500, 500, 500, move_time)
    move_pinky_finger(500, 500, 500, move_time)
    move_thumb(500, 500, 500, 500, move_time)

# function to move the hand to the fist pose
def fist(move_time=default_move_time):
    move_index_finger(500, 500, 500, move_time)
    move_middle_finger(500, 500, 500, move_time)
    move_ring_finger(500, 500, 500, move_time)
    move_pinky_finger(500, 500, 500, move_time)
    move_thumb(500, 500, 500, 500, move_time)

# function to unload torque from all servos if supported by the controller
def unload_all():
    servo_ids = []

    for servo_id in range(1, number_of_servos + 1):
        servo_ids.append(servo_id)

    controller.cmd_mult_servo_unload(servo_ids)