import face_recognition
import os
import pickle

# Folder containing images
image_folder = "images"

known_encodings = []
known_names = []

# Read each image in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        image_path = os.path.join(image_folder, filename)

        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(filename)[0])
            print(f"Encoded: {filename}")
        else:
            print(f"No face found in {filename}")

# Save the encodings
os.makedirs("encodings", exist_ok=True)

with open("encodings/encodings.pkl", "wb") as f:
    pickle.dump((known_encodings, known_names), f)

print("Face encoding completed successfully!")