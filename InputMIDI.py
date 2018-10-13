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
from pygame.locals import *

try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set


class InputMIDI:
    event_get = None
    input_stream = None


    def __init__(self):
        pygame.init()
        pygame.fastevent.init()
        self.event_get = pygame.fastevent.get

        pygame.midi.init()

        input_id = pygame.midi.get_default_input_id()

        self.input_stream = pygame.midi.Input( input_id )


    def getInput(self):
        while self.input_stream.poll():
            midi_event = self.input_stream.read(1)
            # convert it into a pygame event:
            pygame_event = pygame.midi.midis2events(midi_event, self.input_stream.device_id)
          
            # return the integer value of the note that was pressed:
            if pygame_event[0].data2 == 100:
                return pygame_event[0].data1
        
        # if there isn't any new MIDI information:
        return 0


    def __del__(self):
        del self.input_stream
        pygame.midi.quit()
