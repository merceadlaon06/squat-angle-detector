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
is_left_counting = True
is_right_counting= True
is_both_counting = True
left_counter = 0
right_counter = 0
both_counter = 0

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

            # Get landmarks
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

            r_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            l_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

            # Quality feedback
            if r_angle <= 45:
                r_quality = "Good curl"
            else:
                r_quality = "curl more"


            if l_angle <= 45:
                l_quality = "Good curl"
            else:
                l_quality = "curl more"
            # Left arm counter
            if l_angle <= 45:
                if is_left_counting and l_quality == "Good curl":
                    left_counter = left_counter +1
                    is_left_counting =False
            elif l_angle >= 160:
                is_left_counting =True
            #else:
                #is_left_counting = False
            # Right arm counter
            if r_angle <= 45:
                if is_right_counting and r_quality == "Good curl":
                    right_counter = right_counter +1
                    is_right_counting =False
            elif r_angle >= 150:
                is_right_counting =True
            #else:
                #is_right_counting = False
            # Both arms counter
            if l_angle <= 45 and r_angle <= 45:
                if is_both_counting:
                    if r_quality == "Good curl" and l_quality == "Good curl":
                        both_counter = both_counter + 1
                        is_both_counting = False
            elif l_angle >= 150 and r_angle >= 150:
                is_both_counting = True

            #else:
                #is_both_counting = False

            # Show info
            cv2.putText(image, f"Left Angle: {int(l_angle)} Degrees ({l_quality}) | Reps: {left_counter}",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(image, f"Right Angle: {int(r_angle)} deg ({r_quality}) | Reps: {right_counter}",
                        (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            cv2.putText(image, f"Both Arms Reps: {both_counter}",
                        (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('Bicep Curl Counter', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
