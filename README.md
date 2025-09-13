# Eye-Based Cursor Control Project

This project enables control of the mouse cursor using eye movements and blinks. It uses computer vision techniques with OpenCV, dlib, and PyAutoGUI to track eye landmarks, calculate gaze direction, and simulate mouse clicks.

## Features
- Eye tracking for cursor movement.
- Blink detection for left/right eye clicks.
- Single and double click functionality.
- Adjustable parameters for calibration.
- Real-time feedback using debug visuals.

## Folder Structure

eye_cursor_project/
├── main.py
├── eye_tracker.py
├── blink_detector.py
├── utils.py
├── config.py
├── README.md
├── shape_predictor_68_face_landmarks.dat


## Setup Instructions

1. Install Python 3 from https://www.python.org/downloads/.

2. Install required libraries using:
pip install opencv-python dlib numpy pyautogui


3. Download `shape_predictor_68_face_landmarks.dat` from:
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2  
Extract and place it inside this folder.

4. Run the program:
python main.py

## How to Use

1. Allow camera access when prompted.
2. Ensure your face is clearly visible.
3. Move your eyes to control the cursor.
4. Blink left eye to click once, blink twice to double-click.
5. Blink right eye to right-click similarly.
6. Press ESC to exit the program.

## Calibration

You can modify the thresholds in `config.py`:
- `EAR_THRESHOLD` controls blink sensitivity.
- `PUPIL_THRESHOLD` controls pupil detection.
- `SMOOTHING_ALPHA` controls cursor jitter smoothing.


## Notes

- Ensure proper lighting for accurate tracking.
- Face occlusion may cause detection issues.
- Use smoothing to improve cursor stability.

7. shape_predictor_68_face_landmarks.dat – Model File

Download this file from dlib’s website
.

Extract the file and place it inside your project folder.
 
Debug main.py and eye-tracker.py

setup.py to optimize PYautoGUI