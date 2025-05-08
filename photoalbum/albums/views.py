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
            
            # Save the original photo first
            photo.save()
            
            # Process the image for person detection
            detector = PersonDetector()
            processed_image, person_count = detector.detect_persons(photo.image.path)
            
            if processed_image is not None:
                # Save the processed image
                processed_image_path = os.path.splitext(photo.image.path)[0] + '_processed.jpg'
                cv2.imwrite(processed_image_path, processed_image)
                
                # Save the processed image to the model
                with open(processed_image_path, 'rb') as f:
                    photo.processed_image.save(
                        os.path.basename(processed_image_path),
                        ContentFile(f.read()),
                        save=False
                    )
                
                # Update person count
                photo.detected_persons = person_count
                photo.save()
                
                # Clean up temporary file
                os.remove(processed_image_path)
                
                # Create notifications for subscribers
                subscribers = PhotoSubscription.objects.all()
                for subscriber in subscribers:
                    if subscriber.user != request.user:  # Don't notify the uploader
                        Notification.objects.create(
                            user=subscriber.user,
                            message=f'Új kép lett feltöltve: {photo.name} (feltöltő: {request.user.username})'
                        )
                
                messages.success(request, f'A kép sikeresen feltöltve! {person_count} személyt észleltünk a képen.')
            else:
                messages.error(request, 'Hiba történt a kép feldolgozása során.')
            
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