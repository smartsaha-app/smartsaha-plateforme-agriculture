# SmartSaha - Backend (API d'Agriculture de Précision)

Le backend de **SmartSaha** est une API robuste développée avec **Django** et **Django REST Framework (DRF)**. Il centralise la logique métier pour la gestion des cultures, des parcelles, du suivi météorologique et de l'analyse des rendements.

---

## 🚀 Fonctionnalités Principales

- **Gestion des Utilisateurs & Groupes** : Authentification personnalisée, gestion des rôles et des organisations.
- **Agriculture de Précision** : API REST pour la gestion géospatiale des parcelles et le suivi des cultures.
- **Certifications & Conformité** : Module dédié (`suivi_evaluation`) pour la gestion des labels, audits et conformité.
- **Assistant Intelligent (IA)** : Intégration de modèles d'IA (Gemini/Mistral) pour l'aide à la décision via le module `chatbot`.
- **Tableau de Bord BI** : Services de données analytiques pour le suivi de production et les indicateurs clés.
- **Interventions & Tâches** : Planification et suivi des travaux agricoles sur le terrain.
- **Intégration Météo** : Récupération de données météorologiques en temps réel pour l'optimisation des cultures.

---

## 🛠️ Stack Technique

- **Framework** : [Django](https://www.djangoproject.com/)
- **API** : [Django REST Framework](https://www.django-rest-framework.org/)
- **Base de données** : PostgreSQL
- **IA** : Gemini, Mistral, OpenRouter integration
- **Tests** : Pytest

---

## 📂 Structure du Projet

```plaintext
backend/
├── apps/                # Coeur de la logique métier (modulaire)
│   ├── users/           # Utilisateurs et authentification
│   ├── parcels/         # Gestion géospatiale des parcelles
│   ├── crops/           # Catalogue et cycles de cultures
│   ├── tasks/           # Planification des travaux
│   ├── chatbot/         # Logique de l'assistant IA
│   ├── dashboard/       # Analyse et BI
│   └── weather/         # Services météo
├── suivi_evaluation/    # Module transversal pour les certifications
├── config/              # Configuration globale (Settings, URLs, WSGI/ASGI)
│   └── settings/        # Settings divisés par environnement (base, dev, prod)
├── data/                # Données statiques et scripts d'initialisation
└── manage.py            # Script d'administration Django
```

---

## ⚙️ Installation et Configuration

### Prérequis

- Python 3.12.0
- PostgreSQL
- Pip & venv

### Installation

1.  **Cloner le dépôt** :
    ```bash
    git clone https://github.com/Mandroro/smartsaha-plateforme-agriculture.git
    cd smartsaha-plateforme-agriculture/backend
    ```

2.  **Créer un environnement virtuel** :
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/macOS
    source venv/bin/activate
    ```

3.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurer les variables d'environnement** :
    Copiez le fichier `.env.example` vers `.env` et configurez vos accès base de données.
    ```bash
    cp .env.example .env
    ```

5.  **Migrations et Super-utilisateur** :
    ```bash
    python manage.py migrate
    python manage.py createsuperuser
    ```

### Lancement

```bash
python manage.py runserver
```

L'API sera accessible sur `http://127.0.0.1:8000/`. Documentation Swagger/ReDoc disponible selon la configuration.

---
