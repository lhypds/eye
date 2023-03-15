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

    # Display the processed frame
    # No need to display the frame
    cv2.imshow('Eye Tracking', frame)
    
    # Print debug info
    if frame_ct % 60 == 0:
        print("eyes count: " + str(len(eyes)))
        for i, eye in enumerate(eyes):
            print("eye " + str(i) + ": " 
                  + "location = (" + str(eye[0]) + ", " + str(eye[1]) + "), " 
                  + "width = " + str(eye[2]) + ", " 
                  + "height = " + str(eye[3]))

        if len(eyes) != 2:
            print("Pleae look at the camera and make sure there are exactly two eyes in the frame.")
            print("-")
            continue
        
        height_diff = abs(eyes[0][3] - eyes[1][3])
        distance = eye_distance(eyes[0][0], eyes[1][0], eyes[0][1], eyes[1][1])
        eye_size = (eyes[0][2] * eyes[0][3] + eyes[1][2] * eyes[1][3]) / 2
        print("eye height diff:" + str(height_diff))
        print("distance:" + str(distance))
        print("eye size:" + str(eye_size))
        
        # Write to .env file
        dotenv.set_key(dotenv.find_dotenv(), "HEIGHT_DIFF", str(height_diff), quote_mode="never")
        dotenv.set_key(dotenv.find_dotenv(), "DISTANCE", str(distance), quote_mode="never")
        dotenv.set_key(dotenv.find_dotenv(), "EYE_SIZE", str(eye_size), quote_mode="never")
        print("-")

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close the window
cap.release()
cv2.destroyAllWindows()