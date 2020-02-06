__all__ = ['forward', 'backward', 'stop_forward', 'stop_backward', 'left', 'right',
           'stop_left', 'stop_left', 'stop_right', 'turn', 'stop_turn', 'light_on',
           'light_off', 'autopilot', 'goto_power_station', 'battery_lvl', 'retreive_info']

import bitstruct as bs

####################
#      Common      #
####################

# Format strings
MANUAL_FMT = bs.compile('u1u1u3u3')
FEATURE_FMT = bs.compile('u1u1u2u4')

# Compat bit
COMPAT = 0b0
EXTENDED = 0b1

# Drive bit
MANUAL = 0b0
FEATURED = 0b1


####################
#      Manual      #
####################

# Forward / Backward
STOP_FORWARD = 0x00
FORWARD = 0x01
STOP_BACKWARD = 0x02
BACKWARD = 0x03

def forward(amount: int = 0):
    if not 0 <= amount < 8:
        raise ValueError('bad argument, should be a natural < 8')
    return MANUAL_FMT.pack(COMPAT, MANUAL, amount, FORWARD)

def backward(amount: int = 0):
    if not 0 <= amount < 8:
        raise ValueError('bad argument, should be a natural < 8')
    return MANUAL_FMT.pack(COMPAT, MANUAL, amount, BACKWARD)

def stop_forward():
    return MANUAL_FMT.pack(COMPAT, MANUAL, 0b000, STOP_FORWARDS)

def stop_backward():
    return MANUAL_FMT.pack(COMPAT, MANUAL, 0b000, STOP_BACKWARD)

def stop_move():
    return stop_forward() + stop_backward()


# Direction
STOP_LEFT = 0x04
LEFT = 0x05
STOP_RIGHT = 0x06
RIGHT = 0x07

def left(amount: int = 0):
    if not 0 <= amount < 8:
        raise ValueError('bad argument, should be a natural < 8')
    return MANUAL_FMT.pack(COMPAT, MANUAL, amount, LEFT)

def right(amount: int = 0):
    if not 0 <= amount < 8:
        raise ValueError('bad argument, should be a natural < 8')
    return MANUAL_FMT.pack(COMPAT, MANUAL, amount, RIGHT)

def turn(dir: int, amount: int = 0):
    if dir == LEFT:
        return left()
    elif dir == RIGHT:
        return right()
    else:
        raise ValueError('bad argument, direction should be either LEFT or RIGHT')


def stop_left():
    return MANUAL_FMT.pack(COMPAT, MANUAL, 0b000, STOP_LEFT)

def stop_right():
    return MANUAL_FMT.pack(COMPAT, MANUAL, 0b000, STOP_RIGHT)

def stop_turn():
    return stop_left() + stop_right()


####################
#     Feature      #
####################

# Class
LIGHT_AND_SOUND = 0b00
SMART_FEATURE = 0b01
INFO = 0b10

# 00 - Light
LIGHT_ON = 0x0
LIGHT_OFF = 0x1

# 01 - Smart features
AUTOPILOT = 0x1
GOTO_POWER_STATION = 0x2

# 10 - Infos
BATTERY_LVL = 0x0
RETREIVE_INFO = 0x1

# 11 - 4th class, unused yet


def light_on():
    return FEATURE_FMT.pack(COMPAT, MANUAL, LIGHT_AND_SOUND, LIGHT_ON)

def light_off():
    return FEATURE_FMT.pack(COMPAT, MANUAL, LIGHT_AND_SOUND, LIGHT_OFF)

def autopilot():
    return FEATURE_FMT.pack(COMPAT, MANUAL, SMART_FEATURE, AUTOPILOT)

def goto_power_station():
    return FEATURE_FMT.pack(COMPAT, MANUAL, SMART_FEATURE, GOTO_POWER_STATION)

def battery_lvl():
    return FEATURE_FMT.pack(COMPAT, MANUAL, INFO, BATTERY_LVL)

def retreive_info():
    return FEATURE_FMT.pack(COMPAT, MANUAL, INFO, RETREIVE_INFO)
