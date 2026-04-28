# SmartSaha - Frontend (Module Agriculture de Précision)

Bienvenue dans le frontend du projet **SmartSaha**, une plateforme dédiée à l'agriculture de précision. Développé avec **Nuxt 4** et **Vue 3**, ce module offre une interface moderne, intuitive et performante pour la gestion agricole.

Visitez la plateforme : [www.smart-saha.com](https://www.smart-saha.com)

---

## 🚀 Fonctionnalités Principales

- **Dashboard Centralisé** : Vue d'ensemble des activités, indicateurs de production et analyses BI.
- **Agriculture de Précision** : Cartographie interactive des parcelles avec gestion spatiale via Leaflet.
- **Gestion des Cultures & Parcelles** : Suivi complet du cycle de vie des cultures et organisation des unités de production.
- **Certifications & Conformité** : Suivi des labels (Bio, etc.), gestion des audits et rapports de conformité.
- **Assistant Intelligent (IA)** : Support décisionnel et aide aux agriculteurs propulsé par l'IA (Gemini/Mistral).
- **Rapports & Analyses** : Génération de rapports globaux de performance et de production.
- **Gestion de Groupes** : Administration des organisations, des membres et des rôles.
- **Planification des Tâches** : Calendrier interactif pour la gestion des interventions agricoles.
- **Suivi des Rendements** : Enregistrement précis des récoltes et analyses historiques.

---

## 🛠️ Stack Technique

- **Framework** : [Nuxt 4](https://nuxt.com/) (Vue 3)
- **State Management** : [Pinia](https://pinia.vuejs.org/)
- **Styling** : [Tailwind CSS](https://tailwindcss.com/)
- **Cartographie** : [Leaflet](https://leafletjs.com/)
- **Visualisation de données** : [Chart.js](https://www.chartjs.org/)
- **Icônes** : [Iconify](https://iconify.design/) & [Boxicons](https://boxicons.com/)

---

## 📂 Structure du Projet

```plaintext
frontend/
├── app/                 # Coeur de l'application Nuxt
│   ├── components/      # Composants groupés (ui, forms, features)
│   ├── pages/           # Pages (Cultures, Parcelles, IA, Certifications, etc.)
│   ├── layouts/         # Layouts (Dashboard, Default)
│   ├── stores/          # Gestion d'état (Pinia)
│   ├── composables/     # Logiques réutilisables (API, Auth)
│   ├── middleware/      # Middlewares de navigation
│   ├── plugins/         # Plugins Nuxt
│   └── stores/          # Stores Pinia
├── public/              # Fichiers statiques (images, favicons)
└── assets/              # Styles globaux (Tailwind, CSS)
```

---

## ⚙️ Installation et Développement

### Prérequis

- Node.js (Version recommandée : 18.x ou supérieure)
- npm, pnpm, yarn ou bun

### Configuration

1.  **Cloner le dépôt** :
    ```bash
    git clone https://github.com/Mandroro/smartsaha-plateforme-agriculture.git
    cd smartsaha-plateforme-agriculture/frontend
    ```

2.  **Installer les dépendances** :
    ```bash
    npm install
    ```

3.  **Configurer les variables d'environnement** :
    Copiez le fichier `.env.example` vers `.env` et ajustez les valeurs (API URL, etc.).
    ```bash
    cp .env.example .env
    ```

### Commandes utiles

| Action | Commande |
| :--- | :--- |
| Démarrer le serveur de dev | `npm run dev` |
| Builder pour la production | `npm run build` |
| Prévisualiser le build | `npm run preview` |
| Analyser le code (Lint) | `npm run lint` |

---

## 🔗 Liens Utiles

- [Documentation Nuxt](https://nuxt.com/docs)
- [Guide de déploiement](https://nuxt.com/docs/getting-started/deployment)
