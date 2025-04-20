import face_recognition
import cv2
import subprocess
import os
import time
import keyboard

# Ścieżki do skryptów uruchamianych po Face ID
BASE_DIR = os.path.dirname(__file__)
known_image_path = os.path.join(BASE_DIR, 'known_face.jpg')
detection_script = os.path.abspath(
    os.path.join(BASE_DIR, '..', 'Python', 'System for loading data from the camera', 'main.py')
)
reaction_script = os.path.abspath(
    os.path.join(BASE_DIR, '..', 'Python', 'Reaction simulation system', 'main.py')
)

# Wczytanie wzorca twarzy
print("🔍 Ładowanie wzorca twarzy...")
known_image = face_recognition.load_image_file(known_image_path)
known_encoding = face_recognition.face_encodings(known_image)[0]

# Inicjalizacja kamery USB
video_capture = cv2.VideoCapture(0)
print("🎥 Rozpoczynam Face ID na mikrokontrolerze... Naciśnij 'q' aby wyjść.")

face_recognized = False

# Pętla rozpoznawania
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
            print("✔️ Twarz rozpoznana! Uruchamiam systemy...")
            face_recognized = True
            break
    if face_recognized:
        break

    cv2.imshow('Face ID - mikrokontroler', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

# Jeśli rozpoznano, uruchamiamy pozostałe skrypty
if face_recognized:
    procs = []
    for script in (detection_script, reaction_script):
        p = subprocess.Popen(['python3', script], cwd=os.path.dirname(script))
        procs.append(p)
    print("▶️ Skrypty uruchomione. Naciśnij 'q' aby zatrzymać.")
    try:
        while True:
            if keyboard.is_pressed('q'):
                print("❌ Zatrzymuję wszystkie skrypty...")
                for p in procs:
                    p.terminate()
                break
            time.sleep(0.1)
    except KeyboardInterrupt:
        passq
    print("✅ Wszystkie skrypty zatrzymane.")