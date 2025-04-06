import face_recognition
import cv2
import subprocess

# Load the known image and encode the face
known_image = face_recognition.load_image_file("known_face.jpg")  # Load the image of the known person
known_encoding = face_recognition.face_encodings(known_image)[0]  # Encode the face for later comparison

# Initialize the camera
video_capture = cv2.VideoCapture(0)  # Open the default camera (0 is usually the built-in webcam)

print("🎥 Starting the camera... Press 'q' to exit.")  # Inform the user that the camera is starting

# Variable to track if the face has already been recognized
face_recognized = False  # Initially set to False to allow for face recognition

while True:
    ret, frame = video_capture.read()  # Read the current frame from the camera
    if not ret:  # If the frame was not successfully captured
        print("❌ Failed to read from the camera.")  # Display an error message
        break

    # Convert from BGR (OpenCV) to RGB (face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the frame for face recognition processing

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame, model='hog')  # Locate faces using HOG model

    # If faces are detected and no face has been recognized yet
    if face_locations and not face_recognized:
        try:
            # Find the encodings of all faces detected
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                # Compare the detected face encoding to the known encoding
                matches = face_recognition.compare_faces([known_encoding], face_encoding)

                if True in matches:  # If a match is found
                    print("✔️ User recognized! Launching Smart Control Center...")

                    # Release the camera and close the window before launching the program
                    video_capture.release()  # Release the camera
                    cv2.destroyAllWindows()  # Close the OpenCV window

                    # Debug: Check if the script path is correct
                    face_detection_script = r"C:\fork\Python_microcontroller_v1\Python\Smart Control Center\main.py"
                    print(f"Launching program: {face_detection_script}")

                    # Launch another program and stop face recognition
                    process = subprocess.Popen([
                        r"C:\fork\Python_microcontroller_v1\Python\Face ID\venv\Scripts\python.exe",
                        # Python interpreter path
                        face_detection_script  # Path to the Smart Control Center program
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)  # Run the program in the background

                    # Check if the process was started successfully
                    stdout, stderr = process.communicate()  # Get the output and errors from the process

                    if process.returncode != 0:  # If there was an error
                        print(f"❌ Error starting the program: {stderr.decode()}")  # Print the error message
                    else:
                        print(f"✔️ Program started successfully: {stdout.decode()}")  # Print the successful message

                    face_recognized = True  # Set the variable to True to prevent further face recognition
                    break  # Exit the loop once the face has been recognized
                else:
                    print("❌ Unknown face!")  # If no match is found, print an error message
        except Exception as e:
            print(f"⚠️ Error while calculating face encoding: {e}")  # Print any errors during face encoding
    else:
        print("😶 No face detected")  # If no face is detected in the frame

    # Display the current frame in the OpenCV window
    cv2.imshow('Face ID - Press q to exit', frame)

    # Check if the user presses 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Exit the loop if 'q' is pressed

# Release the camera and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
