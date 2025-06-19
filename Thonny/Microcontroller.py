import face_recognition
import cv2
import subprocess
import os
import time
import keyboard

# === Configuration ===

BASE_DIR = os.path.dirname(__file__)
known_image_path = os.path.join(BASE_DIR, 'known_face.jpg')

# Paths to scripts that will be launched upon successful face recognition
detection_script = os.path.abspath(os.path.join(
    BASE_DIR, '..', 'Python', 'System for loading data from the camera', 'main.py'))
reaction_script = os.path.abspath(os.path.join(
    BASE_DIR, '..', 'Python', 'Reaction simulation system', 'main.py'))

# === Load known face encoding ===

print("🔍 Loading known face image...")
known_image = face_recognition.load_image_file(known_image_path)
known_encoding = face_recognition.face_encodings(known_image)[0]

# === Initialize camera ===

video_capture = cv2.VideoCapture(0)
print("🎥 Face ID active. Press 'q' to quit.")

face_recognized = False

# === Face recognition loop ===

while True:
    ret, frame = video_capture.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([known_encoding], face_encoding)
        if True in matches:
            print("✔️ Face recognized! Launching systems...")
            face_recognized = True
            break

    if face_recognized:
        break

    cv2.imshow('Face ID - Microcontroller', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

# === Launch reaction and detection systems if face was recognized ===

if face_recognized:
    procs = []
    for script in (detection_script, reaction_script):
        p = subprocess.Popen(['python3', script], cwd=os.path.dirname(script))
        procs.append(p)

    print("▶️ Scripts launched. Press 'q' to terminate.")

    try:
        while True:
            if keyboard.is_pressed('q'):
                print("❌ Terminating all scripts...")
                for p in procs:
                    p.terminate()
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        for p in procs:
            p.terminate()

    print("✅ All scripts terminated.")
