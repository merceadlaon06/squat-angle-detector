import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Angle calculation function
def calculate_angle(a, b, c):
    a = [a.x, a.y]
    b = [b.x, b.y]
    c = [c.x, c.y]

    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = abs(radians * 180.0 / math.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Rep counting variables
stage = None
counter = 0

cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
            ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

            angle = calculate_angle(hip, knee, ankle)

            # Feedback
            feedback = ""
            if angle < 90:
                feedback = "Good squat!"
                if stage == "up":
                    counter += 1
                    stage = "down"
            elif angle > 160:
                feedback = "Stand up"
                if stage == "down":
                    stage = "up"
            else:
                feedback = "Go lower!"

            # Show angle
            cv2.putText(image, f'Angle: {int(angle)} Degrees',
                        (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # Show feedback
            cv2.putText(image, feedback,
                        (30, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Show rep count
            cv2.putText(image, f'Reps: {counter}',
                        (30, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('Squat Angle Detection', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
