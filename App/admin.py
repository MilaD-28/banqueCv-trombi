from django.contrib import admin
from .models import Personne, ModelCv, Cv

from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Personne

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Personne
    list_display = ('email', 'nom', 'prenom', 'telephone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'telephone', 'adresse', 'photo')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nom', 'prenom', 'telephone', 'adresse', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Personne, CustomUserAdmin)

# Register your models here.

# @admin.register(Personne)
# class PersonneAdmin(admin.ModelAdmin):
#     pass

@admin.register(ModelCv)
class ModelCvAdmin(admin.ModelAdmin):
    pass

@admin.register(Cv)
class CvAdmin(admin.ModelAdmin):
    pass