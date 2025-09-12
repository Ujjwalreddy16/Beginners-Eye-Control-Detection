# utils.py
# This module contains helper functions for EAR calculation, pupil detection, and smoothing.

import numpy as np
import cv2

def get_eye_aspect_ratio(eye_points):
    """
    Calculates the Eye Aspect Ratio (EAR) which is used to detect blinking.

    Arguments:
    eye_points -- List of 6 (x, y) tuples representing eye landmarks.

    Returns:
    EAR value as float.
    """
    A = np.linalg.norm(np.array(eye_points[1]) - np.array(eye_points[5]))
    B = np.linalg.norm(np.array(eye_points[2]) - np.array(eye_points[4]))
    C = np.linalg.norm(np.array(eye_points[0]) - np.array(eye_points[3]))
    return (A + B) / (2.0 * C)

def get_pupil_position(eye_region_gray, threshold_value):
    """
    Finds the pupil position within an eye region using thresholding and contours.

    Arguments:
    eye_region_gray -- Grayscale image of the eye.
    threshold_value -- Threshold for binarizing the image.

    Returns:
    (cx, cy) -- Coordinates of the pupil's center.
    """
    eye_region_gray = cv2.GaussianBlur(eye_region_gray, (5, 5), 0)
    _, thresh = cv2.threshold(eye_region_gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy)
    h, w = eye_region_gray.shape
    return (w // 2, h // 2)

def smooth_position(prev, current, alpha):
    """
    Smooths the current position using an exponential moving average.

    Arguments:
    prev -- Previous position value.
    current -- Current position value.
    alpha -- Smoothing factor between 0 and 1.

    Returns:
    Smoothed position as integer.
    """
    return int(prev * (1 - alpha) + current * alpha)
