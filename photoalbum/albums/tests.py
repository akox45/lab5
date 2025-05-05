import os
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from .models import Photo
from .person_detection import PersonDetector

class PersonDetectionTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test image directory
        self.test_image_dir = os.path.join(os.path.dirname(__file__), 'test_images')
        os.makedirs(self.test_image_dir, exist_ok=True)
        
        # Download test image
        self.test_image_path = os.path.join(self.test_image_dir, 'test_image.jpg')
        if not os.path.exists(self.test_image_path):
            import urllib.request
            urllib.request.urlretrieve(
                'https://raw.githubusercontent.com/opencv/opencv/master/samples/data/lena.jpg',
                self.test_image_path
            )
    
    def test_person_detection(self):
        # Test the PersonDetector class
        detector = PersonDetector()
        processed_image, person_count = detector.detect_persons(self.test_image_path)
        
        self.assertIsNotNone(processed_image)
        self.assertIsInstance(person_count, int)
    
    def test_photo_upload_with_detection(self):
        # Test photo upload with person detection
        with open(self.test_image_path, 'rb') as f:
            image_data = f.read()
        
        uploaded_file = SimpleUploadedFile(
            'test_image.jpg',
            image_data,
            content_type='image/jpeg'
        )
        
        photo = Photo.objects.create(
            name='Test Photo',
            image=uploaded_file,
            description='Test description',
            user=self.user
        )
        
        # Process the image
        detector = PersonDetector()
        processed_image, person_count = detector.detect_persons(photo.image.path)
        
        self.assertIsNotNone(processed_image)
        self.assertIsInstance(person_count, int)
        
        # Update the photo with processed image and person count
        photo.detected_persons = person_count
        photo.save()
        
        # Verify the photo was updated
        updated_photo = Photo.objects.get(id=photo.id)
        self.assertEqual(updated_photo.detected_persons, person_count)
    
    def tearDown(self):
        # Clean up test files
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.test_image_dir):
            os.rmdir(self.test_image_dir)
