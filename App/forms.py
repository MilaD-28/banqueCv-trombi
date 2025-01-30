from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Personne

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Personne
        fields = ('email', 'nom', 'prenom', 'telephone', 'adresse')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Personne
        fields = ('email', 'nom', 'prenom', 'telephone', 'adresse')
