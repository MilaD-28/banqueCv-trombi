
from django.contrib import admin
from django.urls import path
from App import views

from django.conf import settings
from django.conf.urls.static import static  # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('affiche/cv/',views.showCv, name='showCv'),
    path('nouvele-personne/',views.ajouterPersonne, name='ajouterPersonne'),
    path('description/<int:personne_id>',views.description, name='description'),
    path('formation/',views.formation, name='formation'),
    path('competence/',views.competence, name='competence'),
    path('experience-professionnelle/',views.experienceProfessionnelle, name='experience_pro'),
    path('langue/',views.langue, name='langue'),
    path('loisirs/',views.loisirs, name='loisirs'),
    path('connexion/',views.connexion, name='connexion'),
    path('deconnexion/',views.deconnexion, name='deconnexion'),
    path('profil-user/',views.profil, name='profil'),
    path('user/format-cv',views.selectTemplate, name='format-cv'),
    path('user/ajouter-cv/<int:numero>',views.ajouterCv, name='ajouter-cv'),



    path('format/',views.format, name='format'),
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
