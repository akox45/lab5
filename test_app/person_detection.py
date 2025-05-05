import cv2
import numpy as np

class PersonDetector:
    def __init__(self):
        # Load the pre-trained Haar Cascade classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_persons(self, image_path):
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw rectangles around detected faces
        processed_image = image.copy()
        for i, (x, y, w, h) in enumerate(faces):
            cv2.rectangle(processed_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            text = f"Person {i+1}"
            y_text = y - 10 if y - 10 > 10 else y + 10
            cv2.putText(processed_image, text, (x, y_text),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

        return processed_image, len(faces) 