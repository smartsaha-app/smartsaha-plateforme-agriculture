<template>
  <div class="p-8 bg-[#f8fafc] min-h-screen text-[#022c22]">
    
    <!-- ===== HEADER ===== -->
    <PageHeader title="Parcelles">
      <template #subtitle>
        <i class="bx bx-map"></i>
        Gérez et suivez l'ensemble de vos parcelles agricoles
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
    <div class="flex justify-end mb-8">
      <NuxtLink to="/farmer/parcels/create" class="flex items-center gap-2 px-6 py-3 bg-[#013b28] text-white rounded-[12px] text-[13px] font-medium hover:bg-[#022c22] transition-colors shadow-sm">
        <i class="bx bx-plus text-lg"></i>
        Nouvelle Parcelle
      </NuxtLink>
    </div>

    <!-- ===== STATS ROW ===== -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <!-- PARCELLES EXPLOITÉES -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100/50 flex items-center justify-between group hover:shadow-md transition-shadow">
        <div>
          <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-2">Parcelles exploitées</p>
          <p class="text-[34px] font-bold text-[#013b28] leading-none">{{ exploiteesCount }}</p>
          <p class="text-[11px] text-emerald-600 font-medium mt-1.5 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 inline-block"></span>
            En activité
          </p>
        </div>
        <div class="w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0 bg-gradient-to-br from-emerald-400 to-emerald-600 text-white shadow-lg shadow-emerald-200">
          <!-- Plant / sprout icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M21.88 2.15 20.08 2A18 18 0 0 0 2.23 18.91L2 20a1 1 0 0 0 .24.82A1 1 0 0 0 3 21h.17l4-.4a1 1 0 0 0 .65-.37 1 1 0 0 0 .2-.7 11.65 11.65 0 0 0-.47-2.34l2.12-2a14 14 0 0 0 6.07 1.71 1 1 0 0 0 .73-.26 1 1 0 0 0 .3-.7 13.2 13.2 0 0 0-.22-2.25l1.35-.65a1 1 0 0 0 .55-1.22A16.2 16.2 0 0 0 21.88 2.15z"/>
          </svg>
        </div>
      </div>

      <!-- PARCELLES NON EXPLOITÉES -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100/50 flex items-center justify-between group hover:shadow-md transition-shadow">
        <div>
          <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-2">Parcelles non exploitées</p>
          <p class="text-[34px] font-bold text-[#013b28] leading-none">{{ nonExploiteesCount }}</p>
          <p class="text-[11px] text-amber-500 font-medium mt-1.5 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-400 inline-block"></span>
            En attente
          </p>
        </div>
        <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0 bg-gradient-to-br from-amber-300 to-amber-500 text-white shadow-lg shadow-amber-100">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm0 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
          </svg>
        </div>
      </div>

      <!-- PARCELLES EN POSSESSION -->
      <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100/50 flex items-center justify-between group hover:shadow-md transition-shadow">
        <div>
          <p class="text-[11px] font-bold text-gray-400 uppercase tracking-wider mb-2">Parcelles en possession</p>
          <p class="text-[34px] font-bold text-[#013b28] leading-none">{{ fields.length }}</p>
          <p class="text-[11px] text-blue-500 font-medium mt-1.5 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-400 inline-block"></span>
            Total
          </p>
        </div>
        <div class="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0 bg-gradient-to-br from-blue-400 to-blue-600 text-white shadow-lg shadow-blue-100">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z"/>
          </svg>
        </div>
      </div>
    </div>

    <!-- ===== MIDDLE ROW ===== -->
    <div class="grid grid-cols-1 xl:grid-cols-12 gap-6 mb-8">
      
      <!-- Alertes du jour (col-span-7) -->
      <div class="xl:col-span-7 bg-white rounded-2xl p-7 shadow-sm border border-gray-100/50 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-5">
            <div>
              <h2 class="text-xl font-semibold">Alertes du jour</h2>
              <p class="text-[12px] text-gray-400 mt-0.5">
                {{ new Date().toLocaleDateString('fr-FR', { weekday: 'long', day: '2-digit', month: 'long' }) }}
              </p>
            </div>
            <div class="flex items-center gap-2">
              <span v-if="!isWeatherLoading && todayAlerts.length > 0" class="inline-flex items-center justify-center w-5 h-5 bg-red-500 text-white text-[10px] font-bold rounded-full">
                {{ todayAlerts.length }}
              </span>
              <div :class="['w-9 h-9 rounded-xl flex items-center justify-center text-lg', todayAlerts.length > 0 ? 'bg-red-50 text-red-500' : 'bg-emerald-50 text-emerald-600']">
                <i class="bx bx-bell"></i>
              </div>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="isWeatherLoading" class="flex items-center justify-center py-10 gap-2 text-gray-400 text-[13px]">
            <i class="bx bx-loader-alt animate-spin text-base"></i>
            <span>Chargement des alertes...</span>
          </div>

          <!-- Aucune parcelle -->
          <div v-else-if="fields.length === 0" class="flex flex-col items-center justify-center py-10 text-center">
            <div class="w-12 h-12 bg-gray-50 rounded-full flex items-center justify-center mb-3">
              <i class="bx bx-map text-2xl text-gray-400"></i>
            </div>
            <p class="text-[13px] text-gray-400">Aucune parcelle enregistrée.</p>
          </div>

          <!-- Alertes du jour -->
          <template v-else-if="todayAlerts.length > 0">
            <div class="space-y-2.5">
              <div
                v-for="(alert, idx) in todayAlerts.slice(0, 3)"
                :key="idx"
                :class="['flex gap-3 p-3.5 rounded-xl border-l-4 bg-gray-50/60', getAlertBorder(alert.severity)]"
              >
                <div :class="['w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 text-base', getAlertIconBg(alert.severity)]">
                  <i :class="['bx', getAlertTypeIcon(alert.type)]"></i>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between gap-2 mb-0.5">
                    <h4 class="text-[13px] font-semibold text-gray-900 truncate">{{ getAlertLabel(alert.type) }}</h4>
                    <span :class="['text-[9px] font-bold text-white px-2 py-0.5 rounded uppercase tracking-wider flex-shrink-0', getAlertBadge(alert.severity)]">
                      {{ alert.severity }}
                    </span>
                  </div>
                  <p class="text-[12px] text-gray-500 truncate">{{ alert.message }}</p>
                  <div v-if="alert.action" class="flex items-center gap-1 mt-0.5 text-[11px] text-emerald-700 font-medium">
                    <i class="bx bx-bulb text-emerald-500 flex-shrink-0"></i>
                    <span class="truncate">{{ alert.action }}</span>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <!-- Aucune alerte aujourd'hui -->
          <template v-else>
            <div class="flex flex-col items-center justify-center py-10 text-center">
              <div class="w-14 h-14 bg-emerald-50 rounded-full flex items-center justify-center mb-4">
                <i class="bx bx-check-shield text-3xl text-emerald-500"></i>
              </div>
              <p class="text-[14px] font-semibold text-gray-800">Aucune alerte aujourd'hui</p>
              <p class="text-[12px] text-gray-400 mt-1">Conditions météo favorables sur vos parcelles.</p>
            </div>
          </template>
        </div>

        <NuxtLink
          :to="selectedWeatherParcel ? `/farmer/parcels/alerts/${selectedWeatherParcel}` : '/farmer/parcels'"
          class="block w-full mt-6 py-3 bg-[#f8fafc] text-[#013b28] font-semibold text-[13px] rounded-xl hover:bg-gray-100 transition-colors text-center"
        >
          Voir l'historique des alertes
        </NuxtLink>
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
          <NuxtLink
            :to="selectedWeatherParcel ? `/farmer/parcels/show/${selectedWeatherParcel}` : '/farmer/parcels'"
            class="text-[13px] font-semibold text-[#013b28] hover:underline"
          >
            Voir les détails
          </NuxtLink>
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
        
        <button
          v-if="filters.parcel_name"
          @click="filters.parcel_name = ''"
          class="flex items-center gap-2 px-4 py-2 bg-[#f8fafc] text-gray-600 text-[12px] font-semibold rounded-lg hover:bg-gray-100 transition-colors"
        >
          <i class="bx bx-x text-[14px]"></i> Effacer
        </button>
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
                  <span class="text-[13px] text-gray-600">{{ field.area ? field.area + ' ha' : '—' }}</span>
                </td>
                <td class="px-6 py-5">
                  <span class="text-[13px] text-gray-500">{{ field.created_at ? formatDate(field.created_at) : '—' }}</span>
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
      <div v-if="filteredFields.length > 0" class="px-6 py-4 bg-[#f8fafc] border-t border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-4">
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
              <button @click="deleteParcelConfirmed" :disabled="isDeleting" class="w-full py-3.5 bg-rose-500 text-white rounded-xl font-bold text-[12px] uppercase tracking-wider hover:bg-rose-600 disabled:opacity-60 disabled:cursor-not-allowed transition-all">
                <span v-if="isDeleting">Suppression...</span>
                <span v-else>{{ t("deletePermanently") }}</span>
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
const isLoading  = ref(false);
const isDeleting = ref(false);

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

// ===== ALERTES DU JOUR =====
const _SEV_ORDER: Record<string, number> = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 }

const todayAlerts = computed(() => {
  const todayStr = new Date().toISOString().split('T')[0] ?? ""
  return [...dashboardAlerts.value]
    .filter(a => (a.date ?? "").startsWith(todayStr))
    .sort((a, b) => (_SEV_ORDER[a.severity] ?? 4) - (_SEV_ORDER[b.severity] ?? 4))
})

function getAlertBorder(severity: string) {
  const s = (severity || "").toUpperCase()
  if (s === "CRITICAL") return "border-red-500"
  if (s === "HIGH")     return "border-orange-400"
  if (s === "MEDIUM")   return "border-amber-400"
  return "border-blue-300"
}

function getAlertIconBg(severity: string) {
  const s = (severity || "").toUpperCase()
  if (s === "CRITICAL") return "bg-red-50 text-red-500"
  if (s === "HIGH")     return "bg-orange-50 text-orange-500"
  if (s === "MEDIUM")   return "bg-amber-50 text-amber-500"
  return "bg-blue-50 text-blue-500"
}

function getAlertBadge(severity: string) {
  const s = (severity || "").toUpperCase()
  if (s === "CRITICAL") return "bg-red-600"
  if (s === "HIGH")     return "bg-orange-500"
  if (s === "MEDIUM")   return "bg-amber-500"
  return "bg-blue-500"
}

function getAlertTypeIcon(type: string) {
  const t = (type || "").toLowerCase()
  if (t.includes("feu") || t.includes("fire"))                                     return "bxs-flame"
  if (t.includes("pluie") || t.includes("rain") || t.includes("heavy_rain"))       return "bx-cloud-rain"
  if (t.includes("gel") || t.includes("frost"))                                     return "bx-snowflake"
  if (t.includes("vent") || t.includes("wind"))                                     return "bx-wind"
  if (t.includes("humidité") || t.includes("humidity"))                             return "bx-water"
  if (t.includes("sécheresse") || t.includes("drought") || t.includes("stress"))   return "bx-sun"
  return "bx-error-circle"
}

function getAlertLabel(type: string) {
  const map: Record<string, string> = {
    "DROUGHT_RISK":  "Stress hydrique",
    "HEAVY_RAIN":    "Pluies intenses",
    "FROST_RISK":    "Risque de gel",
    "STRONG_WIND":   "Vent fort",
    "HIGH_HUMIDITY": "Humidité élevée",
  }
  return map[type] ?? type
}

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

watch(() => filters.parcel_name, () => {
  currentPage.value = 1;
});

// ===== CHARGEMENT DES DONNÉES =====
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    showNotification(nuxtT("dashboard.mustBeConnected"), "error");
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
  fields.value.filter((f) =>
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
    showNotification(nuxtT("dashboard.mustBeConnected"), "error");
    return;
  }

  isDeleting.value = true;

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
    isDeleting.value = false;
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
