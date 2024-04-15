from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Videojuego
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Videojuego
from .forms import PerfilForm
from .models import Perfil



# Create your views here.
def index (request):

    return render(request, 'core/index.html')

def videojuegos(request):
    return render(request, 'core/videojuegos.html')

def vermas(request):
    return render(request, 'core/vermas.html')

def foro(request):
    comentarios = Videojuego.objects.all()

    return render(request, 'core/foro.html', {'comentarios': comentarios})

@login_required
def ver_perfil(request):
    return render(request, 'core/ver_perfil.html')

def editar_perfil(request):
    
    return render(request, 'core/editar_perfil.html')


def registrate(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Usuario registrado exitosamente') 
            return redirect('crear_perfil')
    else:
        form = UserCreationForm()
    return render(request, 'core/registrate.html', {'form': form})



def sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso!')
            return redirect('ver_perfil')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'core/sesion.html')



def cerrar_sesion(request):
    logout(request)
    return redirect('index') 



@login_required
def crear_videojuego(request):
    if request.method == 'POST':
        tipo_videojuego = request.POST.get('tipo_videojuego')
        comentario = request.POST.get('comentario')
        puntuacion = request.POST.get('puntuacion')
        usuario = request.user  # Obtener el usuario actual

        try:
            Videojuego.objects.create(
                tipo_videojuego=tipo_videojuego,
                comentario=comentario,
                puntuacion=puntuacion,
                usuario=usuario  # Asignar el usuario actual al campo de usuario
            )
            messages.success(request, 'El videojuego se ha ingresado correctamente.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al ingresar el videojuego: {str(e)}')

        return redirect('index')
    else:
        return render(request, 'core/error.html', {'mensaje': 'Acceso no autorizado'})
    



def crear_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user
            perfil.save()
            return redirect('ver_perfil')
    else:       
        form = PerfilForm()
    return render(request, 'core/crear_perfil.html', {'form': form})

def ver_perfil(request):
    perfil = Perfil.objects.get(usuario=request.user)
    return render(request, 'core/ver_perfil.html', {'perfil': perfil})

@login_required
def editar_perfil(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('ver_perfil')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'core/editar_perfil.html', {'form': form})