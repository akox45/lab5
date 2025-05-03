from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register_view(request):
    """Felhasználói regisztráció"""
    if request.user.is_authenticated:
        return redirect('photo_list')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Sikeres regisztráció és bejelentkezés!')
            return redirect('photo_list')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Bejelentkezés"""
    if request.user.is_authenticated:
        return redirect('photo_list')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Sikeres bejelentkezés!')
            
            # Ha van next paraméter, akkor redirect oda
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('photo_list')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    """Kijelentkezés"""
    logout(request)
    messages.success(request, 'Sikeres kijelentkezés!')
    return redirect('photo_list')

@login_required
def profile_view(request):
    """Felhasználói profil"""
    user_photos = request.user.photos.all()
    return render(request, 'accounts/profile.html', {'user_photos': user_photos})