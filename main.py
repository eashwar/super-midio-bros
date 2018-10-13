#!/usr/bin/env python

"""Contains an example of midi input, and a separate example of midi output.

By default it runs the output example.
python midi.py --output
python midi.py --input

"""

import sys
import os

import pygame
import pygame.midi
import sequences
import InputMIDI

from pygame.locals import *

try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))
        



def input_main(device_id = None):
    pygame.init()
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    pygame.midi.init()

    _print_device_info()


    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print ("using input_id :%s:" % input_id)
    i = pygame.midi.Input( input_id )

    pygame.display.set_mode((1,1))



    going = True
    while going:
        events = event_get()
        for e in events:
            if e.type in [QUIT]:
                going = False
            if e.type in [KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:
                print (e)

        if i.poll():
            midi_events = i.read(10)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post( m_e )

    del i
    pygame.midi.quit()

def usage():
    print ("--input [device_id] : Midi message logger")
    print ("--list : list available midi devices")



inputs = InputMIDI.InputMIDI()
melodyPosition = 0
goingRight = True
while True:
	currentNote = inputs.getInput()
	if currentNote == melody1_1[melodyPosition]:
#		if goingRight:
#			MOVE FORWARD
#		else:
#			MOVE BACKWARD
#		melodyPosition += 1
#		if melodyPosition == 238:
#			melodyPosition = 0
#	elif currentNote == jump[0]:
#		currentNote = inputs.getInput()
#		if currentNote == jump[1]:
#			JUMP
#	elif currentNote == reverse[0]:
#		currentNote = inputs.getInput()
#		if currentNote == reverse[1]:
#			goingRight = !goingRight
#	elif currentNote == pause[0]:
#		currentNote = inputs.getInput()
#		if currentNote == pause[1]:
#			currentNote = inputs.getInput()
#			if currentNote == pause[2]:
#				currentNote = inputs.getInput()
#				if currentNote == pause[3]:
#					PAUSE