<template>
  <div class="relative min-h-screen">
    <!-- Overlay de chargement Premium (Splash) -->
    <AppSplash :show="showSplash" />

    <!-- Overlay de chargement Fonctionnel (Spinner) -->
    <AppSpinner :show="showSpinner" />

    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>


<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";
import { onMounted, ref, computed } from "vue";
import { useRoute } from "vue-router";
import AppSplash from "~/components/ui/AppSplash.vue";
import AppSpinner from "~/components/ui/AppSpinner.vue";

const authStore = useAuthStore();
const { apiFetch } = useApi();
const route = useRoute();

// États de chargement
const splashMinTimeReached = ref(false);
const isInitialized = computed(() => authStore.isInitialized);

// Logique : Splash au premier démarrage sur la landing, Spinner sur les liens directs/rechargements
// On utilise une regex pour détecter la racine même avec un préfixe de langue (ex: /fr/ ou /)
const isRootPath = computed(() => /^\/(\w{2}\/)?$/.test(route.path));
const showSplash = computed(() => !isInitialized.value && isRootPath.value);
const showSpinner = computed(() => !isInitialized.value && !isRootPath.value);

onMounted(async () => {
  // 1. Démarrer le chrono pour l'effet "Premium Splash" (minimum 1.5s)
  setTimeout(() => {
    splashMinTimeReached.value = true;
  }, 1800);

  // 2. Initialisation Auth
  await new Promise(resolve => setTimeout(resolve, 500));
  
  if (authStore.isAuthenticated && authStore.uuid) {
    try {
      const userData: any = await apiFetch(`/api/users/${authStore.uuid}/`);
      authStore.setUserData({
        username: userData.username,
        spaces: userData.spaces,
      });
    } catch (e) {
      console.error("Auth initialization failed:", e);
      await authStore.clearUserData();
    }
  }
  
  // 3. Finalisation (On attend aussi le temps minimum du splash si on est au début)
  const finishInit = () => authStore.setInitialized(true);
  
  if (isRootPath.value) {
    // Si on est sur le splash, on attend la fin de l'animation
    const checkSplash = setInterval(() => {
      if (splashMinTimeReached.value) {
        clearInterval(checkSplash);
        finishInit();
      }
    }, 100);
  } else {
    finishInit();
  }
});

useHead({
  title: "SmartSaha – Agriculture intelligente, durable et connectée à Madagascar",
  meta: [
    {
      name: "description",
      content:
        "SmartSaha est une plateforme d’agriculture intelligente à Madagascar. Elle aide les agriculteurs à recevoir des recommandations personnalisées sur la santé des sols, les conditions météo, la végétation et les risques environnementaux. SmartSaha intègre aussi un marketplace agricole et un assistant agronome alimenté par l’IA."
    },
    {
      name: "keywords",
      content:
        "SmartSaha, agriculture intelligente, Madagascar, agriculture de précision, marketplace agricole, traçabilité, assistant agronome IA, gestion des parcelles, prévision météo, durabilité, data management, suivi et évaluation"
    },
    {
      name: "author",
      content: "SmartSaha Team"
    },
    // Open Graph pour Facebook, WhatsApp, LinkedIn
    {
      property: "og:title",
      content: "SmartSaha – Agriculture intelligente et durable à Madagascar"
    },
    {
      property: "og:description",
      content:
        "SmartSaha relie les petits producteurs, entreprises et coopératives agricoles à des outils d’agriculture de précision, un assistant agronome IA et un marché mondial équitable pour les produits agricoles."
    },
    {
      property: "og:type",
      content: "website"
    },
    {
      property: "og:url",
      content: "https://app.smart-saha.com/"
    },
    {
      property: "og:image",
      content: "https://app.smart-saha.com/logo.png"
    },
    // Twitter Cards
    {
      name: "twitter:card",
      content: "summary_large_image"
    },
    {
      name: "twitter:title",
      content: "SmartSaha – Plateforme d’agriculture intelligente à Madagascar"
    },
    {
      name: "twitter:description",
      content:
        "Optimisez vos cultures, suivez vos parcelles et accédez à un marché mondial équitable grâce à SmartSaha, la plateforme d’agriculture intelligente pour producteurs et entreprises à Madagascar."
    },
    {
      name: "twitter:image",
      content: "https://app.smart-saha.com/logo.png"
    },
    // Langue et géolocalisation
    {
      name: "geo.region",
      content: "MG"
    },
    {
      name: "geo.placename",
      content: "Madagascar"
    },
    {
      name: "geo.position",
      content: "-18.8792;47.5079"
    }
  ],
  link: [
    {
      rel: "canonical",
      href: "https://app.smart-saha.com/"
    },
    {
      rel: "stylesheet",
      href: "https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css"
    },
    {
      rel: "stylesheet",
      href: "https://cdn.boxicons.com/fonts/basic/boxicons.min.css"
    },
    {
      rel: "stylesheet",
      href: "https://fonts.googleapis.com/css2?family=Readex+Pro:wght@400;500;700;800&display=swap"
    },
    {
      rel: "icon",
      type: "image/png",
      href: "/favicon.ico"
    },
    {
      rel: "stylesheet",
      href: "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
    }
  ],
  htmlAttrs: {
    lang: "fr"
  }
});

</script>