from time import sleep
import cv2
import math

import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())


# Load the Haar cascade classifiers for detecting eyes
eye_cascade = cv2.CascadeClassifier("C:\\code\\github-gcc\\eye\\haarcascade_eye.xml")

# Initialize the video capture device
cap = cv2.VideoCapture(0)

# Count left and right eye frames
left_count = right_count = 0

# Calculate the distance between two points
def eye_distance(ex1, ex2, ey1, ey2):
    return math.sqrt((ex1 - ex2) * (ex1 - ex2) + (ey1 - ey2) * (ey1 - ey2))

# Output the count to a file
def output(left_count, right_count):
    f = open("C:\\.keycache\\face_direction.txt", "w")
    if left_count > right_count:
        print("diff = " + str(diff_left_right) + " : <-")
        f.write("<-")
    elif left_count < right_count:
        print(str(diff_left_right) + ": ->")
        f.write("->")
    else:
        print(str(diff_left_right) + ": =")
        f.write("=")
    f.close()

# Frame looper
while True:
    # Read a frame from the video capture device
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the grayscale frame using the Haar cascade classifier
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles around the detected eyes
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    
    # Eyes filtering
    # 1. Two eyes should be at almost same height
    # 2. Two eyes are not far apart
    # 3. Eyes are not too big or too smalls

    left_eye = right_eye = None
    left_eye_size = right_eye_size = 0

    # Find the left and right eye
    for (ex, ey, ew, eh) in eyes:
        # Calculate the centroid of the eye
        cx, cy = ex + ew // 2, ey + eh // 2
        
        if left_eye is None or cx < left_eye[0]:
            left_eye = (cx, cy)
            left_eye_size = ew * eh
            
        if right_eye is None or cx > right_eye[0]:
            right_eye = (cx, cy)
            right_eye_size = ew * eh
    
    # Draw a dot at the centroid of the eyes
    # left eye is blue, right eye is red
    cv2.circle(frame, left_eye, 4, (255, 0, 0), -1)
    cv2.circle(frame, right_eye, 4, (0, 0, 255), -1)

    # Count the number of frames the eyes are facing left or right
    diff_left_right = left_eye_size - right_eye_size
    if diff_left_right > 0:
        right_count += 1
    elif diff_left_right < 0:
        left_count += 1
    else:
        right_count += 1
        left_count += 1

    # Output the direction the face is facing
    if left_count + right_count >= 10:
        output(left_count, right_count)
        left_count = right_count = 0

    # Display the processed frame
    # No need to display the frame
    cv2.imshow('Eye Tracking', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the window
cap.release()
cv2.destroyAllWindows()