import cv2
import numpy as np
import os
from person_detection import PersonDetector

def test_person_detection():
    # Create a test image with a face
    test_image = np.zeros((300, 300, 3), dtype=np.uint8)
    
    # Draw a simple face-like shape
    cv2.circle(test_image, (150, 150), 50, (255, 255, 255), -1)  # Face
    cv2.circle(test_image, (130, 140), 5, (0, 0, 0), -1)  # Left eye
    cv2.circle(test_image, (170, 140), 5, (0, 0, 0), -1)  # Right eye
    cv2.ellipse(test_image, (150, 160), (20, 10), 0, 0, 180, (0, 0, 0), 2)  # Mouth
    
    # Save the test image
    test_image_path = 'test_face.jpg'
    cv2.imwrite(test_image_path, test_image)
    
    # Initialize PersonDetector
    detector = PersonDetector()
    
    # Detect persons
    processed_image, person_count = detector.detect_persons(test_image_path)
    
    # Save the processed image
    cv2.imwrite('processed_test_face.jpg', processed_image)
    
    print(f"Detected {person_count} persons in the image")
    print("Original and processed images saved as 'test_face.jpg' and 'processed_test_face.jpg'")
    
    # Clean up
    os.remove(test_image_path)
    os.remove('processed_test_face.jpg')

if __name__ == '__main__':
    test_person_detection() 