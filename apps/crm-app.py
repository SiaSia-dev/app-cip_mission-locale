import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import io
import os
import base64
import random

# Configuration de la page
st.set_page_config(
    page_title="CRM Relations Entreprises",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fonction pour charger les données (dans un environnement réel, cela viendrait d'une base de données)
@st.cache_data
def load_data():
    # Si les fichiers existent, on les charge
    if os.path.exists("entreprises.csv"):
        entreprises_df = pd.read_csv("entreprises.csv")
    else:
        # Sinon on crée des données de démonstration
        entreprises_data = {
            "id": list(range(1, 31)),
            "nom": [f"Entreprise {i}" for i in range(1, 31)],
            "secteur": np.random.choice(["Tech", "Industrie", "Services", "Commerce", "Finance"], 30),
            "taille": np.random.choice(["TPE (<10)", "PME (10-250)", "ETI (250-5000)", "GE (>5000)"], 30),
            "adresse": [f"Adresse {i}" for i in range(1, 31)],
            "ville": np.random.choice(["Paris", "Lyon", "Marseille", "Nantes", "Bordeaux", "Lille", "Toulouse"], 30),
            "code_postal": np.random.choice(["75000", "69000", "13000", "44000", "33000", "59000", "31000"], 30),
            "contact_principal": [f"Contact {i}" for i in range(1, 31)],
            "email": [f"contact{i}@entreprise{i}.com" for i in range(1, 31)],
            "telephone": [f"06{np.random.randint(10000000, 99999999)}" for _ in range(30)],
            "date_premier_contact": pd.date_range(start="2023-01-01", end="2023-12-31", periods=30).strftime('%Y-%m-%d').tolist(),
            "statut": np.random.choice(["Prospect", "En discussion", "Partenaire actif", "Partenaire inactif"], 30),
            "niveau_engagement": np.random.choice([1, 2, 3, 4, 5], 30),
            "offres_emploi_annuelles": np.random.randint(0, 15, 30),
            "stages_annuels": np.random.randint(0, 20, 30),
            "alternances_annuelles": np.random.randint(0, 10, 30),
            "dernier_contact": pd.date_range(start="2023-06-01", end="2024-03-01", periods=30).strftime('%Y-%m-%d').tolist(),
            "notes": ["" for _ in range(30)]
        }
        entreprises_df = pd.DataFrame(entreprises_data)
        entreprises_df.to_csv("entreprises.csv", index=False)
    
    if os.path.exists("interactions.csv"):
        interactions_df = pd.read_csv("interactions.csv")
    else:
        # Données de démonstration pour les interactions
        interactions_data = []
        for i in range(1, 101):
            entreprise_id = np.random.randint(1, 31)
            date = (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d')
            interactions_data.append({
                "id": i,
                "entreprise_id": entreprise_id,
                "entreprise_nom": f"Entreprise {entreprise_id}",
                "date": date,
                "type": np.random.choice(["Email", "Téléphone", "Réunion", "Événement", "Autre"]),
                "sujet": np.random.choice(["Prospection", "Suivi", "Offre d'emploi", "Stage", "Alternance", "Événement", "Feedback"]),
                "description": f"Description de l'interaction {i}",
                "resultat": np.random.choice(["Positif", "Neutre", "À suivre", "Négatif"]),
                "suivi_requis": np.random.choice([True, False]),
                "date_suivi": (datetime.now() + timedelta(days=np.random.randint(1, 30))).strftime('%Y-%m-%d') if np.random.choice([True, False]) else "",
            })
        interactions_df = pd.DataFrame(interactions_data)
        interactions_df.to_csv("interactions.csv", index=False)
    
    if os.path.exists("evenements.csv"):
        evenements_df = pd.read_csv("evenements.csv")
    else:
        # Données de démonstration pour les événements
        evenements_data = []
        for i in range(1, 21):
            date = (datetime.now() + timedelta(days=np.random.randint(-30, 180))).strftime('%Y-%m-%d')
            entreprises_participants = np.random.choice(range(1, 31), size=np.random.randint(1, 10), replace=False)
            entreprises_participants_str = ",".join(map(str, entreprises_participants))
            evenements_data.append({
                "id": i,
                "nom": f"Événement {i}",
                "type": np.random.choice(["Forum", "Workshop", "Conférence", "Petit-déjeuner", "Visite", "Autre"]),
                "date": date,
                "lieu": np.random.choice(["Nos locaux", "Locaux partenaire", "Lieu externe", "En ligne"]),
                "description": f"Description de l'événement {i}",
                "entreprises_participants": entreprises_participants_str,
                "nombre_participants": len(entreprises_participants),
                "statut": np.random.choice(["Planifié", "En préparation", "Terminé", "Annulé"]),
                "notes_bilan": "" if date > datetime.now().strftime('%Y-%m-%d') else f"Bilan de l'événement {i}"
            })
        evenements_df = pd.DataFrame(evenements_data)
        evenements_df.to_csv("evenements.csv", index=False)

    if os.path.exists("offres.csv"):
        offres_df = pd.read_csv("offres.csv")
    else:
        # Données de démonstration pour les offres
        offres_data = []
        for i in range(1, 51):
            entreprise_id = np.random.randint(1, 31)
            date_publication = (datetime.now() - timedelta(days=np.random.randint(0, 90))).strftime('%Y-%m-%d')
            offres_data.append({
                "id": i,
                "entreprise_id": entreprise_id,
                "entreprise_nom": f"Entreprise {entreprise_id}",
                "titre": f"Offre {i}",
                "type": np.random.choice(["Emploi", "Stage", "Alternance"]),
                "date_publication": date_publication,
                "date_expiration": (datetime.strptime(date_publication, '%Y-%m-%d') + timedelta(days=np.random.randint(30, 120))).strftime('%Y-%m-%d'),
                "description": f"Description de l'offre {i}",
                "compétences_requises": "Compétence 1, Compétence 2, Compétence 3",
                "localisation": np.random.choice(["Paris", "Lyon", "Marseille", "Nantes", "Bordeaux", "Lille", "Toulouse", "Télétravail"]),
                "statut": np.random.choice(["Active", "Pourvue", "Expirée"]),
                "candidatures": np.random.randint(0, 20),
                "candidatures_retenues": np.random.randint(0, 5)
            })
        offres_df = pd.DataFrame(offres_data)
        offres_df.to_csv("offres.csv", index=False)
    
    return entreprises_df, interactions_df, evenements_df, offres_df

# Fonction pour sauvegarder les données
def save_data(df, file_name):
    df.to_csv(file_name, index=False)

# Fonction pour télécharger un fichier
def get_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 {text}</a>'
    return href

# Fonction pour formater la date en français
def format_date_fr(date_str):
    if pd.isna(date_str) or date_str == "":
        return ""
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    month_names = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
    return f"{date_obj.day} {month_names[date_obj.month - 1]} {date_obj.year}"

# Fonction pour calculer les statistiques
def calculate_stats(entreprises_df, interactions_df, evenements_df, offres_df):
    stats = {}
    
    # Statistiques globales
    stats["total_entreprises"] = len(entreprises_df)
    stats["total_partenaires_actifs"] = len(entreprises_df[entreprises_df["statut"] == "Partenaire actif"])
    stats["total_prospects"] = len(entreprises_df[entreprises_df["statut"] == "Prospect"])
    stats["total_interactions"] = len(interactions_df)
    stats["total_evenements"] = len(evenements_df)
    stats["total_offres"] = len(offres_df)
    
    # Statistiques sur les offres
    stats["offres_emploi"] = len(offres_df[offres_df["type"] == "Emploi"])
    stats["offres_stage"] = len(offres_df[offres_df["type"] == "Stage"])
    stats["offres_alternance"] = len(offres_df[offres_df["type"] == "Alternance"])
    
    # Calcul du taux de conversion (prospects en partenaires)
    if stats["total_prospects"] + stats["total_partenaires_actifs"] > 0:
        stats["taux_conversion"] = (stats["total_partenaires_actifs"] / (stats["total_prospects"] + stats["total_partenaires_actifs"])) * 100
    else:
        stats["taux_conversion"] = 0
    
    # Interactions récentes (30 derniers jours)
    today = datetime.now()
    thirty_days_ago = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    stats["interactions_recentes"] = len(interactions_df[interactions_df["date"] >= thirty_days_ago])
    
    # Interactions par type
    interactions_par_type = interactions_df["type"].value_counts().to_dict()
    stats["interactions_par_type"] = interactions_par_type
    
    # Entreprises par secteur
    entreprises_par_secteur = entreprises_df["secteur"].value_counts().to_dict()
    stats["entreprises_par_secteur"] = entreprises_par_secteur
    
    # Offres par mois (6 derniers mois)
    offres_df["mois"] = pd.to_datetime(offres_df["date_publication"]).dt.strftime('%Y-%m')
    six_months_ago = (today - timedelta(days=180)).strftime('%Y-%m')
    offres_recentes = offres_df[pd.to_datetime(offres_df["date_publication"]).dt.strftime('%Y-%m') >= six_months_ago]
    offres_par_mois = offres_recentes.groupby("mois").size().to_dict()
    stats["offres_par_mois"] = offres_par_mois
    
    return stats

# Charger les données
entreprises_df, interactions_df, evenements_df, offres_df = load_data()

# Appliquer le style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #34495e;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .stat-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #3498db;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #7f8c8d;
    }
    .table-container {
        margin-top: 20px;
        margin-bottom: 30px;
        max-height: 500px;
        overflow-y: auto;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .action-button {
        width: 100%;
        margin-bottom: 10px;
    }
    .form-section {
        background-color: #f0f2f5;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 20px;
        color: #7f8c8d;
        font-size: 0.8rem;
    }
    .badge-prospect {
        background-color: #f39c12;
        color: white;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
    }
    .badge-actif {
        background-color: #2ecc71;
        color: white;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
    }
    .badge-inactif {
        background-color: #e74c3c;
        color: white;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
    }
    .badge-discussion {
        background-color: #3498db;
        color: white;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Barre latérale pour la navigation
with st.sidebar:
    st.image("./img/crm.jpg", width=150)
    st.markdown("<div class='sidebar-header'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio("", [
        "📊 Tableau de bord", 
        "🏢 Entreprises", 
        "💬 Interactions", 
        "📅 Événements",
        "📝 Offres",
        "📈 Analyse des données",
        "⚙️ Paramètres"
    ])
    
    st.markdown("---")
    st.markdown("<div class='sidebar-header'>Actions rapides</div>", unsafe_allow_html=True)
    
    quick_action = st.selectbox("", [
        "Ajouter une entreprise",
        "Enregistrer une interaction",
        "Planifier un événement",
        "Ajouter une offre"
    ])
    
    if st.button("Exécuter", key="quick_action_button"):
        if "Ajouter une entreprise" in quick_action:
            page = "🏢 Entreprises"
            st.session_state["show_add_company_form"] = True
        elif "Enregistrer une interaction" in quick_action:
            page = "💬 Interactions"
            st.session_state["show_add_interaction_form"] = True
        elif "Planifier un événement" in quick_action:
            page = "📅 Événements"
            st.session_state["show_add_event_form"] = True
        elif "Ajouter une offre" in quick_action:
            page = "📝 Offres"
            st.session_state["show_add_offer_form"] = True
    
    st.markdown("---")
    st.markdown("<div class='footer'>CRM Relations Entreprises v1.0<br>© 2025 Alexia Fontaine</div>", unsafe_allow_html=True)

# Page Tableau de bord
if page == "📊 Tableau de bord":
    st.markdown("<h1 class='main-header'>Tableau de bord CRM Relations Entreprises</h1>", unsafe_allow_html=True)
    
    # Calcul des statistiques
    stats = calculate_stats(entreprises_df, interactions_df, evenements_df, offres_df)
    
    # Affichage des statistiques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>{}</div>
            <div class='stat-label'>Entreprises partenaires</div>
        </div>
        """.format(stats["total_entreprises"]), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>{}</div>
            <div class='stat-label'>Interactions ce mois</div>
        </div>
        """.format(stats["interactions_recentes"]), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>{}</div>
            <div class='stat-label'>Offres actives</div>
        </div>
        """.format(len(offres_df[offres_df["statut"] == "Active"])), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>{:.1f}%</div>
            <div class='stat-label'>Taux de conversion</div>
        </div>
        """.format(stats["taux_conversion"]), unsafe_allow_html=True)
    
    # Graphiques
    st.markdown("<h2 class='sub-header'>Analyse des données</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Répartition des entreprises par secteur")
        fig = px.pie(
            values=list(stats["entreprises_par_secteur"].values()),
            names=list(stats["entreprises_par_secteur"].keys()),
            hole=0.4
        )
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Interactions par type")
        fig = px.bar(
            x=list(stats["interactions_par_type"].keys()),
            y=list(stats["interactions_par_type"].values()),
            color=list(stats["interactions_par_type"].keys()),
            labels={'x': 'Type', 'y': 'Nombre'}
        )
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Actions requises
    st.markdown("<h2 class='sub-header'>Actions requises</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Suivis à effectuer")
        
        # Filtrer les interactions qui nécessitent un suivi
        suivis = interactions_df[interactions_df["suivi_requis"] == True].sort_values(by="date_suivi")
        
        if len(suivis) > 0:
            for _, suivi in suivis.head(5).iterrows():
                st.markdown(f"""
                **{suivi['entreprise_nom']}** - {format_date_fr(suivi['date_suivi'])}  
                {suivi['sujet']} - {suivi['description'][:50]}...
                """)
            
            if len(suivis) > 5:
                st.info(f"+ {len(suivis) - 5} autres suivis à effectuer")
        else:
            st.info("Aucun suivi à effectuer pour le moment.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Événements à venir")
        
        # Filtrer les événements à venir
        today = datetime.now().strftime('%Y-%m-%d')
        evenements_a_venir = evenements_df[evenements_df["date"] >= today].sort_values(by="date")
        
        if len(evenements_a_venir) > 0:
            for _, event in evenements_a_venir.head(5).iterrows():
                st.markdown(f"""
                **{event['nom']}** - {format_date_fr(event['date'])}  
                {event['type']} - {event['lieu']} - {event['nombre_participants']} participants prévus
                """)
            
            if len(evenements_a_venir) > 5:
                st.info(f"+ {len(evenements_a_venir) - 5} autres événements à venir")
        else:
            st.info("Aucun événement à venir pour le moment.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Dernières activités
    st.markdown("<h2 class='sub-header'>Dernières activités</h2>", unsafe_allow_html=True)
    
    # Combiner les interactions et les événements pour afficher une timeline
    interactions_recentes = interactions_df.sort_values(by="date", ascending=False).head(10)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for _, interaction in interactions_recentes.iterrows():
        st.markdown(f"""
        **{format_date_fr(interaction['date'])}** - {interaction['entreprise_nom']}  
        {interaction['type']} - {interaction['sujet']} - Résultat: {interaction['resultat']}
        """)
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

# Page Entreprises
elif page == "🏢 Entreprises":
    st.markdown("<h1 class='main-header'>Gestion des Entreprises Partenaires</h1>", unsafe_allow_html=True)
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["Liste des entreprises", "Ajouter une entreprise", "Vue détaillée"])
    
    with tab1:
        # Filtres
        col1, col2, col3 = st.columns(3)
        with col1:
            secteur_filter = st.multiselect(
                "Secteur",
                options=sorted(entreprises_df["secteur"].unique()),
                default=[]
            )
        with col2:
            statut_filter = st.multiselect(
                "Statut",
                options=sorted(entreprises_df["statut"].unique()),
                default=[]
            )
        with col3:
            ville_filter = st.multiselect(
                "Ville",
                options=sorted(entreprises_df["ville"].unique()),
                default=[]
            )
        
        # Appliquer les filtres
        filtered_df = entreprises_df.copy()
        if secteur_filter:
            filtered_df = filtered_df[filtered_df["secteur"].isin(secteur_filter)]
        if statut_filter:
            filtered_df = filtered_df[filtered_df["statut"].isin(statut_filter)]
        if ville_filter:
            filtered_df = filtered_df[filtered_df["ville"].isin(ville_filter)]
        
        # Affichage du nombre d'entreprises filtrées
        st.write(f"**{len(filtered_df)} entreprises** correspondent aux critères")
        
        # Affichage de la liste des entreprises avec pagination
        st.markdown("<div class='table-container'>", unsafe_allow_html=True)
        
        # Créer une version du DataFrame avec des badges pour le statut
        display_df = filtered_df.copy()
        
        # Afficher le tableau
        st.dataframe(
            display_df[["id", "nom", "secteur", "ville", "contact_principal", "statut", "niveau_engagement", "dernier_contact"]],
            column_config={
                "id": "ID",
                "nom": "Nom",
                "secteur": "Secteur",
                "ville": "Ville",
                "contact_principal": "Contact",
                "statut": "Statut",
                "niveau_engagement": st.column_config.ProgressColumn(
                    "Engagement",
                    help="Niveau d'engagement de l'entreprise (1-5)",
                    format="%d",
                    min_value=0,
                    max_value=5,
                ),
                "dernier_contact": "Dernier contact"
            },
            hide_index=True,
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Bouton pour télécharger les données filtrées
        st.markdown(get_download_link(filtered_df, "entreprises_export.csv", "Télécharger les données filtrées"), unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Ajouter une nouvelle entreprise")
        
        # Formulaire d'ajout d'entreprise
        with st.form(key="add_company_form"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom de l'entreprise*")
                secteur = st.selectbox("Secteur d'activité*", ["Tech", "Industrie", "Services", "Commerce", "Finance", "Autre"])
                taille = st.selectbox("Taille de l'entreprise", ["TPE (<10)", "PME (10-250)", "ETI (250-5000)", "GE (>5000)"])
                adresse = st.text_input("Adresse")
            
            with col2:
                ville = st.text_input("Ville*")
                code_postal = st.text_input("Code postal")
                statut = st.selectbox("Statut*", ["Prospect", "En discussion", "Partenaire actif", "Partenaire inactif"])
                niveau_engagement = st.slider("Niveau d'engagement", 1, 5, 3)
            
            st.markdown("### Contact principal")
            col1, col2 = st.columns(2)
            with col1:
                contact_principal = st.text_input("Nom du contact principal*")
                email = st.text_input("Email du contact*")
            
            with col2:
                telephone = st.text_input("Téléphone")
                date_premier_contact = st.date_input("Date du premier contact", datetime.now())
            
            st.markdown("### Opportunités")
            col1, col2, col3 = st.columns(3)
            with col1:
                offres_emploi_annuelles = st.number_input("Offres d'emploi annuelles estimées", 0, 100, 0)
            with col2:
                stages_annuels = st.number_input("Stages annuels estimés", 0, 100, 0)
            with col3:
                alternances_annuelles = st.number_input("Alternances annuelles estimées", 0, 100, 0)
            
            notes = st.text_area("Notes", height=100)
            
            submit_button = st.form_submit_button(label="Ajouter l'entreprise")
        
        if submit_button:
            if not nom or not ville or not contact_principal or not email:
                st.error("Veuillez remplir tous les champs obligatoires (marqués d'un *)")
            else:
                # Générer un nouvel ID
                new_id = entreprises_df["id"].max() + 1 if len(entreprises_df) > 0 else 1
                
                # Créer un nouveau dictionnaire pour la nouvelle entreprise
                new_company = {
                    "id": new_id,
                    "nom": nom,
                    "secteur": secteur,
                    "taille": taille,
                    "adresse": adresse,
                    "ville": ville,
                    "code_postal": code_postal,
                    "contact_principal": contact_principal,
                    "email": email,
                    "telephone": telephone,
                    "date_premier_contact": date_premier_contact.strftime('%Y-%m-%d'),
                    "statut": statut,
                    "niveau_engagement": niveau_engagement,
                    "offres_emploi_annuelles": offres_emploi_annuelles,
                    "stages_annuels": stages_annuels,
                    "alternances_annuelles": alternances_annuelles,
                    "dernier_contact": date_premier_contact.strftime('%Y-%m-%d'),
                    "notes": notes
                }
                
                # Ajouter la nouvelle entreprise au DataFrame
                entreprises_df = pd.concat([entreprises_df, pd.DataFrame([new_company])], ignore_index=True)
                
                # Sauvegarder les données
                save_data(entreprises_df, "entreprises.csv")
                
                st.success(f"L'entreprise {nom} a été ajoutée avec succès!")
                st.balloons()
    
    with tab3:
        st.subheader("Vue détaillée d'une entreprise")
        
        # Sélection de l'entreprise
        selected_company = st.selectbox(
            "Sélectionner une entreprise",
            options=entreprises_df["id"].tolist(),
            format_func=lambda x: entreprises_df[entreprises_df["id"] == x]["nom"].iloc[0]
        )
        
        if selected_company:
            # Récupérer les données de l'entreprise sélectionnée
            company = entreprises_df[entreprises_df["id"] == selected_company].iloc[0]
            
            # Afficher les informations générales
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"# {company['nom']}")
                st.markdown(f"**Secteur**: {company['secteur']} | **Taille**: {company['taille']}")
                st.markdown(f"**Statut**: {company['statut']} | **Niveau d'engagement**: {company['niveau_engagement']}/5")
                st.markdown(f"**Adresse**: {company['adresse']}, {company['code_postal']} {company['ville']}")
                st.markdown(f"**Contact**: {company['contact_principal']} | **Email**: {company['email']} | **Tél**: {company['telephone']}")
                st.markdown(f"**Premier contact**: {format_date_fr(company['date_premier_contact'])} | **Dernier contact**: {format_date_fr(company['dernier_contact'])}")
            
            with col2:
                # Afficher un indicateur visuel de l'engagement
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=company['niveau_engagement'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Engagement"},
                    gauge={'axis': {'range': [0, 5]},
                           'bar': {'color': "#2ecc71"},
                           'steps': [
                               {'range': [0, 2], 'color': "#f39c12"},
                               {'range': [2, 4], 'color': "#3498db"},
                               {'range': [4, 5], 'color': "#2ecc71"}
                           ]}
                ))
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
            
            # Afficher les opportunités
            st.markdown("### Opportunités annuelles")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Offres d'emploi", company['offres_emploi_annuelles'])
            
            with col2:
                st.metric("Stages", company['stages_annuels'])
            
            with col3:
                st.metric("Alternances", company['alternances_annuelles'])
            
            # Afficher les notes
            st.markdown("### Notes")
            st.text_area("", value=company['notes'], height=100, key="notes_display", disabled=True)
            
            # Afficher les interactions avec cette entreprise
            st.markdown("### Historique des interactions")
            company_interactions = interactions_df[interactions_df["entreprise_id"] == selected_company].sort_values(by="date", ascending=False)
            
            if len(company_interactions) > 0:
                for _, interaction in company_interactions.iterrows():
                    st.markdown(f"""
                    **{format_date_fr(interaction['date'])}** - {interaction['type']}  
                    {interaction['sujet']} - {interaction['description']}  
                    Résultat: {interaction['resultat']}
                    """)
                    st.markdown("---")
            else:
                st.info("Aucune interaction enregistrée pour cette entreprise.")
            
            # Afficher les offres de cette entreprise
            st.markdown("### Offres")
            company_offers = offres_df[offres_df["entreprise_id"] == selected_company].sort_values(by="date_publication", ascending=False)
            
            if len(company_offers) > 0:
                for _, offer in company_offers.iterrows():
                    st.markdown(f"""
                    **{offer['titre']}** - {offer['type']} - {offer['statut']}  
                    Publication: {format_date_fr(offer['date_publication'])} | Expiration: {format_date_fr(offer['date_expiration'])}  
                    Candidatures: {offer['candidatures']} (dont {offer['candidatures_retenues']} retenues)
                    """)
                    st.markdown("---")
            else:
                st.info("Aucune offre enregistrée pour cette entreprise.")
            
            # Formulaire pour éditer l'entreprise
            st.markdown("### Modifier les informations")
            if st.button("Éditer cette entreprise"):
                st.session_state["edit_company"] = True
            
            if st.session_state.get("edit_company", False):
                with st.form(key="edit_company_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_nom = st.text_input("Nom de l'entreprise*", value=company['nom'])
                        edit_secteur = st.selectbox("Secteur d'activité*", ["Tech", "Industrie", "Services", "Commerce", "Finance", "Autre"], index=["Tech", "Industrie", "Services", "Commerce", "Finance", "Autre"].index(company['secteur']) if company['secteur'] in ["Tech", "Industrie", "Services", "Commerce", "Finance", "Autre"] else 0)
                        edit_taille = st.selectbox("Taille de l'entreprise", ["TPE (<10)", "PME (10-250)", "ETI (250-5000)", "GE (>5000)"], index=["TPE (<10)", "PME (10-250)", "ETI (250-5000)", "GE (>5000)"].index(company['taille']) if company['taille'] in ["TPE (<10)", "PME (10-250)", "ETI (250-5000)", "GE (>5000)"] else 0)
                        edit_adresse = st.text_input("Adresse", value=company['adresse'])
                    
                    with col2:
                        edit_ville = st.text_input("Ville*", value=company['ville'])
                        edit_code_postal = st.text_input("Code postal", value=company['code_postal'])
                        edit_statut = st.selectbox("Statut*", ["Prospect", "En discussion", "Partenaire actif", "Partenaire inactif"], index=["Prospect", "En discussion", "Partenaire actif", "Partenaire inactif"].index(company['statut']) if company['statut'] in ["Prospect", "En discussion", "Partenaire actif", "Partenaire inactif"] else 0)
                        edit_niveau_engagement = st.slider("Niveau d'engagement", 1, 5, int(company['niveau_engagement']))
                    
                    st.markdown("### Contact principal")
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_contact_principal = st.text_input("Nom du contact principal*", value=company['contact_principal'])
                        edit_email = st.text_input("Email du contact*", value=company['email'])
                    
                    with col2:
                        edit_telephone = st.text_input("Téléphone", value=company['telephone'])
                        edit_date_premier_contact = st.date_input("Date du premier contact", datetime.strptime(company['date_premier_contact'], '%Y-%m-%d') if not pd.isna(company['date_premier_contact']) else datetime.now())
                    
                    st.markdown("### Opportunités")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        edit_offres_emploi_annuelles = st.number_input("Offres d'emploi annuelles estimées", 0, 100, int(company['offres_emploi_annuelles']))
                    with col2:
                        edit_stages_annuels = st.number_input("Stages annuels estimés", 0, 100, int(company['stages_annuels']))
                    with col3:
                        edit_alternances_annuelles = st.number_input("Alternances annuelles estimées", 0, 100, int(company['alternances_annuelles']))
                    
                    edit_notes = st.text_area("Notes", value=company['notes'], height=100)
                    
                    submit_edit_button = st.form_submit_button(label="Enregistrer les modifications")
                
                if submit_edit_button:
                    if not edit_nom or not edit_ville or not edit_contact_principal or not edit_email:
                        st.error("Veuillez remplir tous les champs obligatoires (marqués d'un *)")
                    else:
                        # Mettre à jour les informations de l'entreprise
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "nom"] = edit_nom
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "secteur"] = edit_secteur
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "taille"] = edit_taille
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "adresse"] = edit_adresse
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "ville"] = edit_ville
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "code_postal"] = edit_code_postal
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "contact_principal"] = edit_contact_principal
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "email"] = edit_email
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "telephone"] = edit_telephone
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "date_premier_contact"] = edit_date_premier_contact.strftime('%Y-%m-%d')
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "statut"] = edit_statut
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "niveau_engagement"] = edit_niveau_engagement
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "offres_emploi_annuelles"] = edit_offres_emploi_annuelles
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "stages_annuels"] = edit_stages_annuels
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "alternances_annuelles"] = edit_alternances_annuelles
                        entreprises_df.loc[entreprises_df["id"] == selected_company, "notes"] = edit_notes
                        
                        # Sauvegarder les données
                        save_data(entreprises_df, "entreprises.csv")
                        
                        st.success(f"Les informations de l'entreprise {edit_nom} ont été mises à jour avec succès!")
                        st.session_state["edit_company"] = False
                        st.experimental_rerun()

# Page Interactions
elif page == "💬 Interactions":
    st.markdown("<h1 class='main-header'>Gestion des Interactions</h1>", unsafe_allow_html=True)
    
    # Onglets
    tab1, tab2 = st.tabs(["Liste des interactions", "Ajouter une interaction"])
    
    with tab1:
        # Filtres
        col1, col2, col3 = st.columns(3)
        with col1:
            entreprise_filter = st.multiselect(
                "Entreprise",
                options=sorted(entreprises_df["nom"].unique()),
                default=[]
            )
        with col2:
            type_filter = st.multiselect(
                "Type d'interaction",
                options=sorted(interactions_df["type"].unique()),
                default=[]
            )
        with col3:
            sujet_filter = st.multiselect(
                "Sujet",
                options=sorted(interactions_df["sujet"].unique()),
                default=[]
            )
        
        # Période
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Date de début", datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("Date de fin", datetime.now())
        
        # Appliquer les filtres
        filtered_interactions = interactions_df.copy()
        if entreprise_filter:
            filtered_interactions = filtered_interactions[filtered_interactions["entreprise_nom"].isin(entreprise_filter)]
        if type_filter:
            filtered_interactions = filtered_interactions[filtered_interactions["type"].isin(type_filter)]
        if sujet_filter:
            filtered_interactions = filtered_interactions[filtered_interactions["sujet"].isin(sujet_filter)]
        
        # Filtrer par date
        filtered_interactions = filtered_interactions[
            (pd.to_datetime(filtered_interactions["date"]) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(filtered_interactions["date"]) <= pd.to_datetime(end_date))
        ]
        
        # Affichage du nombre d'interactions filtrées
        st.write(f"**{len(filtered_interactions)} interactions** correspondent aux critères")
        
        # Affichage de la liste des interactions
        st.markdown("<div class='table-container'>", unsafe_allow_html=True)
        st.dataframe(
            filtered_interactions[["id", "entreprise_nom", "date", "type", "sujet", "resultat", "suivi_requis", "date_suivi"]],
            column_config={
                "id": "ID",
                "entreprise_nom": "Entreprise",
                "date": "Date",
                "type": "Type",
                "sujet": "Sujet",
                "resultat": "Résultat",
                "suivi_requis": "Suivi requis",
                "date_suivi": "Date de suivi"
            },
            hide_index=True,
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Bouton pour télécharger les données filtrées
        st.markdown(get_download_link(filtered_interactions, "interactions_export.csv", "Télécharger les données filtrées"), unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Ajouter une nouvelle interaction")
        
        # Formulaire d'ajout d'interaction
        with st.form(key="add_interaction_form"):
            # Sélection de l'entreprise
            entreprise_id = st.selectbox(
                "Entreprise*",
                options=entreprises_df["id"].tolist(),
                format_func=lambda x: entreprises_df[entreprises_df["id"] == x]["nom"].iloc[0]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                date_interaction = st.date_input("Date de l'interaction*", datetime.now())
                type_interaction = st.selectbox("Type d'interaction*", ["Email", "Téléphone", "Réunion", "Événement", "Autre"])
            
            with col2:
                sujet = st.selectbox("Sujet*", ["Prospection", "Suivi", "Offre d'emploi", "Stage", "Alternance", "Événement", "Feedback", "Autre"])
                resultat = st.selectbox("Résultat*", ["Positif", "Neutre", "À suivre", "Négatif"])
            
            description = st.text_area("Description de l'interaction*", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                suivi_requis = st.checkbox("Suivi requis")
            
            with col2:
                date_suivi = st.date_input("Date de suivi", datetime.now() + timedelta(days=7), disabled=not suivi_requis)
            
            submit_button = st.form_submit_button(label="Enregistrer l'interaction")
        
        if submit_button:
            if not entreprise_id or not description:
                st.error("Veuillez remplir tous les champs obligatoires (marqués d'un *)")
            else:
                # Générer un nouvel ID
                new_id = interactions_df["id"].max() + 1 if len(interactions_df) > 0 else 1
                
                # Récupérer le nom de l'entreprise
                entreprise_nom = entreprises_df[entreprises_df["id"] == entreprise_id]["nom"].iloc[0]
                
                # Créer un nouveau dictionnaire pour la nouvelle interaction
                new_interaction = {
                    "id": new_id,
                    "entreprise_id": entreprise_id,
                    "entreprise_nom": entreprise_nom,
                    "date": date_interaction.strftime('%Y-%m-%d'),
                    "type": type_interaction,
                    "sujet": sujet,
                    "description": description,
                    "resultat": resultat,
                    "suivi_requis": suivi_requis,
                    "date_suivi": date_suivi.strftime('%Y-%m-%d') if suivi_requis else "",
                }
                
                # Ajouter la nouvelle interaction au DataFrame
                interactions_df = pd.concat([interactions_df, pd.DataFrame([new_interaction])], ignore_index=True)
                
                # Mettre à jour la date du dernier contact de l'entreprise
                entreprises_df.loc[entreprises_df["id"] == entreprise_id, "dernier_contact"] = date_interaction.strftime('%Y-%m-%d')
                
                # Sauvegarder les données
                save_data(interactions_df, "interactions.csv")
                save_data(entreprises_df, "entreprises.csv")
                
                st.success(f"L'interaction avec {entreprise_nom} a été enregistrée avec succès!")
                st.balloons()

# Page Événements
elif page == "📅 Événements":
    st.markdown("<h1 class='main-header'>Gestion des Événements</h1>", unsafe_allow_html=True)
    
    # Onglets
    tab1, tab2 = st.tabs(["Liste des événements", "Planifier un événement"])
    
    with tab1:
        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            type_filter = st.multiselect(
                "Type d'événement",
                options=sorted(evenements_df["type"].unique()),
                default=[]
            )
        with col2:
            statut_filter = st.multiselect(
                "Statut",
                options=sorted(evenements_df["statut"].unique()),
                default=[]
            )
        
        # Période
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Date de début", datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("Date de fin", datetime.now() + timedelta(days=180))
        
        # Appliquer les filtres
        filtered_events = evenements_df.copy()
        if type_filter:
            filtered_events = filtered_events[filtered_events["type"].isin(type_filter)]
        if statut_filter:
            filtered_events = filtered_events[filtered_events["statut"].isin(statut_filter)]
        
        # Filtrer par date
        filtered_events = filtered_events[
            (pd.to_datetime(filtered_events["date"]) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(filtered_events["date"]) <= pd.to_datetime(end_date))
        ]
        
        # Affichage du nombre d'événements filtrés
        st.write(f"**{len(filtered_events)} événements** correspondent aux critères")
        
        # Affichage de la liste des événements
        st.markdown("<div class='table-container'>", unsafe_allow_html=True)
        st.dataframe(
            filtered_events[["id", "nom", "type", "date", "lieu", "nombre_participants", "statut"]],
            column_config={
                "id": "ID",
                "nom": "Nom",
                "type": "Type",
                "date": "Date",
                "lieu": "Lieu",
                "nombre_participants": "Participants",
                "statut": "Statut"
            },
            hide_index=True,
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Bouton pour télécharger les données filtrées
        st.markdown(get_download_link(filtered_events, "evenements_export.csv", "Télécharger les données filtrées"), unsafe_allow_html=True)
        
        # Affichage détaillé d'un événement
        st.subheader("Détails de l'événement")
        selected_event = st.selectbox(
            "Sélectionner un événement",
            options=filtered_events["id"].tolist(),
            format_func=lambda x: f"{filtered_events[filtered_events['id'] == x]['nom'].iloc[0]} - {filtered_events[filtered_events['id'] == x]['date'].iloc[0]}"
        )
        
        if selected_event:
            event = filtered_events[filtered_events["id"] == selected_event].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### {event['nom']}")
                st.markdown(f"**Type**: {event['type']}")
                st.markdown(f"**Date**: {format_date_fr(event['date'])}")
                st.markdown(f"**Lieu**: {event['lieu']}")
                st.markdown(f"**Statut**: {event['statut']}")
            
            with col2:
                st.markdown(f"**Nombre de participants**: {event['nombre_participants']}")
                st.markdown(f"**Description**: {event['description']}")
                
                if event['statut'] == "Terminé":
                    st.markdown(f"**Bilan**: {event['notes_bilan']}")
            
            # Afficher les entreprises participantes
            st.subheader("Entreprises participantes")
            
            if event['entreprises_participants']:
                entreprises_ids = [int(id) for id in event['entreprises_participants'].split(",")]
                entreprises_participantes = entreprises_df[entreprises_df["id"].isin(entreprises_ids)]
                
                st.dataframe(
                    entreprises_participantes[["id", "nom", "secteur", "contact_principal"]],
                    column_config={
                        "id": "ID",
                        "nom": "Nom",
                        "secteur": "Secteur",
                        "contact_principal": "Contact principal"
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("Aucune entreprise participante enregistrée pour cet événement.")
            
            # Formulaire pour ajouter un bilan
            if event['statut'] == "Terminé" and not event['notes_bilan']:
                st.subheader("Ajouter un bilan")
                
                with st.form(key="add_event_report"):
                    bilan = st.text_area("Bilan de l'événement", height=150)
                    submit_report = st.form_submit_button("Enregistrer le bilan")
                
                if submit_report:
                    if bilan:
                        # Mettre à jour le bilan de l'événement
                        evenements_df.loc[evenements_df["id"] == selected_event, "notes_bilan"] = bilan
                        
                        # Sauvegarder les données
                        save_data(evenements_df, "evenements.csv")
                        
                        st.success("Le bilan a été enregistré avec succès!")
                        st.experimental_rerun()
                    else:
                        st.error("Veuillez remplir le champ du bilan.")
    
    with tab2:
        st.subheader("Planifier un nouvel événement")
        
        # Formulaire pour planifier un événement
        with st.form(key="add_event_form"):
            col1, col2 = st.columns(2)
            with col1:
                nom_evenement = st.text_input("Nom de l'événement*")
                type_evenement = st.selectbox("Type d'événement*", ["Forum", "Workshop", "Conférence", "Petit-déjeuner", "Visite", "Autre"])
                date_evenement = st.date_input("Date de l'événement*", datetime.now() + timedelta(days=30))
            
            with col2:
                lieu_evenement = st.selectbox("Lieu*", ["Nos locaux", "Locaux partenaire", "Lieu externe", "En ligne"])
                statut_evenement = st.selectbox("Statut*", ["Planifié", "En préparation", "Terminé", "Annulé"])
            
            description_evenement = st.text_area("Description*", height=100)
            
            # Sélection des entreprises participantes
            st.subheader("Entreprises participantes")
            
            entreprises_participantes = st.multiselect(
                "Sélectionner les entreprises participantes",
                options=entreprises_df["id"].tolist(),
                format_func=lambda x: entreprises_df[entreprises_df["id"] == x]["nom"].iloc[0]
            )
            
            submit_button = st.form_submit_button(label="Planifier l'événement")
        
        if submit_button:
            if not nom_evenement or not description_evenement:
                st.error("Veuillez remplir tous les champs obligatoires (marqués d'un *)")
            else:
                # Générer un nouvel ID
                new_id = evenements_df["id"].max() + 1 if len(evenements_df) > 0 else 1
                
                # Convertir la liste des entreprises participantes en chaîne
                entreprises_participants_str = ",".join(map(str, entreprises_participantes)) if entreprises_participantes else ""
                
                # Créer un nouveau dictionnaire pour le nouvel événement
                new_event = {
                    "id": new_id,
                    "nom": nom_evenement,
                    "type": type_evenement,
                    "date": date_evenement.strftime('%Y-%m-%d'),
                    "lieu": lieu_evenement,
                    "description": description_evenement,
                    "entreprises_participants": entreprises_participants_str,
                    "nombre_participants": len(entreprises_participantes),
                    "statut": statut_evenement,
                    "notes_bilan": ""
                }
                
                # Ajouter le nouvel événement au DataFrame
                evenements_df = pd.concat([evenements_df, pd.DataFrame([new_event])], ignore_index=True)
                
                # Sauvegarder les données
                save_data(evenements_df, "evenements.csv")
                
                st.success(f"L'événement {nom_evenement} a été planifié avec succès!")
                st.balloons()

# Page Offres
elif page == "📝 Offres":
    st.markdown("<h1 class='main-header'>Gestion des Offres</h1>", unsafe_allow_html=True)
    
    # Onglets
    tab1, tab2 = st.tabs(["Liste des offres", "Ajouter une offre"])
    
    with tab1:
        # Filtres
        col1, col2, col3 = st.columns(3)
        with col1:
            entreprise_filter = st.multiselect(
                "Entreprise",
                options=sorted(entreprises_df["nom"].unique()),
                default=[]
            )
        with col2:
            type_filter = st.multiselect(
                "Type d'offre",
                options=sorted(offres_df["type"].unique()),
                default=[]
            )
        with col3:
            statut_filter = st.multiselect(
                "Statut",
                options=sorted(offres_df["statut"].unique()),
                default=[]
            )
        
        # Période
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Date de publication début", datetime.now() - timedelta(days=90))
        with col2:
            end_date = st.date_input("Date de publication fin", datetime.now())
        
        # Appliquer les filtres
        filtered_offers = offres_df.copy()
        if entreprise_filter:
            filtered_offers = filtered_offers[filtered_offers["entreprise_nom"].isin(entreprise_filter)]
        if type_filter:
            filtered_offers = filtered_offers[filtered_offers["type"].isin(type_filter)]
        if statut_filter:
            filtered_offers = filtered_offers[filtered_offers["statut"].isin(statut_filter)]
        
        # Filtrer par date
        filtered_offers = filtered_offers[
            (pd.to_datetime(filtered_offers["date_publication"]) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(filtered_offers["date_publication"]) <= pd.to_datetime(end_date))
        ]
        
        # Affichage du nombre d'offres filtrées
        st.write(f"**{len(filtered_offers)} offres** correspondent aux critères")
        
        # Affichage de la liste des offres
        st.markdown("<div class='table-container'>", unsafe_allow_html=True)
        st.dataframe(
            filtered_offers[["id", "entreprise_nom", "titre", "type", "date_publication", "date_expiration", "localisation", "statut", "candidatures"]],
            column_config={
                "id": "ID",
                "entreprise_nom": "Entreprise",
                "titre": "Titre",
                "type": "Type",
                "date_publication": "Publication",
                "date_expiration": "Expiration",
                "localisation": "Localisation",
                "statut": "Statut",
                "candidatures": "Candidatures"
            },
            hide_index=True,
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Bouton pour télécharger les données filtrées
        st.markdown(get_download_link(filtered_offers, "offres_export.csv", "Télécharger les données filtrées"), unsafe_allow_html=True)
        
        # Affichage détaillé d'une offre
        st.subheader("Détails de l'offre")
        selected_offer = st.selectbox(
            "Sélectionner une offre",
            options=filtered_offers["id"].tolist(),
            format_func=lambda x: f"{filtered_offers[filtered_offers['id'] == x]['titre'].iloc[0]} - {filtered_offers[filtered_offers['id'] == x]['entreprise_nom'].iloc[0]}"
        )
        
        if selected_offer:
            offer = filtered_offers[filtered_offers["id"] == selected_offer].iloc[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### {offer['titre']}")
                st.markdown(f"**Entreprise**: {offer['entreprise_nom']}")
                st.markdown(f"**Type**: {offer['type']}")
                st.markdown(f"**Publication**: {format_date_fr(offer['date_publication'])}")
                st.markdown(f"**Expiration**: {format_date_fr(offer['date_expiration'])}")
            
            with col2:
                st.markdown(f"**Localisation**: {offer['localisation']}")
                st.markdown(f"**Statut**: {offer['statut']}")
                st.markdown(f"**Candidatures**: {offer['candidatures']} (dont {offer['candidatures_retenues']} retenues)")
            
            st.markdown("### Description")
            st.write(offer['description'])
            
            st.markdown("### Compétences requises")
            for competence in offer['compétences_requises'].split(","):
                st.markdown(f"- {competence.strip()}")
            
            # Formulaire pour mettre à jour le statut de l'offre
            st.subheader("Mettre à jour le statut")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nouveau_statut = st.selectbox("Nouveau statut", ["Active", "Pourvue", "Expirée"], index=["Active", "Pourvue", "Expirée"].index(offer['statut']) if offer['statut'] in ["Active", "Pourvue", "Expirée"] else 0)
            
            with col2:
                nb_candidatures = st.number_input("Nombre total de candidatures", min_value=0, value=int(offer['candidatures']))
                nb_candidatures_retenues = st.number_input("Nombre de candidatures retenues", min_value=0, max_value=nb_candidatures, value=int(offer['candidatures_retenues']))
            
            if st.button("Mettre à jour"):
                # Mettre à jour le statut de l'offre
                offres_df.loc[offres_df["id"] == selected_offer, "statut"] = nouveau_statut
                offres_df.loc[offres_df["id"] == selected_offer, "candidatures"] = nb_candidatures
                offres_df.loc[offres_df["id"] == selected_offer, "candidatures_retenues"] = nb_candidatures_retenues
                
                # Sauvegarder les données
                save_data(offres_df, "offres.csv")
                
                st.success("Le statut de l'offre a été mis à jour avec succès!")
                st.experimental_rerun()
    
    with tab2:
        st.subheader("Ajouter une nouvelle offre")
        
        # Formulaire pour ajouter une offre
        with st.form(key="add_offer_form"):
            # Sélection de l'entreprise
            entreprise_id = st.selectbox(
                "Entreprise*",
                options=entreprises_df["id"].tolist(),
                format_func=lambda x: entreprises_df[entreprises_df["id"] == x]["nom"].iloc[0]
            )
            
            col1, col2 = st.columns(2)
            with col1:
                titre = st.text_input("Titre de l'offre*")
                type_offre = st.selectbox("Type d'offre*", ["Emploi", "Stage", "Alternance"])
                date_publication = st.date_input("Date de publication*", datetime.now())
                date_expiration = st.date_input("Date d'expiration*", datetime.now() + timedelta(days=60))
            
            with col2:
                localisation = st.text_input("Localisation*")
                competences = st.text_input("Compétences requises (séparées par des virgules)*")
                statut = st.selectbox("Statut*", ["Active", "Pourvue", "Expirée"])
            
            description = st.text_area("Description de l'offre*", height=150)
            
            submit_button = st.form_submit_button(label="Ajouter l'offre")
        
        if submit_button:
            if not titre or not localisation or not competences or not description:
                st.error("Veuillez remplir tous les champs obligatoires (marqués d'un *)")
            else:
                # Générer un nouvel ID
                new_id = offres_df["id"].max() + 1 if len(offres_df) > 0 else 1
                
                # Récupérer le nom de l'entreprise
                entreprise_nom = entreprises_df[entreprises_df["id"] == entreprise_id]["nom"].iloc[0]
                
                # Créer un nouveau dictionnaire pour la nouvelle offre
                new_offer = {
                    "id": new_id,
                    "entreprise_id": entreprise_id,
                    "entreprise_nom": entreprise_nom,
                    "titre": titre,
                    "type": type_offre,
                    "date_publication": date_publication.strftime('%Y-%m-%d'),
                    "date_expiration": date_expiration.strftime('%Y-%m-%d'),
                    "description": description,
                    "compétences_requises": competences,
                    "localisation": localisation,
                    "statut": statut,
                    "candidatures": 0,
                    "candidatures_retenues": 0
                }
                
                # Ajouter la nouvelle offre au DataFrame
                offres_df = pd.concat([offres_df, pd.DataFrame([new_offer])], ignore_index=True)
                
                # Sauvegarder les données
                save_data(offres_df, "offres.csv")
                
                st.success(f"L'offre {titre} a été ajoutée avec succès!")
                st.balloons()

# Page Analyse des données
elif page == "📈 Analyse des données":
    st.markdown("<h1 class='main-header'>Analyse des Données</h1>", unsafe_allow_html=True)
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["Tendances générales", "Analyse des entreprises", "Analyse des offres"])
    
    with tab1:
        st.subheader("Tendances générales")
        
        # Convertir les dates en datetime pour les analyses temporelles
        interactions_df["date"] = pd.to_datetime(interactions_df["date"])
        offres_df["date_publication"] = pd.to_datetime(offres_df["date_publication"])
        evenements_df["date"] = pd.to_datetime(evenements_df["date"])
        
        # Définir la période d'analyse
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Période du", datetime.now() - timedelta(days=365))
        with col2:
            end_date = st.date_input("au", datetime.now())
        
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # Filtrer les données pour la période sélectionnée
        interactions_periode = interactions_df[(interactions_df["date"] >= start_date) & (interactions_df["date"] <= end_date)]
        offres_periode = offres_df[(offres_df["date_publication"] >= start_date) & (offres_df["date_publication"] <= end_date)]
        evenements_periode = evenements_df[(evenements_df["date"] >= start_date) & (evenements_df["date"] <= end_date)]
        
        # Statistiques générales sur la période
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>{}</div>
                <div class='stat-label'>Interactions</div>
            </div>
            """.format(len(interactions_periode)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>{}</div>
                <div class='stat-label'>Offres publiées</div>
            </div>
            """.format(len(offres_periode)), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>{}</div>
                <div class='stat-label'>Événements</div>
            </div>
            """.format(len(evenements_periode)), unsafe_allow_html=True)
        
        with col4:
            nouveaux_partenaires = len(entreprises_df[pd.to_datetime(entreprises_df["date_premier_contact"]).between(start_date, end_date)])
            st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>{}</div>
                <div class='stat-label'>Nouveaux partenaires</div>
            </div>
            """.format(nouveaux_partenaires), unsafe_allow_html=True)
        
        # Évolution du nombre d'interactions par mois
        st.subheader("Évolution des interactions")
        
        interactions_periode["mois"] = interactions_periode["date"].dt.to_period('M')
        interactions_par_mois = interactions_periode.groupby("mois").size().reset_index(name="count")
        interactions_par_mois["mois"] = interactions_par_mois["mois"].astype(str)
        
        fig = px.line(
            interactions_par_mois,
            x="mois",
            y="count",
            markers=True,
            title="Nombre d'interactions par mois"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Évolution du nombre d'offres par mois
        st.subheader("Évolution des offres")
        
        offres_periode["mois"] = offres_periode["date_publication"].dt.to_period('M')
        offres_par_mois = offres_periode.groupby(["mois", "type"]).size().reset_index(name="count")
        offres_par_mois["mois"] = offres_par_mois["mois"].astype(str)
        
        fig = px.line(
            offres_par_mois,
            x="mois",
            y="count",
            color="type",
            markers=True,
            title="Nombre d'offres par mois et par type"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribution des types d'interactions
        st.subheader("Distribution des types d'interactions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            interactions_par_type = interactions_periode.groupby("type").size().reset_index(name="count")
            fig = px.pie(
                interactions_par_type,
                values="count",
                names="type",
                title="Répartition des types d'interactions",
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            interactions_par_sujet = interactions_periode.groupby("sujet").size().reset_index(name="count")
            fig = px.pie(
                interactions_par_sujet,
                values="count",
                names="sujet",
                title="Répartition des sujets d'interactions",
                hole=0.3
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Analyse des entreprises")
        
        # Distribution par secteur
        st.markdown("### Distribution des entreprises par secteur")
        entreprises_par_secteur = entreprises_df.groupby("secteur").size().reset_index(name="count")
        fig = px.bar(
            entreprises_par_secteur,
            x="secteur",
            y="count",
            color="secteur",
            title="Nombre d'entreprises par secteur"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribution par statut
        st.markdown("### Distribution des entreprises par statut")
        entreprises_par_statut = entreprises_df.groupby("statut").size().reset_index(name="count")
        fig = px.pie(
            entreprises_par_statut,
            values="count",
            names="statut",
            title="Répartition des statuts des entreprises",
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse de l'engagement
        st.markdown("### Analyse du niveau d'engagement")
        
        col1, col2 = st.columns(2)
        
        with col1:
            engagement_par_secteur = entreprises_df.groupby("secteur")["niveau_engagement"].mean().reset_index()
            fig = px.bar(
                engagement_par_secteur,
                x="secteur",
                y="niveau_engagement",
                color="secteur",
                title="Niveau d'engagement moyen par secteur"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            engagement_par_taille = entreprises_df.groupby("taille")["niveau_engagement"].mean().reset_index()
            fig = px.bar(
                engagement_par_taille,
                x="taille",
                y="niveau_engagement",
                color="taille",
                title="Niveau d'engagement moyen par taille d'entreprise"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top 10 des entreprises les plus engagées
        st.markdown("### Top 10 des entreprises les plus engagées")
        top_entreprises = entreprises_df.sort_values(by="niveau_engagement", ascending=False).head(10)
        fig = px.bar(
            top_entreprises,
            x="nom",
            y="niveau_engagement",
            color="secteur",
            title="Top 10 des entreprises par niveau d'engagement"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse géographique
        st.markdown("### Répartition géographique")
        entreprises_par_ville = entreprises_df.groupby("ville").size().reset_index(name="count")
        fig = px.pie(
            entreprises_par_ville,
            values="count",
            names="ville",
            title="Répartition des entreprises par ville"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Analyse des offres")
        
        # Distribution par type
        st.markdown("### Distribution des offres par type")
        offres_par_type = offres_df.groupby("type").size().reset_index(name="count")
        fig = px.pie(
            offres_par_type,
            values="count",
            names="type",
            title="Répartition des types d'offres",
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Évolution du nombre d'offres par type et par mois
        st.markdown("### Évolution mensuelle des offres par type")
        offres_df["mois"] = offres_df["date_publication"].dt.to_period('M')
        offres_par_mois_type = offres_df.groupby(["mois", "type"]).size().reset_index(name="count")
        offres_par_mois_type["mois"] = offres_par_mois_type["mois"].astype(str)
        
        fig = px.bar(
            offres_par_mois_type,
            x="mois",
            y="count",
            color="type",
            title="Évolution du nombre d'offres par type et par mois",
            barmode="group"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top entreprises qui publient le plus d'offres
        st.markdown("### Top 10 des entreprises qui publient le plus d'offres")
        offres_par_entreprise = offres_df.groupby("entreprise_nom").size().reset_index(name="count").sort_values(by="count", ascending=False).head(10)
        fig = px.bar(
            offres_par_entreprise,
            x="entreprise_nom",
            y="count",
            title="Top 10 des entreprises par nombre d'offres publiées"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse des candidatures
        st.markdown("### Analyse des candidatures")
        
        col1, col2 = st.columns(2)
        
        with col1:
            candidatures_par_type = offres_df.groupby("type").agg({"candidatures": "sum", "candidatures_retenues": "sum"}).reset_index()
            candidatures_par_type["taux_conversion"] = (candidatures_par_type["candidatures_retenues"] / candidatures_par_type["candidatures"]) * 100
            
            fig = px.bar(
                candidatures_par_type,
                x="type",
                y=["candidatures", "candidatures_retenues"],
                title="Nombre de candidatures par type d'offre",
                barmode="group"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                candidatures_par_type,
                x="type",
                y="taux_conversion",
                title="Taux de conversion des candidatures par type d'offre (%)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Durée de vie des offres
        st.markdown("### Durée de vie moyenne des offres")
        
        # Calculer la durée de vie des offres (en jours)
        offres_df["duree"] = (pd.to_datetime(offres_df["date_expiration"]) - pd.to_datetime(offres_df["date_publication"])).dt.days
        
        duree_par_type = offres_df.groupby("type")["duree"].mean().reset_index()
        fig = px.bar(
            duree_par_type,
            x="type",
            y="duree",
            color="type",
            title="Durée de vie moyenne des offres par type (en jours)"
        )
        st.plotly_chart(fig, use_container_width=True)

# Page Paramètres
elif page == "⚙️ Paramètres":
    st.markdown("<h1 class='main-header'>Paramètres</h1>", unsafe_allow_html=True)
    
    # Onglets
    tab1, tab2, tab3 = st.tabs(["Exportation des données", "Importation des données", "À propos"])
    
    with tab1:
        st.subheader("Exportation des données")
        
        st.markdown("### Télécharger les données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(get_download_link(entreprises_df, "entreprises_export.csv", "Télécharger la liste des entreprises"), unsafe_allow_html=True)
            st.markdown(get_download_link(interactions_df, "interactions_export.csv", "Télécharger la liste des interactions"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(get_download_link(evenements_df, "evenements_export.csv", "Télécharger la liste des événements"), unsafe_allow_html=True)
            st.markdown(get_download_link(offres_df, "offres_export.csv", "Télécharger la liste des offres"), unsafe_allow_html=True)
        
        st.info("Les données sont exportées au format CSV et peuvent être ouvertes avec Excel ou tout autre tableur.")
    
    with tab2:
        st.subheader("Importation des données")
        
        st.warning("L'importation de données remplacera les données existantes. Assurez-vous d'avoir fait une sauvegarde avant d'importer de nouvelles données.")
        
        uploaded_file = st.file_uploader("Choisir un fichier CSV", type=["csv"])
        
        if uploaded_file is not None:
            st.write("Fichier chargé avec succès :", uploaded_file.name)
            
            # Déterminer le type de données à importer
            data_type = st.radio(
                "Type de données à importer",
                ["Entreprises", "Interactions", "Événements", "Offres"]
            )
            
            if st.button("Importer les données"):
                try:
                    imported_data = pd.read_csv(uploaded_file)
                    
                    if data_type == "Entreprises":
                        # Vérifier que les colonnes nécessaires sont présentes
                        required_columns = ["nom", "secteur", "statut"]
                        if all(col in imported_data.columns for col in required_columns):
                            save_data(imported_data, "entreprises.csv")
                            st.success("Les données des entreprises ont été importées avec succès!")
                        else:
                            st.error("Le format du fichier ne correspond pas à celui attendu pour les entreprises.")
                    
                    elif data_type == "Interactions":
                        required_columns = ["entreprise_id", "date", "type", "sujet"]
                        if all(col in imported_data.columns for col in required_columns):
                            save_data(imported_data, "interactions.csv")
                            st.success("Les données des interactions ont été importées avec succès!")
                        else:
                            st.error("Le format du fichier ne correspond pas à celui attendu pour les interactions.")
                    
                    elif data_type == "Événements":
                        required_columns = ["nom", "type", "date", "statut"]
                        if all(col in imported_data.columns for col in required_columns):
                            save_data(imported_data, "evenements.csv")
                            st.success("Les données des événements ont été importées avec succès!")
                        else:
                            st.error("Le format du fichier ne correspond pas à celui attendu pour les événements.")
                    
                    elif data_type == "Offres":
                        required_columns = ["entreprise_id", "titre", "type", "date_publication"]
                        if all(col in imported_data.columns for col in required_columns):
                            save_data(imported_data, "offres.csv")
                            st.success("Les données des offres ont été importées avec succès!")
                        else:
                            st.error("Le format du fichier ne correspond pas à celui attendu pour les offres.")
                    
                    st.experimental_rerun()
                
                except Exception as e:
                    st.error(f"Une erreur s'est produite lors de l'importation : {e}")
    
    with tab3:
        st.subheader("À propos")
        
        st.markdown("""
        ### CRM Relations Entreprises v1.0
        
        Cette application (démo) a été développée pour faciliter la gestion des relations avec les entreprises partenaires, dans le cadre de l'insertion professionnelle des jeunes.
        
        #### Fonctionnalités principales :
        - Gestion des entreprises partenaires
        - Suivi des interactions
        - Organisation d'événements
        - Gestion des offres d'emploi, de stage et d'alternance
        - Analyse de données et tableaux de bord
        
        #### Comment utiliser l'application :
        1. Ajoutez des entreprises partenaires
        2. Enregistrez vos interactions avec ces entreprises
        3. Planifiez des événements
        4. Publiez et suivez les offres
        5. Analysez vos données pour améliorer votre stratégie
        
        Pour toute question ou suggestion, contactez l'administrateur de l'application.
        """)
        
        st.info("Cette application est une démonstration et peut être personnalisée selon vos besoins spécifiques.")

# Initialiser les variables de session si elles n'existent pas
if "edit_company" not in st.session_state:
    st.session_state["edit_company"] = False

if "show_add_company_form" not in st.session_state:
    st.session_state["show_add_company_form"] = False

if "show_add_interaction_form" not in st.session_state:
    st.session_state["show_add_interaction_form"] = False

if "show_add_event_form" not in st.session_state:
    st.session_state["show_add_event_form"] = False

if "show_add_offer_form" not in st.session_state:
    st.session_state["show_add_offer_form"] = False

# Ajouter un style personnalisé pour l'application
st.markdown("""
<style>
    /* Styles généraux */
    .highlight {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* Animation pour les cartes de statistiques */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-effect:hover {
        animation: pulse 1s infinite;
    }
    
    /* Style pour les badges d'étiquette */
    .tag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-right: 5px;
    }
    
    .tag-tech {
        background-color: #3498db;
        color: white;
    }
    
    .tag-industrie {
        background-color: #e74c3c;
        color: white;
    }
    
    .tag-services {
        background-color: #2ecc71;
        color: white;
    }
    
    .tag-commerce {
        background-color: #f39c12;
        color: white;
    }
    
    .tag-finance {
        background-color: #9b59b6;
        color: white;
    }
    
    /* Style pour la barre de recherche */
    .search-container {
        margin-bottom: 20px;
    }
    
    /* Style pour améliorer la lisibilité des tableaux */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Style pour les notifications */
    .notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #2ecc71;
        color: white;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 1000;
        display: none;
    }
    
    /* Timeline pour l'historique des interactions */
    .timeline {
        position: relative;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .timeline::after {
        content: '';
        position: absolute;
        width: 6px;
        background-color: #e0e0e0;
        top: 0;
        bottom: 0;
        left: 50%;
        margin-left: -3px;
    }
    
    .timeline-container {
        padding: 10px 40px;
        position: relative;
        background-color: inherit;
        width: 50%;
    }
    
    .timeline-container::after {
        content: '';
        position: absolute;
        width: 20px;
        height: 20px;
        right: -10px;
        background-color: white;
        border: 4px solid #3498db;
        top: 15px;
        border-radius: 50%;
        z-index: 1;
    }
    
    .left {
        left: 0;
    }
    
    .right {
        left: 50%;
    }
    
    .right::after {
        left: -10px;
    }
    
    .timeline-content {
        padding: 20px 30px;
        background-color: white;
        position: relative;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Message de bienvenue lors du premier chargement
if "first_load" not in st.session_state:
    st.session_state["first_load"] = True
    st.balloons()
    st.success("Bienvenue dans l'application CRM Relations Entreprises!")

# Ajouter un mode de démonstration pour précharger des données
if st.sidebar.checkbox("Mode démonstration", value=True):
    st.sidebar.info("Le mode démonstration est activé. Des données fictives sont chargées pour vous permettre de tester l'application.")
else:
    st.sidebar.warning("Le mode démonstration est désactivé. Vous utilisez vos propres données.")

# Ajouter une fonction de recherche globale dans la barre latérale
st.sidebar.markdown("---")
st.sidebar.markdown("<div class='sidebar-header'>Recherche globale</div>", unsafe_allow_html=True)
search_query = st.sidebar.text_input("Rechercher une entreprise, un contact...", key="global_search")

if search_query:
    # Recherche dans les entreprises
    entreprises_results = entreprises_df[
        entreprises_df["nom"].str.contains(search_query, case=False) |
        entreprises_df["contact_principal"].str.contains(search_query, case=False) |
        entreprises_df["email"].str.contains(search_query, case=False) |
        entreprises_df["ville"].str.contains(search_query, case=False)
    ]
    
    # Recherche dans les offres
    offres_results = offres_df[
        offres_df["titre"].str.contains(search_query, case=False) |
        offres_df["entreprise_nom"].str.contains(search_query, case=False) |
        offres_df["description"].str.contains(search_query, case=False)
    ]
    
    # Afficher les résultats dans une fenêtre modale
    with st.sidebar.expander(f"Résultats ({len(entreprises_results) + len(offres_results)})", expanded=True):
        if len(entreprises_results) > 0:
            st.markdown("#### Entreprises")
            for _, entreprise in entreprises_results.iterrows():
                st.markdown(f"[{entreprise['nom']}](#) - {entreprise['secteur']}")
        
        if len(offres_results) > 0:
            st.markdown("#### Offres")
            for _, offre in offres_results.iterrows():
                st.markdown(f"[{offre['titre']}](#) - {offre['entreprise_nom']}")
        
        if len(entreprises_results) == 0 and len(offres_results) == 0:
            st.info("Aucun résultat trouvé.")

# Ajouter une fonction de sauvegarde/restauration dans les paramètres
if page == "⚙️ Paramètres":
    # Ajouter un nouvel onglet pour la sauvegarde
    tab1, tab2, tab3, tab4 = st.tabs(["Exportation des données", "Importation des données", "Sauvegarde", "À propos"])
    
    with tab3:
        st.subheader("Sauvegarde et restauration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Sauvegarde complète")
            
            if st.button("Créer une sauvegarde"):
                # Créer un buffer en mémoire pour stocker le zip
                buffer = io.BytesIO()
                
                # Dans un environnement réel, on zipperait les fichiers
                # Pour cette démonstration, on simule simplement
                
                # Générer un lien de téléchargement
                now = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.markdown(
                    f'<a href="#" download="backup_{now}.zip">📥 Télécharger la sauvegarde</a>',
                    unsafe_allow_html=True
                )
                
                st.success("Sauvegarde créée avec succès!")
        
        with col2:
            st.markdown("### Restauration")
            
            uploaded_backup = st.file_uploader("Choisir un fichier de sauvegarde", type=["zip"])
            
            if uploaded_backup is not None:
                if st.button("Restaurer les données"):
                    # Dans un environnement réel, on extrairait les fichiers du zip
                    # Pour cette démonstration, on simule simplement
                    
                    st.success("Restauration effectuée avec succès!")
                    st.warning("L'application va redémarrer...")

# Ajouter une fonctionnalité de prospection automatisée dans le tableau de bord
if page == "📊 Tableau de bord":
    # Ajouter une section pour les suggestions de prospection
    st.markdown("<h2 class='sub-header'>Suggestions de prospection</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Entreprises à contacter en priorité")
        
        # Identifier les entreprises qui n'ont pas été contactées depuis longtemps
        today = datetime.now()
        entreprises_df["jours_dernier_contact"] = (today - pd.to_datetime(entreprises_df["dernier_contact"])).dt.days
        
        # Filtrer les entreprises partenaires actives non contactées depuis plus de 30 jours
        entreprises_a_contacter = entreprises_df[
            (entreprises_df["statut"] == "Partenaire actif") &
            (entreprises_df["jours_dernier_contact"] > 30)
        ].sort_values(by="jours_dernier_contact", ascending=False)
        
        if len(entreprises_a_contacter) > 0:
            for _, entreprise in entreprises_a_contacter.head(5).iterrows():
                st.markdown(f"""
                **{entreprise['nom']}** - {entreprise['jours_dernier_contact']} jours  
                Contact: {entreprise['contact_principal']} | {entreprise['email']}
                """)
            
            if len(entreprises_a_contacter) > 5:
                st.info(f"+ {len(entreprises_a_contacter) - 5} autres entreprises à contacter")
        else:
            st.info("Aucune entreprise partenaire active n'a besoin d'être contactée en priorité.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Opportunités de conversion")
        
        # Identifier les prospects avec un niveau d'engagement élevé
        prospects_a_convertir = entreprises_df[
            (entreprises_df["statut"] == "Prospect") &
            (entreprises_df["niveau_engagement"] >= 4)
        ].sort_values(by="niveau_engagement", ascending=False)
        
        if len(prospects_a_convertir) > 0:
            for _, prospect in prospects_a_convertir.head(5).iterrows():
                st.markdown(f"""
                **{prospect['nom']}** - Engagement: {prospect['niveau_engagement']}/5  
                Contact: {prospect['contact_principal']} | {prospect['email']}
                """)
            
            if len(prospects_a_convertir) > 5:
                st.info(f"+ {len(prospects_a_convertir) - 5} autres prospects à convertir")
        else:
            st.info("Aucun prospect n'est prêt à être converti en partenaire pour le moment.")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Ajouter une fonctionnalité de génération de rapport dans l'analyse des données
if page == "📈 Analyse des données":
    st.sidebar.markdown("---")
    st.sidebar.markdown("<div class='sidebar-header'>Générer un rapport</div>", unsafe_allow_html=True)
    
    rapport_type = st.sidebar.selectbox(
        "Type de rapport",
        ["Rapport mensuel", "Rapport trimestriel", "Rapport annuel", "Rapport personnalisé"]
    )
    
    if st.sidebar.button("Générer"):
        with st.spinner("Génération du rapport en cours..."):
            # Simuler un délai de traitement
            time.sleep(2)
            
            st.sidebar.success(f"Rapport {rapport_type} généré avec succès!")
            st.sidebar.markdown(
                f'<a href="#" download="rapport_{rapport_type.lower().replace(" ", "_")}.pdf">📥 Télécharger le rapport</a>',
                unsafe_allow_html=True
            )

# Ajouter une fonctionnalité de tableau de bord personnalisable
if page == "📊 Tableau de bord":
    # Ajouter un nouvel onglet pour la personnalisation
    st.markdown("<h2 class='sub-header'>Personnalisation du tableau de bord</h2>", unsafe_allow_html=True)
    
    if st.button("Personnaliser mon tableau de bord"):
        st.session_state["show_dashboard_customization"] = True
    
    if st.session_state.get("show_dashboard_customization", False):
        with st.expander("Options de personnalisation", expanded=True):
            st.markdown("### Sélectionnez les widgets à afficher")
            
            col1, col2 = st.columns(2)
            
            with col1:
                widget1 = st.checkbox("Statistiques générales", value=True)
                widget2 = st.checkbox("Dernières activités", value=True)
                widget3 = st.checkbox("Actions requises", value=True)
            
            with col2:
                widget4 = st.checkbox("Répartition par secteur", value=True)
                widget5 = st.checkbox("Interactions par type", value=True)
                widget6 = st.checkbox("Suggestions de prospection", value=True)
            
            st.markdown("### Disposition")
            layout = st.radio("Choisir la disposition", ["Standard", "Compact", "Étendu"])
            
            st.markdown("### Thème de couleurs")
            theme = st.selectbox("Choisir un thème", ["Défaut", "Sombre", "Clair", "Professionnel"])
            
            if st.button("Appliquer les modifications"):
                st.success("Les modifications ont été appliquées avec succès!")
                st.session_state["show_dashboard_customization"] = False
                st.experimental_rerun()

# Ajouter une fonctionnalité d'intégration de calendrier dans les événements
if page == "📅 Événements":
    # Ajouter un nouvel onglet pour le calendrier
    tab1, tab2, tab3 = st.tabs(["Liste des événements", "Planifier un événement", "Calendrier"])
    
    with tab3:
        st.subheader("Calendrier des événements")
        
        # Simuler un calendrier simple
        mois = st.selectbox("Mois", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])
        annee = st.selectbox("Année", list(range(2023, 2026)))
        
        # Créer un calendrier mensuel
        st.markdown("<div class='highlight'>", unsafe_allow_html=True)
        
        # En-têtes des jours de la semaine
        cols = st.columns(7)
        jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        
        for i, jour in enumerate(jours):
            with cols[i]:
                st.markdown(f"<center><strong>{jour}</strong></center>", unsafe_allow_html=True)
        
        # Convertir le mois en numéro
        mois_num = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"].index(mois) + 1
        
        # Obtenir le premier jour du mois et le nombre de jours
        premier_jour, nb_jours = calendar.monthrange(annee, mois_num)
        
        # Créer les semaines
        jour = 1
        for semaine in range(6):  # Maximum 6 semaines dans un mois
            cols = st.columns(7)
            
            for i in range(7):
                with cols[i]:
                    if semaine == 0 and i < premier_jour:
                        # Jours du mois précédent
                        st.markdown("<center style='color:#ccc'>-</center>", unsafe_allow_html=True)
                    elif jour > nb_jours:
                        # Jours du mois suivant
                        st.markdown("<center style='color:#ccc'>-</center>", unsafe_allow_html=True)
                    else:
                        # Vérifier si des événements ont lieu ce jour
                        date_str = f"{annee}-{mois_num:02d}-{jour:02d}"
                        evenements_jour = evenements_df[evenements_df["date"] == date_str]
                        
                        if len(evenements_jour) > 0:
                            st.markdown(f"<center><div style='background-color:#3498db; color:white; border-radius:50%; width:30px; height:30px; line-height:30px;'>{jour}</div></center>", unsafe_allow_html=True)
                            for _, evt in evenements_jour.iterrows():
                                st.markdown(f"<center><small>{evt['nom']}</small></center>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<center>{jour}</center>", unsafe_allow_html=True)
                        
                        jour += 1
            
            # Sortir de la boucle si tous les jours ont été affichés
            if jour > nb_jours:
                break
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Option pour synchroniser avec d'autres calendriers
        st.subheader("Synchronisation")
        sync_option = st.selectbox("Synchroniser avec", ["Google Calendar", "Outlook", "Apple Calendar", "Aucun"])
        
        if sync_option != "Aucun":
            st.info(f"La synchronisation avec {sync_option} sera disponible prochainement.")

# Ajouter un système de notifications
if "notifications" not in st.session_state:
    st.session_state["notifications"] = []

if "notifications_count" not in st.session_state:
    st.session_state["notifications_count"] = 0

# Simuler quelques notifications
if len(st.session_state["notifications"]) == 0:
    st.session_state["notifications"].append({
        "title": "Suivi à effectuer",
        "message": "Vous avez 3 suivis à effectuer aujourd'hui.",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False
    })
    
    st.session_state["notifications"].append({
        "title": "Nouvel événement",
        "message": "Un nouvel événement a été planifié.",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False
    })
    
    st.session_state["notifications_count"] = 2

# Afficher un indicateur de notifications dans la barre latérale
st.sidebar.markdown("---")
st.sidebar.markdown(f"<div class='sidebar-header'>Notifications ({st.session_state['notifications_count']})</div>", unsafe_allow_html=True)

if st.session_state["notifications_count"] > 0:
    for i, notif in enumerate(st.session_state["notifications"]):
        if not notif["read"]:
            with st.sidebar.expander(f"{notif['title']} ({notif['date']})", expanded=False):
                st.write(notif["message"])
                if st.button("Marquer comme lu", key=f"notif_{i}"):
                    st.session_state["notifications"][i]["read"] = True
                    st.session_state["notifications_count"] -= 1
                    st.experimental_rerun()
else:
    st.sidebar.info("Aucune nouvelle notification.")

# Ajouter des fonctionnalités d'export avancées
if page == "⚙️ Paramètres" and tab1.id == "tab-0":
    st.subheader("Options d'exportation avancées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox("Format d'exportation", ["CSV", "Excel", "JSON"])
    
    with col2:
        export_encoding = st.selectbox("Encodage", ["UTF-8", "ISO-8859-1", "Windows-1252"])
    
    if st.button("Exporter toutes les données"):
        # Dans un environnement réel, on générerait les fichiers selon les options choisies
        st.success(f"Exportation au format {export_format} avec encodage {export_encoding} réussie!")
        st.markdown("<a href='#'>Télécharger l'archive</a>", unsafe_allow_html=True)

# Ajouter un outil d'aide et guide utilisateur
st.sidebar.markdown("---")
with st.sidebar.expander("Aide et documentation"):
    st.markdown("""
    ### Besoin d'aide ?
    
    - [Guide de démarrage rapide](#)
    - [Manuel utilisateur complet](#)
    - [Tutoriels vidéo](#)
    - [FAQ](#)
    
    ### Support
    
    Pour toute question ou assistance, contactez le support technique à l'adresse support@crm-relations.fr
    """)

# Ajouter un système de messages d'information système
system_messages = [
    "Le système sera en maintenance ce weekend entre 2h et 4h du matin.",
    "Une nouvelle mise à jour est disponible! Cliquez ici pour en savoir plus.",
    "Rappel: Pensez à sauvegarder régulièrement vos données."
]

if random.random() < 0.3:  # Afficher un message aléatoirement 30% du temps
    message = random.choice(system_messages)
    st.info(message)

# Créer un footer avec des liens utiles
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: #f8f9fa; padding: 10px; text-align: center; font-size: 0.8rem; border-top: 1px solid #ddd;">
    © 2025 Démo - CRM Relations Entreprises | <a href="#">Politique de confidentialité</a> | <a href="#">Conditions d'utilisation</a> | <a href="#">Contact</a>
</div>
""", unsafe_allow_html=True)
        