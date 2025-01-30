
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
    path('description/',views.description, name='description'),
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
    path('g-description/',views.getDescription, name='getDescription'),
    path('get-cv/<int:cv_id>',views.getCv, name='getCv'),
    path('mes-cv/',views.mesCv, name='mesCv'),



    path('format/',views.format, name='format'),
    path('nouveau-cv/<int:id>',views.creerCv, name='cv'),

    path('get-formation/',views.getFormation, name='get-formation'),
    path('get-competence/',views.getCompetence, name='get-competence'),
    path('get-langue/',views.getLangue, name='get-langue'),
    path('get-loisir/',views.getLoisir, name='get-loisir'),
    path('get-experience/',views.getExperience, name='get-experience'),
    path('enregistrer-cv/',views.creerCv, name='enregistrer_cv'),

    path('edit-competence/<int:id>',views.editCompetence, name='edit-competence'),
    path('edit-formation/<int:id>',views.editFormation, name='edit-formation'),
    path('edit-langue/<int:id>',views.editLangue, name='edit-langue'),
    path('edit-loisir/<int:id>',views.editLoisir, name='edit-loisir'),
    path('edit-exp/<int:id>',views.editExp, name='edit-exp'),
    path('edit-profil/<int:id>',views.editProfil, name='edit-profil'),
    path('edit-cv/<int:id>',views.editCv, name='edit-cv'),

    path('envoyer-email',views.envoyer_email, name='envoyer_email'),

]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
