from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

def get_upload_path(instance, filename):
    return os.path.join(
        f"photos/{instance.user.username}",
        timezone.now().strftime('%Y/%m/%d'),
        filename
    )

class Photo(models.Model):
    name = models.CharField(max_length=40, verbose_name="Fénykép neve")
    image = models.ImageField(upload_to=get_upload_path, verbose_name="Kép")
    description = models.TextField(verbose_name="Leírás", blank=True)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Feltöltés dátuma")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")
    detected_persons = models.IntegerField(default=0, verbose_name="Észlelt személyek száma")
    processed_image = models.ImageField(upload_to=get_upload_path, verbose_name="Feldolgozott kép", null=True, blank=True)
    
    class Meta:
        ordering = ['-upload_date']
        verbose_name = "Fénykép"
        verbose_name_plural = "Fényképek"
    
    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        if self.processed_image:
            self.processed_image.delete()
        super().delete(*args, **kwargs)