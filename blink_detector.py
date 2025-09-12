# blink_detector.py
# This module defines the BlinkDetector class for detecting blinks and triggering mouse clicks.

import time
import pyautogui
from config import EAR_THRESHOLD, BLINK_TIME_THRESHOLD

class BlinkDetector:
    def __init__(self):
        self.blink_time = time.time()
        self.left_blink = False
        self.right_blink = False

    def detect_blink(self, ear, side="left"):
        """
        Detects blinks based on the Eye Aspect Ratio (EAR) and triggers mouse clicks.

        Arguments:
        ear -- EAR value for the eye.
        side -- "left" or "right" to differentiate eyes.
        """
        if ear < EAR_THRESHOLD:
            if side == "left":
                if not self.left_blink:
                    self.left_blink = True
                    self._click("left")
            else:
                if not self.right_blink:
                    self.right_blink = True
                    self._click("right")
        else:
            if side == "left":
                self.left_blink = False
            else:
                self.right_blink = False

    def _click(self, button):
        current_time = time.time()
        if current_time - self.blink_time < BLINK_TIME_THRESHOLD:
            pyautogui.doubleClick(button=button)
        else:
            pyautogui.click(button=button)
        self.blink_time = current_time
