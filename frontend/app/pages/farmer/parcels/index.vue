<template>
  <div class="p-8 bg-[#f8fafc] min-h-screen text-[#022c22]">
    
    <!-- ===== HEADER ===== -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-4xl font-bold mb-2">Parcelles</h1>
        <p class="text-[14px] text-gray-500">Gérez et suivez l'ensemble de vos parcelles agricoles en temps réel.</p>
      </div>
      <NuxtLink to="/farmer/parcels/create" class="flex items-center gap-2 px-6 py-3 bg-[#013b28] text-white rounded-[12px] text-[13px] font-medium hover:bg-[#022c22] transition-colors shadow-sm">
        <i class="bx bx-plus text-lg"></i>
        Nouvelle Parcelle
      </NuxtLink>
    </div>

    <!-- ===== STATS ROW ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <!-- PARCELLES EXPLOITÉES -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100/50 flex items-center justify-between">
        <div>
          <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-2">Parcelles exploitées</p>
          <p class="text-[34px] font-bold text-[#013b28]">{{ exploiteesCount }}</p>
        </div>
        <div class="w-12 h-12 bg-[#bbf7d0]/60 rounded-xl flex items-center justify-center text-emerald-700 text-2xl">
          <i class="bx bx-tractor"></i>
        </div>
      </div>
      
      <!-- PARCELLES NON EXPLOITÉES -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100/50 flex items-center justify-between">
        <div>
          <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-2">Parcelles non exploitées</p>
          <p class="text-[34px] font-bold text-[#013b28]">{{ nonExploiteesCount }}</p>
        </div>
        <div class="w-12 h-12 bg-[#f1ebd9] rounded-xl flex items-center justify-center text-[#8e8574] text-2xl">
          <i class="bx bx-grid-alt"></i>
        </div>
      </div>
      
      <!-- PARCELLES EN POSSESSION -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100/50 flex items-center justify-between">
        <div>
          <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-2">Parcelles en possession</p>
          <p class="text-[34px] font-bold text-[#013b28]">{{ fields.length }}</p>
        </div>
        <div class="w-12 h-12 bg-[#a7f3d0]/60 rounded-xl flex items-center justify-center text-emerald-700 text-2xl">
          <i class="bx bx-map-alt"></i>
        </div>
      </div>
    </div>

    <!-- ===== MIDDLE ROW ===== -->
    <div class="grid grid-cols-1 xl:grid-cols-12 gap-6 mb-8">
      
      <!-- Recommandations (col-span-7) -->
      <div class="xl:col-span-7 bg-white rounded-2xl p-7 shadow-sm border border-gray-100/50 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-8">
            <h2 class="text-xl font-semibold">Recommandations</h2>
            <i class="bx bx-bulb text-xl text-emerald-600"></i>
          </div>
          
          <div class="space-y-6">
            <template v-if="dashboardAlerts.length > 0">
              <div v-for="(alert, idx) in dashboardAlerts.slice(0, 2)" :key="idx" class="flex gap-4">
                <div class="w-11 h-11 bg-[#d1fae5] rounded-[10px] flex items-center justify-center text-emerald-600 text-xl shrink-0">
                  <i :class="alert.type.includes('HYDRO') || alert.type.includes('EAU') || alert.type.includes('PLUIE') ? 'bx bx-drop' : 'bx bx-test-tube'"></i>
                </div>
                <div>
                  <h3 class="text-[14px] font-semibold mb-1">{{ alert.type }}</h3>
                  <p class="text-[13px] text-gray-500">{{ alert.message }} <span v-if="alert.action">({{ alert.action }})</span></p>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="text-sm text-gray-400 text-center py-4">Aucune recommandation pour le moment.</div>
            </template>
          </div>
        </div>
        
        <button class="w-full mt-8 py-3 bg-[#f8fafc] text-[#013b28] font-semibold text-[13px] rounded-xl hover:bg-gray-100 transition-colors">
          Voir les analyses
        </button>
      </div>

      <!-- Météo (col-span-5) -->
      <div class="xl:col-span-5 bg-white rounded-2xl p-7 shadow-sm border border-gray-100/50 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-xl font-semibold">Météo</h2>
            <select v-model="selectedWeatherParcel" class="px-3 py-1.5 bg-[#f8fafc] border-gray-100 text-[#013b28] text-[12px] font-semibold rounded-lg focus:ring-1 focus:ring-emerald-500 outline-none cursor-pointer max-w-[150px] truncate">
              <option v-for="field in fields" :key="field.fieldId" :value="field.fieldId">{{ field.parcel_name }}</option>
            </select>
          </div>
          <p class="text-[12px] text-gray-400 mb-6">Météo de la parcelle sélectionnée</p>

          <template v-if="isWeatherLoading">
            <div class="text-center py-10 text-sm text-gray-400">Chargement de la météo...</div>
          </template>
          <template v-else-if="todayWeather">
            <div class="flex items-center justify-between mb-8">
              <div>
                <div class="flex items-end gap-2 mb-3">
                  <span class="text-4xl font-bold tracking-tight">{{ todayWeather.day ? Math.round(todayWeather.day.maxtemp_c) : '--' }}°C</span>
                  <span class="text-gray-500 text-[14px] mb-1">/ {{ todayWeather.day?.condition?.text || 'Ensoleillé' }}</span>
                </div>
                <div class="flex items-center gap-4 text-[12px] text-gray-500 font-medium">
                  <span class="flex items-center gap-1.5"><i class="bx bx-droplet text-gray-400"></i> {{ todayWeather.day?.avghumidity || '--' }}%</span>
                  <span class="flex items-center gap-1.5"><i class="bx bx-wind text-gray-400"></i> {{ todayWeather.day ? Math.round(todayWeather.day.maxwind_kph) : '--' }} km/h</span>
                </div>
              </div>
              <div class="w-20 h-20 bg-[#ecfdf5] rounded-[16px] flex items-center justify-center text-emerald-500 text-4xl shadow-inner border border-emerald-50/50">
                <span class="filter drop-shadow-sm">{{ getWeatherIcon(todayWeather.day?.condition?.text) }}</span>
              </div>
            </div>

            <div class="grid grid-cols-5 gap-2 mb-2">
              <div v-for="(day, idx) in upcomingForecasts" :key="idx" class="flex flex-col items-center text-center">
                <span class="text-[10px] font-bold text-gray-400 uppercase mb-2">{{ new Date(day.date).toLocaleDateString('fr-FR', { weekday: 'short' }).replace('.', '') }}</span>
                <span class="text-emerald-500 text-xl mb-2">{{ getWeatherIcon(day.day?.condition?.text) }}</span>
                <span class="text-[13px] font-bold">{{ Math.round(day.day?.maxtemp_c) }}°</span>
                <span class="text-[11px] text-gray-400">{{ Math.round(day.day?.mintemp_c) }}°</span>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="text-center py-10 text-sm text-gray-400">Données météo non disponibles</div>
          </template>
        </div>
        
        <div class="text-right mt-4">
          <a href="#" class="text-[13px] font-semibold text-[#013b28] hover:underline">Voir plus</a>
        </div>
      </div>
    </div>

    <!-- ===== BOTTOM TABLE ===== -->
    <div class="bg-white rounded-[20px] shadow-sm border border-gray-100/50 overflow-hidden">
      <!-- Toolbar -->
      <div class="p-5 flex flex-col md:flex-row items-center justify-between gap-4 border-b border-gray-50/80">
        <div class="relative w-full md:w-80">
          <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-[18px] text-gray-400"></i>
          <input
            v-model="filters.parcel_name"
            type="text"
            placeholder="Rechercher une parcelle..."
            class="w-full pl-11 pr-4 py-2.5 bg-[#f8fafc] border-none rounded-xl text-[13px] font-medium focus:ring-1 focus:ring-emerald-500 outline-none placeholder:text-gray-400"
          />
        </div>
        
        <div class="flex items-center gap-3 w-full md:w-auto">
          <button class="flex items-center gap-2 px-4 py-2 bg-[#f8fafc] text-gray-600 text-[12px] font-semibold rounded-lg hover:bg-gray-100 transition-colors">
            <i class="bx bx-filter text-[14px]"></i> Statut
          </button>
          <button class="flex items-center gap-2 px-4 py-2 bg-[#f8fafc] text-gray-600 text-[12px] font-semibold rounded-lg hover:bg-gray-100 transition-colors">
            <i class="bx bx-leaf text-[14px]"></i> Culture
          </button>
          <button class="flex items-center gap-2 px-4 py-2 bg-[#f8fafc] text-gray-600 text-[12px] font-semibold rounded-lg hover:bg-gray-100 transition-colors">
            <i class="bx bx-sort text-[14px]"></i> Trier
          </button>
        </div>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse min-w-[700px]">
          <thead>
            <tr class="bg-[#f8fafc]">
              <th class="px-6 py-4 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100">Nom de la parcelle</th>
              <th class="px-6 py-4 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100">Superficie (ha)</th>
              <th class="px-6 py-4 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100">Date de création</th>
              <th class="px-6 py-4 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100 text-right">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50/80">
            <template v-if="isLoading">
               <tr>
                 <td colspan="4" class="px-6 py-10 text-center text-sm text-gray-400">Chargement...</td>
               </tr>
            </template>
            <template v-else-if="paginatedFields.length > 0">
              <tr v-for="field in paginatedFields" :key="field.fieldId" class="hover:bg-[#f8fafc]/50 transition-colors">
                <td class="px-6 py-5">
                  <span class="text-[13px] font-semibold text-[#022c22]">{{ field.parcel_name }}</span>
                </td>
                <td class="px-6 py-5">
                  <span class="text-[13px] text-gray-600">{{ field.area ? field.area + ' ha' : '4.5 ha' }}</span>
                </td>
                <td class="px-6 py-5">
                  <span class="text-[13px] text-gray-500">{{ field.created_at ? formatDate(field.created_at) : '12 Mars 2024' }}</span>
                </td>
                <td class="px-6 py-5 text-right">
                  <div class="flex items-center justify-end gap-4 text-gray-600">
                    <NuxtLink :to="`/farmer/parcels/show/${field.fieldId}`" class="hover:text-[#013b28] transition-colors"><i class="bx bx-show text-[18px]"></i></NuxtLink>
                    <NuxtLink :to="`/farmer/parcels/edit/${field.fieldId}`" class="hover:text-emerald-600 transition-colors"><i class="bx bx-pencil text-[18px]"></i></NuxtLink>
                    <button @click="confirmDelete(field.fieldId)" class="hover:text-rose-500 transition-colors"><i class="bx bx-trash text-[18px]"></i></button>
                  </div>
                </td>
              </tr>
            </template>
            <tr v-else>
              <td colspan="4" class="px-6 py-12 text-center text-gray-500 text-[13px]">
                Aucune parcelle trouvée.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Footer -->
      <div v-if="totalPages > 0" class="px-6 py-4 bg-[#f8fafc] border-t border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-4">
        <span class="text-[11px] font-semibold text-gray-500 uppercase tracking-wide">
          Affichage {{ Math.min((currentPage - 1) * rowsPerPage + 1, filteredFields.length) }}-{{ Math.min(currentPage * rowsPerPage, filteredFields.length) }} sur {{ filteredFields.length }} parcelles
        </span>
        <div class="flex items-center gap-1.5">
          <button @click="prevPage" :disabled="currentPage === 1" class="w-8 h-8 flex items-center justify-center bg-transparent border border-gray-200 rounded-lg text-gray-500 hover:border-emerald-500 disabled:opacity-30 disabled:hover:border-gray-200 transition-colors">
            <i class="bx bx-chevron-left text-lg"></i>
          </button>
          
          <template v-for="page in visiblePages" :key="page">
            <button v-if="page !== '...'" @click="goToPage(page)" 
                    :class="['w-8 h-8 flex items-center justify-center rounded-lg text-[12px] font-bold transition-colors', currentPage === page ? 'bg-[#013b28] text-white border-none' : 'bg-transparent border border-gray-200 text-gray-600 hover:border-emerald-500']">
              {{ page }}
            </button>
            <span v-else class="px-1 text-gray-400 text-xs">...</span>
          </template>
          
          <button @click="nextPage" :disabled="currentPage === totalPages" class="w-8 h-8 flex items-center justify-center bg-transparent border border-gray-200 rounded-lg text-gray-500 hover:border-emerald-500 disabled:opacity-30 disabled:hover:border-gray-200 transition-colors">
            <i class="bx bx-chevron-right text-lg"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- ===== OVERLAYS & MODALS ===== -->
    <!-- Delete Modal -->
    <Teleport to="body">
      <transition name="pop-notification">
        <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center z-[100] px-4">
          <div class="absolute inset-0 bg-[#022c22]/80 backdrop-blur-sm" @click="cancelDelete"></div>
          <div class="bg-white rounded-3xl p-10 w-full max-w-sm text-center shadow-2xl relative z-10">
            <div class="w-20 h-20 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto mb-6">
              <i class="bx bx-trash text-4xl text-rose-500"></i>
            </div>
            <h3 class="text-xl font-bold text-[#022c22] mb-3">{{ t("deleteParcel") }}</h3>
            <p class="text-gray-500 text-[13px] mb-8">{{ t("textConfirmDeleteParcel") }}</p>
            <div class="flex flex-col gap-3">
              <button @click="deleteParcelConfirmed" class="w-full py-3.5 bg-rose-500 text-white rounded-xl font-bold text-[12px] uppercase tracking-wider hover:bg-rose-600 transition-all">
                {{ t("deletePermanently") }}
              </button>
              <button @click="cancelDelete" class="w-full py-3.5 bg-gray-50 text-gray-500 rounded-xl font-bold text-[12px] uppercase tracking-wider hover:bg-gray-100 transition-all">
                {{ t("cancel") }}
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>

    <!-- Notifications -->
    <transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-8 right-8 z-[120] w-full max-w-sm">
        <div :class="['bg-white rounded-2xl shadow-xl p-5 flex items-center gap-4 border border-gray-50', notification.type === 'success' ? 'border-l-4 border-l-emerald-500' : 'border-l-4 border-l-rose-500']">
          <div :class="['w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0', notification.type === 'success' ? 'bg-emerald-50 text-emerald-500' : 'bg-rose-50 text-rose-500']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div class="flex-1">
            <p class="text-[13px] font-bold text-[#022c22]">{{ notification.message }}</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

// ===== INITIALISATION =====
const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const { t: nuxtT } = useI18n();

const t = (key: string) => nuxtT(`dashboard.${key}`);

definePageMeta({ layout: "dashboard" });

// ===== ÉTAT DE L'UI =====
const isLoading = ref(false);

const notification = reactive({
  visible: false,
  message: "",
  type: "success" as "success" | "error",
});

const showNotification = (
  message: string,
  type: "success" | "error" = "success",
  duration = 3000
) => {
  notification.message = message;
  notification.type = type;
  notification.visible = true;
  setTimeout(() => (notification.visible = false), duration);
};

// ===== FILTRES ET DONNÉES =====
const filters = reactive({
  owner: "",
  parcel_name: "",
});

const fields = ref<any[]>([]);
const rowsPerPage = ref(4);
const currentPage = ref(1);

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" })
}

const weatherIconMap: Record<string, string> = {
  "Soleil":                                   "☀️",
  "Clair":                                    "☀️",
  "Partiellement nuageux":                    "⛅",
  "Nuageux":                                  "☁️",
  "Couvert":                                  "☁️",
  "Brume":                                    "🌫️",
  "Brouillard épars":                         "🌫️",
  "Brouillard givrant épars":                 "🌫️",
  "Bruine légère éparse":                     "🌦️",
  "Bruine légère":                            "🌦️",
  "Bruine verglaçante éparse":                "🌦️",
  "Forte bruine verglaçante":                 "🌧️",
  "Pluie légère éparse":                      "🌦️",
  "Pluie légère":                             "🌦️",
  "Pluie modérée par moments":                "🌧️",
  "Pluie modérée":                            "🌧️",
  "Forte pluie par moments":                  "🌧️",
  "Forte pluie":                              "🌧️",
  "Légère pluie verglaçante":                 "🌧️",
  "Pluie verglaçante modérée ou forte":       "🌧️",
  "Légère chute de neige fondante":           "❄️",
  "Chute de neige fondante modérée ou forte": "❄️",
  "Neige légère éparse":                      "❄️",
  "Neige légère":                             "❄️",
  "Neige modérée éparse":                     "❄️",
  "Neige modérée":                            "❄️",
  "Forte neige éparse":                       "❄️",
  "Forte neige":                              "❄️",
  "Grésil léger":                             "❄️",
  "Grésil modéré ou fort":                    "❄️",
  "Averses de pluie légère":                  "🌦️",
  "Averses de pluie modérée ou forte":        "🌧️",
  "Averses torrentielles":                    "🌧️",
  "Averses de neige fondante légère":         "❄️",
  "Averses de neige fondante modérées ou fortes": "❄️",
  "Averses de neige légère":                  "❄️",
  "Averses de neige modérées ou fortes":      "❄️",
  "Averses de grésil légère":                 "❄️",
  "Averses de grésil modérées ou fortes":     "❄️",
  "Foyers orageux à proximité":               "⛈️",
  "Grêle":                                    "⛈️",
  "Averses de grêle légère":                  "⛈️",
  "Averses de grêle modérée ou forte":        "⛈️",
  "Pluie légère éparse avec orages":          "⛈️",
  "Pluie modérée ou forte avec orages":       "⛈️",
  "Neige légère éparse avec orages":          "⛈️",
  "Neige modérée ou forte avec orages":       "⛈️",
}

const getWeatherIcon = (condition?: string) => {
  if (!condition) return "☀️"
  if (weatherIconMap[condition]) return weatherIconMap[condition]

  const c = condition.toLowerCase()
  if (c.includes("orage") || c.includes("grêle") || c.includes("tempête")) return "⛈️"
  if (c.includes("neige") || c.includes("grésil") || c.includes("blizzard"))  return "❄️"
  if (c.includes("averse") || c.includes("bruine"))                            return "🌦️"
  if (c.includes("pluie"))                                                     return "🌧️"
  if (c.includes("brouillard") || c.includes("brume"))                         return "🌫️"
  if (c.includes("nuageux") || c.includes("couvert"))                          return "☁️"
  if (c.includes("éclaircies") || c.includes("partiellement"))                 return "⛅"
  if (c.includes("soleil") || c.includes("ensoleillé") || c.includes("clair")) return "☀️"

  return "☀️"
}

const dashboardWeather = ref<any>(null)
const dashboardAlerts = ref<any[]>([])
const exploiteesCount = computed(() => fields.value.filter(f => f.is_exploited).length);
const nonExploiteesCount = computed(() => fields.value.filter(f => !f.is_exploited).length);

const selectedWeatherParcel = ref<string>("")
const isWeatherLoading = ref(false)

const upcomingForecasts = computed(() => {
  if (!dashboardWeather.value?.forecast?.forecastday) return [];
  const todayStr = new Date().toISOString().split('T')[0] ?? "";
  const list = dashboardWeather.value.forecast.forecastday;
  return list.filter((d: any) => d.date >= todayStr).slice(0, 5);
});

const todayWeather = computed(() => {
  return upcomingForecasts.value.length > 0 ? upcomingForecasts.value[0] : null;
});

async function loadWeatherForParcel(parcelId: string) {
  if (!parcelId) return;
  isWeatherLoading.value = true;
  try {
    const fullData: any = await apiFetch(`/api/parcels/${parcelId}/full_data/`);
    if (fullData?.weather_data) {
      dashboardWeather.value = fullData.weather_data.data;
      dashboardAlerts.value = fullData.weather_data.alerts || [];
    } else {
      dashboardWeather.value = null;
      dashboardAlerts.value = [];
    }
  } catch (e) {
    console.error("Impossible de charger les données météo globales", e);
    dashboardWeather.value = null;
    dashboardAlerts.value = [];
  } finally {
    isWeatherLoading.value = false;
  }
}

watch(selectedWeatherParcel, (newVal) => {
  if (newVal) loadWeatherForParcel(newVal);
});

// ===== CHARGEMENT DES DONNÉES =====
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    alert(nuxtT("dashboard.mustBeConnected"));
    return;
  }

  isLoading.value = true;
  try {
    const data: any = await apiFetch('/api/parcels/');
    const records = data?.results || data || [];

    fields.value = records.map((parcel: any, idx: number) => ({
      id:          idx + 1,
      fieldId:     parcel.uuid,
      owner:       "Moi",
      parcel_name: parcel.parcel_name,
      area:        parcel.area_ha ?? null,
      created_at:  parcel.created_at ?? null,
      latitude:    parcel.parcel_points?.[0]?.latitude ?? null,
      longitude:   parcel.parcel_points?.[0]?.longitude ?? null,
      is_exploited:parcel.is_exploited ?? false,
    }));


    // Charger les recommandations et météo pour la première parcelle par défaut
    if (fields.value.length > 0) {
      selectedWeatherParcel.value = fields.value[0].fieldId;
    }
  } catch (err) {
    console.error("Erreur réseau:", err);
    showNotification(nuxtT("dashboard.errorLoadingParcels"), "error");
  } finally {
    isLoading.value = false;
  }
});

// ===== COMPUTED =====
const filteredFields = computed(() =>
  fields.value.filter(
    (f) =>
      f.owner.toLowerCase().includes(filters.owner.toLowerCase()) &&
      f.parcel_name.toLowerCase().includes(filters.parcel_name.toLowerCase())
  )
);

const totalPages = computed(() =>
  Math.max(1, Math.ceil(filteredFields.value.length / rowsPerPage.value))
);

const paginatedFields = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value;
  return filteredFields.value.slice(start, start + rowsPerPage.value);
});

const visiblePages = computed(() => {
  const pages: (number | string)[] = [];
  const total = totalPages.value;
  const current = currentPage.value;

  if (total <= 5) {
    for (let i = 1; i <= total; i++) pages.push(i);
  } else if (current <= 3) {
    pages.push(1, 2, 3, 4, "...", total);
  } else if (current >= total - 2) {
    pages.push(1, "...", total - 3, total - 2, total - 1, total);
  } else {
    pages.push(1, "...", current - 1, current, current + 1, "...", total);
  }
  return pages;
});

// ===== ACTIONS =====
function resetFilters() {
  filters.owner = "";
  filters.parcel_name = "";
  currentPage.value = 1;
}

const showDeleteModal = ref(false);
const parcelToDelete = ref<string | null>(null);

function confirmDelete(uuid: string) {
  parcelToDelete.value = uuid;
  showDeleteModal.value = true;
}

function cancelDelete() {
  showDeleteModal.value = false;
  parcelToDelete.value = null;
}

async function deleteParcelConfirmed() {
  if (!parcelToDelete.value) return;

  if (!authStore.isAuthenticated) {
    alert(nuxtT("dashboard.mustBeConnected"));
    return;
  }

  isLoading.value = true;

  try {
    await apiFetch(`/api/parcels/${parcelToDelete.value}/`, {
      method: "DELETE",
    });

    fields.value = fields.value.filter((f) => f.fieldId !== parcelToDelete.value);

    if (paginatedFields.value.length === 0 && currentPage.value > 1) {
      currentPage.value--;
    }

    showDeleteModal.value = false;
    parcelToDelete.value = null;
    showNotification(nuxtT("dashboard.parcelDeletedSuccess"), "success");

  } catch (err) {
    console.error(err);
    showNotification(nuxtT("dashboard.parcelDeleteFailed"), "error");
  } finally {
    isLoading.value = false;
  }
}

// ===== PAGINATION =====
function prevPage() {
  if (currentPage.value > 1) currentPage.value--;
}

function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++;
}

function goToPage(page: number | string) {
  if (typeof page === "number") currentPage.value = page;
}
</script>

<style scoped>
.pop-notification-enter-active,
.pop-notification-leave-active {
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from,
.pop-notification-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}
</style>
