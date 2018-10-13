#!/usr/bin/env python

import sys
import os
import time
import pyautogui
import pygame
import pygame.midi
import sequences
import InputMIDI
import pickle
import os
from pygame.locals import *

try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set

def emu_controller(input):
    buffer = 3

    recentTime = time.time() 
    # Most recent time of last command 

    lastDirection = ""
    # 'left', 'right', 'jump', 'pause', 'end'

    latestCommand = input#unpickler.load("pickler.txt")
    while latestCommand != 'end':
        if latestCommand == 'right':
            pyautogui.keyDown('right')
            recentTime = time.time()
            lastDirection = 'right'

        elif latestCommand == 'left':
            pyautogui.keyDown('left')
            recentTime = time.time()
            lastDirection = 'left'

        elif latestCommand == 'jump':
            pyautogui.keyDown('.')
            #pyautogui.keyDown('alt')
            pyautogui.keyDown(lastDirection)

        elif latestCommand == 'pause':
            pyautogui.keyDown('esc')

        elif time.time() - latestTime > buffer:
            pyautogui.keyUp(lastDirection)

        latestCommand = 'end'#unpickler.load("pickler.txt")

# os.system("python p_input.py")
# instructionFile = open("pickler.txt", w)
# pickler = pickle.Pickler(instructionFile)
inputs = InputMIDI.InputMIDI()
melodyPosition = 0
goingRight = True

while True:
    currentNote = inputs.getInput()
    if currentNote == sequences.melody1_1[melodyPosition]:
        if goingRight:
            emu_controller("right")
            #pickler.dump("right")
            print("heading right from correct melody")
        else:
            emu_controller("left")
            # pickler.dump("left")
            print("heading left from correct melody")
        melodyPosition += 1
        if melodyPosition == 238:
            melodyPosition = 0
    elif currentNote == sequences.jump[0]:
        currentNote = inputs.getInput()
        while currentNote == 0:
            currentNote = inputs.getInput()
        if currentNote == sequences.jump[1]:
            emu_controller("jump")
            # pickler.dump("jump")
            print("jump!")
    elif currentNote == sequences.reverse[0]:
        currentNote = inputs.getInput()
        while currentNote == 0:
            currentNote = inputs.getInput()
        if currentNote == sequences.reverse[1]:
            goingRight = not goingRight
            print("reverse!")
    elif currentNote == sequences.pause[0]:
        currentNote = 0
        pauseIndex = 1
        while pauseIndex < len(sequences.pause):
            while currentNote == 0:
                currentNote = inputs.getInput()
            if currentNote == sequences.pause[pauseIndex]:
                pauseIndex = pauseIndex + 1
                currentNote = 0
            else:
                break
        if pauseIndex == len(sequences.pause):
            # pickler.dump("pause")
            print("pause!")
    elif currentNote == 36:
        # pickler.dump("end")
        print("end")
        break
sys.exit()
