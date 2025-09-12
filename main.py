# main.py
# This is the main script that initializes the camera, loads models,
# and continuously processes video frames to control the mouse using eye tracking.

import cv2
import dlib
import pyautogui
from config import EAR_THRESHOLD, BLINK_TIME_THRESHOLD, PUPIL_THRESHOLD, SMOOTHING_ALPHA, SHOW_DEBUG
from eye_tracker import EyeTracker
from blink_detector import BlinkDetector

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera could not be opened.")
        return

    # Load dlib's face detector and shape predictor
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # Get screen size
    screen_width, screen_height = pyautogui.size()

    # Initialize eye tracker and blink detector
    eye_tracker = EyeTracker(predictor, detector, screen_width, screen_height)
    blink_detector = BlinkDetector()

    # Main loop
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Frame not captured.")
            continue

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Process the frame for eye tracking
        processed = eye_tracker.process_frame(gray, frame)

        if isinstance(processed, tuple):
            frame, left_ear, right_ear = processed
            # Detect blinks and trigger clicks
            blink_detector.detect_blink(left_ear, side="left")
            blink_detector.detect_blink(right_ear, side="right")

        # Show the video with tracking
        cv2.imshow("Eye Cursor Control", frame)

        # Exit when ESC is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

if __name__ == "__main__":
    main()
