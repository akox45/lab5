import os
import cv2
import numpy as np

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
    
    # Load the pre-trained Haar Cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Read the image
    image = cv2.imread(test_image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # Initialize counter and processed image
    person_count = len(faces)
    processed_image = image.copy()
    
    # Draw rectangles around detected faces
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(processed_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        text = f"Person {i+1}"
        y_text = y - 10 if y - 10 > 10 else y + 10
        cv2.putText(processed_image, text, (x, y_text),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
    
    # Save the processed image
    cv2.imwrite('processed_test_face.jpg', processed_image)
    
    print(f"Detected {person_count} persons in the image")
    print("Original and processed images saved as 'test_face.jpg' and 'processed_test_face.jpg'")
    
    # Clean up
    os.remove(test_image_path)
    os.remove('processed_test_face.jpg')

if __name__ == '__main__':
    test_person_detection() 