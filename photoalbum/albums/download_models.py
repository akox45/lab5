import os
import urllib.request
from django.conf import settings

def download_models():
    # Create models directory if it doesn't exist
    models_dir = os.path.join(settings.BASE_DIR, 'albums', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # URLs for the pre-trained models
    deploy_url = 'https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt'
    model_url = 'https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_uint8/res10_300x300_ssd_iter_140000.caffemodel'
    
    # Download files
    deploy_path = os.path.join(models_dir, 'deploy.prototxt')
    model_path = os.path.join(models_dir, 'res10_300x300_ssd_iter_140000.caffemodel')
    
    if not os.path.exists(deploy_path):
        print('Downloading deploy.prototxt...')
        urllib.request.urlretrieve(deploy_url, deploy_path)
    
    if not os.path.exists(model_path):
        print('Downloading pre-trained model...')
        urllib.request.urlretrieve(model_url, model_path)
    
    print('Models downloaded successfully!')

if __name__ == '__main__':
    download_models() 