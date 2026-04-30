<template>
  <AssistantParcel :parcelId="($route.params.id as string)" />
</template>
<script setup lang="ts">
import { useRoute } from 'vue-router';
import AssistantParcel from '~/components/features/shared/assistant/AssistantParcel.vue';
const route = useRoute();
definePageMeta({ layout: 'dashboard' })
</script>
