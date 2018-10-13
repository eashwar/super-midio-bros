import time
import pyautogui
import pickle

buffer = 1

recentTime = time.time() 
# Most recent time of last command 

string lastDirection;
# 'left', 'right', 'jump', 'pause', 'end'

latestCommand = unpickler.load("pickler.txt")
while latestCommand != 'end':
    if latestCommand == 'right':
        pyautogui.keyDown('right')
        recentTime = time.time()
        lastDirection = 'right'

    else if latestCommand == 'left':
        pyautogui.keyDown('left')
        recentTime = time.time()
        lastDirection = 'left'

    else if latestCommand == 'jump':
        pyautogui.keyDown('alt')
        pyautogui.keyDown(lastDirection)

    else if latestCommand == 'pause':
        pyautogui.keyDown('esc')

    else if time.time() - latestTime > buffer:
        pyautogui.keyUp(lastDirection)

    latestCommand = unpickler.load("pickler.txt")
