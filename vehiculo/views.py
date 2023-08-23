from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.db import models
from .forms import VehiculoForm, RegistroUsuarioForm
from .models import Vehiculo
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission



# index
class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


# Vehiculo Add
class VehiculoAddView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        form = VehiculoForm()
        return render(request, "vehiculo_add.html", {"form": form})

    def post(self, request):
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("correct_addView")
        return render(request, "vehiculo_add.html", {"form": form})


# Listar Vehiculos query searchbar selector filtro precio_condicion
class ListarVehiculosView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        query = request.GET.get("query")
        precio_condicion = request.GET.get("precio_condicion")
        annio = request.GET.get("año")  # Obtener el valor seleccionado para el año

        vehiculos = Vehiculo.objects.all()

        if query:
            vehiculos = vehiculos.filter(
                models.Q(marca__icontains=query)
                | models.Q(modelo__icontains=query)
                | models.Q(serial_carroceria__icontains=query)
                | models.Q(serial_motor__icontains=query)
                | models.Q(año__icontains=query)
                | models.Q(categoria__icontains=query)
                | models.Q(precio__icontains=query)
            )

        if precio_condicion == 'bajo':
            vehiculos = vehiculos.filter(precio__lte=7000000)
        elif precio_condicion == 'medio':
            vehiculos = vehiculos.filter(precio__gt=7500000, precio__lte=16000000)
        elif precio_condicion == 'alto':
            vehiculos = vehiculos.filter(precio__gt=16000000)

        if annio:  # Aplicar el filtro por año si se selecciona un año
            vehiculos = vehiculos.filter(año=annio)

        return render(request, "listar.html", {"vehiculos": vehiculos, "año": annio})



# Registro
class RegistroView(View):
    def get(self, request):
        form = RegistroUsuarioForm()
        context = {"register_form": form}
        return render(request, "registro.html", context)

    def post(self, request):
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            content_type = ContentType.objects.get_for_model(Vehiculo)  #permiso
            visualizar_catalogo = Permission.objects.get(codename='visualizar_catalogo', content_type=content_type) #permiso
            user = form.save()
            user.user_permissions.add(visualizar_catalogo) #permiso
            login(request, user)
            messages.success(request, "Registro Exitoso.")
            return redirect("/")
        else:
            messages.error(request, "Registro invalido. Algunos datos ingresados no son correctos")
            context = {"register_form": form}
            return render(request, "registro.html", context)


# Login
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {"login_form": form}
        return render(request, "login.html", context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Iniciaste sesion como: {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalido username o password.")
        else:
            messages.error(request, "Invalido username o password.")

        context = {"login_form": form}
        return render(request, "login.html", context)


# Logout
class LogoutView(LoginRequiredMixin, View):
    login_url = '/login/'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redirección

    def get(self, request):
        logout(request)
        messages.info(request, "Se ha cerrado la sesión satisfactoriamente.")
        return redirect("/")


#add vehiculo con exito
def correct_addView(request):
    return render(request, "correct_add.html")

# actualizar vehiculo
class VehiculoUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
        form = VehiculoForm(instance=vehiculo)
        return render(request, "vehiculo_edit.html", {"form": form, "vehiculo": vehiculo})

    def post(self, request, pk):
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo actualizado con éxito.")
            return redirect("listar")  # Asegúrate de que esta ruta coincida con tu lista de vehículos
        return render(request, "vehiculo_edit.html", {"form": form, "vehiculo": vehiculo})

#eliminar vehiculo

class VehiculoDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        vehiculo = get_object_or_404(Vehiculo, pk=pk)
        vehiculo.delete()
        messages.success(request, "Vehículo eliminado con éxito.")
        return redirect("listar")
