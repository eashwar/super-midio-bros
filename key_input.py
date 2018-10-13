import time
import pyautogui

def hold_Key (hold_time, key_string):
    start = time.time()
    while time.time() - start < hold_time:
        pyautogui.keyDown(key_string)
    pyautogui.keyUp(key_string)

def hold_Two_Keys (hold_time, key_string1, key_string2):
    start = time.time()
    while time.time() - start < hold_time:
        pyautogui.keyDown(key_string1)
        pyautogui.keyDown(key_string2)
    pyautogui.keyUp(key_string1)
    pyautogui.keyUp(key_string2)
