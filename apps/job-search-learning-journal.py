import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import json
import os

# Configuration de la page
st.set_page_config(
    page_title="Journal d'Apprentissage - Recherche d'Emploi",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #2E86C1;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.8rem;
        color: #2471A3;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .subsection-title {
        font-size: 1.4rem;
        color: #1A5276;
        margin-top: 0.8rem;
        margin-bottom: 0.4rem;
    }
    .badge {
        background-color: #E8F4FD;
        padding: 0.3rem 0.6rem;
        border-radius: 0.5rem;
        font-weight: bold;
        color: #2471A3;
    }
    .card {
        background-color: #F8F9F9;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 0.15rem 0.3rem rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .tip-box {
        background-color: #E8F8F5;
        border-left: 0.3rem solid #1ABC9C;
        padding: 1rem;
        margin: 1rem 0;
    }
    .progress-container {
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour sauvegarder les données
def save_data(data, file_name):
    try:
        with open(file_name, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde: {e}")

# Fonction pour charger les données
def load_data(file_name):
    if os.path.exists(file_name):
        try:
            with open(file_name, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Erreur lors du chargement: {e}")
            return {}
    return {}

# Initialisation des fichiers de données
profile_file = "profile_data.json"
journal_file = "journal_entries.json"
applications_file = "job_applications.json"
skills_file = "skills_tracker.json"

# Chargement des données
profile_data = load_data(profile_file)
journal_entries = load_data(journal_file)
job_applications = load_data(applications_file)
skills_data = load_data(skills_file)

# Convertir les entrées de journal en liste si nécessaire
if not isinstance(journal_entries, list):
    journal_entries = []

# Convertir les candidatures en liste si nécessaire
if not isinstance(job_applications, list):
    job_applications = []

# Initialiser les données de compétences si nécessaire
if not skills_data:
    skills_data = {
        "cv": {"niveau": 0, "log": []},
        "lettre_motivation": {"niveau": 0, "log": []},
        "recherche_offres": {"niveau": 0, "log": []},
        "reseautage": {"niveau": 0, "log": []},
        "preparation_entretien": {"niveau": 0, "log": []},
        "communication": {"niveau": 0, "log": []},
        "competences_techniques": {"niveau": 0, "log": []}
    }

# Barre latérale pour la navigation
st.sidebar.markdown("<h2 style='text-align: center;'>Navigation</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("", [
    "📌 Accueil",
    "👤 Mon Profil", 
    "📔 Journal d'Apprentissage", 
    "📊 Suivi des Candidatures",
    "🧠 Progression des Compétences",
    "🏆 Objectifs et Plans d'Action",
    "🛠️ Ressources Utiles"
])

# Afficher le profil de l'utilisateur dans la barre latérale
st.sidebar.markdown("---")
st.sidebar.markdown("<h3 style='text-align: center;'>Mon Profil</h3>", unsafe_allow_html=True)

if profile_data:
    st.sidebar.markdown(f"**Nom**: {profile_data.get('nom', 'Non défini')}")
    st.sidebar.markdown(f"**Objectif**: {profile_data.get('objectif_carriere', 'Non défini')}")
    
    # Calcul du niveau global
    if skills_data:
        niveaux = [data["niveau"] for data in skills_data.values()]
        if niveaux:
            niveau_global = sum(niveaux) / len(niveaux)
            st.sidebar.markdown(f"**Niveau global**: {niveau_global:.1f}/5")
            st.sidebar.progress(niveau_global / 5)

# Page d'accueil
if page == "📌 Accueil":
    st.markdown("<h1 class='main-title'>Journal d'Apprentissage pour la Recherche d'Emploi</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Bienvenue dans votre journal d'apprentissage !</h2>", unsafe_allow_html=True)
        st.markdown("""
        Cet outil vous accompagne pas à pas dans votre parcours de recherche d'emploi en vous permettant de :
        - 📝 Documenter votre progression
        - 🎯 Suivre vos objectifs et compétences
        - 📊 Organiser vos candidatures
        - 💡 Réfléchir sur vos apprentissages
        - 🚀 Préparer efficacement vos entretiens
        
        Commencez par compléter votre profil, puis explorez les différentes sections pour tirer le meilleur parti de cet outil.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Statistiques rapides
        st.markdown("<h2 class='section-title'>Tableau de bord</h2>", unsafe_allow_html=True)
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        with stats_col1:
            st.markdown("<div class='card' style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: #3498DB;'>{len(journal_entries)}</h1>", unsafe_allow_html=True)
            st.markdown("<p>Entrées de journal</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with stats_col2:
            st.markdown("<div class='card' style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: #2ECC71;'>{len(job_applications)}</h1>", unsafe_allow_html=True)
            st.markdown("<p>Candidatures suivies</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with stats_col3:
            active_applications = sum(1 for app in job_applications if app.get('statut') not in ['Refusé', 'Abandonné'])
            st.markdown("<div class='card' style='text-align: center;'>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: #E74C3C;'>{active_applications}</h1>", unsafe_allow_html=True)
            st.markdown("<p>Candidatures actives</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Dernière activité
        if journal_entries:
            st.markdown("<h3 class='subsection-title'>Dernière entrée de journal</h3>", unsafe_allow_html=True)
            last_entry = journal_entries[-1]
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>{last_entry.get('date', 'Date inconnue')}</strong> - <span class='badge'>{last_entry.get('categorie', 'Non catégorisé')}</span></p>", unsafe_allow_html=True)
            st.markdown(f"<h4>{last_entry.get('titre', 'Sans titre')}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p>{last_entry.get('contenu', '')[:150]}... <a href='#'>Voir plus</a></p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Conseil du jour
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='subsection-title'>💡 Conseil du jour</h3>", unsafe_allow_html=True)
        conseils = [
            "Personnalisez votre CV pour chaque offre en mettant en avant les compétences pertinentes.",
            "Préparez des exemples concrets pour illustrer vos compétences lors des entretiens.",
            "Recherchez l'entreprise avant un entretien : histoire, valeurs, actualités récentes.",
            "Activez votre réseau LinkedIn en participant aux discussions de votre secteur.",
            "Suivez systématiquement après un entretien avec un email de remerciement.",
            "Exercez-vous aux entretiens vidéo en vous enregistrant puis en analysant votre prestation.",
            "Créez une signature email professionnelle avec vos coordonnées et liens pertinents."
        ]
        import random
        st.markdown(f"<p><em>{random.choice(conseils)}</em></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Prochaines étapes suggérées
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='subsection-title'>⏭️ Prochaines étapes suggérées</h3>", unsafe_allow_html=True)
        
        if not profile_data:
            st.markdown("- ✅ Compléter votre profil")
        if len(journal_entries) < 2:
            st.markdown("- 📝 Ajouter une entrée dans votre journal")
        if len(job_applications) < 1:
            st.markdown("- 🎯 Enregistrer votre première candidature")
        if sum(data["niveau"] for data in skills_data.values()) < 5:
            st.markdown("- 📊 Évaluer vos compétences actuelles")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Progression globale
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='subsection-title'>📈 Progression globale</h3>", unsafe_allow_html=True)
        
        if skills_data:
            competences = {
                "CV et profil": skills_data["cv"]["niveau"],
                "Lettre de motivation": skills_data["lettre_motivation"]["niveau"],
                "Recherche d'offres": skills_data["recherche_offres"]["niveau"],
                "Réseautage": skills_data["reseautage"]["niveau"],
                "Préparation entretien": skills_data["preparation_entretien"]["niveau"],
                "Communication": skills_data["communication"]["niveau"],
                "Comp. techniques": skills_data["competences_techniques"]["niveau"]
            }
            
            chart_data = pd.DataFrame({
                "Compétence": list(competences.keys()),
                "Niveau": list(competences.values())
            })
            
            fig = px.bar(
                chart_data, 
                x="Niveau", 
                y="Compétence", 
                orientation='h',
                range_x=[0, 5],
                color="Niveau",
                color_continuous_scale="blues"
            )
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Commencez à évaluer vos compétences pour voir votre progression.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Page de profil
elif page == "👤 Mon Profil":
    st.markdown("<h1 class='main-title'>Mon Profil Professionnel</h1>", unsafe_allow_html=True)
    
    with st.form("profile_form"):
        st.markdown("<h2 class='section-title'>Informations personnelles</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet", profile_data.get("nom", ""))
            email = st.text_input("Email", profile_data.get("email", ""))
            telephone = st.text_input("Téléphone", profile_data.get("telephone", ""))
        
        with col2:
            ville = st.text_input("Ville", profile_data.get("ville", ""))
            linkedin = st.text_input("Profil LinkedIn", profile_data.get("linkedin", ""))
            portfolio = st.text_input("Site web / Portfolio", profile_data.get("portfolio", ""))
        
        st.markdown("<h2 class='section-title'>Objectifs professionnels</h2>", unsafe_allow_html=True)
        
        objectif_carriere = st.text_area("Objectif de carrière (en une phrase)", profile_data.get("objectif_carriere", ""))
        secteurs = st.multiselect(
            "Secteurs d'intérêt",
            ["Informatique & Tech", "Finance", "Marketing & Communication", "Ressources Humaines", "Santé", 
             "Éducation", "Commerce & Vente", "Industrie", "Art & Design", "Médias", "Conseil", "Autre"],
            profile_data.get("secteurs", [])
        )
        
        # Formations
        st.markdown("<h2 class='section-title'>Formation</h2>", unsafe_allow_html=True)
        
        formations = profile_data.get("formations", [{"annee": "", "diplome": "", "etablissement": ""}])
        for i in range(len(formations)):
            col1, col2, col3, col4 = st.columns([1, 3, 3, 1])
            with col1:
                formations[i]["annee"] = st.text_input(f"Année #{i+1}", formations[i]["annee"], key=f"form_annee_{i}")
            with col2:
                formations[i]["diplome"] = st.text_input(f"Diplôme #{i+1}", formations[i]["diplome"], key=f"form_diplome_{i}")
            with col3:
                formations[i]["etablissement"] = st.text_input(f"Établissement #{i+1}", formations[i]["etablissement"], key=f"form_etab_{i}")
            with col4:
                if i == len(formations) - 1:
                    if st.button("➕", key=f"add_formation"):
                        formations.append({"annee": "", "diplome": "", "etablissement": ""})
                else:
                    if st.button("❌", key=f"remove_formation_{i}"):
                        formations.pop(i)
        
        # Expériences
        st.markdown("<h2 class='section-title'>Expériences professionnelles</h2>", unsafe_allow_html=True)
        
        experiences = profile_data.get("experiences", [{"periode": "", "poste": "", "entreprise": "", "description": ""}])
        for i in range(len(experiences)):
            col1, col2, col3 = st.columns([1, 2, 2])
            with col1:
                experiences[i]["periode"] = st.text_input(f"Période #{i+1}", experiences[i]["periode"], key=f"exp_periode_{i}")
            with col2:
                experiences[i]["poste"] = st.text_input(f"Poste #{i+1}", experiences[i]["poste"], key=f"exp_poste_{i}")
            with col3:
                experiences[i]["entreprise"] = st.text_input(f"Entreprise #{i+1}", experiences[i]["entreprise"], key=f"exp_entreprise_{i}")
            
            experiences[i]["description"] = st.text_area(f"Description #{i+1}", experiences[i]["description"], key=f"exp_desc_{i}")
            
            col1, col2 = st.columns([5, 1])
            with col2:
                if i == len(experiences) - 1:
                    if st.button("➕", key=f"add_experience"):
                        experiences.append({"periode": "", "poste": "", "entreprise": "", "description": ""})
                else:
                    if st.button("❌", key=f"remove_experience_{i}"):
                        experiences.pop(i)
            
            if i < len(experiences) - 1:
                st.markdown("---")
        
        # Compétences
        st.markdown("<h2 class='section-title'>Compétences</h2>", unsafe_allow_html=True)
        
        competences_techniques = st.text_area("Compétences techniques (séparées par des virgules)", 
                                            profile_data.get("competences_techniques", ""))
        competences_linguistiques = st.text_area("Langues (format: Langue - Niveau, séparées par des virgules)", 
                                                profile_data.get("competences_linguistiques", ""))
        competences_transversales = st.text_area("Compétences transversales (séparées par des virgules)", 
                                                profile_data.get("competences_transversales", ""))
        
        submit_button = st.form_submit_button("Enregistrer mon profil")
        
        if submit_button:
            updated_profile = {
                "nom": nom,
                "email": email,
                "telephone": telephone,
                "ville": ville,
                "linkedin": linkedin,
                "portfolio": portfolio,
                "objectif_carriere": objectif_carriere,
                "secteurs": secteurs,
                "formations": formations,
                "experiences": experiences,
                "competences_techniques": competences_techniques,
                "competences_linguistiques": competences_linguistiques,
                "competences_transversales": competences_transversales
            }
            
            save_data(updated_profile, profile_file)
            st.success("Profil mis à jour avec succès !")
            
    # Aperçu du CV
    if profile_data:
        with st.expander("Aperçu de mon profil (format CV)"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"# {profile_data.get('nom', 'Votre Nom')}")
                st.markdown(f"📧 {profile_data.get('email', '')}")
                st.markdown(f"📱 {profile_data.get('telephone', '')}")
                st.markdown(f"🏙️ {profile_data.get('ville', '')}")
                
                if profile_data.get('linkedin'):
                    st.markdown(f"🔗 [LinkedIn]({profile_data.get('linkedin')})")
                if profile_data.get('portfolio'):
                    st.markdown(f"🌐 [Portfolio]({profile_data.get('portfolio')})")
                
                st.markdown("### Compétences")
                if profile_data.get('competences_techniques'):
                    st.markdown("**Techniques:**")
                    for comp in profile_data.get('competences_techniques').split(','):
                        st.markdown(f"- {comp.strip()}")
                
                if profile_data.get('competences_linguistiques'):
                    st.markdown("**Langues:**")
                    for langue in profile_data.get('competences_linguistiques').split(','):
                        st.markdown(f"- {langue.strip()}")
                
                if profile_data.get('competences_transversales'):
                    st.markdown("**Transversales:**")
                    for comp in profile_data.get('competences_transversales').split(','):
                        st.markdown(f"- {comp.strip()}")
            
            with col2:
                st.markdown("## Objectif professionnel")
                st.markdown(f"*{profile_data.get('objectif_carriere', '')}*")
                
                if profile_data.get('secteurs'):
                    st.markdown("**Secteurs d'intérêt:** " + ", ".join(profile_data.get('secteurs')))
                
                st.markdown("## Formation")
                for formation in profile_data.get('formations', []):
                    if formation['diplome'] and formation['etablissement']:
                        st.markdown(f"**{formation['annee']}** - {formation['diplome']} - {formation['etablissement']}")
                
                st.markdown("## Expériences professionnelles")
                for exp in profile_data.get('experiences', []):
                    if exp['poste'] and exp['entreprise']:
                        st.markdown(f"### {exp['poste']} | {exp['entreprise']}")
                        st.markdown(f"*{exp['periode']}*")
                        st.markdown(exp['description'])

# Page du journal d'apprentissage
elif page == "📔 Journal d'Apprentissage":
    st.markdown("<h1 class='main-title'>Mon Journal d'Apprentissage</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Nouvelle entrée", "📚 Historique des entrées"])
    
    with tab1:
        with st.form("journal_entry_form"):
            st.markdown("<h2 class='section-title'>Ajouter une nouvelle entrée</h2>", unsafe_allow_html=True)
            
            date = st.date_input("Date", datetime.now().date())
            titre = st.text_input("Titre de l'entrée")
            
            categorie = st.selectbox(
                "Catégorie",
                ["Réflexion", "Apprentissage", "Entretien", "Candidature", "Formation", "Réseautage", "Autre"]
            )
            
            contenu = st.text_area("Contenu de l'entrée", height=200,
                                 placeholder="Décrivez ce que vous avez appris, ressenti, ou les questions que vous vous posez...")
            
            col1, col2 = st.columns(2)
            
            with col1:
                apprentissages = st.text_area("Ce que j'ai appris", 
                                         placeholder="Listez les nouvelles connaissances ou compétences acquises...")
            
            with col2:
                questions = st.text_area("Questions en suspens", 
                                     placeholder="Notez les points sur lesquels vous avez besoin de clarification...")
            
            ressources = st.text_area("Ressources utiles", 
                                    placeholder="Sites web, contacts, outils, livres... (optionnel)")
            
            actions = st.text_area("Prochaines actions", 
                                 placeholder="Quelles sont vos prochaines étapes suite à cette expérience ? (optionnel)")
            
            emotions = st.slider("Comment vous êtes-vous senti durant cette expérience ?", 1, 10, 5, 
                                help="1 = Très négatif, 10 = Très positif")
            
            submit_entry = st.form_submit_button("Enregistrer cette entrée")
            
            if submit_entry:
                if titre and contenu:
                    new_entry = {
                        "date": date.strftime("%d/%m/%Y"),
                        "titre": titre,
                        "categorie": categorie,
                        "contenu": contenu,
                        "apprentissages": apprentissages,
                        "questions": questions,
                        "ressources": ressources,
                        "actions": actions,
                        "emotions": emotions
                    }
                    
                    journal_entries.append(new_entry)
                    save_data(journal_entries, journal_file)
                    st.success("Entrée ajoutée avec succès !")
                    
                    # Mise à jour automatique des compétences en fonction des apprentissages
                    update_skills = False
                    keywords = {
                        "cv": ["cv", "curriculum", "resume", "profil"],
                        "lettre_motivation": ["lettre", "motivation", "candidature"],
                        "recherche_offres": ["recherche", "offre", "annonce", "veille"],
                        "reseautage": ["réseau", "networking", "contact", "linkedin"],
                        "preparation_entretien": ["entretien", "interview", "recruteur", "question"],
                        "communication": ["communiquer", "présentation", "expression", "pitch"],
                        "competences_techniques": ["technique", "logiciel", "programmation", "outil"]
                    }
                    
                    for skill, words in keywords.items():
                        if any(word in apprentissages.lower() for word in words):
                            update_skills = True
                            skills_data[skill]["niveau"] = min(5, skills_data[skill]["niveau"] + 0.5)
                            skills_data[skill]["log"].append({
                                "date": date.strftime("%d/%m/%Y"),
                                "note": f"Progression depuis l'entrée: '{titre}'"
                            })
                    
                    if update_skills:
                        save_data(skills_data, skills_file)
                        st.info("Vos compétences ont été automatiquement mises à jour !")
                else:
                    st.error("Veuillez remplir au moins le titre et le contenu.")
    
    with tab2:
        st.markdown("<h2 class='section-title'>Historique de mon journal</h2>", unsafe_allow_html=True)
        
        if not journal_entries:
            st.info("Vous n'avez pas encore d'entrées dans votre journal. Commencez par en ajouter une !")
        else:
            # Filtres
            col1, col2 = st.columns(2)
            with col1:
                categories = ["Toutes"] + list(set(entry.get("categorie", "Autre") for entry in journal_entries))
                selected_category = st.selectbox("Filtrer par catégorie", categories)
            
            with col2:
                sort_order = st.radio("Trier par", ["Plus récent", "Plus ancien"], horizontal=True)
            
            # Filtrage des entrées
            filtered_entries = journal_entries
            if selected_category != "Toutes":
                filtered_entries = [entry for entry in journal_entries if entry.get("categorie") == selected_category]
            
            # Tri des entrées
            if sort_order == "Plus récent":
                filtered_entries = sorted(filtered_entries, 
                                        key=lambda x: datetime.strptime(x.get("date", "01/01/2000"), "%d/%m/%Y"), 
                                        reverse=True)
            else:
                filtered_entries = sorted(filtered_entries, 
                                        key=lambda x: datetime.strptime(x.get("date", "01/01/2000"), "%d/%m/%Y"))
            
            # Affichage des entrées
            for i, entry in enumerate(filtered_entries):
                with st.expander(f"{entry.get('date', 'Date inconnue')} - {entry.get('titre', 'Sans titre')} ({entry.get('categorie', 'Non catégorisé')})"):
                    st.markdown(f"<h3>{entry.get('titre', 'Sans titre')}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Date:</strong> {entry.get('date', 'Date inconnue')} | <span class='badge'>{entry.get('categorie', 'Non catégorisé')}</span></p>", unsafe_allow_html=True)
                    
                    st.markdown("<h4>Contenu</h4>", unsafe_allow_html=True)
                    st.markdown(entry.get("contenu", ""))
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("<h4>Ce que j'ai appris</h4>", unsafe_allow_html=True)
                        st.markdown(entry.get("apprentissages", "Non spécifié"))
                    
                    with col2:
                        st.markdown("<h4>Questions en suspens</h4>", unsafe_allow_html=True)
                        st.markdown(entry.get("questions", "Aucune question"))
                    
                    if entry.get("ressources"):
                        st.markdown("<h4>Ressources utiles</h4>", unsafe_allow_html=True)
                        st.markdown(entry.get("ressources", ""))
                    
                    if entry.get("actions"):
                        st.markdown("<h4>Prochaines actions</h4>", unsafe_allow_html=True)
                        st.markdown(entry.get("actions", ""))
                    
                    # Affichage du niveau d'émotion
                    st.markdown("<h4>Niveau d'émotion</h4>", unsafe_allow_html=True)
                    emotion_value = entry.get("emotions", 5)
                    if emotion_value <= 3:
                        emotion_color = "🔴"
                    elif emotion_value <= 7:
                        emotion_color = "🟡"
                    else:
                        emotion_color = "🟢"
                    
                    st.markdown(f"{emotion_color} {emotion_value}/10")
                    
                    # Boutons d'action
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏️ Modifier cette entrée", key=f"edit_{i}"):
                            st.session_state["editing_entry"] = i
                    with col2:
                        if st.button("🗑️ Supprimer cette entrée", key=f"delete_{i}"):
                            if st.session_state.get("confirm_delete") == i:
                                journal_entries.pop(i)
                                save_data(journal_entries, journal_file)
                                st.success("Entrée supprimée !")
                                st.rerun()
                            else:
                                st.session_state["confirm_delete"] = i
                                st.warning("Cliquez à nouveau pour confirmer la suppression.")

# Page de suivi des candidatures
elif page == "📊 Suivi des Candidatures":
    st.markdown("<h1 class='main-title'>Suivi de mes Candidatures</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Nouvelle candidature", "📋 Liste des candidatures"])
    
    with tab1:
        with st.form("job_application_form"):
            st.markdown("<h2 class='section-title'>Ajouter une nouvelle candidature</h2>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                entreprise = st.text_input("Entreprise")
                poste = st.text_input("Intitulé du poste")
                date_candidature = st.date_input("Date de candidature", datetime.now().date())
                
            with col2:
                lieu = st.text_input("Lieu (ville)")
                type_contrat = st.selectbox("Type de contrat", 
                                          ["CDI", "CDD", "Stage", "Alternance", "Freelance", "Intérim", "Autre"])
                source = st.selectbox("Source de l'offre", 
                                    ["LinkedIn", "Indeed", "Pôle Emploi", "Site entreprise", "Réseau", "Autre"])
            
            lien_offre = st.text_input("Lien vers l'offre (optionnel)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                contact_nom = st.text_input("Nom du contact (optionnel)")
                contact_email = st.text_input("Email du contact (optionnel)")
            
            with col2:
                statut = st.selectbox("Statut de la candidature", 
                                    ["Préparation", "Envoyée", "Relance", "Entretien planifié", "En attente", "Offre reçue", "Refusé", "Abandonné"])
                salaire = st.text_input("Salaire proposé (optionnel)")
            
            notes = st.text_area("Notes", placeholder="Informations importantes, documents envoyés, préparation nécessaire...")
            
            soumettre_candidature = st.form_submit_button("Enregistrer cette candidature")
            
            if soumettre_candidature:
                if entreprise and poste:
                    nouvelle_candidature = {
                        "entreprise": entreprise,
                        "poste": poste,
                        "date_candidature": date_candidature.strftime("%d/%m/%Y"),
                        "lieu": lieu,
                        "type_contrat": type_contrat,
                        "source": source,
                        "lien_offre": lien_offre,
                        "contact_nom": contact_nom,
                        "contact_email": contact_email,
                        "statut": statut,
                        "salaire": salaire,
                        "notes": notes,
                        "historique": [{
                            "date": date_candidature.strftime("%d/%m/%Y"),
                            "statut": statut,
                            "commentaire": f"Candidature {statut.lower()}"
                        }]
                    }
                    
                    job_applications.append(nouvelle_candidature)
                    save_data(job_applications, applications_file)
                    st.success("Candidature ajoutée avec succès !")
                else:
                    st.error("Veuillez au moins renseigner l'entreprise et le poste.")
    
    with tab2:
        st.markdown("<h2 class='section-title'>Mes candidatures</h2>", unsafe_allow_html=True)
        
        if not job_applications:
            st.info("Vous n'avez pas encore enregistré de candidatures. Commencez par en ajouter une !")
        else:
            # Filtres et recherche
            col1, col2, col3 = st.columns(3)
            
            with col1:
                statut_filter = st.multiselect(
                    "Filtrer par statut",
                    list(set(app.get("statut", "Inconnu") for app in job_applications)),
                    []
                )
            
            with col2:
                search_term = st.text_input("Rechercher une entreprise ou un poste")
            
            with col3:
                sort_by = st.selectbox(
                    "Trier par",
                    ["Date (récent → ancien)", "Date (ancien → récent)", "Entreprise (A → Z)", "Statut"]
                )
            
            # Application des filtres
            filtered_apps = job_applications
            
            if statut_filter:
                filtered_apps = [app for app in filtered_apps if app.get("statut") in statut_filter]
            
            if search_term:
                filtered_apps = [app for app in filtered_apps if 
                               search_term.lower() in app.get("entreprise", "").lower() or 
                               search_term.lower() in app.get("poste", "").lower()]
            
            # Tri
            if sort_by == "Date (récent → ancien)":
                filtered_apps = sorted(filtered_apps, 
                                     key=lambda x: datetime.strptime(x.get("date_candidature", "01/01/2000"), "%d/%m/%Y"), 
                                     reverse=True)
            elif sort_by == "Date (ancien → récent)":
                filtered_apps = sorted(filtered_apps, 
                                     key=lambda x: datetime.strptime(x.get("date_candidature", "01/01/2000"), "%d/%m/%Y"))
            elif sort_by == "Entreprise (A → Z)":
                filtered_apps = sorted(filtered_apps, key=lambda x: x.get("entreprise", "").lower())
            elif sort_by == "Statut":
                status_order = {
                    "Préparation": 0,
                    "Envoyée": 1,
                    "Relance": 2,
                    "Entretien planifié": 3,
                    "En attente": 4,
                    "Offre reçue": 5,
                    "Refusé": 6,
                    "Abandonné": 7
                }
                filtered_apps = sorted(filtered_apps, key=lambda x: status_order.get(x.get("statut"), 99))
            
            # Résumé
            st.markdown(f"**{len(filtered_apps)}** candidature(s) affichée(s) sur un total de **{len(job_applications)}**")
            
            # Statistiques des candidatures
            if job_applications:
                st.markdown("<h3 class='subsection-title'>Statistiques de candidatures</h3>", unsafe_allow_html=True)
                
                statut_counts = {}
                for app in job_applications:
                    status = app.get("statut", "Inconnu")
                    statut_counts[status] = statut_counts.get(status, 0) + 1
                
                chart_data = pd.DataFrame({
                    "Statut": list(statut_counts.keys()),
                    "Nombre": list(statut_counts.values())
                })
                
                fig = px.pie(chart_data, values="Nombre", names="Statut", hole=0.4)
                fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
                st.plotly_chart(fig, use_container_width=True)
            
            # Liste des candidatures
            st.markdown("<h3 class='subsection-title'>Liste des candidatures</h3>", unsafe_allow_html=True)
            
            for i, app in enumerate(filtered_apps):
                status_color = {
                    "Préparation": "#AED6F1",  # Bleu clair
                    "Envoyée": "#D4E6F1",      # Bleu très clair
                    "Relance": "#A9CCE3",      # Bleu-gris
                    "Entretien planifié": "#A3E4D7",  # Vert clair
                    "En attente": "#FAD7A0",   # Orange clair
                    "Offre reçue": "#ABEBC6",  # Vert
                    "Refusé": "#F5B7B1",       # Rouge clair
                    "Abandonné": "#D7DBDD"     # Gris
                }
                
                color = status_color.get(app.get("statut", ""), "#F5F5F5")
                
                st.markdown(f"""
                <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0;">{app.get('poste', 'Poste inconnu')} - {app.get('entreprise', 'Entreprise inconnue')}</h4>
                            <p style="margin: 0; font-size: 0.9em;">
                                {app.get('date_candidature', '')} | {app.get('lieu', 'Lieu non spécifié')} | {app.get('type_contrat', 'Type non spécifié')}
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <strong>{app.get('statut', 'Statut inconnu')}</strong>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Voir les détails"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Poste:** {app.get('poste', '')}")
                        st.markdown(f"**Entreprise:** {app.get('entreprise', '')}")
                        st.markdown(f"**Lieu:** {app.get('lieu', '')}")
                        st.markdown(f"**Type de contrat:** {app.get('type_contrat', '')}")
                        if app.get('salaire'):
                            st.markdown(f"**Salaire:** {app.get('salaire', '')}")
                    
                    with col2:
                        st.markdown(f"**Date de candidature:** {app.get('date_candidature', '')}")
                        st.markdown(f"**Statut actuel:** {app.get('statut', '')}")
                        st.markdown(f"**Source de l'offre:** {app.get('source', '')}")
                        if app.get('contact_nom'):
                            st.markdown(f"**Contact:** {app.get('contact_nom', '')} ({app.get('contact_email', '')})")
                    
                    if app.get('lien_offre'):
                        st.markdown(f"**Lien vers l'offre:** [{app.get('lien_offre', '')}]({app.get('lien_offre', '')})")
                    
                    if app.get('notes'):
                        st.markdown("**Notes:**")
                        st.markdown(app.get('notes', ''))
                    
                    # Historique de la candidature
                    st.markdown("### Historique")
                    
                    historique = app.get('historique', [])
                    if historique:
                        for event in historique:
                            st.markdown(f"**{event.get('date', '')} - {event.get('statut', '')}**: {event.get('commentaire', '')}")
                    
                    # Mise à jour du statut
                    st.markdown("### Mettre à jour le statut")
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        nouveau_statut = st.selectbox(
                            "Nouveau statut",
                            ["Préparation", "Envoyée", "Relance", "Entretien planifié", "En attente", "Offre reçue", "Refusé", "Abandonné"],
                            index=["Préparation", "Envoyée", "Relance", "Entretien planifié", "En attente", "Offre reçue", "Refusé", "Abandonné"].index(app.get("statut", "Envoyée")),
                            key=f"status_select_{i}"
                        )
                        commentaire = st.text_input("Commentaire (optionnel)", key=f"comment_{i}")
                    
                    with col2:
                        if st.button("Mettre à jour", key=f"update_status_{i}"):
                            job_applications[i]["statut"] = nouveau_statut
                            
                            if "historique" not in job_applications[i]:
                                job_applications[i]["historique"] = []
                            
                            job_applications[i]["historique"].append({
                                "date": datetime.now().strftime("%d/%m/%Y"),
                                "statut": nouveau_statut,
                                "commentaire": commentaire if commentaire else f"Statut mis à jour à '{nouveau_statut}'"
                            })
                            
                            save_data(job_applications, applications_file)
                            st.success("Statut mis à jour avec succès !")
                            st.rerun()
                    
                    # Supprimer la candidature
                    if st.button("🗑️ Supprimer cette candidature", key=f"delete_app_{i}"):
                        if st.session_state.get("confirm_delete_app") == i:
                            job_applications.pop(i)
                            save_data(job_applications, applications_file)
                            st.success("Candidature supprimée !")
                            st.rerun()
                        else:
                            st.session_state["confirm_delete_app"] = i
                            st.warning("Cliquez à nouveau pour confirmer la suppression.")
                    
                    # Créer une entrée de journal basée sur cette candidature
                    if st.button("📝 Créer une entrée dans le journal", key=f"journal_from_app_{i}"):
                        st.session_state["create_journal_from_app"] = {
                            "titre": f"Candidature: {app.get('poste')} chez {app.get('entreprise')}",
                            "categorie": "Candidature",
                            "contenu": f"J'ai candidaté pour le poste de {app.get('poste')} chez {app.get('entreprise')} ({app.get('lieu')}). " +
                                    f"Type de contrat: {app.get('type_contrat')}. " +
                                    f"Statut actuel: {app.get('statut')}."
                        }
                        st.info("Une nouvelle entrée de journal a été préremplie. Veuillez aller dans l'onglet 'Journal d'Apprentissage'.")

# Page de progression des compétences
elif page == "🧠 Progression des Compétences":
    st.markdown("<h1 class='main-title'>Progression de mes Compétences</h1>", unsafe_allow_html=True)
    
    # Structure des compétences
    competences_structure = {
        "cv": {
            "nom": "CV et profil", 
            "description": "Capacité à créer et optimiser un CV et des profils professionnels en ligne",
            "sous_competences": ["Format et mise en page", "Contenu pertinent", "Optimisation SEO", "Portfolio en ligne"]
        },
        "lettre_motivation": {
            "nom": "Lettre de motivation", 
            "description": "Aptitude à rédiger une lettre de motivation personnalisée et convaincante",
            "sous_competences": ["Structure claire", "Contenu ciblé", "Accroche efficace", "Relecture et correction"]
        },
        "recherche_offres": {
            "nom": "Recherche d'offres", 
            "description": "Capacité à identifier et filtrer efficacement les offres d'emploi pertinentes",
            "sous_competences": ["Utilisation des jobboards", "Veille d'emploi", "Recherche avancée", "Analyse d'offres"]
        },
        "reseautage": {
            "nom": "Réseautage", 
            "description": "Aptitude à développer et utiliser son réseau professionnel",
            "sous_competences": ["Profil LinkedIn optimisé", "Prise de contact", "Suivi de relations", "Participation événements"]
        },
        "preparation_entretien": {
            "nom": "Préparation aux entretiens", 
            "description": "Capacité à se préparer et réussir les entretiens d'embauche",
            "sous_competences": ["Recherche sur l'entreprise", "Questions fréquentes", "Mise en situation", "Questions à poser"]
        },
        "communication": {
            "nom": "Communication", 
            "description": "Aptitude à communiquer efficacement à l'écrit et à l'oral",
            "sous_competences": ["Expression orale", "Expression écrite", "Posture et gestuelle", "Écoute active"]
        },
        "competences_techniques": {
            "nom": "Compétences techniques", 
            "description": "Maîtrise des compétences techniques spécifiques à votre domaine",
            "sous_competences": ["Compétences clés du métier", "Logiciels spécifiques", "Formation continue", "Veille technologique"]
        }
    }
    
    tab1, tab2 = st.tabs(["📊 Vue d'ensemble", "📈 Évaluation détaillée"])
    
    with tab1:
        st.markdown("<h2 class='section-title'>Vue d'ensemble de mes compétences</h2>", unsafe_allow_html=True)
        
        # Graphique radar des compétences
        categories = []
        values = []
        
        for key, data in competences_structure.items():
            categories.append(data["nom"])
            values.append(skills_data.get(key, {}).get("niveau", 0))
        
        # Création du graphique radar
        fig = px.line_polar(
            r=values,
            theta=categories,
            line_close=True,
            range_r=[0, 5],
            markers=True
        )
        fig.update_traces(fill='toself')
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tableau récapitulatif
        st.markdown("<h3 class='subsection-title'>Résumé des compétences</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Points forts")
            # Identifiez les 3 meilleures compétences
            top_skills = sorted([(key, skills_data.get(key, {}).get("niveau", 0)) for key in competences_structure.keys()], 
                             key=lambda x: x[1], reverse=True)[:3]
            
            for key, value in top_skills:
                if value > 0:
                    st.markdown(f"- {competences_structure[key]['nom']}: **{value}/5**")
        
        with col2:
            st.markdown("#### À améliorer")
            # Identifiez les 3 compétences les plus faibles
            weak_skills = sorted([(key, skills_data.get(key, {}).get("niveau", 0)) for key in competences_structure.keys()], 
                             key=lambda x: x[1])[:3]
            
            for key, value in weak_skills:
                st.markdown(f"- {competences_structure[key]['nom']}: **{value}/5**")
        
        with col3:
            st.markdown("#### Progression récente")
            # Identifiez les compétences avec des entrées récentes dans le log
            recent_progress = []
            for key, data in skills_data.items():
                if "log" in data and data["log"]:
                    # Trier les entrées par date (en supposant un format DD/MM/YYYY)
                    sorted_logs = sorted(data["log"], 
                                     key=lambda x: datetime.strptime(x.get("date", "01/01/2000"), "%d/%m/%Y"),
                                     reverse=True)
                    if sorted_logs:
                        recent_progress.append((key, sorted_logs[0]["date"]))
            
            # Prendre les 3 plus récentes
            recent_progress = sorted(recent_progress, 
                                   key=lambda x: datetime.strptime(x[1], "%d/%m/%Y"), 
                                   reverse=True)[:3]
            
            for key, date in recent_progress:
                st.markdown(f"- {competences_structure[key]['nom']} ({date})")
        
        # Conseils personnalisés
        st.markdown("<h3 class='subsection-title'>Conseils personnalisés</h3>", unsafe_allow_html=True)
        
        st.markdown("<div class='tip-box'>", unsafe_allow_html=True)
        
        lowest_skill_key = min(skills_data.keys(), key=lambda k: skills_data[k]["niveau"])
        lowest_skill = competences_structure[lowest_skill_key]["nom"]
        
        conseils = {
            "cv": [
                "Utilisez un modèle de CV moderne et adapté à votre secteur d'activité.",
                "Quantifiez vos réalisations avec des chiffres précis.",
                "Faites relire votre CV par un professionnel ou un ami du secteur.",
                "Adaptez votre CV à chaque offre en mettant en avant les compétences pertinentes."
            ],
            "lettre_motivation": [
                "Personnalisez chaque lettre en mentionnant l'entreprise et le poste.",
                "Structurez votre lettre en 3 parties : accroche, argumentaire, conclusion.",
                "Mettez en évidence l'adéquation entre votre profil et les besoins de l'entreprise.",
                "Relisez-vous pour éliminer les fautes et les phrases trop longues."
            ],
            "recherche_offres": [
                "Créez des alertes sur plusieurs plateformes d'emploi.",
                "Utilisez les filtres avancés pour affiner vos recherches.",
                "Consultez les sites de recrutement spécialisés dans votre domaine.",
                "N'hésitez pas à consulter directement les sites carrières des entreprises qui vous intéressent."
            ],
            "reseautage": [
                "Optimisez votre profil LinkedIn avec un résumé percutant et une photo professionnelle.",
                "Participez à des événements professionnels dans votre secteur.",
                "Contactez d'anciens camarades d'études ou collègues pour élargir votre réseau.",
                "Engagez la conversation avec des professionnels de votre secteur en commentant leurs publications."
            ],
            "preparation_entretien": [
                "Entraînez-vous avec des simulations d'entretien enregistrées en vidéo.",
                "Préparez des exemples concrets pour illustrer vos compétences.",
                "Renseignez-vous en profondeur sur l'entreprise avant l'entretien.",
                "Préparez des questions pertinentes à poser au recruteur."
            ],
            "communication": [
                "Enregistrez-vous pour améliorer votre élocution et votre posture.",
                "Pratiquez la méthode STAR pour structurer vos réponses (Situation, Tâche, Action, Résultat).",
                "Demandez des retours constructifs après des présentations.",
                "Travaillez votre langage corporel et votre contact visuel."
            ],
            "competences_techniques": [
                "Identifiez les compétences techniques les plus demandées dans votre secteur.",
                "Suivez des formations en ligne pour combler vos lacunes.",
                "Pratiquez régulièrement ces compétences dans des projets personnels.",
                "Obtenez des certifications reconnues dans votre domaine."
            ]
        }
        
        conseil_choisi = random.choice(conseils[lowest_skill_key])
        
        st.markdown(f"""
        <h4>Pour améliorer votre compétence '{lowest_skill}' :</h4>
        <p>{conseil_choisi}</p>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<h2 class='section-title'>Évaluer mes compétences</h2>", unsafe_allow_html=True)
        
        for skill_key, skill_info in competences_structure.items():
            with st.expander(f"{skill_info['nom']} - Niveau actuel: {skills_data.get(skill_key, {}).get('niveau', 0)}/5"):
                st.markdown(f"**Description:** {skill_info['description']}")
                
                st.markdown("**Sous-compétences:**")
                for sous_comp in skill_info['sous_competences']:
                    st.markdown(f"- {sous_comp}")
                
                # Afficher l'historique des évaluations
                if skills_data.get(skill_key, {}).get("log"):
                    st.markdown("**Historique des évaluations:**")
                    for log in sorted(skills_data[skill_key]["log"], 
                                     key=lambda x: datetime.strptime(x.get("date", "01/01/2000"), "%d/%m/%Y"),
                                     reverse=True):
                        st.markdown(f"- **{log.get('date')}**: {log.get('note')}")
                
                # Permettre à l'utilisateur de s'auto-évaluer
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    new_level = st.slider(
                        f"Évaluez votre niveau en {skill_info['nom']}",
                        0.0, 5.0, skills_data.get(skill_key, {}).get("niveau", 0.0),
                        0.5,
                        key=f"slider_{skill_key}"
                    )
                    note = st.text_input("Note (optionnelle)", key=f"note_{skill_key}")
                
                with col2:
                    if st.button("Enregistrer", key=f"save_{skill_key}"):
                        # S'assurer que la structure existe
                        if skill_key not in skills_data:
                            skills_data[skill_key] = {"niveau": 0, "log": []}
                        
                        # Mettre à jour le niveau
                        skills_data[skill_key]["niveau"] = new_level
                        
                        # Ajouter au journal si le niveau a changé ou si une note est fournie
                        current_level = skills_data.get(skill_key, {}).get("niveau", 0)
                        if new_level != current_level or note:
                            skills_data[skill_key]["log"].append({
                                "date": datetime.now().strftime("%d/%m/%Y"),
                                "note": note if note else f"Niveau mis à jour: {current_level} → {new_level}"
                            })
                        
                        save_data(skills_data, skills_file)
                        st.success(f"Niveau de compétence '{skill_info['nom']}' mis à jour !")
                        st.rerun()

# Page des objectifs et plans d'action
elif page == "🏆 Objectifs et Plans d'Action":
    st.markdown("<h1 class='main-title'>Mes Objectifs et Plans d'Action</h1>", unsafe_allow_html=True)
    
    # Fichier pour stocker les objectifs
    objectives_file = "objectives_data.json"
    objectives_data = load_data(objectives_file)
    
    # Convertir en liste si nécessaire
    if not isinstance(objectives_data, list):
        objectives_data = []
    
    tab1, tab2 = st.tabs(["🎯 Mes objectifs", "📅 Planifier un nouvel objectif"])
    
    with tab1:
        st.markdown("<h2 class='section-title'>Mes objectifs actuels</h2>", unsafe_allow_html=True)
        
        if not objectives_data:
            st.info("Vous n'avez pas encore défini d'objectifs. Utilisez l'onglet 'Planifier un nouvel objectif' pour commencer.")
        else:
            # Filtrer les objectifs
            statut_filter = st.multiselect(
                "Filtrer par statut",
                ["En cours", "Accompli", "En retard", "Abandonné"],
                ["En cours"]
            )
            
            filtered_objectives = objectives_data
            if statut_filter:
                filtered_objectives = [obj for obj in objectives_data if obj.get("statut") in statut_filter]
            
            # Afficher les objectifs
            for i, objective in enumerate(filtered_objectives):
                status_color = {
                    "En cours": "#A3E4D7",     # Vert clair
                    "Accompli": "#ABEBC6",     # Vert
                    "En retard": "#F5B7B1",    # Rouge clair
                    "Abandonné": "#D7DBDD"     # Gris
                }
                
                color = status_color.get(objective.get("statut", "En cours"), "#F5F5F5")
                
                # Calculer la progression
                etapes = objective.get("etapes", [])
                etapes_completees = sum(1 for etape in etapes if etape.get("accompli", False))
                progression = 0
                if etapes:
                    progression = etapes_completees / len(etapes)
                
                st.markdown(f"""
                <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0;">{objective.get('titre', 'Objectif sans titre')}</h4>
                            <p style="margin: 0; font-size: 0.9em;">
                                Échéance: {objective.get('echeance', 'Non spécifiée')} | 
                                Priorité: {objective.get('priorite', 'Normale')} | 
                                Statut: {objective.get('statut', 'En cours')}
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <div>Progression: {int(progression * 100)}%</div>
                        </div>
                    </div>
                    <div style="margin-top: 8px; width: 100%; background-color: #E8E8E8; height: 8px; border-radius: 4px;">
                        <div style="width: {int(progression * 100)}%; background-color: #3498DB; height: 8px; border-radius: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Voir les détails"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Objectif:** {objective.get('titre', '')}")
                        st.markdown(f"**Description:** {objective.get('description', '')}")
                        st.markdown(f"**Catégorie:** {objective.get('categorie', '')}")
                    
                    with col2:
                        st.markdown(f"**Échéance:** {objective.get('echeance', '')}")
                        st.markdown(f"**Priorité:** {objective.get('priorite', '')}")
                        st.markdown(f"**Statut:** {objective.get('statut', '')}")
                    
                    # Compétences liées
                    competences_liees = objective.get('competences_liees', [])
                    if competences_liees:
                        st.markdown("**Compétences liées:**")
                        for comp in competences_liees:
                            st.markdown(f"- {competences_structure.get(comp, {}).get('nom', comp)}")
                    
                    # Plan d'action / Étapes
                    st.markdown("### Plan d'action")
                    
                    etapes = objective.get("etapes", [])
                    for j, etape in enumerate(etapes):
                        col1, col2 = st.columns([5, 1])
                        with col1:
                            accomplished = st.checkbox(
                                f"{etape.get('description', 'Étape non définie')}",
                                value=etape.get("accompli", False),
                                key=f"step_{i}_{j}"
                            )
                        
                        # Mettre à jour l'état de complétion de l'étape
                        if accomplished != etape.get("accompli", False):
                            objectives_data[i]["etapes"][j]["accompli"] = accomplished
                            save_data(objectives_data, objectives_file)
                            st.rerun()
                    
                    # Mise à jour du statut
                    st.markdown("### Mettre à jour le statut")
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        nouveau_statut = st.selectbox(
                            "Nouveau statut",
                            ["En cours", "Accompli", "En retard", "Abandonné"],
                            index=["En cours", "Accompli", "En retard", "Abandonné"].index(objective.get("statut", "En cours")),
                            key=f"status_select_obj_{i}"
                        )
                    
                    with col2:
                        if st.button("Mettre à jour", key=f"update_status_obj_{i}"):
                            objectives_data[i]["statut"] = nouveau_statut
                            save_data(objectives_data, objectives_file)
                            st.success("Statut mis à jour avec succès !")
                            st.rerun()
                    
                    # Supprimer l'objectif
                    if st.button("🗑️ Supprimer cet objectif", key=f"delete_obj_{i}"):
                        if st.session_state.get("confirm_delete_obj") == i:
                            objectives_data.pop(i)
                            save_data(objectives_data, objectives_file)
                            st.success("Objectif supprimé !")
                            st.rerun()
                        else:
                            st.session_state["confirm_delete_obj"] = i
                            st.warning("Cliquez à nouveau pour confirmer la suppression.")
            
            # Graphique de progression
            st.markdown("<h3 class='subsection-title'>Progression globale des objectifs</h3>", unsafe_allow_html=True)
            
            statuts = {"En cours": 0, "Accompli": 0, "En retard": 0, "Abandonné": 0}
            for obj in objectives_data:
                statut = obj.get("statut", "En cours")
                statuts[statut] = statuts.get(statut, 0) + 1
            
            chart_data = pd.DataFrame({
                "Statut": list(statuts.keys()),
                "Nombre": list(statuts.values())
            })
            
            fig = px.bar(
                chart_data, 
                x="Statut", 
                y="Nombre",
                color="Statut",
                color_discrete_map={
                    "En cours": "#A3E4D7",
                    "Accompli": "#ABEBC6",
                    "En retard": "#F5B7B1",
                    "Abandonné": "#D7DBDD"
                }
            )
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("<h2 class='section-title'>Définir un nouvel objectif</h2>", unsafe_allow_html=True)
        
        with st.form("new_objective_form"):
            st.markdown("<h3 class='subsection-title'>Informations générales</h3>", unsafe_allow_html=True)
            
            titre = st.text_input("Titre de l'objectif")
            description = st.text_area("Description détaillée", placeholder="Décrivez précisément ce que vous souhaitez accomplir...")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                categorie = st.selectbox(
                    "Catégorie",
                    ["Recherche d'emploi", "Compétence à développer", "Formation", "Réseau", "Préparation entretien", "Autre"]
                )
            
            with col2:
                echeance = st.date_input("Date d'échéance", datetime.now().date() + pd.Timedelta(days=30))
            
            with col3:
                priorite = st.selectbox(
                    "Priorité",
                    ["Basse", "Normale", "Haute", "Urgente"]
                )
            
            # Compétences liées
            st.markdown("<h3 class='subsection-title'>Compétences liées</h3>", unsafe_allow_html=True)
            
            competences_options = {key: data["nom"] for key, data in competences_structure.items()}
            competences_liees = st.multiselect(
                "Compétences concernées par cet objectif",
                options=list(competences_options.keys()),
                format_func=lambda x: competences_options[x]
            )
            
            # Plan d'action / Étapes
            st.markdown("<h3 class='subsection-title'>Plan d'action</h3>", unsafe_allow_html=True)
            
            etapes = []
            for i in range(5):  # Par défaut, 5 champs pour les étapes
                etape = st.text_input(f"Étape {i+1}", key=f"etape_{i}")
                if etape:
                    etapes.append({"description": etape, "accompli": False})
            
            # Ressources nécessaires
            ressources = st.text_area("Ressources nécessaires", placeholder="Livres, outils, personnes, formations...")
            
            submit_objective = st.form_submit_button("Enregistrer cet objectif")
            
            if submit_objective:
                if titre and description and etapes:
                    nouvel_objectif = {
                        "titre": titre,
                        "description": description,
                        "categorie": categorie,
                        "echeance": echeance.strftime("%d/%m/%Y"),
                        "priorite": priorite,
                        "statut": "En cours",
                        "competences_liees": competences_liees,
                        "etapes": etapes,
                        "ressources": ressources,
                        "date_creation": datetime.now().strftime("%d/%m/%Y")
                    }
                    
                    objectives_data.append(nouvel_objectif)
                    save_data(objectives_data, objectives_file)
                    st.success("Objectif ajouté avec succès !")
                    
                    # Mettre à jour les compétences liées
                    update_skills = False
                    for comp in competences_liees:
                        if comp in skills_data:
                            skills_data[comp]["log"].append({
                                "date": datetime.now().strftime("%d/%m/%Y"),
                                "note": f"Nouvel objectif associé: '{titre}'"
                            })
                            update_skills = True
                    
                    if update_skills:
                        save_data(skills_data, skills_file)
                else:
                    st.error("Veuillez remplir au minimum le titre, la description et au moins une étape.")

# Page des ressources utiles
elif page == "🛠️ Ressources Utiles":
    st.markdown("<h1 class='main-title'>Ressources Utiles</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h2 class='section-title'>Outils pour la recherche d'emploi</h2>", unsafe_allow_html=True)
        
        with st.expander("🔍 Sites d'offres d'emploi", expanded=True):
            st.markdown("""
            - **LinkedIn Jobs** - [linkedin.com/jobs](https://www.linkedin.com/jobs/)
            - **Indeed** - [indeed.fr](https://www.indeed.fr/)
            - **Pôle Emploi** - [pole-emploi.fr](https://www.pole-emploi.fr/)
            - **Welcome to the Jungle** - [welcometothejungle.com](https://www.welcometothejungle.com/)
            - **RegionsJob** - [regionsjob.com](https://www.regionsjob.com/)
            - **APEC** - [apec.fr](https://www.apec.fr/) (pour les cadres)
            """)
        
        with st.expander("📝 Création de CV"):
            st.markdown("""
            - **Canva** - [canva.com](https://www.canva.com/) (modèles de CV modernes)
            - **Zety** - [zety.fr](https://zety.fr/) (générateur de CV avec conseils)
            - **Enhancv** - [enhancv.com](https://enhancv.com/) (CV personnalisés et innovants)
            - **Novoresume** - [novoresume.com](https://novoresume.com/) (CV optimisés pour ATS)
            - **Resume.io** - [resume.io](https://resume.io/) (interface simple et efficace)
            """)
        
        with st.expander("🌐 Réseautage professionnel"):
            st.markdown("""
            - **LinkedIn** - [linkedin.com](https://www.linkedin.com/) (le réseau professionnel incontournable)
            - **Meetup** - [meetup.com](https://www.meetup.com/) (événements professionnels locaux)
            - **Shapr** - Application mobile (networking professionnel en mode swipe)
            - **Slack Communities** - Recherchez des communautés dans votre secteur
            - **Discord** - Serveurs professionnels spécialisés dans votre domaine
            """)
        
        with st.expander("🎯 Préparation aux entretiens"):
            st.markdown("""
            - **Glassdoor** - [glassdoor.fr](https://www.glassdoor.fr/) (avis sur les entreprises et questions d'entretien)
            - **Pramp** - [pramp.com](https://www.pramp.com/) (entretiens d'embauche simulés)
            - **Big Interview** - [biginterview.com](https://biginterview.com/) (plateforme d'entraînement aux entretiens)
            - **Interview Warmup (Google)** - [grow.google/interview-warmup](https://grow.google/interview-warmup/)
            - **MockQuestions** - [mockquestions.com](https://www.mockquestions.com/) (banque de questions par secteur)
            """)
    
    with col2:
        st.markdown("<h2 class='section-title'>Guides et ressources pédagogiques</h2>", unsafe_allow_html=True)
        
        with st.expander("📊 Tests et bilans de compétences", expanded=True):
            st.markdown("""
            - **123test** - [123test.fr](https://www.123test.fr/) (tests de personnalité et d'orientation)
            - **Clearer Thinking** - [clearerthinking.org](https://www.clearerthinking.org/) (tests de compétences et de carrière)
            - **16Personalities** - [16personalities.com](https://www.16personalities.com/) (test MBTI pour mieux se connaître)
            - **StrengthsFinder** - [gallup.com/cliftonstrengths](https://www.gallup.com/cliftonstrengths/) (outil payant pour identifier vos forces)
            """)
        
        with st.expander("📚 Développement de compétences"):
            st.markdown("""
            - **Coursera** - [coursera.org](https://www.coursera.org/) (cours en ligne de grandes universités)
            - **OpenClassrooms** - [openclassrooms.com](https://openclassrooms.com/) (formations certifiantes)
            - **LinkedIn Learning** - [linkedin.com/learning](https://www.linkedin.com/learning/) (cours vidéo professionnels)
            - **YouTube** - Chaînes spécialisées dans votre domaine
            - **Google Digital Garage** - [learndigital.withgoogle.com](https://learndigital.withgoogle.com/) (compétences numériques)
            """)
        
        with st.expander("📖 Guides pratiques"):
            st.markdown("""
            - **Guide de recherche d'emploi** - [PDF téléchargeable](https://www.pole-emploi.fr/candidat/vos-recherches/preparer-votre-candidature/le-guide-pratique-de-recherche-de.html)
            - **Guide des entretiens d'embauche** - [PDF téléchargeable](https://www.apec.fr/files/live/sites/apec/files/media-kit/2020/Reussir%20ses%20entretiens%20de%20recrutement.pdf)
            - **Harvard Guide to Resume Writing** - [PDF téléchargeable](https://cdn-careerservices.fas.harvard.edu/wp-content/uploads/sites/161/2019/11/13163213/College-Guide-to-Resume-Writing-2019-20.pdf)
            - **Techniques de réseautage** - [Article](https://www.welcome-to-the-jungle.com/fr/articles/guide-pratique-reseautage-professionnel/)
            """)
        
        with st.expander("💼 Modèles et exemples"):
            st.markdown("""
            - **Exemples de CV par secteur** - [Consulter](https://www.cadremploi.fr/editorial/conseils/conseils-candidature/cv-par-secteur)
            - **Modèles de lettres de motivation** - [Consulter](https://www.monster.fr/conseil-carriere/article/exemple-lettre-motivation-par-metier)
            - **Exemples de questions/réponses d'entretien** - [Consulter](https://www.indeed.fr/conseils-carriere/entretiens/questions-entretien-embauche)
            - **Exemples d'emails de suivi post-entretien** - [Consulter](https://www.welcometothejungle.com/fr/articles/email-apres-entretien-embauche)
            """)
        
        # Conseils quotidiens
        st.markdown("<h2 class='section-title'>Conseil du jour</h2>", unsafe_allow_html=True)
        
        conseils_avances = [
            "Optimisez votre CV pour les ATS (systèmes de suivi des candidatures) en utilisant des mots-clés pertinents tirés de l'offre d'emploi.",
            "Avant un entretien, étudiez le parcours LinkedIn de votre recruteur pour trouver des points communs à mentionner.",
            "Utilisez la méthode STAR (Situation, Tâche, Action, Résultat) pour structurer vos réponses aux questions comportementales.",
            "Maintenez un tableau de bord de suivi de candidatures avec des rappels pour relancer après 7-10 jours sans réponse.",
            "Personnalisez votre pitch de présentation selon l'entreprise et le poste visé - une version unique ne suffit pas.",
            "Préparez 3-5 accomplissements clés quantifiés que vous pouvez mentionner à différents moments de l'entretien.",
            "Après un refus, demandez poliment un retour constructif au recruteur pour améliorer vos futures candidatures.",
            "Positionnez-vous comme apporteur de solutions plutôt que demandeur d'emploi lors des contacts avec les entreprises.",
            "Analysez la culture de l'entreprise via leurs réseaux sociaux pour adapter votre discours et votre tenue lors de l'entretien.",
            "Préparez une présentation de 2-3 minutes de vos réalisations professionnelles à l'aide d'un portfolio ou d'exemples concrets."
        ]
        
        st.markdown("<div class='tip-box'>", unsafe_allow_html=True)
        st.markdown(f"<p><em>{random.choice(conseils_avances)}</em></p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Téléchargements
        st.markdown("<h2 class='section-title'>Téléchargements utiles</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - 📝 [Checklist de préparation d'entretien](https://example.com)
            - 📊 [Modèle de suivi de candidatures (Excel)](https://example.com)
            """)
        
        with col2:
            st.markdown("""
            - 📋 [Questions à poser aux recruteurs](https://example.com)
            - 🗓️ [Plan d'action hebdomadaire](https://example.com)
            """)

if __name__ == "__main__":
    st.markdown("##### Développé pour accompagner les jeunes dans leur recherche d'emploi")
    st.markdown("Version 1.0 - 2025")