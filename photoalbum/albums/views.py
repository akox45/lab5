from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.files.base import ContentFile
import os
from .models import Photo, PhotoSubscription, Notification
from .forms import PhotoUploadForm
from .person_detection import PersonDetector
import cv2

def photo_list(request):
    """Fényképek listázása név vagy dátum szerint"""
    sort_by = request.GET.get('sort', 'date')  
    
    if sort_by == 'name':
        photos = Photo.objects.all().order_by('name')
    else:  # date
        photos = Photo.objects.all().order_by('-upload_date')
    
    # Get unread notifications only for authenticated users
    notifications = []
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False)
    
    context = {
        'photos': photos,
        'sort_by': sort_by,
        'notifications': notifications
    }
    return render(request, 'albums/list.html', context)

def photo_detail(request, photo_id):
    """Egy fénykép részletes nézete"""
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'albums/detail.html', {'photo': photo})

@login_required
def photo_upload(request):
    """Fénykép feltöltése (csak bejelentkezett felhasználóknak)"""
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user

            # Process the image
            detector = PersonDetector()
            processed_image, person_count = detector.detect_persons(request.FILES['image'])

            # Save the processed image
            photo.image.save(
                os.path.basename(request.FILES['image'].name),
                processed_image,
                save=False
            )
            photo.detected_persons = person_count
            photo.save()

            messages.success(request, 'Photo uploaded successfully!')
            return redirect('photo_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'albums/upload.html', {'form': form})

@login_required
def photo_delete(request, photo_id):
    """Fénykép törlése (csak a tulajdonos számára)"""
    photo = get_object_or_404(Photo, id=photo_id)
    
    if request.user != photo.user:
        messages.error(request, 'Csak a kép tulajdonosa törölheti a képet!')
        return redirect('photo_detail', photo_id=photo.id)
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'A kép sikeresen törölve!')
        return redirect('photo_list')
    
    return render(request, 'albums/delete.html', {'photo': photo})

@login_required
def subscribe_photos(request):
    """Feliratkozás a fénykép értesítésekre"""
    subscription, created = PhotoSubscription.objects.get_or_create(user=request.user)
    
    if created:
        messages.success(request, 'Sikeresen feliratkoztál a fénykép értesítésekre!')
    else:
        subscription.delete()
        messages.success(request, 'Sikeresen leiratkoztál a fénykép értesítésekről!')
    
    return redirect('photo_list')

@login_required
def mark_notifications_read(request):
    """Mark all notifications as read"""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('photo_list')