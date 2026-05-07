"""
************************************************************************************************************************
Libraries:
  [1] PyLX-16A Library. Python library for LewanSoul / Hiwonder serial bus servos.
************************************************************************************************************************
"""

from pylx16a.lx16a import *
import time

# global constants
port = "COM1" # make sure to change this to actual com port for motor control board
neutral_position = 500
number_of_servos = 16

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

# global servo limits, experimentally determined values (REMEMBER TO REPLACE THESE WITH TESTED VALUES WHEN IN LAB!!!!!!!!!!!!!! IMPORTANT. REQUIRES FULL TIGHTENING OF ALL SERVO MOTORS BEFORE)
servo_limits = {
    1:  (350, 650),
    2:  (350, 650),
    3:  (350, 650),
    4:  (350, 650),
    5:  (350, 650),
    6:  (350, 650),
    7:  (350, 650),
    8:  (350, 650),
    9:  (350, 650),
    10: (350, 650),
    11: (350, 650),
    12: (350, 650),
    13: (350, 650),
    14: (350, 650),
    15: (350, 650),
    16: (350, 650),
}

# global variable to store servo objects
servos = {}

# motors setup function to initialise connection to all bus servos
def motors_setup():
    LX16A.initialize(port)

    for servo_id in range(1, number_of_servos + 1):
        servos[servo_id] = LX16A(servo_id)

# function to constrain servo position within hard limits
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
def move_servo(servo_id, position):
    safe_position = constrain_servo_position(servo_id, position)
    servos[servo_id].move(safe_position)

# function to move multiple servos using a dictionary of servo ids and positions
def move_servos(servo_positions):
    for servo_id, position in servo_positions.items():
        move_servo(servo_id, position)

# function to move all servos to the neutral position
def neutral_all():
    for servo_id in range(1, number_of_servos + 1):
        move_servo(servo_id, neutral_position)

# emergency stop function, currently returns all servos to neutral open hand position (need to make this better somehow)
def emergency_stop():
    open_hand()

# function to move the index finger
def move_index_finger(mcp_abduction, mcp_flexion, pip_dip_flexion):
    move_servos({
        index_mcp_abduction: mcp_abduction,
        index_mcp_flexion: mcp_flexion,
        index_pip_dip_flexion: pip_dip_flexion,
    })

# function to move the middle finger
def move_middle_finger(mcp_abduction, mcp_flexion, pip_dip_flexion):
    move_servos({
        middle_mcp_abduction: mcp_abduction,
        middle_mcp_flexion: mcp_flexion,
        middle_pip_dip_flexion: pip_dip_flexion,
    })

# function to move the ring finger
def move_ring_finger(mcp_abduction, mcp_flexion, pip_dip_flexion):
    move_servos({
        ring_mcp_abduction: mcp_abduction,
        ring_mcp_flexion: mcp_flexion,
        ring_pip_dip_flexion: pip_dip_flexion,
    })

# function to move the pinky finger
def move_pinky_finger(mcp_abduction, mcp_flexion, pip_dip_flexion):
    move_servos({
        pinky_mcp_abduction: mcp_abduction,
        pinky_mcp_flexion: mcp_flexion,
        pinky_pip_dip_flexion: pip_dip_flexion,
    })

# function to move the thumb
def move_thumb(cmc_abduction, cmc_flexion, mp_flexion, ip_flexion):
    move_servos({
        thumb_cmc_abduction: cmc_abduction,
        thumb_cmc_flexion: cmc_flexion,
        thumb_mp_flexion: mp_flexion,
        thumb_ip_flexion: ip_flexion,
    })

# function to move the hand to the open hand pose
def open_hand():
    move_index_finger(500, 500, 500)
    move_middle_finger(500, 500, 500)
    move_ring_finger(500, 500, 500)
    move_pinky_finger(500, 500, 500)
    move_thumb(500, 500, 500, 500)

# function to move the hand to the power grasp pose
def power_grasp():
    move_index_finger(500, 500, 500)
    move_middle_finger(500, 500, 500)
    move_ring_finger(500, 500, 500)
    move_pinky_finger(500, 500, 500)
    move_thumb(500, 500, 500, 500)

# function to move the hand to the pinch pose
def pinch():
    move_index_finger(500, 500, 500)
    move_middle_finger(500, 500, 500)
    move_ring_finger(500, 500, 500)
    move_pinky_finger(500, 500, 500)
    move_thumb(500, 500, 500, 500)

# function to move the hand to the fist pose
def fist():
    move_index_finger(500, 500, 500)
    move_middle_finger(500, 500, 500)
    move_ring_finger(500, 500, 500)
    move_pinky_finger(500, 500, 500)
    move_thumb(500, 500, 500, 500)
