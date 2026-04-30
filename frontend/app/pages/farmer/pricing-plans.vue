<template>
  <section class="bg-gray-50 py-20">
    <div class="max-w-7xl mx-auto px-6 text-center">
      <h2 class="text-3xl font-bold text-gray-900 mb-4">
        Des solutions adaptées à chaque type d’agriculteur
      </h2>
      <p class="text-gray-600 mb-12">
        De l’agriculteur individuel à la grande coopérative, Smart Saha vous
        accompagne vers une agriculture intelligente et durable.
      </p>

      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div
          v-for="(plan, index) in plans"
          :key="index"
          :class="[
            'rounded-2xl shadow p-8 hover:shadow-lg transition flex flex-col justify-between border',
            plan.highlight
              ? 'bg-[#f1fcf8] border-[#10b481]'
              : 'bg-white border-gray-100',
          ]"
        >
          <div>
            <div class="text-3xl text-[#10b481] mb-4">
              <i :class="plan.icon"></i>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-4">
              {{ plan.title }}
            </h3>
            <p class="text-gray-500 mb-6">{{ plan.description }}</p>

            <p class="text-3xl font-bold mb-4 text-gray-800">
              {{ plan.price }}
              <span v-if="plan.limit" class="text-sm text-gray-500"
                >({{ plan.limit }})</span
              >
            </p>

            <ul class="text-left text-gray-700 space-y-2 mb-8">
              <li v-for="(feature, i) in plan.features" :key="i">
                <i class="bx bx-check text-[#10b481] mr-2"></i> {{ feature }}
              </li>
            </ul>
          </div>

          <button
            class="bg-[#10b481] text-white px-6 py-2 rounded-xl hover:bg-[#0b7a58] mt-auto"
          >
            {{ plan.button }}
          </button>
        </div>
      </div>

      <p class="text-gray-500 mt-12">
        💬 Vos données vous appartiennent — vous pouvez les modifier ou les
        supprimer à tout moment.
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "dashboard",
});

const plans = [
  {
    title: "Gratuit - Smallholder Farmer",
    icon: "bx bx-leaf",
    description:
      "Pour les petits producteurs souhaitant découvrir les outils Smart Saha avec des fonctionnalités essentielles.",
    price: "0 Ar",
    limit: "jusqu’à 3 parcelles",
    button: "Essayer gratuitement",
    highlight: false,
    features: [
      "Diagnostic du sol et nutriments",
      "Suivi humidité et stress hydrique",
      "Prévisions météo 7 jours (Bêta)",
      "Agronomist AI : conseils et Q&R",
      "Forecast culture (prévision des récoltes)",
      "Historique de rendement",
      "Gestion du rendement et des tâches",
      "Carte interactive et suivi des parcelles",
      "Suivi limité des feux et déforestation",
    ],
  },
  {
    title: "Standard - MVP Illimité",
    icon: "bx bx-seedling",
    description:
      "Pour les agripreneurs et producteurs souhaitant un suivi complet de leurs parcelles sans limitation.",
    price: "29 000 Ar / mois",
    button: "Passer au Standard",
    highlight: false,
    features: [
      "Toutes les fonctions du plan Gratuit",
      "Nombre illimité de parcelles",
      "Télédétection pour suivi de la santé des cultures (Bêta)",
      "Suivi des dégradations environnementales (feux et déforestation)",
      "Agronomist AI avancé",
      "Gestion complète du rendement et des tâches",
      "Rapports météo détaillés",
      "Gestion et modification des données",
    ],
  },
  {
    title: "Avancé - Entreprise / Coopérative",
    icon: "bx bx-briefcase-alt-2",
    description:
      "Pour les organisations agricoles, coopératives et suivi collectif.",
    price: "150 000 Ar / mois",
    button: "Demander une démo",
    highlight: true,
    features: [
      "Toutes les fonctions du plan Standard",
      "Gestion multi-utilisateurs",
      "Dashboard orienté Business Intelligence",
      "Cartographie avancée des parcelles",
      "IA pour aide à la décision",
      "Rapports personnalisables par parcelle ou thème",
      "Suivi feux et déforestation à grande échelle",
      "(Bêta) Quantification du carbone aboveground",
    ],
  },
  {
    title: "Premium - Institutions / ONG",
    icon: "bx bx-diamond",
    description:
      "Pour les projets institutionnels ou commerciaux souhaitant un suivi global et des certifications.",
    price: "350 000 Ar / mois",
    button: "Contactez-nous",
    highlight: false,
    features: [
      "Toutes les fonctions du plan Avancé",
      "Gestion de certifications : Bio, Fair Trade…",
      "Rapports détaillés et comparatifs multi-parcelles",
      "Tableaux de bord dynamiques",
      "Analyses IA avancées pour décisions stratégiques",
      "Accès API pour intégration externe",
      "Support prioritaire et mises à jour en priorité",
    ],
  },
];
</script>
