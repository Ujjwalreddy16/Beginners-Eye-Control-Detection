# config.py
# This file contains configurable parameters such as thresholds and debug flags.

# Eye Aspect Ratio threshold to detect blinks
EAR_THRESHOLD = 0.2

# Time threshold (seconds) to distinguish between single and double clicks
BLINK_TIME_THRESHOLD = 0.5

# Threshold for pupil detection in grayscale images
PUPIL_THRESHOLD = 20

# Smoothing factor for cursor movement (between 0 and 1)
SMOOTHING_ALPHA = 0.4

# Enable or disable debug visualization
SHOW_DEBUG = True
