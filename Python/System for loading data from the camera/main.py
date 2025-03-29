import json
import time
import cv2

# Load pre-trained Haar cascade classifiers for face and smile detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Initialize video capture from the default camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not found")
    exit()

prev_frame = None  # Store the previous frame for motion detection
motion_detection_value = 4000  # Threshold for detecting movement

# Counters for smile detection stabilization
smile_counter = 0
no_smile_counter = 0
threshold = 5  # Number of consecutive frames required to confirm detection

# Variables to store the last detected statuses
last_smile_status = None
last_move_status = None


def save_detection_data(data, filename="detection_data.json"):
    """
    Save the detection results to a JSON file.
    :param data: Dictionary containing detection information
    :param filename: Name of the JSON file where data is saved
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Error writing to file:", e)


last_save_time = time.time()  # Track the last time detection data was saved

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop if frame is not captured

    frame = cv2.resize(frame, (640, 480))  # Resize frame for consistency
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert frame to grayscale

    # Dictionary to store detection results for the current frame
    detection_info = {
        "face_detected": False,
        "smile_detected": False,
        "movement_detected": False
    }

    # Face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
    if len(faces) == 0:
        smile_counter = 0
        no_smile_counter = 0
        print("No face detected")
    else:
        detection_info["face_detected"] = True
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)  # Draw rectangle around face
            roi_gray = gray[y:y + h, x:x + w]  # Region of interest (ROI) for smile detection

            # Smile detection within the detected face
            smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=30, minSize=(30, 30))
            if len(smiles) > 0:
                no_smile_counter = 0
                if smile_counter < threshold:
                    smile_counter += 1

                if smile_counter >= threshold:
                    detection_info["smile_detected"] = True
                    if last_smile_status != "smile":
                        print("Smile detected")
                        last_smile_status = "smile"
            else:
                smile_counter = 0
                if no_smile_counter < threshold:
                    no_smile_counter += 1

                if no_smile_counter >= threshold and last_smile_status != "no_smile":
                    detection_info["smile_detected"] = False
                    print("Smile not detected")
                    last_smile_status = "no_smile"

            break  # Process only the first detected face

    # Movement detection in the lower half of the frame
    roi_move = gray[240:480, :]
    if prev_frame is not None:
        prev_roi_move = prev_frame[240:480, :]
        frame_diff = cv2.absdiff(prev_roi_move, roi_move)  # Compute difference between consecutive frames
        thresh_img = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
        non_zero_count = cv2.countNonZero(thresh_img)  # Count the number of changed pixels

        # Display motion value on frame
        cv2.putText(frame, f"Motion: {non_zero_count}", (10, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Detect movement based on threshold
        if non_zero_count > motion_detection_value:
            detection_info["movement_detected"] = True
            if last_move_status != "movement":
                print("Movement detected")
                last_move_status = "movement"
        else:
            last_move_status = "none"
    prev_frame = gray.copy()  # Store current frame for next iteration

    # Save detection data every 0.5 seconds
    if time.time() - last_save_time >= 0.5:
        save_detection_data(detection_info)
        last_save_time = time.time()

    # Display the frame with detection overlays
    cv2.imshow("Face, facial expression and movement detection", gray)

    # Exit loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
