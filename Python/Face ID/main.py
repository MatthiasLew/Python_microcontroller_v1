import face_recognition
import cv2
import subprocess
import os

# Zakładamy, że Smart Control Center jest w katalogu Python/Smart Control Center/main.py
BASE_DIR = os.path.dirname(__file__)
SMART_CENTER = os.path.join(BASE_DIR, 'Python', 'Smart Control Center', 'main.py')

# Wbudowana kamera USB (numer 0)
video_capture = cv2.VideoCapture(0)

print("🎥 Starting the camera... Press 'q' to exit.")
face_recognized = False

# Wczytanie wzorca twarzy (z pliku known_face.jpg w folderze z tym skryptem)
known_image = face_recognition.load_image_file(os.path.join(BASE_DIR, 'known_face.jpg'))
known_encoding = face_recognition.face_encodings(known_image)[0]

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("❌ Failed to read from the camera.")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame, model='hog')

    if face_locations and not face_recognized:
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([known_encoding], face_encoding)
            if True in matches:
                print("✔️ User recognized! Launching Smart Control Center...")
                video_capture.release()
                cv2.destroyAllWindows()

                # Uruchomienie Smart Control Center
                proc = subprocess.Popen([
                    'python3', SMART_CENTER
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = proc.communicate()
                if proc.returncode != 0:
                    print(f"❌ Error: {err.decode()}")
                else:
                    print(f"✔️ Started: {out.decode()}")

                face_recognized = True
                break
            else:
                print("❌ Unknown face!")
    else:
        print("😶 No face detected")

    cv2.imshow('Face ID - Press q to exit', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
