from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

# Personnalisation de la gestion des utilisateurs
class PersonneManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire.")
        email = self.normalize_email(email)

        # Extraction des champs supplémentaires
        nom = extra_fields.pop('nom', None)
        prenom = extra_fields.pop('prenom', None)
        telephone = extra_fields.pop('telephone', None)
        adresse = extra_fields.pop('adresse', None)
        photo = extra_fields.pop('photo', None)

        user = self.model(
            email=email,
            nom=nom,
            prenom=prenom,
            telephone=telephone,
            adresse=adresse,
            photo=photo,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Personne(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    last_name = None
    first_name = None

    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    telephone = models.CharField(max_length=30, unique=True)
    adresse = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="photos/")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone','adresse']

    # Utiliser notre propre manager
    objects = PersonneManager()
class ModelCv(models.Model):
    numero = models.CharField(max_length=5)
    photo = models.ImageField(upload_to="cv/")


class Cv(models.Model):
    poste = models.CharField(max_length=225, default=None)
    description = models.TextField(default=None)
    photo = models.ImageField(upload_to="PhotoCv/", null=True)
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
    modele = models.ForeignKey(ModelCv, on_delete=models.CASCADE, default=0)
    terminer = models.BooleanField(default=False)

class Formation(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    etablissement = models.CharField(max_length=255)
    diplome = models.CharField(max_length=255)
    periode = models.CharField(max_length=4)

class Loisir(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    loisirs = models.CharField(max_length=255)

class ExperienceProfessionnelle(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    job_titre = models.CharField(max_length=255)
    entreprise = models.CharField(max_length=255)
    localite = models.CharField(max_length=255, null=True)
    periode = models.CharField(max_length=50)
    description = models.TextField()

class Langue(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)

class Competence(models.Model):
    cv = models.ForeignKey(Cv, on_delete=models.CASCADE)
    competence = models.CharField(max_length=255)
    niveau = models.CharField(max_length=50)


