import cv2
import numpy as np
import tempfile
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class PersonDetector:
    def __init__(self):
        # Load the Haar Cascade classifier for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_persons(self, image_file):
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            # Read the image from the uploaded file
            image_content = image_file.read()
            temp_file.write(image_content)
            temp_file.flush()

            # Read the image from the temporary file
            image = cv2.imread(temp_file.name)
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

            # Draw rectangles around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Save the processed image to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as processed_temp:
                cv2.imwrite(processed_temp.name, image)
                processed_temp.flush()

                # Read the processed image and create a ContentFile
                with open(processed_temp.name, 'rb') as f:
                    processed_image = ContentFile(f.read())

            # Clean up temporary files
            os.unlink(temp_file.name)
            os.unlink(processed_temp.name)

            return processed_image, len(faces) 