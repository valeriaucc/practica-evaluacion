LINK DESPLIEGUE RENDER: https://practica-evaluacion.onrender.com/
# 📘 Proyecto Django CRUD - Sistema de Calificaciones

## 🚀 1. Clonar repositorio

```bash
git clone https://github.com/valeriaucc/practica-evaluacion.git
cd practica-evaluacion
```

---

# 📄 2. Crear archivo .gitignore

```cat > .gitignore << 'EOF'
# Virtual env
venv/
.venv/
env/

# Python cache
__pycache__/
*.py[cod]

# SQLite
db.sqlite3
*.sqlite3

# Logs
*.log

# Pytest
.pytest_cache/

# Mypy
.mypy_cache/

# Ruff
.ruff_cache/

# VSCode
.vscode/

# PyCharm
.idea/

# Environment vars
.env

# OS files
.DS_Store
Thumbs.db
EOF
```

Guardar cambios:

```bash
git add .
git commit -m "Agrega gitignore"
git push origin main
```

---

# 🧪 3. Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno:

```bash
venv\Scripts\activate
```

---

# 📦 4. Instalar Django

```bash
pip install django
```

Verificar instalación:

```bash
pip list
```

---

# 📄 5. Crear requirements.txt

```bash
pip freeze > requirements.txt
```

Guardar cambios:

```bash
git add .
git commit -m "Agrega requirements"
git push origin main
```

---

# 🏗️ 6. Crear proyecto Django

```bash
django-admin startproject evaluaciones
cd evaluaciones
```

---

# 📦 7. Crear aplicación

```bash
python manage.py startapp calificaciones
```

Guardar cambios:

```bash
cd ..
git add .
git commit -m "Proyecto Django y app creados"
git push origin main
```

---

# ⚙️ 8. Registrar app en settings.py

Archivo:

```text
evaluaciones/settings.py
```

Agregar:

```python
'calificaciones',
```

---

# 🧱 9. Crear modelo

Archivo:

```text
calificaciones/models.py
```

Código:

```python
from django.db import models

class Calificacion(models.Model):
    nombre_estudiante = models.CharField(max_length=150)
    identificacion = models.CharField(max_length=15)
    asignatura = models.CharField(max_length=100)
    nota1 = models.DecimalField(max_digits=5, decimal_places=2)
    nota2 = models.DecimalField(max_digits=5, decimal_places=2)
    nota3 = models.DecimalField(max_digits=5, decimal_places=2)
    promedio = models.DecimalField(max_digits=5, decimal_places=2, editable=False)

    def calcular_promedio(self):
        return round((self.nota1 + self.nota2 + self.nota3) / 3, 2)

    def save(self, *args, **kwargs):
        self.promedio = self.calcular_promedio()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_estudiante
```

---

# 🔁 10. Crear migraciones

```bash
cd evaluaciones
python manage.py makemigrations
python manage.py migrate
```

---

# 👤 11. Crear superusuario

```bash
python manage.py createsuperuser
```

---

# ⚙️ 12. Registrar modelo en admin

Archivo:

```text
calificaciones/admin.py
```

Código:

```python
from django.contrib import admin
from .models import Calificacion

admin.site.register(Calificacion)
```

---

# 📝 13. Crear formulario

Archivo:

```text
calificaciones/forms.py
```

Código:

```python
from django import forms
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        exclude = ['promedio']
```

---

# 🔄 14. Crear vistas genéricas

Archivo:

```text
calificaciones/views.py
```

Código:

```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Calificacion
from django.urls import reverse_lazy
from django.db.models import Avg

class ListaCalificaciones(ListView):
    model = Calificacion
    template_name = 'calificaciones/listar.html'
    context_object_name = 'calificaciones'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promedio_general'] = Calificacion.objects.aggregate(
            Avg('promedio')
        )['promedio__avg']
        return context

class CrearCalificacion(CreateView):
    model = Calificacion
    fields = ['nombre_estudiante', 'identificacion', 'asignatura', 'nota1', 'nota2', 'nota3']
    template_name = 'calificaciones/crear.html'
    success_url = reverse_lazy('listar')

class EditarCalificacion(UpdateView):
    model = Calificacion
    fields = ['nombre_estudiante', 'identificacion', 'asignatura', 'nota1', 'nota2', 'nota3']
    template_name = 'calificaciones/editar.html'
    success_url = reverse_lazy('listar')

class EliminarCalificacion(DeleteView):
    model = Calificacion
    template_name = 'calificaciones/eliminar.html'
    success_url = reverse_lazy('listar')
```

---

# 🌐 15. Configurar URLs

Archivo:

```text
calificaciones/urls.py
```

Código:

```python
from django.urls import path
from .views import *

urlpatterns = [
    path('', ListaCalificaciones.as_view(), name='listar'),
    path('crear/', CrearCalificacion.as_view(), name='crear'),
    path('editar/<int:pk>/', EditarCalificacion.as_view(), name='editar'),
    path('eliminar/<int:pk>/', EliminarCalificacion.as_view(), name='eliminar'),
]
```

---

# 🌍 16. Configurar URLs principales

Archivo:

```text
evaluaciones/urls.py
```

Código:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calificaciones.urls')),
]
```

---

# 🎨 17. Crear templates HTML

Ruta:

```text
calificaciones/templates/calificaciones/
```

Archivos:

* listar.html
* crear.html
* editar.html
* eliminar.html

---

# ▶️ 18. Ejecutar proyecto

```bash
python manage.py runserver
```

Abrir en navegador:

```text
http://127.0.0.1:8000/
```

---

# 🚀 19. Preparar despliegue en Render

Instalar gunicorn:

```bash
pip install gunicorn
```

Actualizar requirements:

```bash
pip freeze > requirements.txt
```

---

# ⚙️ 20. Configurar settings.py para producción

Archivo:

```text
evaluaciones/settings.py
```

Modificar:

```python
ALLOWED_HOSTS = ['*']
```

Agregar:

```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

---

# 🌐 21. Configuración en Render

## Build Command

```bash
pip install -r requirements.txt && python evaluaciones/manage.py migrate && python evaluaciones/manage.py collectstatic --no-input
```

## Start Command

```bash
gunicorn evaluaciones.wsgi:application --chdir evaluaciones
```

---

# 🎉 Resultado final

El proyecto queda desplegado públicamente en internet usando Render y GitHub.
