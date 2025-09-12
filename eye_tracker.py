# eye_tracker.py
# This module defines the EyeTracker class for gaze estimation using eye landmarks.

import numpy as np
import cv2
import pyautogui
from utils import get_pupil_position, get_eye_aspect_ratio, smooth_position
from config import PUPIL_THRESHOLD, SMOOTHING_ALPHA, SHOW_DEBUG

class EyeTracker:
    def __init__(self, predictor, detector, screen_width, screen_height):
        self.detector = detector
        self.predictor = predictor
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.prev_x = 0
        self.prev_y = 0

    def process_frame(self, gray, frame):
        faces = self.detector(gray)
        if not faces:
            cv2.putText(frame, "No face detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return frame

        face = faces[0]
        landmarks = self.predictor(gray, face)

        # Extract eye landmarks
        left_eye_points = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]
        right_eye_points = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]

        # Calculate Eye Aspect Ratio (EAR)
        left_ear = get_eye_aspect_ratio(left_eye_points)
        right_ear = get_eye_aspect_ratio(right_eye_points)

        # Estimate gaze by finding pupil position
        avg_px_norm, avg_py_norm = self.estimate_gaze(gray, left_eye_points, right_eye_points)

        # Map gaze to screen coordinates and smooth cursor movement
        #cursor_x = int((1 - avg_px_norm) * self.screen_width)
        #cursor_y = int(avg_py_norm * self.screen_height)
        #pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)
        # Map gaze to screen coordinates with scaling and smooth cursor movement
        min_val = 0.0   # Lower bound of pupil movement (adjust as needed)
        max_val = 1.0   # Upper bound of pupil movement (adjust as needed)

        # Clamp avg_px_norm and avg_py_norm to min_val and max_val
        avg_px_norm = max(min(avg_px_norm, max_val), min_val)
        avg_py_norm = max(min(avg_py_norm, max_val), min_val)

        # Scale to 0 - 1 range
        scaled_px = (avg_px_norm - min_val) / (max_val - min_val)
        scaled_py = (avg_py_norm - min_val) / (max_val - min_val)

        # Map to screen coordinates
        cursor_x = int((1 - scaled_px) * self.screen_width)
        cursor_y = int(scaled_py * self.screen_height)

        # Smooth the cursor movement
        cursor_x = smooth_position(self.prev_x, cursor_x, SMOOTHING_ALPHA)
        cursor_y = smooth_position(self.prev_y, cursor_y, SMOOTHING_ALPHA)
        self.prev_x, self.prev_y = cursor_x, cursor_y

        # Move the mouse cursor
        pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

        # Visualize tracking data if debug mode is enabled
        if SHOW_DEBUG:
            self.visualize(frame, left_eye_points, right_eye_points, left_ear, right_ear)

        return frame, left_ear, right_ear

    def estimate_gaze(self, gray, left_eye_points, right_eye_points):
        # Process left eye
        left_eye_np = np.array(left_eye_points)
        lx, ly, lw, lh = cv2.boundingRect(left_eye_np)
        left_eye_img = gray[ly:ly+lh, lx:lx+lw]
        left_pupil = get_pupil_position(left_eye_img, PUPIL_THRESHOLD)
        left_px_norm = left_pupil[0] / lw
        left_py_norm = left_pupil[1] / lh

        # Process right eye
        right_eye_np = np.array(right_eye_points)
        rx, ry, rw, rh = cv2.boundingRect(right_eye_np)
        right_eye_img = gray[ry:ry+rh, rx:rx+rw]
        right_pupil = get_pupil_position(right_eye_img, PUPIL_THRESHOLD)
        right_px_norm = right_pupil[0] / rw
        right_py_norm = right_pupil[1] / rh

        # Average coordinates for smoother tracking
        avg_px_norm = (left_px_norm + right_px_norm) / 2
        avg_py_norm = (left_py_norm + right_py_norm) / 2
        
        return avg_px_norm, avg_py_norm

    def visualize(self, frame, left_eye_points, right_eye_points, left_ear, right_ear):
        for point in left_eye_points + right_eye_points:
            cv2.circle(frame, point, 2, (0, 255, 0), -1)
        cv2.putText(frame, f"Left EAR: {left_ear:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Right EAR: {right_ear:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
