from django import forms
from .models import Photo

class PhotoUploadForm(forms.ModelForm):
    """Fénykép feltöltési űrlap"""
    class Meta:
        model = Photo
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Add meg a kép nevét (max. 40 karakter)'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }
    
    def clean_name(self):
        """Ellenőrzi, hogy a név megfelelő hosszúságú"""
        name = self.cleaned_data.get('name')
        if len(name) > 40:
            raise forms.ValidationError('A kép neve maximum 40 karakter lehet!')
        return name
    
    def clean_image(self):
        """Ellenőrzi, hogy a feltöltött fájl kép-e"""
        image = self.cleaned_data.get('image')
        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise forms.ValidationError('Csak képfájlokat lehet feltölteni!')
        return image