import { onMounted, ref } from "vue"
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const { apiFetch } = useApi()
const authStore = useAuthStore()
const alerts = ref([])
const activeAlerts = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  if (!authStore.isAuthenticated) return;

  try {
    const [allRes, activeRes] = await Promise.all([
      apiFetch("/api/agricultural-alerts/"),
      apiFetch("/api/agricultural-alerts/active_alerts/")
    ])

    alerts.value = allRes as any
    activeAlerts.value = activeRes as any

  } catch (err) {
    error.value = "Erreur de chargement des données."
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>

<pre class="bg-black text-green-400 p-4 rounded-xl text-sm overflow-x-auto">
{{ JSON.stringify(alerts, null, 2) }}
</pre>

<pre class="bg-black text-yellow-300 p-4 rounded-xl text-sm overflow-x-auto">
{{ JSON.stringify(activeAlerts, null, 2) }}
</pre>

  <div class="p-6 space-y-10">
    <h1 class="text-2xl font-bold">📢 Alerts Dashboard</h1>

    <div v-if="loading" class="text-gray-500">Chargement...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <!-- 1️⃣ Toutes les alertes -->
    <section>
      <h2 class="text-xl font-semibold mb-3">Toutes les alertes</h2>

      <div class="grid gap-4">
        <div
          v-for="a in alerts"
          :key="a.id"
          class="p-4 border rounded-xl bg-gray-50 shadow"
        >
          <h3 class="font-bold">{{ a.alert_type }} — {{ a.severity }}</h3>
          <p>{{ a.message }}</p>
          <p class="text-sm text-gray-600">Recommandation : {{ a.recommendation }}</p>
          <p class="text-sm">📍 Parcelle : {{ a.parcel_name }}</p>
          <p class="text-xs text-gray-500">📅 {{ a.alert_date }}</p>
        </div>
      </div>
    </section>

    <!-- 2️⃣ Alertes actives -->
    <section>
      <h2 class="text-xl font-semibold mb-3">Alertes Actives 🔥</h2>

      <div class="grid gap-4">
        <div
          v-for="a in activeAlerts"
          :key="a.id"
          class="p-4 border rounded-xl bg-red-50 shadow"
        >
          <h3 class="font-bold">{{ a.alert_type }} — {{ a.severity }}</h3>
          <p>{{ a.message }}</p>
          <p class="text-sm text-gray-700">Recommandation : {{ a.recommendation }}</p>
        </div>
      </div>
    </section>
  </div>
</template>
