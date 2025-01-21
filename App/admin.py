from django.contrib import admin
from .models import Personne, ModelCv, Cv

# Register your models here.

@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    pass

@admin.register(ModelCv)
class ModelCvAdmin(admin.ModelAdmin):
    pass

@admin.register(Cv)
class CvAdmin(admin.ModelAdmin):
    pass