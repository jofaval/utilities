"""
Simulate activity on a PC so it doesn't get suspended
"""
import random
import time

import pyautogui

SECONDS_TO_SLEEP_IN_BETWEEN: int = 1*60


def custom_random(variance: int, negative_range: bool = True) -> int:
    """Custom random number generation"""
    max_number = variance
    min_number = 0

    if negative_range:
        max_number /= 2
        min_number -= (variance / 2)
    return random.randint(min_number, max_number)


def start():
    """
    Main entrypoint

    @source https://stackoverflow.com/questions/1181464/controlling-mouse-with-python
    """
    while True:
        print("moving mouse...")
        pyautogui.moveRel(custom_random(20), custom_random(20), .2)
        print("mouse moved!")
        time.sleep(SECONDS_TO_SLEEP_IN_BETWEEN)


if __name__ == "__main__":
    start()
