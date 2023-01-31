from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Genero)
admin.site.register(models.Idioma)
admin.site.register(models.Autor)
admin.site.register(models.Livro)
admin.site.register(models.Review)
