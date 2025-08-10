# Bicep Curl Counter with MediaPipe and OpenCV

This project uses **MediaPipe** and **OpenCV** to track arm positions via a webcam and count bicep curl repetitions. It detects both left arm, right arm, and simultaneous curls while giving real-time feedback on form.

## Features
- Tracks **left arm**, **right arm**, and **both arms** curls.
- Real-time feedback on curl quality ("Good curl" or "curl more").
- Displays elbow angles in degrees.
- Counts reps for each arm separately and together.
- Uses **MediaPipe Pose** for accurate landmark detection.

## How It Works
1. Captures live video feed from your webcam using **OpenCV**.
2. Detects body landmarks with **MediaPipe Pose**.
3. Calculates the elbow joint angle using trigonometry.
4. Updates repetition count when correct curl form is detected.

## Requirements
Install dependencies with:
'''bash
pip install opencv-python mediapipe
'''

## Usage
Run the script with:
'''bash
python bicep_curl_counter.py
'''

Controls:
- Press 'q' to quit the program.

## Code Highlights
- **Angle Calculation**: The 'calculate_angle()' function determines the angle between shoulder, elbow, and wrist.
- **Repetition Logic**: Counters increment when arm angle is below 45° and resets when fully extended (above ~150°).
- **Form Feedback**: Helps ensure correct curl movement.

## Example Output
- 'Left Angle: 42 Degrees (Good curl) | Reps: 5'
- 'Right Angle: 47 Degrees (curl more) | Reps: 3'
- 'Both Arms Reps: 2'

