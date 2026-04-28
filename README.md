# SmartSaha - Plateforme d'Agriculture de Précision

Bienvenue dans le projet **SmartSaha**, une solution complète intégrée pour l'agriculture de précision. Ce projet combine une interface utilisateur moderne et une API robuste pour optimiser la gestion des exploitations agricoles.

---

## 🏗️ Architecture du Projet

Le projet est divisé en deux parties principales :

1.  **[Frontend](./frontend)** : Développé avec **Nuxt 4**, il gère l'interface utilisateur, la cartographie interactive et les tableaux de bord.
2.  **[Backend](./backend)** : Développé avec **Django**, il fournit une API REST pour la gestion des données (cultures, parcelles, météo, etc.).

---

## 🚀 Installation Rapide

Suivez ces étapes pour installer et lancer le projet localement.

### 1. Clonage du projet
```bash
git clone https://github.com/Mandroro/smartsaha-plateforme-agriculture.git
cd smartsaha-plateforme-agriculture
```

### 2. Configuration du Backend
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate 
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env # Configurez vos accès DB dans ce fichier
python manage.py migrate
python manage.py runserver
```
*Le backend sera accessible sur `http://127.0.0.1:8000/`.*

### 3. Configuration du Frontend
Ouvrez un nouveau terminal :
```bash
cd frontend
npm install
cp .env.example .env # Assurez-vous que l'URL de l'API pointe vers le backend
npm run dev
```
*Le frontend sera accessible sur `http://localhost:3000/`.*

---

## 🛠️ Technologies Utilisées

- **Frontend** : Nuxt 4, Vue 3, Tailwind CSS, Leaflet, Chart.js, Pinia.
- **Backend** : Django, Django REST Framework, PostgreSQL.

---

## 📖 Documentations Spécifiques

Pour plus de détails sur chaque module, consultez leurs README respectifs :
- [Documentation Frontend](./frontend/README.md)
- [Documentation Backend](./backend/README.md)

---

## 📧 Contact & Support

Site web : [www.smart-saha.com](https://www.smart-saha.com)
