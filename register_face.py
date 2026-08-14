import cv2
import face_recognition
import os

name = input("Enter student name: ")

camera = cv2.VideoCapture(0)

print("Look at the camera.")
print("Press S to capture the face.")
print("Press Q to cancel.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("Camera error!")
        break

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
        os.makedirs("images", exist_ok=True)

        image_path = f"images/{name}.jpg"

        cv2.imwrite(image_path, frame)

        print("Photo saved!")

        camera.release()
        cv2.destroyAllWindows()

        # Check the saved photo
        image = face_recognition.load_image_file(image_path)
        locations = face_recognition.face_locations(image)

        if len(locations) == 0:
            print("No face detected in the photo.")
            os.remove(image_path)
        else:
            print("================================")
            print("Face registered successfully!")
            print("Student:", name)
            print("================================")

        break

    elif key == ord("q"):
        print("Registration cancelled.")
        break

camera.release()
cv2.destroyAllWindows()