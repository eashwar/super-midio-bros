#!/usr/bin/env python

import sys
import os
import time
import math
import pyautogui
import pygame
import pygame.midi
import sequences
import InputMIDI
from pygame.locals import *
from queue import Queue
import threading
commandKey = {
        'right':'d',
        'left':'a',
        'jump':'.',
        'pause':'enter'
    }

try:  # Ensure set available for output example
    set
except NameError:
    from sets import Set as set

def emu_controller():
    buffer = .2

    recentTime = 0.0
    # Most recent time of last command 

    lastDirection = 'right'
    # 'left', 'right', 'jump', 'pause', 'end'

    keyPressed = False
    jumpHappening = False
    latestCommand = q.get()
    q.task_done()
    lastTime = time.time()
    while True:
        if keyPressed: 
            pyautogui.keyDown(commandKey[latestNonWait])

        if latestCommand == 'end':
            break
        
        if latestCommand != 'wait':
            latestNonWait = latestCommand


            pyautogui.keyDown(commandKey[latestCommand])

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
                        pyautogui.keyUp(commandKey[latestNonWait])
                        pyautogui.keyUp(commandKey['left'])
                        pyautogui.keyUp(commandKey['right'])
            else: 
                keyPressed = False 
                if latestNonWait == 'jump':
                    if latestCommand in ['left', 'right']:
                        pyautogui.keyDown(commandKey[latestCommand])
                pyautogui.keyUp(commandKey[latestNonWait])


    
inputs = InputMIDI.InputMIDI()

q = Queue()
t = threading.Thread(target=emu_controller)
t.daemon = True
t.start()

disp_width = 1261
disp_height = 200

keyboardDisp = pygame.display.set_mode((disp_width, disp_height))
pygame.display.set_caption("Super MIDIo Bros.")
keyboardImg = pygame.image.load("res/keyboard.png")
introImg = pygame.image.load("res/introduction.png")

red = (255, 0, 0)
lightred = (255, 147, 140)
green = (0, 255, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
octave_width = math.trunc((disp_width - 34) / 5)
white_key_width = math.trunc(octave_width / 7)
rect_width = 21
rect_height = 40
rect_black_key_top = 60
rect_white_key_top = 120

semitone_to_scale_degree = {
    0: 0,
    2: 1,
    4: 2,
    5: 3,
    7: 4,
    9: 5,
    11: 6,
}

def get_octave(note):
    return math.trunc((note - 36) / 12)

def is_black_key(note):
    return ((note % 12) in [1, 3, 6, 8, 10])

def get_rect(note):
    if is_black_key(note):
        rect_left = (octave_width * get_octave(note)) + 25 + semitone_to_scale_degree[(note % 12) - 1] * white_key_width
        rect_top = rect_black_key_top
    else:
        rect_left = (octave_width * get_octave(note)) + 6 + semitone_to_scale_degree[note % 12] * white_key_width
        rect_top = rect_white_key_top
    return Rect(rect_left, rect_top, rect_width, rect_height)

def draw_sfx_rects():
    pygame.draw.rect(keyboardDisp, green, get_rect(sequences.jump[0]))
    pygame.draw.rect(keyboardDisp, green, get_rect(sequences.jump[1]))
    pygame.draw.rect(keyboardDisp, blue, get_rect(sequences.reverse[0]))
    pygame.draw.rect(keyboardDisp, blue, get_rect(sequences.reverse[1]))
    pygame.draw.rect(keyboardDisp, cyan, get_rect(sequences.pause[0]))
    pygame.draw.rect(keyboardDisp, cyan, get_rect(sequences.pause[1]))

clock = pygame.time.Clock()

melodyPosition = 0
jumpPosition = 0
betweenJumpCounter = 0
goingRight = True

keyboardDisp.blit(introImg, (0, 0))
pygame.display.flip()
currentNote = inputs.getInput()
while currentNote == 0:
    pygame.event.get()
    keyboardDisp.blit(introImg, (0, 0))
    pygame.display.flip()
    clock.tick(60)
    currentNote = inputs.getInput()

while True:
    pygame.event.get()

    keyboardDisp.blit(keyboardImg, (0, 0))
    draw_sfx_rects()
    pygame.draw.rect(keyboardDisp, red, get_rect(sequences.melody1_1[melodyPosition]))        
    pygame.display.flip()
    clock.tick(60)

    currentNote = inputs.getInput()

    if currentNote == sequences.melody1_1[melodyPosition]:
        betweenJumpCounter += 1
        if betweenJumpCounter > 2 and jumpPosition == 1:
            jumpPosition = 0
            betweenJumpCounter = 0
        if goingRight:
            q.put("right")
        else:
            q.put("left")
        melodyPosition += 1
        if melodyPosition == len(sequences.melody1_1):
            melodyPosition = 0
    elif currentNote == sequences.jump[jumpPosition]:
        jumpPosition += 1
        if jumpPosition == 2:
            q.put("jump")
            jumpPosition = 0
            betweenJumpCounter = 0
    elif currentNote == sequences.reverse[0]:
        betweenJumpCounter += 1
        if betweenJumpCounter > 2 and jumpPosition == 1:
            jumpPosition = 0
            betweenJumpCounter = 0
        currentNote = inputs.getInput()
        while currentNote == 0:
            currentNote = inputs.getInput()
        if currentNote == sequences.reverse[1]:
            goingRight = not goingRight
    elif currentNote == sequences.pause[0]:
        betweenJumpCounter += 1
        if betweenJumpCounter > 2 and jumpPosition == 1:
            jumpPosition = 0
            betweenJumpCounter = 0
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
    elif currentNote == 37:
        melodyPosition = 0
    elif currentNote == 36:
        q.put("end")
        break
q.join()
sys.exit()
