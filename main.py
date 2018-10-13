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

try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set

def emu_controller():
    buffer = 3

    recentTime = 0.0
    # Most recent time of last command 

    lastDirection = ""
    # 'left', 'right', 'jump', 'pause', 'end'

    latestCommand = q.get()
    q.task_done()
    while True:
        if latestCommand == 'right':
            pyautogui.press('right')
            recentTime = time.time()
            lastDirection = 'right'

        elif latestCommand == 'left':
            pyautogui.press('left')
            recentTime = time.time()
            lastDirection = 'left'

        elif latestCommand == 'jump':
            pyautogui.press(lastDirection)
            pyautogui.press('.')

        elif latestCommand == 'pause':
            pyautogui.press('esc')

        elif latestCommand == 'end':
            break
            
        if not q.empty():            
            latestCommand = q.get()
            q.task_done()
        else:
            latestCommand = 'wait'
    
    print("exited queue")

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
        if melodyPosition == 238:
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
