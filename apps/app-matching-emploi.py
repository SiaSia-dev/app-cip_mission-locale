import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import matplotlib.pyplot as plt
import random
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(
    page_title="Match'Emploi - Mission Locale",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2a6d81;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #336b78;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f6f9fc;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .highlight {
        color: #2a6d81;
        font-weight: bold;
    }
    .match-score {
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
    }
    .match-high {
        background-color: #c9dfd6;
        color: #1d4954;
    }
    .match-medium {
        background-color: #f0f7f4;
        color: #336b78;
    }
    .match-low {
        background-color: #f7f7f7;
        color: #666;
    }
    .sidebar-content {
        padding: 1rem;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        color: #666;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Données simulées
@st.cache_data
def generate_dummy_data():
    # Données des jeunes
    skills = ['Communication', 'Travail d\'équipe', 'Autonomie', 'Rigueur', 'Informatique', 
              'Langues étrangères', 'Vente', 'Service client', 'Gestion de projet', 'Marketing digital']
    
    sectors = ['Commerce', 'Administratif', 'Restauration', 'Informatique', 'Industrie', 
               'Santé', 'Communication', 'Logistique', 'BTP', 'Services']
    
    contract_types = ['CDI', 'CDD', 'Alternance', 'Stage', 'Intérim']
    
    locations = ['Chartres Centre', 'Chartres Nord', 'Chartres Sud', 'Lucé', 'Mainvilliers', 
                'Luisant', 'Champhol', 'Lèves', 'Le Coudray', 'Barjouville']
    
    qualifications = ['Sans diplôme', 'CAP/BEP', 'Bac', 'Bac+2', 'Bac+3 et plus']
    
    young_people = []
    for i in range(30):
        young_skills = random.sample(skills, random.randint(3, 6))
        preferred_sectors = random.sample(sectors, random.randint(2, 4))
        preferred_contracts = random.sample(contract_types, random.randint(1, 3))
        
        young_person = {
            'id': f'J{i+1:03d}',
            'name': f'Jeune {i+1}',
            'age': random.randint(18, 26),
            'qualification': random.choice(qualifications),
            'skills': young_skills,
            'preferred_sectors': preferred_sectors,
            'preferred_contracts': preferred_contracts,
            'mobility': random.randint(5, 30),
            'preferred_location': random.choice(locations),
            'experience_years': random.randint(0, 5),
            'registration_date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
            'last_appointment': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
            'status': random.choice(['En recherche active', 'En formation', 'En emploi partiel', 'Nouveau'])
        }
        young_people.append(young_person)
    
    # Données des entreprises et offres d'emploi
    companies = []
    job_offers = []
    
    company_names = [
        'Tech Solutions', 'MarketPro', 'Restaurant Gourmet', 'Logistique Express', 
        'Bâtiment Durable', 'InfoSys', 'Santé Plus', 'Commerce Factory', 
        'Admin Services', 'Communication Créative'
    ]
    
    job_titles = {
        'Commerce': ['Vendeur', 'Responsable magasin', 'Assistant commercial'],
        'Administratif': ['Assistant administratif', 'Secrétaire', 'Agent d\'accueil'],
        'Restauration': ['Serveur', 'Cuisinier', 'Commis de cuisine'],
        'Informatique': ['Développeur', 'Technicien informatique', 'Support technique'],
        'Industrie': ['Opérateur de production', 'Technicien de maintenance', 'Magasinier'],
        'Santé': ['Aide-soignant', 'Agent de service hospitalier', 'Secrétaire médical'],
        'Communication': ['Assistant communication', 'Community manager', 'Chargé d\'événementiel'],
        'Logistique': ['Préparateur de commandes', 'Cariste', 'Agent logistique'],
        'BTP': ['Maçon', 'Électricien', 'Peintre'],
        'Services': ['Agent d\'entretien', 'Auxiliaire de vie', 'Agent de sécurité']
    }
    
    for i in range(10):
        company = {
            'id': f'E{i+1:03d}',
            'name': company_names[i],
            'sector': random.choice(sectors),
            'size': random.choice(['TPE', 'PME', 'Grande entreprise']),
            'location': random.choice(locations),
            'contact_person': f'Contact {i+1}',
            'last_contact': (datetime.now() - timedelta(days=random.randint(1, 120))).strftime('%Y-%m-%d'),
            'partnership_level': random.choice(['Nouveau', 'Régulier', 'Partenaire privilégié'])
        }
        companies.append(company)
        
        # Génération des offres d'emploi pour chaque entreprise
        for j in range(random.randint(1, 3)):
            sector = company['sector']
            job_title = random.choice(job_titles.get(sector, ['Employé']))
            
            required_skills = random.sample(skills, random.randint(2, 5))
            
            job_offer = {
                'id': f'O{i+1:03d}_{j+1}',
                'company_id': company['id'],
                'company_name': company['name'],
                'title': job_title,
                'sector': sector,
                'contract_type': random.choice(contract_types),
                'required_qualification': random.choice(qualifications),
                'required_skills': required_skills,
                'required_experience': random.choice([0, 1, 2, 3]),
                'location': company['location'],
                'publication_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                'status': random.choice(['Active', 'Pourvu', 'En attente']),
                'applications': random.randint(0, 10)
            }
            job_offers.append(job_offer)
    
    return pd.DataFrame(young_people), pd.DataFrame(companies), pd.DataFrame(job_offers)

# Charger les données simulées
young_people_df, companies_df, job_offers_df = generate_dummy_data()

# Fonction pour calculer le score de matching
def calculate_match_score(young_person, job_offer):
    score = 0
    max_score = 0
    
    # Match sur les compétences
    skill_overlap = set(young_person['skills']).intersection(set(job_offer['required_skills']))
    skill_score = len(skill_overlap) / max(len(job_offer['required_skills']), 1) * 40
    score += skill_score
    max_score += 40
    
    # Match sur le secteur
    sector_match = job_offer['sector'] in young_person['preferred_sectors']
    sector_score = 20 if sector_match else 0
    score += sector_score
    max_score += 20
    
    # Match sur le type de contrat
    contract_match = job_offer['contract_type'] in young_person['preferred_contracts']
    contract_score = 15 if contract_match else 0
    score += contract_score
    max_score += 15
    
    # Match sur la qualification
    qualification_levels = {'Sans diplôme': 0, 'CAP/BEP': 1, 'Bac': 2, 'Bac+2': 3, 'Bac+3 et plus': 4}
    young_qual_level = qualification_levels.get(young_person['qualification'], 0)
    job_qual_level = qualification_levels.get(job_offer['required_qualification'], 0)
    
    # Le jeune peut avoir une qualification supérieure à celle requise
    qualification_score = 10 if young_qual_level >= job_qual_level else 0
    score += qualification_score
    max_score += 10
    
    # Match sur l'expérience
    experience_match = young_person['experience_years'] >= job_offer['required_experience']
    experience_score = 10 if experience_match else 0
    score += experience_score
    max_score += 10
    
    # Match sur la localisation et la mobilité
    same_location = young_person['preferred_location'] == job_offer['location']
    location_score = 5 if same_location else 0
    score += location_score
    max_score += 5
    
    # Calcul du pourcentage final
    match_percentage = (score / max_score) * 100 if max_score > 0 else 0
    return round(match_percentage)

# Interface utilisateur Streamlit
def main():
    # Sidebar pour la navigation
    st.sidebar.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.sidebar.image("./img/hand-819279_640.jpg", width=150)
    st.sidebar.title("Match'Emploi")
    
    # Menu de navigation
    page = st.sidebar.radio(
        "Navigation",
        ["Tableau de bord", "Recherche de jeunes", "Offres d'emploi", "Matching", "Suivi des mises en relation"]
    )
    
    st.sidebar.markdown('<hr>', unsafe_allow_html=True)
    st.sidebar.subheader("Filtres rapides")
    
    # Filtres généraux dans la sidebar
    if page in ["Recherche de jeunes", "Matching"]:
        statut_filter = st.sidebar.multiselect(
            "Statut des jeunes",
            options=["En recherche active", "En formation", "En emploi partiel", "Nouveau"],
            default=["En recherche active"]
        )
    
    if page in ["Offres d'emploi", "Matching"]:
        sector_filter = st.sidebar.multiselect(
            "Secteurs d'activité",
            options=sorted(job_offers_df['sector'].unique()),
            default=[]
        )
        
        contract_filter = st.sidebar.multiselect(
            "Types de contrat",
            options=sorted(job_offers_df['contract_type'].unique()),
            default=[]
        )
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Contenu principal selon la page sélectionnée
    if page == "Tableau de bord":
        display_dashboard()
    elif page == "Recherche de jeunes":
        display_young_people_search(statut_filter)
    elif page == "Offres d'emploi":
        display_job_offers(sector_filter, contract_filter)
    elif page == "Matching":
        display_matching(statut_filter, sector_filter, contract_filter)
    elif page == "Suivi des mises en relation":
        display_follow_up()
    
    # Footer
    st.markdown("""
    <div class="footer">
        Match'Emploi © 2025 - Développé par Alexia Fontaine pour la Mission Locale de l'Arrondissement de Chartres
    </div>
    """, unsafe_allow_html=True)

# Fonctions pour afficher chaque page
def display_dashboard():
    st.markdown('<h1 class="main-header">Tableau de bord</h1>', unsafe_allow_html=True)
    
    # Statistiques rapides
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Jeunes en recherche active", len(young_people_df[young_people_df['status'] == 'En recherche active']))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Offres d'emploi actives", len(job_offers_df[job_offers_df['status'] == 'Active']))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Entreprises partenaires", len(companies_df))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Mises en relation ce mois", 37)  # Valeur simulée
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h2 class="sub-header">Répartition par secteur d\'activité</h2>', unsafe_allow_html=True)
        sector_counts = job_offers_df['sector'].value_counts().reset_index()
        sector_counts.columns = ['Secteur', 'Nombre d\'offres']
        fig = px.pie(sector_counts, values='Nombre d\'offres', names='Secteur', hole=0.4,
           color_discrete_sequence=px.colors.sequential.Teal)
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True, key="pie_sectors")  # Ajout d'une clé unique ici
    
    with col2:
        st.markdown('<h2 class="sub-header">Offres par type de contrat</h2>', unsafe_allow_html=True)
        contract_counts = job_offers_df['contract_type'].value_counts().reset_index()
        contract_counts.columns = ['Type de contrat', 'Nombre d\'offres']
        fig = px.bar(contract_counts, x='Type de contrat', y='Nombre d\'offres',
           color='Nombre d\'offres', color_continuous_scale='Teal')
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True, key="bar_contracts")  # Ajout d'une clé unique ici
    
    # Activité récente
    st.markdown('<h2 class="sub-header">Activité récente</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Dernières offres d'emploi")
        recent_offers = job_offers_df.sort_values('publication_date', ascending=False).head(5)
        for _, offer in recent_offers.iterrows():
            st.markdown(f"""
            **{offer['title']}** - {offer['company_name']}  
            *{offer['contract_type']} | {offer['location']} | {offer['publication_date']}*
            """)
            st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Derniers jeunes inscrits")
        recent_young = young_people_df.sort_values('registration_date', ascending=False).head(5)
        for _, young in recent_young.iterrows():
            st.markdown(f"""
            **{young['name']}** - {young['age']} ans  
            *{young['qualification']} | {', '.join(young['preferred_sectors'][:2])} | {young['status']}*
            """)
            st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def display_young_people_search(status_filter):
    st.markdown('<h1 class="main-header">Recherche de jeunes</h1>', unsafe_allow_html=True)
    
    # Filtres supplémentaires
    col1, col2, col3 = st.columns(3)
    
    with col1:
        age_range = st.slider("Âge", min_value=18, max_value=30, value=(18, 26))
    
    with col2:
        qualification_filter = st.multiselect(
            "Qualification",
            options=sorted(young_people_df['qualification'].unique()),
            default=[]
        )
    
    with col3:
        preferred_sectors_filter = st.multiselect(
            "Secteurs préférés",
            options=sorted(set([sector for sublist in young_people_df['preferred_sectors'] for sector in sublist])),
            default=[]
        )
    
    # Application des filtres
    filtered_young_people = young_people_df.copy()
    
    if status_filter:
        filtered_young_people = filtered_young_people[filtered_young_people['status'].isin(status_filter)]
    
    filtered_young_people = filtered_young_people[
        (filtered_young_people['age'] >= age_range[0]) & 
        (filtered_young_people['age'] <= age_range[1])
    ]
    
    if qualification_filter:
        filtered_young_people = filtered_young_people[filtered_young_people['qualification'].isin(qualification_filter)]
    
    if preferred_sectors_filter:
        filtered_young_people = filtered_young_people[
            filtered_young_people['preferred_sectors'].apply(
                lambda sectors: any(sector in preferred_sectors_filter for sector in sectors)
            )
        ]
    
    # Affichage des résultats
    st.markdown(f"<h2 class='sub-header'>{len(filtered_young_people)} jeunes correspondant aux critères</h2>", unsafe_allow_html=True)
    
    # Bouton d'exportation
    if not filtered_young_people.empty:
        col1, col2 = st.columns([4, 1])
        with col2:
            st.download_button(
                label="Exporter les résultats",
                data=filtered_young_people.to_csv(index=False).encode('utf-8'),
                file_name="jeunes_filtres.csv",
                mime="text/csv"
            )
    
    # Affichage des profils filtrés
    for i, (_, young) in enumerate(filtered_young_people.iterrows()):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
        
        with col1 if i % 2 == 0 else col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            st.markdown(f"<h3>{young['name']} ({young['age']} ans)</h3>", unsafe_allow_html=True)
            st.markdown(f"**Qualification:** {young['qualification']}")
            st.markdown(f"**Expérience:** {young['experience_years']} an(s)")
            st.markdown(f"**Statut:** {young['status']}")
            st.markdown(f"**Secteurs préférés:** {', '.join(young['preferred_sectors'])}")
            st.markdown(f"**Compétences:** {', '.join(young['skills'])}")
            st.markdown(f"**Contrats recherchés:** {', '.join(young['preferred_contracts'])}")
            st.markdown(f"**Mobilité:** {young['mobility']} km autour de {young['preferred_location']}")
            
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.button(f"Voir le profil complet", key=f"view_young_{young['id']}")
            with col_b:
                st.button(f"Contacter", key=f"contact_young_{young['id']}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# Modification à apporter à la fonction display_job_offers

def display_job_offers(sector_filter, contract_filter):
    st.markdown('<h1 class="main-header">Offres d\'emploi</h1>', unsafe_allow_html=True)
    
    # Initialiser un état pour suivre l'offre sélectionnée pour la proposition de candidats
    if 'selected_job_for_candidates' not in st.session_state:
        st.session_state.selected_job_for_candidates = None
    
    # Filtres supplémentaires
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Statut de l'offre",
            options=sorted(job_offers_df['status'].unique()),
            default=["Active"]
        )
    
    with col2:
        location_filter = st.multiselect(
            "Localisation",
            options=sorted(job_offers_df['location'].unique()),
            default=[]
        )
    
    with col3:
        qualification_filter = st.multiselect(
            "Qualification requise",
            options=sorted(job_offers_df['required_qualification'].unique()),
            default=[]
        )
    
    # Application des filtres
    filtered_job_offers = job_offers_df.copy()
    
    if status_filter:
        filtered_job_offers = filtered_job_offers[filtered_job_offers['status'].isin(status_filter)]
    
    if sector_filter:
        filtered_job_offers = filtered_job_offers[filtered_job_offers['sector'].isin(sector_filter)]
    
    if contract_filter:
        filtered_job_offers = filtered_job_offers[filtered_job_offers['contract_type'].isin(contract_filter)]
    
    if location_filter:
        filtered_job_offers = filtered_job_offers[filtered_job_offers['location'].isin(location_filter)]
    
    if qualification_filter:
        filtered_job_offers = filtered_job_offers[filtered_job_offers['required_qualification'].isin(qualification_filter)]
    
    # Affichage des résultats
    st.markdown(f"<h2 class='sub-header'>{len(filtered_job_offers)} offres correspondant aux critères</h2>", unsafe_allow_html=True)
    
    # Bouton d'exportation
    if not filtered_job_offers.empty:
        col1, col2 = st.columns([4, 1])
        with col2:
            st.download_button(
                label="Exporter les offres",
                data=filtered_job_offers.to_csv(index=False).encode('utf-8'),
                file_name="offres_filtrees.csv",
                mime="text/csv"
            )
    
    # Affichage des offres filtrées
    for i, (_, job) in enumerate(filtered_job_offers.iterrows()):
        if i % 2 == 0:
            col1, col2 = st.columns(2)
        
        with col1 if i % 2 == 0 else col2:
            job_id = job['id']  # Récupérer l'ID de l'offre
            status_color = {
                'Active': '#c9dfd6',
                'Pourvu': '#f0f0f0',
                'En attente': '#f9f9f9'
            }
            
            st.markdown(f"""
            <div class="card" style="border-left: 5px solid {status_color.get(job['status'], '#ddd')}">
                <h3>{job['title']} - {job['company_name']}</h3>
                <p><strong>Secteur:</strong> {job['sector']} | <strong>Contrat:</strong> {job['contract_type']}</p>
                <p><strong>Qualification requise:</strong> {job['required_qualification']} | <strong>Expérience:</strong> {job['required_experience']} an(s)</p>
                <p><strong>Localisation:</strong> {job['location']} | <strong>Publication:</strong> {job['publication_date']}</p>
                <p><strong>Compétences requises:</strong> {', '.join(job['required_skills'])}</p>
                <p><strong>Statut:</strong> {job['status']} | <strong>Candidatures:</strong> {job['applications']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Utiliser des boutons Streamlit réels pour les actions
            col_a, col_b = st.columns(2)
            with col_a:
                st.button("Voir l'offre complète", key=f"view_offer_{job_id}")
            with col_b:
                # Utiliser un unique identifiant pour chaque bouton basé sur l'ID de l'offre
                if st.button("Proposer des candidats", key=f"propose_{job_id}"):
                    st.session_state.selected_job_for_candidates = job_id

    # Afficher les candidats correspondants si une offre est sélectionnée
    if st.session_state.selected_job_for_candidates:
        # Récupérer les détails de l'offre sélectionnée
        selected_job = job_offers_df[job_offers_df['id'] == st.session_state.selected_job_for_candidates]
        
        if not selected_job.empty:
            job_offer = selected_job.iloc[0]
            
            # Délimiteur visuel
            st.markdown("---")
            
            # Titre de la section
            st.markdown(f"<h2 class='sub-header'>Candidats pour: {job_offer['title']} - {job_offer['company_name']}</h2>", unsafe_allow_html=True)
            
            # Bouton pour fermer la section de candidats
            if st.button("Fermer", key="close_candidates"):
                st.session_state.selected_job_for_candidates = None
                st.rerun()
            
            # Trouver des candidats correspondants
            active_young_people = young_people_df[young_people_df['status'] == 'En recherche active'].copy()
            
            # Calcul des scores de matching
            match_results = []
            for _, young in active_young_people.iterrows():
                score = calculate_match_score(young, job_offer)
                match_results.append({
                    'young_id': young['id'],
                    'name': young['name'],
                    'age': young['age'],
                    'qualification': young['qualification'],
                    'experience_years': young['experience_years'],
                    'skills': young['skills'],
                    'preferred_location': young['preferred_location'],
                    'match_score': score
                })
            
            if match_results:
                match_df = pd.DataFrame(match_results).sort_values('match_score', ascending=False)
                
                # Affichage des candidats correspondants
                for _, match in match_df.head(5).iterrows():
                    score = match['match_score']
                    score_class = "match-high" if score >= 70 else "match-medium" if score >= 40 else "match-low"
                    
                    st.markdown(f"""
                    <div class="card" style="display: flex; align-items: center;">
                        <div style="flex: 0.2;">
                            <div class="match-score {score_class}">{score}%</div>
                        </div>
                        <div style="flex: 0.8; padding-left: 15px;">
                            <h3>{match['name']} ({match['age']} ans)</h3>
                            <p><strong>Qualification:</strong> {match['qualification']} | <strong>Expérience:</strong> {match['experience_years']} an(s)</p>
                            <p><strong>Compétences:</strong> {', '.join(match['skills'][:3])}...</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Graphique des meilleurs candidats
                st.markdown('<h3>Top 10 des candidats</h3>', unsafe_allow_html=True)
                top_candidates = match_df.head(10).sort_values('match_score')
                fig = px.bar(
                    top_candidates, 
                    x='match_score', 
                    y='name',
                    orientation='h',
                    color='match_score',
                    color_continuous_scale='Teal',
                    labels={'match_score': 'Score de matching (%)', 'name': 'Candidat'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True, key=f"bar_candidates_for_job_{job_offer['id']}")
            else:
                st.info("Aucun candidat ne correspond aux critères de l'offre.")

def display_matching(status_filter, sector_filter, contract_filter):
    st.markdown('<h1 class="main-header">Matching Jeunes - Offres</h1>', unsafe_allow_html=True)
    
    # Interface de sélection d'un jeune ou d'une offre
    tabs = st.tabs(["Trouver des offres pour un jeune", "Trouver des candidats pour une offre"])
    
    # Onglet 1: Trouver des offres pour un jeune
    with tabs[0]:
        # Filtre des jeunes
        filtered_young_people = young_people_df.copy()
        if status_filter:
            filtered_young_people = filtered_young_people[filtered_young_people['status'].isin(status_filter)]
        
        if filtered_young_people.empty:
            st.warning("Aucun jeune ne correspond aux filtres sélectionnés. Veuillez modifier vos critères de recherche.")
            return
        
        # Sélection d'un jeune
        selected_young = st.selectbox(
            "Sélectionner un jeune",
            options=filtered_young_people['id'].tolist(),
            format_func=lambda x: f"{filtered_young_people[filtered_young_people['id'] == x]['name'].iloc[0]} ({x})"
        )
        
        young_person = filtered_young_people[filtered_young_people['id'] == selected_young].iloc[0]
        
        # Affichage des détails du jeune sélectionné
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.image("https://via.placeholder.com/150x150.png?text=Profile", width=150)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"<h3>{young_person['name']} ({young_person['age']} ans)</h3>", unsafe_allow_html=True)
            st.markdown(f"**Qualification:** {young_person['qualification']}")
            st.markdown(f"**Expérience:** {young_person['experience_years']} an(s)")
            st.markdown(f"**Statut:** {young_person['status']}")
            st.markdown(f"**Secteurs préférés:** {', '.join(young_person['preferred_sectors'])}")
            st.markdown(f"**Compétences:** {', '.join(young_person['skills'])}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Trouver des offres correspondantes
        active_offers = job_offers_df[job_offers_df['status'] == 'Active'].copy()
        
        if sector_filter:
            active_offers = active_offers[active_offers['sector'].isin(sector_filter)]
        
        if contract_filter:
            active_offers = active_offers[active_offers['contract_type'].isin(contract_filter)]
        
        # Calcul des scores de matching
        match_results = []
        for _, offer in active_offers.iterrows():
            score = calculate_match_score(young_person, offer)
            match_results.append({
                'offer_id': offer['id'],
                'company_name': offer['company_name'],
                'title': offer['title'],
                'sector': offer['sector'],
                'contract_type': offer['contract_type'],
                'location': offer['location'],
                'match_score': score
            })
        
        # Vérifier si match_results contient des données avant de créer le DataFrame
        if match_results:
            match_df = pd.DataFrame(match_results).sort_values('match_score', ascending=False)
            
            # Affichage des résultats
            if not match_df.empty:
                st.markdown('<h2 class="sub-header">Offres correspondantes</h2>', unsafe_allow_html=True)
                
                for _, match in match_df.head(5).iterrows():
                    score = match['match_score']
                    score_class = "match-high" if score >= 70 else "match-medium" if score >= 40 else "match-low"
                    
                    st.markdown(f"""
                    <div class="card" style="display: flex; align-items: center;">
                        <div style="flex: 0.2;">
                            <div class="match-score {score_class}">{score}%</div>
                        </div>
                        <div style="flex: 0.8; padding-left: 15px;">
                            <h3>{match['title']} - {match['company_name']}</h3>
                            <p><strong>Secteur:</strong> {match['sector']} | <strong>Contrat:</strong> {match['contract_type']}</p>
                            <p><strong>Localisation:</strong> {match['location']}</p>
                            <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
                                <button style="background-color: #2a6d81; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-right: 10px;">Voir l'offre</button>
                                <button style="background-color: #90c5b5; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Proposer ce candidat</button>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Graphique de répartition des scores
                st.markdown('<h3>Répartition des scores de matching</h3>', unsafe_allow_html=True)
                fig = px.histogram(match_df, x='match_score', nbins=10, color_discrete_sequence=['#2a6d81'])
                fig.update_layout(
                    xaxis_title="Score de matching (%)",
                    yaxis_title="Nombre d'offres",
                    bargap=0.1
                )
                st.plotly_chart(fig, use_container_width=True, key="histogram_offers")
        else:
            st.info("Aucune offre ne correspond aux critères sélectionnés.")
    
    # Onglet 2: Trouver des candidats pour une offre
    with tabs[1]:
        # Filtre des offres
        filtered_job_offers = job_offers_df.copy()
        
        if 'Active' in filtered_job_offers['status'].unique():
            filtered_job_offers = filtered_job_offers[filtered_job_offers['status'] == 'Active']
        
        if sector_filter:
            filtered_job_offers = filtered_job_offers[filtered_job_offers['sector'].isin(sector_filter)]
        
        if contract_filter:
            filtered_job_offers = filtered_job_offers[filtered_job_offers['contract_type'].isin(contract_filter)]
        
        if filtered_job_offers.empty:
            st.warning("Aucune offre active ne correspond aux filtres sélectionnés. Veuillez modifier vos critères de recherche.")
            return
        
        # Sélection d'une offre
        selected_offer = st.selectbox(
            "Sélectionner une offre",
            options=filtered_job_offers['id'].tolist(),
            format_func=lambda x: f"{filtered_job_offers[filtered_job_offers['id'] == x]['title'].iloc[0]} - {filtered_job_offers[filtered_job_offers['id'] == x]['company_name'].iloc[0]} ({x})"
        )
        
        # Vérifier si l'offre sélectionnée existe encore dans les données filtrées
        if selected_offer in filtered_job_offers['id'].values:
            job_offer = filtered_job_offers[filtered_job_offers['id'] == selected_offer].iloc[0]
            
            # Affichage des détails de l'offre sélectionnée
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"<h3>{job_offer['title']} - {job_offer['company_name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"**Secteur:** {job_offer['sector']} | **Contrat:** {job_offer['contract_type']}")
            st.markdown(f"**Qualification requise:** {job_offer['required_qualification']} | **Expérience:** {job_offer['required_experience']} an(s)")
            st.markdown(f"**Localisation:** {job_offer['location']} | **Publication:** {job_offer['publication_date']}")
            st.markdown(f"**Compétences requises:** {', '.join(job_offer['required_skills'])}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Trouver des candidats correspondants
            active_young_people = young_people_df[young_people_df['status'] == 'En recherche active'].copy()
            
            if status_filter:
                active_young_people = active_young_people[active_young_people['status'].isin(status_filter)]
            
            # Calcul des scores de matching
            match_results = []
            for _, young in active_young_people.iterrows():
                score = calculate_match_score(young, job_offer)
                match_results.append({
                    'young_id': young['id'],
                    'name': young['name'],
                    'age': young['age'],
                    'qualification': young['qualification'],
                    'experience_years': young['experience_years'],
                    'skills': young['skills'],
                    'preferred_location': young['preferred_location'],
                    'match_score': score
                })
            
            # Vérifier si match_results contient des données avant de créer le DataFrame
            if match_results:
                match_df = pd.DataFrame(match_results).sort_values('match_score', ascending=False)
                
                # Affichage des résultats
                if not match_df.empty:
                    st.markdown('<h2 class="sub-header">Candidats correspondants</h2>', unsafe_allow_html=True)
                    
                    for _, match in match_df.head(5).iterrows():
                        score = match['match_score']
                        score_class = "match-high" if score >= 70 else "match-medium" if score >= 40 else "match-low"
                        
                        st.markdown(f"""
                        <div class="card" style="display: flex; align-items: center;">
                            <div style="flex: 0.2;">
                                <div class="match-score {score_class}">{score}%</div>
                            </div>
                            <div style="flex: 0.8; padding-left: 15px;">
                                <h3>{match['name']} ({match['age']} ans)</h3>
                                <p><strong>Qualification:</strong> {match['qualification']} | <strong>Expérience:</strong> {match['experience_years']} an(s)</p>
                                <p><strong>Compétences:</strong> {', '.join(match['skills'][:3])}...</p>
                                <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
                                    <button style="background-color: #2a6d81; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-right: 10px;">Voir le profil</button>
                                    <button style="background-color: #90c5b5; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Proposer cette offre</button>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Graphique des meilleurs candidats
                    top_candidates = match_df.head(10).sort_values('match_score')
                    if not top_candidates.empty:
                        st.markdown('<h3>Top 10 des candidats</h3>', unsafe_allow_html=True)
                        fig = px.bar(
                            top_candidates, 
                            x='match_score', 
                            y='name',
                            orientation='h',
                            color='match_score',
                            color_continuous_scale='Teal',
                            labels={'match_score': 'Score de matching (%)', 'name': 'Candidat'}
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True, key="bar_candidates")
            else:
                st.info("Aucun candidat ne correspond aux critères de l'offre.")
        else:
            st.error("L'offre sélectionnée n'est plus disponible. Veuillez en choisir une autre.")

def display_follow_up():
    st.markdown('<h1 class="main-header">Suivi des mises en relation</h1>', unsafe_allow_html=True)
    
    # Création de données fictives pour les mises en relation
    @st.cache_data
    def generate_matching_data():
        matches = []
        statuses = ['Proposé', 'Entretien programmé', 'Entretien réalisé', 'Embauche', 'Refus employeur', 'Refus candidat']
        
        # Vérifier que nous avons des données pour générer des matchs
        if young_people_df.empty or job_offers_df.empty:
            return pd.DataFrame()  # Retourner un DataFrame vide
        
        for i in range(20):
            # Utiliser random.randint pour éviter les index out of bounds
            if len(young_people_df) > 0:
                young_idx = random.randint(0, len(young_people_df) - 1)
                young_id = young_people_df.iloc[young_idx]['id']
                young_name = young_people_df.iloc[young_idx]['name']
            else:
                continue  # S'il n'y a pas de jeunes, on passe à l'itération suivante
            
            if len(job_offers_df) > 0:
                job_idx = random.randint(0, len(job_offers_df) - 1)
                offer_id = job_offers_df.iloc[job_idx]['id']
                offer_title = job_offers_df.iloc[job_idx]['title']
                company_name = job_offers_df.iloc[job_idx]['company_name']
            else:
                continue  # S'il n'y a pas d'offres, on passe à l'itération suivante
            
            match_date = (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d')
            status = random.choice(statuses)
            last_update = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            
            matches.append({
                'id': f'M{i+1:03d}',
                'young_id': young_id,
                'young_name': young_name,
                'offer_id': offer_id,
                'offer_title': offer_title,
                'company_name': company_name,
                'match_date': match_date,
                'status': status,
                'last_update': last_update,
                'notes': f"Note de suivi pour la mise en relation {i+1}" if random.random() > 0.5 else ""
            })
        
        return pd.DataFrame(matches)
    
    # Générer les données de suivi
    matches_df = generate_matching_data()
    
    # Vérifier si nous avons des données à afficher
    if matches_df.empty:
        st.warning("Aucune donnée de suivi disponible. Veuillez d'abord créer des mises en relation.")
        return
    
    # Filtres
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_filter = st.multiselect(
            "Statut de la mise en relation",
            options=sorted(matches_df['status'].unique()),
            default=[]
        )
    
    with col2:
        date_range = st.date_input(
            "Période de mise en relation",
            value=(
                datetime.now() - timedelta(days=30),
                datetime.now()
            ),
            format="YYYY-MM-DD"
        )
    
    with col3:
        search_term = st.text_input("Rechercher (candidat ou entreprise)", "")
    
    # Application des filtres
    filtered_matches = matches_df.copy()
    
    if status_filter:
        filtered_matches = filtered_matches[filtered_matches['status'].isin(status_filter)]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_matches = filtered_matches[
            (pd.to_datetime(filtered_matches['match_date']) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(filtered_matches['match_date']) <= pd.to_datetime(end_date))
        ]
    
    if search_term:
        filtered_matches = filtered_matches[
            (filtered_matches['young_name'].str.contains(search_term, case=False)) |
            (filtered_matches['company_name'].str.contains(search_term, case=False)) |
            (filtered_matches['offer_title'].str.contains(search_term, case=False))
        ]
    
    # Vérifier si nous avons des données après filtrage
    if filtered_matches.empty:
        st.info("Aucune mise en relation ne correspond aux critères de filtrage.")
        return
    
    # Affichage des statistiques
    col1, col2, col3, col4 = st.columns(4)
    
    total_matches = len(filtered_matches)
    successful_matches = len(filtered_matches[filtered_matches['status'] == 'Embauche'])
    ongoing_matches = len(filtered_matches[filtered_matches['status'].isin(['Proposé', 'Entretien programmé', 'Entretien réalisé'])])
    rejected_matches = len(filtered_matches[filtered_matches['status'].isin(['Refus employeur', 'Refus candidat'])])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Total des mises en relation", total_matches)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Embauches réalisées", successful_matches)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("En cours", ongoing_matches)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.metric("Refus", rejected_matches)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualisation de l'état des mises en relation
    col1, col2 = st.columns(2)
    
    with col1:
        status_counts = filtered_matches['status'].value_counts().reset_index()
        status_counts.columns = ['Statut', 'Nombre']
        if not status_counts.empty:
            fig = px.pie(status_counts, values='Nombre', names='Statut', hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Teal)
            fig.update_layout(title="Répartition par statut")
            st.plotly_chart(fig, use_container_width=True, key="pie_status")
    
    with col2:
        # Convertir les dates en datetime pour le traitement
        filtered_matches['match_date'] = pd.to_datetime(filtered_matches['match_date'])
        matches_by_month = filtered_matches.groupby(filtered_matches['match_date'].dt.strftime('%Y-%m')).size().reset_index()
        matches_by_month.columns = ['Mois', 'Nombre']
        if not matches_by_month.empty:
            fig = px.line(matches_by_month, x='Mois', y='Nombre', markers=True,
                        color_discrete_sequence=['#2a6d81'])
            fig.update_layout(title="Évolution mensuelle des mises en relation")
            st.plotly_chart(fig, use_container_width=True, key="line_monthly")
    
    # Tableau des mises en relation
    st.markdown('<h2 class="sub-header">Liste des mises en relation</h2>', unsafe_allow_html=True)
    
    # Options d'affichage
    col1, col2 = st.columns([4, 1])
    with col2:
        st.download_button(
            label="Exporter les données",
            data=filtered_matches.to_csv(index=False).encode('utf-8'),
            file_name="suivi_mises_en_relation.csv",
            mime="text/csv"
        )
    
    # Tableau interactif
    for _, match in filtered_matches.iterrows():
        status_color = {
            'Proposé': '#f0f7f4',
            'Entretien programmé': '#c9dfd6',
            'Entretien réalisé': '#90c5b5',
            'Embauche': '#2a6d81',
            'Refus employeur': '#f7e4e4',
            'Refus candidat': '#f7e4e4'
        }
        
        st.markdown(f"""
        <div class="card" style="border-left: 5px solid {status_color.get(match['status'], '#ddd')};">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <h3>{match['young_name']} → {match['offer_title']} ({match['company_name']})</h3>
                </div>
                <div>
                    <span style="background-color: {status_color.get(match['status'], '#ddd')}; padding: 5px 10px; border-radius: 20px; font-size: 0.8rem;">{match['status']}</span>
                </div>
            </div>
            <p><strong>Date de mise en relation:</strong> {match['match_date']} | <strong>Dernière mise à jour:</strong> {match['last_update']}</p>
            <p><strong>Notes:</strong> {match['notes'] if match['notes'] else 'Aucune note'}</p>
            <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
                <button style="background-color: #2a6d81; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; margin-right: 10px;">Mettre à jour le statut</button>
                <button style="background-color: #90c5b5; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Ajouter une note</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Lancement de l'application
if __name__ == "__main__":
    main()        