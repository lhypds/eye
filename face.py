import cv2
import dlib
import imutils
from imutils.video import VideoStream
from imutils import face_utils
import time

import os
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Initialize the web camera
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Output the count to a file
def output(result):
    f = open(os.getenv("OUTPUT_PATH"), "w")
    print(result)
    f.write(result)
    f.close()

def calculate_face_direction(shape):
    left_eye_pts = shape[36:42]
    right_eye_pts = shape[42:48]
    nose_tip = shape[33]

    eye_center = left_eye_pts.mean(axis=0).astype(int) * 0.5 + right_eye_pts.mean(axis=0).astype(int) * 0.5
    nose_to_eye_vec = eye_center - nose_tip

    if nose_to_eye_vec[0] > 0:
        output("<-")
        return "Left"
    elif nose_to_eye_vec[0] < 0:
        output("->")
        return "Right"
    else:
        output("=")
        return "Center"

frame_ct = 0
while True:
    # Capture each frame from the video stream
    frame = vs.read()
    frame_ct += 1

    # Resize the frame and convert to grayscale
    frame = imutils.resize(frame, width=800)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if frame_ct % 10 == 0:
        # Detect faces in the grayscale frame
        rects = detector(gray, 0)

        for rect in rects:
            # Get facial landmarks
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            face_direction = calculate_face_direction(shape)

            # Draw a rectangle around the face and display the face direction
            (x, y, w, h) = face_utils.rect_to_bb(rect)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, face_direction, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Display the processed frame
    if os.getenv("SHOW_CAMERA_VIEW") == "1":
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # Break the loop when 'q' key is pressed
        if key == ord("q"):
            break

cv2.destroyAllWindows()
vs.stop()