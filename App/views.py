from django.shortcuts import render, redirect, get_object_or_404
from .models import Personne, Cv, Loisir, Competence, ExperienceProfessionnelle, Formation, ModelCv, Langue
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms.models import model_to_dict

# Create your views here.
def showCv(request):
    return render(request, 'formatCv/defaut.html')

def index(request):
    # personnes = Personne.objects.all()
    data_list = Personne.objects.all()  # Fetch data from your model
    paginator = Paginator(data_list, 3)  # Show 10 items per page

    page_number = request.GET.get('page')  # Get the page number from the query string
    try:
        personne = paginator.page(page_number)
    except PageNotAnInteger:
        personne = paginator.page(1)  # If page is not an integer, show the first page
    except EmptyPage:
        personne = paginator.page(paginator.num_pages)


    return render(request, 'index.html', {'data':personne})

# enregistrer une nouvelle personne
def ajouterPersonne(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenoms = request.POST.get('prenoms')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        mdp = request.POST.get('mdp')
        cmdp = request.POST.get('cmdp')
        photo = request.FILES.get('photo')

        # Vérifier si tous les champs obligatoires sont remplis
        if not all([nom, prenoms, telephone, email, adresse, mdp, cmdp]):
            messages.error(request, "Tous les champs doivent être remplis.")
            return redirect('ajouterPersonne')

        # Vérifier si les deux mots de passe sont identiques
        if mdp != cmdp:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('ajouterPersonne')

        # Enregistrer la personne
        try:
            personne = Personne.objects.create_user(
                nom=nom,
                prenom=prenoms,
                telephone=telephone,
                adresse=adresse,
                email=email,
                photo=photo,
            )
            # Définir et sécuriser le mot de passe
            personne.set_password(mdp)
            personne.save()

            Cv.objects.create(
                poste="",
                description="",
                photo="",
                personne=personne,
                modele=ModelCv.objects.get(numero=0)
            )

            # Connecter automatiquement l'utilisateur
            login(request, personne)

            # Redirection après création
            return redirect('profil')
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite : {str(e)}")
            return redirect('ajouterPersonne')

    return render(request, 'cv/ajouterPersonne.html')
    

# def description(request, personnde_id):
#     if request.method == "POST":
#         titre = request.POST.get('titre')
#         description = request.POST.get('description')
#         personne = get_object_or_404(Personne, id=personnde_id)

#         cv = Cv.objects.create(
#             poste=titre,
#             description=description,
#             personne=personne
#         )

#         # Garder l'id du cv en session 
#         request.session["cv_id"] = cv.id
#         return redirect('formation')

#     else:
#         user_id = request.session.get("user")
#         if not user_id:
#             redirect("ajouterPersonne")
#         return render(request, 'cv/description.html')

@login_required
def description(request):
    if request.method == "POST":
        photo = request.POST.get('photo') 
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        modele = get_object_or_404(ModelCv, id=request.session.get("modele"))
        cv = Cv.objects.create(
            poste=titre,
            description=description,
            modele=modele,
            photo=photo,
            personne=request.user
        )

        # Garder l'id du cv en session 
        request.session["cv_id"] = cv.id


        return JsonResponse({"success": True, "message": "CV enregistré avec succès"}, status=200)

    return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=405)


@login_required
def getDescription(request):
    if request.method == "GET":
        cv_id = request.session.get("cv_id")

        if not cv_id:
            return JsonResponse({"success": False, "message": "CV non trouvé."}, status=404)

        try:
            # Récupérer le CV depuis la base de données
            cvData = Cv.objects.get(id=cv_id)

            # Convertir en dictionnaire pour l'envoyer comme JSON

            cv_dict = {
                'id':cvData.id,
                'poste':cvData.poste,
                'description':cvData.description,
            }

            return JsonResponse({"success": True, "cvData": cv_dict}, status=200)

        except Cv.DoesNotExist:
            return JsonResponse({"success": False, "message": "CV introuvable."}, status=404)

    return JsonResponse({"success": False, "message": "Méthode non autorisée."}, status=405)



@login_required
def formation(request):
    # Reccuperer l'id du cv gardé en session
    if request.method == "POST":
        # Récupérer les données envoyées
        periodes = request.POST.getlist("periode[]")
        formations = request.POST.getlist("formation[]")
        etablissements = request.POST.getlist("etablissement[]")
        cv_id = request.session.get("cv_id")


        cv = get_object_or_404(Cv, id=cv_id)
        if not cv:
            return JsonResponse({"success": False, "message": "CV introuvable."})

        # # Sauvegarder les données dans la base
        for i in range(len(periodes)) :
            Formation.objects.create(
                cv=cv,
                etablissement=etablissements[i],
                diplome=formations[i],
                periode=periodes[i]
            )
        
        return JsonResponse({"success": True, "message": "Les formations ont été enregistrées avec succès."})

    return JsonResponse({"success": False, "message": "Requête non valide."})
    
@login_required
def experienceProfessionnelle(request):

    if request.method == "POST":
        periodes = request.POST.getlist('periode[]')
        postes = request.POST.getlist('poste[]')
        entreprises = request.POST.getlist('entreprise[]')
        localites = request.POST.getlist('localite[]')
        descriptions = request.POST.getlist('description[]')
        cv_id = request.session.get("cv_id")

        print(f"------------------:{postes}")

        cv = get_object_or_404(Cv, id=cv_id)
        if not cv:
            return JsonResponse({"success": False, "message": "CV introuvable."})

        # Sauvegarder les données dans la base
        for i in range(len(periodes)):
            ExperienceProfessionnelle.objects.create(
                cv=cv,
                job_titre=postes[i],
                periode=periodes[i],
                entreprise=entreprises[i],
                localite=localites[i],
                description=descriptions[i],
            )
        
        return JsonResponse({"success": True, "message": "Enregistrement reussit!"})

    return JsonResponse({"success": False, "message": "Requête non valide."})
    
@login_required
def competence(request): 
    if request.method == "POST":
        competences = request.POST.getlist('competence[]')
        niveaux = request.POST.getlist('niveau[]')
        cv_id = request.session.get("cv_id")

        cv = get_object_or_404(Cv, id=cv_id)
        if not cv:
            return JsonResponse({"success": False, "message": "CV introuvable."})

        # # Sauvegarder les données dans la base
        for i in range(len(competences)):
            Competence.objects.create(
                cv=cv,
                competence=competences[i],
                niveau=niveaux[i],
            )
        
        return JsonResponse({"success": True, "message": "Enregistrement reussit!"})

    return JsonResponse({"success": False, "message": "Requête non valide."})
        
    
@login_required
def langue(request):
    if request.method == "POST":
        langues = request.POST.getlist('langue[]')
        niveaux = request.POST.getlist('niveau[]')
        cv_id = request.session.get("cv_id")

        cv = get_object_or_404(Cv, id=cv_id)
        if not cv:
            return JsonResponse({"success": False, "message": "CV introuvable."})

        # # Sauvegarder les données dans la base
        for i in range(len(niveaux)):
            Langue.objects.create(
                cv=cv,
                langue=langues[i],
                niveau=niveaux[i],
            )
        
        return JsonResponse({"success": True, "message": "Enregistrement reussit!"})

    return JsonResponse({"success": False, "message": "Requête non valide."})
    
@login_required
def loisirs(request):
    if request.method == "POST":
        loisirs = request.POST.getlist('loisirs[]')
        cv_id = request.session.get("cv_id")

        cv = get_object_or_404(Cv, id=cv_id)
        if not cv:
            return JsonResponse({"success": False, "message": "CV introuvable."})

        # # Sauvegarder les données dans la base
        for i in range(len(loisirs)):
            Loisir.objects.create(
                cv=cv,
                loisirs=loisirs[i],
            )
        
        return redirect("getCv")

    return JsonResponse({"success": False, "message": "Requête non valide."})
    
# gerer la connexion de l'utilisateur
def connexion(request):
    context = {}
    if request.method == "POST":
        if request.session.get('slug'):
            del request.session['slug']

        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user:

            login(request, user)
            # request.session["user"] = user

            return redirect('profil')
        else:
            context['error'] = True
            return render(request, "utilisateur/connexion.html", context)
    else:
        slug = request.session.get("slug")
        if slug:
            context["slug"] = slug

        return render(request, "utilisateur/connexion.html", context)

def deconnexion(request):
    logout(request)
    return redirect("connexion")

@login_required
def profil(request):
    user_cv = Cv.objects.filter(personne=request.user)
    nbIncomplet = len(user_cv.filter(terminer=False))
    return render(request, "utilisateur/profil/home.html",{'user_cv':user_cv, 'nbIncomplet':nbIncomplet})

@login_required
def selectTemplate(request):
    models = ModelCv.objects.all()
    return render(request, "utilisateur/profil/templateCv/index.html",{'models':models})

@login_required
def ajouterCv(request, numero):
    template_path = f"formatCv/{numero}.html"  # Génération du chemin dynamique
    request.session["modele"] = numero
    return render(request, "utilisateur/profil/templateCv/ajouterCv.html", {'template_path': template_path})


def format(request):
    return render(request, "formatCv/1.html")

def getCv(request):
    cv_id = request.session.get("cv_id")
    cv = get_object_or_404(Cv, id=cv_id)
    
    loisirs = cv.loisir_set.all()
    experiences = cv.experienceprofessionnelle_set.all()
    langues = cv.langue_set.all()
    competences = cv.competence_set.all()
    
    contexte = {
        'cv': cv,
        'loisirs': loisirs,
        'experiences': experiences,
        'langues': langues,
        'competences': competences,
    }

    return render(request, "utilisateur/profil/detail-cv.html", contexte)