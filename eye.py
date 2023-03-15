from time import sleep
import cv2
import math
import os

import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

DEBUG = False

# Load the Haar cascade classifiers for detecting eyes
eye_cascade = cv2.CascadeClassifier("C:\\code\\github-gcc\\eye\\haarcascade_eye.xml")

# Initialize the video capture device
cap = cv2.VideoCapture(0)

# Count left and right eye frames
left_count = right_count = 0

# Calculate the distance between two points
def get_eye_distance(eye1, eye2):
    return math.sqrt((eye1[0] - eye2[0]) * (eye1[0] - eye2[0]) + (eye1[1] - eye2[1]) * (eye1[1] - eye2[1]))

# Calculate the size of an eye
def get_eye_size(eye):
    return eye[2] * eye[3]

# Calculate the center of an eye
def get_eye_center(eye):
    return eye[0] + eye[2] // 2, eye[1] + eye[3] // 2

# Count result
left_ct = right_ct = 0
def count_result(result):
    global left_ct
    global right_ct
    if result == "<-":
        left_ct += 1
    elif result == "->":
        right_ct += 1
    if left_ct + right_ct >= 50:
        if left_ct > right_ct + 10:
            output("<-")
        elif right_ct > left_ct + 10:
            output("->")
        else:
            output("==")
        left_ct = right_ct = 0

# Output the count to a file
def output(result):
    f = open("C:\\.keycache\\face_direction.txt", "w")
    print(result)
    f.write(result)
    f.close()

frame_ct = 0
while True:
    # Read a frame from the video capture device
    ret, frame = cap.read()
    frame_ct += 1

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the grayscale frame using the Haar cascade classifier
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles around the detected eyes
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    
    # Found two eyes
    if len(eyes) == 2:
        if eyes[0][0] > eyes[1][0]:
            left_eye = eyes[0]
            right_eye = eyes[1]
        else:
            left_eye = eyes[1]
            right_eye = eyes[0]
            
        # Draw a dot at the centroid of the eyes
        # left eye is blue, right eye is red
        cv2.circle(frame, get_eye_center(left_eye), 4, (255, 0, 0), -1)
        cv2.circle(frame, get_eye_center(right_eye), 4, (0, 0, 255), -1)
    
    # Face direction detection
    if frame_ct % 1 == 0:
        if DEBUG: print("eyes count: " + str(len(eyes)))
        for i, eye in enumerate(eyes):
            if DEBUG: print("eye " + str(i) + ": " 
                  + "location = (" + str(eye[0]) + ", " + str(eye[1]) + "), " 
                  + "width = " + str(eye[2]) + ", " 
                  + "height = " + str(eye[3]))

        if len(eyes) == 2:
            height_diff = abs(left_eye[3] - right_eye[3])
            distance = get_eye_distance(left_eye, right_eye)
            eye_size = (get_eye_size(left_eye) + get_eye_size(right_eye)) / 2  # average size
            eye_size_diff = get_eye_size(left_eye) - get_eye_size(right_eye)
            
            # Print out
            if DEBUG: print("eye height diff: " + str(height_diff))
            if DEBUG: print("distance: " + str(int(distance)))
            if DEBUG: print("left eye size: " + str(get_eye_size(left_eye)))
            if DEBUG: print("right eye size: " + str(get_eye_size(right_eye)))
            if DEBUG: print("average eye size: " + str(int(eye_size)))
            if DEBUG: print("eye size diff: " + str(eye_size_diff))
            
            # Count the number of frames the eyes are facing left or right
            if eye_size_diff >= int(os.getenv("EYE_SIZE_DIFF")):
                count_result("->")
            else:
                count_result("<-")
        else:
            if DEBUG: print("Pleae look at the camera and make sure there are exactly two eyes in the frame.")
        if DEBUG: print("-")
    
    # Display the processed frame
    if os.getenv("SHOW_CAMERA_VIEW") == "1":
        cv2.imshow('Eye Tracking', frame)
    
        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture device and close the window
cap.release()
cv2.destroyAllWindows()