<!--
  components/PageHeader.vue
  ------------------------------------
  En-tête unifié pour toutes les pages de l'espace agriculteur.

  Props:
    - title    : titre principal (obligatoire)
    - subtitle : sous-titre optionnel (texte statique)
    - icon     : classe Boxicons pour l'icône du sous-titre (ex: "bx-map")

  Slots:
    - default     : surcharge le titre (pour contenu dynamique)
    - subtitle    : surcharge le sous-titre (pour contenu dynamique/i18n)
    - breadcrumb  : éléments du fil d'Ariane (NuxtLinks + séparateurs)

  Usage:
    <PageHeader title="Parcelles">
      <template #subtitle>
        <i class="bx bx-map"></i>
        3 parcelle(s)
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Parcelles</span>
      </template>
    </PageHeader>
-->
<template>
  <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-6">
    <!-- Titre + sous-titre -->
    <div>
      <h2 class="text-3xl sm:text-4xl font-black text-[#112830] tracking-tight leading-tight">
        <slot>{{ title }}</slot>
      </h2>
      <p
        v-if="subtitle || $slots.subtitle"
        class="text-gray-400 font-medium text-[13px] flex items-center gap-2 mt-2"
      >
        <i v-if="icon" :class="`bx ${icon} text-[#10b481]`"></i>
        <slot name="subtitle">{{ subtitle }}</slot>
      </p>
    </div>

    <!-- Fil d'Ariane -->
    <nav
      v-if="$slots.breadcrumb"
      class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400"
      aria-label="Breadcrumb"
    >
      <slot name="breadcrumb" />
    </nav>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title?:    string
  subtitle?: string
  icon?:     string
}>()
</script>
