#!/usr/bin/env python

import sys
import os
import time
import pyautogui
import pygame
import pygame.midi
import sequences
import InputMIDI
from pygame.locals import *
from queue import Queue
import threading
commandKey = {
        'right':'right',
        'left':'left',
        'jump':'alt',
        'pause':'esc'
    }

try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set

def emu_controller():
    buffer = .5

    recentTime = 0.0
    # Most recent time of last command 

    lastDirection = 'right'
    # 'left', 'right', 'jump', 'pause', 'end'

    keyPressed = False
    latestCommand = q.get()
    q.task_done()
    lastTime = time.time()
    while True:
        if keyPressed: 
            pyautogui.keyDown(commandKey[latestNonWait])
            print("Pressed " + latestNonWait + " key down!")

        if latestCommand == 'end':
            break
        
        if latestCommand != 'wait':
            latestNonWait = latestCommand

            if latestCommand == 'jump':
                pyautogui.keyDown(commandKey[lastDirection])

            pyautogui.keyDown(commandKey[latestCommand])
            print("Pressed " + latestCommand + " key down!")

            recentTime = time.time()
            keyPressed = True

            if latestCommand == 'right' or latestCommand == 'left':
                lastDirection = latestCommand

        if not q.empty():     
            latestCommand = q.get() 
            q.task_done()
        else:
            latestCommand = 'wait'

        # Latest command here is really your next command
        if latestCommand != latestNonWait:
            if latestCommand == 'wait':
                if keyPressed:
                    if time.time() - recentTime > buffer:
                        keyPressed = False; 
                        if latestNonWait == 'jump':
                            pyautogui.keyUp(commandKey[lastDirection])
                        pyautogui.keyUp(commandKey[latestNonWait])
                        print("Lifted " + latestNonWait + " key up!")
            else: 
                keyPressed = False 
                if latestNonWait == 'jump':
                        pyautogui.keyUp(commandKey[lastDirection])
                pyautogui.keyUp(commandKey[latestNonWait])
                print("Lifted " + latestNonWait + " key up!")


    
inputs = InputMIDI.InputMIDI()
melodyPosition = 0
goingRight = True

q = Queue()
t = threading.Thread(target=emu_controller)
t.daemon = True
t.start()

while True:
    currentNote = inputs.getInput()
    if currentNote == sequences.melody1_1[melodyPosition]:
        if goingRight:
            q.put("right")
            print("right")
        else:
            q.put("left")
            print("left")
        melodyPosition += 1
        if melodyPosition == len(sequences.melody1_1):
            melodyPosition = 0
    elif currentNote == sequences.jump[0]:
        currentNote = inputs.getInput()
        while currentNote == 0:
            currentNote = inputs.getInput()
        if currentNote == sequences.jump[1]:
            q.put("jump")
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
            q.put("pause")
            print("pause!")
    elif currentNote == 36:
        q.put("end")
        print("end")
        break
q.join()
sys.exit()
