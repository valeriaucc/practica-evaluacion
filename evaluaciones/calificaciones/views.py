from django.shortcuts import render, redirect, get_object_or_404
from .models import Calificacion
from .forms import CalificacionForm
from django.db.models import Avg

def listar_calificaciones(request):
    calificaciones = Calificacion.objects.all()

    promedio_general = Calificacion.objects.aggregate(
        Avg('promedio')
    )['promedio__avg']

    return render(request, 'calificaciones/listar.html', {
        'calificaciones': calificaciones,
        'promedio_general': promedio_general
    })


def crear_calificacion(request):
    form = CalificacionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar')
    return render(request, 'calificaciones/crear.html', {'form': form})


def editar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)
    form = CalificacionForm(request.POST or None, instance=calificacion)

    if form.is_valid():
        form.save()
        return redirect('listar')

    return render(request, 'calificaciones/editar.html', {'form': form})


def eliminar_calificacion(request, id):
    calificacion = get_object_or_404(Calificacion, id=id)

    if request.method == 'POST':
        calificacion.delete()
        return redirect('listar')

    return render(request, 'calificaciones/eliminar.html', {'calificacion': calificacion})