import cv2
import numpy as np
import tempfile
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class PersonDetector:
    def __init__(self):
        self.net = cv2.dnn.readNetFromTensorflow('models/opencv_face_detector.pbtxt',
                                                'models/opencv_face_detector.pb')
        self.conf_threshold = 0.7

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

            # Get image dimensions
            height, width = image.shape[:2]

            # Create a blob from the image
            blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123], False, False)

            # Set the input to the network
            self.net.setInput(blob)

            # Run forward pass
            detections = self.net.forward()

            # Process detections
            person_count = 0
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > self.conf_threshold:
                    person_count += 1
                    # Get bounding box coordinates
                    x1 = int(detections[0, 0, i, 3] * width)
                    y1 = int(detections[0, 0, i, 4] * height)
                    x2 = int(detections[0, 0, i, 5] * width)
                    y2 = int(detections[0, 0, i, 6] * height)

                    # Draw rectangle around face
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

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

            return processed_image, person_count 