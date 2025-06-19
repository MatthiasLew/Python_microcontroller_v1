import json
import cv2

# Load pre-trained Haar cascade classifiers for face and smile detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera not found")
    exit()

# Initialize previous frame for motion detection
prev_frame = None
motion_detection_value = 10000

# Smile detection stabilization counters
smile_counter = 0
no_smile_counter = 0
threshold = 5

# Last known detection states
last_smile_status = None
last_move_status = None
last_saved_detection_info = {}


def save_detection_data(data, filename="detection_data.json"):
    """
    Save the detection result dictionary to a JSON file.

    Args:
        data (dict): A dictionary containing detection status.
        filename (str): File path to save the detection results.
    """
    try:
        with open(filename, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Error writing to file:", e)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply CLAHE to enhance contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    detection_info = {
        "face_detected": False,
        "smile_detected": False,
        "movement_detected": False
    }

    # Face detection with adjusted parameters
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(80, 80))
    if len(faces) == 0:
        smile_counter = 0
        no_smile_counter = 0
        if last_smile_status != "no_face":
            print("No face detected")
            last_smile_status = "no_face"
    else:
        detection_info["face_detected"] = True
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]

            # Smile detection within face region
            smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.5, minNeighbors=15, minSize=(25, 25))
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
            break  # Only process first detected face

    # Motion detection in lower half of frame
    roi_move = gray[240:480, :]
    if prev_frame is not None:
        prev_roi_move = prev_frame[240:480, :]
        frame_diff = cv2.absdiff(prev_roi_move, roi_move)
        thresh_img = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
        non_zero_count = cv2.countNonZero(thresh_img)

        cv2.putText(frame, f"Motion: {non_zero_count}", (10, 450),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if non_zero_count > motion_detection_value:
            detection_info["movement_detected"] = True
            if last_move_status != "movement":
                print("Movement detected")
                last_move_status = "movement"
        else:
            last_move_status = "none"

    prev_frame = gray.copy()

    # Save detection data only when values change
    if detection_info != last_saved_detection_info:
        save_detection_data(detection_info)
        last_saved_detection_info = detection_info.copy()

    cv2.imshow("Face, facial expression and movement detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
