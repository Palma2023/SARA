#!/usr/bin/env python3

from daqhats import mcc118, hat_list, HatIDs
import sys

def read_analog(pin_number):
    # get hat list of MCC daqhat boards
    board_list = hat_list(filter_by_id = HatIDs.ANY)
    if not board_list:
        print("No boards found")
        sys.exit()

    # Read and return the value from the specified channel
    for entry in board_list:
        if entry.id == HatIDs.MCC_118:
            print("Board {}: MCC 118".format(entry.address))
            board = mcc118(entry.address)
            if pin_number < board.info().NUM_AI_CHANNELS:
                value = board.a_in_read(pin_number)
                print("Ch {0}: {1:.3f}".format(pin_number, value))
                return value
            else:
                print("Invalid pin number")
                return None

# Exemple d'utilisation
#value = read_analog(0)  # Lire la valeur du pin 2
#print("Value read from pin 2: ", value)

