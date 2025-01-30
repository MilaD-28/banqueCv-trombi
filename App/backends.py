from django.contrib.auth.backends import ModelBackend
from .models import Personne

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Cherche un utilisateur avec l'email fourni
            print(f"passe email----------------------: {request}")
            user = Personne.objects.get(email=email)
            print(f"passe email----------------------: {user.password}")
            print(f"password----------------------: {user.check_password(password)}")
            # Vérifie si le mot de passe est correct
            if user.check_password(password):
                print(f"passe email password----------------------: {user}")
                return user
        except Personne.DoesNotExist:
            # Si l'utilisateur n'existe pas, retourne None
            return None
