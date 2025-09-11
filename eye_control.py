print("Starting Eye Control Script...")

import cv2
import dlib
import pyautogui
import time

print("Libraries imported ✅")

# Load camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera could not be opened.")
    exit()
print("Camera opened ✅")

# Dlib face detector and shape predictor
detector = dlib.get_frontal_face_detector()
print("Face detector loaded ✅")

predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
print("Model loaded ✅")

def get_eye_aspect_ratio(eye_points):
    A = ((eye_points[1][0] - eye_points[5][0])**2 + (eye_points[1][1] - eye_points[5][1])**2) ** 0.5
    B = ((eye_points[2][0] - eye_points[4][0])**2 + (eye_points[2][1] - eye_points[4][1])**2) ** 0.5
    C = ((eye_points[0][0] - eye_points[3][0])**2 + (eye_points[0][1] - eye_points[3][1])**2) ** 0.5
    return (A + B) / (2.0 * C)

blink_time = time.time()
left_blink = False
right_blink = False

print("Starting main loop... Press ESC to quit.")

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("❌ Frame not captured.")
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        left_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)]
        right_eye = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)]

        left_ear = get_eye_aspect_ratio(left_eye)
        right_ear = get_eye_aspect_ratio(right_eye)

        if left_ear < 0.2:
            if not left_blink:
                left_blink = True
                if time.time() - blink_time < 0.5:
                    pyautogui.doubleClick()
                blink_time = time.time()
        else:
            left_blink = False

        if right_ear < 0.2:
            if not right_blink:
                right_blink = True
                if time.time() - blink_time < 0.5:
                    pyautogui.doubleClick(button='right')
                blink_time = time.time()
        else:
            right_blink = False

    cv2.imshow("Eye Controller", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
