import face_recognition
import os
from pathlib import Path

known_faces = {}
known_faces_dir = Path("known_faces")

# Load reference faces into known_faces dictionary
def load_known_faces():
    for image_path in known_faces_dir.iterdir():
        if image_path.suffix in ['.jpg', '.jpeg', '.png']:
            name = image_path.stem
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_faces[name] = encoding

load_known_faces()

# Function to recognize face
def recognize_face(image_path):
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)
    
    if unknown_encoding:
        unknown_encoding = unknown_encoding[0]
        for name, encoding in known_faces.items():
            match = face_recognition.compare_faces([encoding], unknown_encoding)
            if match[0]:
                return name
    return None
