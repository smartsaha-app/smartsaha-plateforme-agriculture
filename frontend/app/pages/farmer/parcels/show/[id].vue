<template>
  <div class="p-8 bg-[#f8fafc] min-h-screen font-sans">
    
    <!-- ===== HEADER ===== -->
    <div class="mb-6">
      <h1 class="text-[28px] font-medium text-gray-900 mb-1 tracking-tight">Parcelle</h1>
      <p class="text-[15px] text-gray-500">Vue complète des données agronomiques, climatiques et environnementales.</p>
    </div>

    <!-- ===== MAP BANNER & SOIL DETAILS GRID ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
      <!-- Left: Map (span 2) -->
      <div class="lg:col-span-2 relative h-[400px] rounded-2xl overflow-hidden shadow-sm border border-gray-100">
        <!-- The Map -->
        <div id="map" class="w-full h-full z-0 bg-gray-200"></div>
        
        <!-- Overlay Card -->
        <div class="absolute top-6 left-6 z-10 bg-white/95 backdrop-blur-md p-5 rounded-[20px] shadow-lg border border-white/40 w-64">
          <h3 class="text-[13px] font-medium text-gray-500 uppercase tracking-wider mb-4">{{ parcelData.name || 'PARCELLE-EXAMPLE' }}</h3>
          <div class="flex justify-between items-start">
            <div>
              <p class="text-[13px] text-gray-500 mb-0.5">Superficie</p>
              <p class="text-[15px] text-gray-900">{{ formatM2(parcelAreaHa) !== '- m²' ? parcelAreaHa + ' ha' : '2.8 ha' }}</p>
            </div>
            <div>
              <p class="text-[13px] text-gray-500 mb-0.5">Création</p>
              <p class="text-[15px] text-gray-900">{{ parcelData.created_at ? formatDate(parcelData.created_at) : '20 Fév 2024' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Soil Analysis Synthesis (span 1) -->
      <div class="lg:col-span-1 bg-white rounded-2xl p-7 shadow-sm border border-gray-100/50 flex flex-col justify-between h-[400px]">
        <div>
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-[15px] font-medium text-gray-900">Analyse & Diagnostic du sol</h3>
            <span class="w-8 h-8 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600">
              <i class="bx bx-vial text-lg"></i>
            </span>
          </div>
          
          <div class="bg-gradient-to-br from-emerald-50/40 to-teal-50/10 p-5 rounded-2xl border border-emerald-100/30 flex flex-col justify-between min-h-[260px]">
            <div>
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 text-emerald-800 text-[10px] font-bold uppercase rounded-md tracking-wider mb-4">
                <i class="bx bx-check-shield text-xs"></i> Diagnostic Agronomique
              </span>
              <p class="text-[12px] leading-relaxed text-gray-700 italic">
                "{{ soilSynthesis }}"
              </p>
            </div>
            
            <div class="mt-6 flex items-center gap-2 pt-4 border-t border-emerald-100/20 text-[11px] text-gray-400 font-medium">
              <i class="bx bx-info-circle text-[14px] text-emerald-600"></i>
              <span>Généré d'après les données pédologiques physiques et chimiques.</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ===== TOP GRID: MÉTÉO & ALERTES ===== -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
      
      <!-- Météo & Prévisions (Col span 2) -->
      <div class="lg:col-span-2 bg-white rounded-2xl p-7 shadow-sm border border-gray-100/50 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-2">
            <h2 class="text-xl font-semibold">Météo & Prévisions</h2>
            <span class="px-3 py-1.5 bg-[#f8fafc] text-gray-600 text-[11px] font-semibold rounded-lg">Aperçu général</span>
          </div>
          <p class="text-[12px] text-gray-400 mb-6">Prévisions de la parcelle</p>

          <template v-if="todayWeather">
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
      </div>

      <!-- Alertes Actives (Col span 1) -->
      <div class="lg:col-span-1 bg-[#fcfcfc] rounded-[24px] p-7 border border-gray-100/50 flex flex-col h-full shadow-sm">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-[15px] font-medium text-gray-900">Alertes Actives</h3>
          <span v-if="translatedAlerts.length" class="px-2.5 py-0.5 bg-rose-50 text-rose-600 rounded-full text-xs font-bold">
            {{ translatedAlerts.length }}
          </span>
        </div>
        
        <div class="space-y-4 flex-1 overflow-y-auto max-h-[300px]">
          <!-- Si pas d'alertes, afficher un état neutre et rassurant -->
          <template v-if="!translatedAlerts.length">
            <div class="flex flex-col items-center justify-center py-12 text-center h-full">
              <span class="w-12 h-12 bg-emerald-50 rounded-full flex items-center justify-center text-emerald-600 mb-4">
                <i class="bx bx-check-shield text-2xl"></i>
              </span>
              <h4 class="text-[14px] font-semibold text-gray-900 mb-1">Tout est sous contrôle</h4>
              <p class="text-[12px] text-gray-400 max-w-[200px] leading-relaxed">Aucune alerte active pour cette parcelle actuellement.</p>
            </div>
          </template>

          <template v-else>
            <div v-for="alert in translatedAlerts" :key="alert.type" 
                :class="[
                  'rounded-[16px] p-5 border-l-[3px] shadow-sm relative transition-all hover:scale-[1.01]',
                  getSeverityClass(alert.severity).bg
                ]">
                <div class="flex gap-4 relative z-10">
                  <i :class="['bx text-2xl mt-0.5', getAlertIcon(alert.type)]"></i>
                  <div>
                    <h4 class="text-[15px] font-semibold text-gray-900 mb-1">{{ getAlertTitle(alert.type) }}</h4>
                    <p class="text-[13px] text-gray-500 mb-2 leading-normal">{{ alert.message }}</p>
                    <p v-if="alert.action" class="text-[11.5px] text-emerald-700 font-medium mb-3 flex items-center gap-1">
                      <i class="bx bx-bulb animate-pulse text-emerald-600"></i> Action : {{ alert.action }}
                    </p>
                    <span :class="[
                      'text-[9px] font-bold text-white px-2.5 py-0.5 rounded-[6px] uppercase tracking-wider',
                      getSeverityClass(alert.severity).badge
                    ]">{{ alert.severity }}</span>
                  </div>
                </div>
            </div>
          </template>
        </div>
        
        <div class="mt-6 pt-4 text-center border-t border-gray-100/50">
          <button class="text-[13px] text-gray-500 hover:text-gray-900 transition-colors flex items-center justify-center gap-2 mx-auto font-medium">
            Historique des alertes <i class="bx bx-right-arrow-alt text-lg"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- ===== BOTTOM LAYOUT: GESTION DES PLANTATIONS ===== -->
    <div class="pb-10">
      <!-- Gestion des cultures & plantations -->
      <div class="bg-white rounded-[24px] p-7 shadow-sm border border-gray-100/50">
        <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-4 mb-6">
          <div>
            <h3 class="text-[15px] font-medium text-gray-900">Gestion des cultures & plantations</h3>
            <p class="text-[12px] text-gray-400">Suivez et gérez l'historique des cultures de cette parcelle.</p>
          </div>
          <button @click="openAddCropModal" class="flex items-center gap-2 px-5 py-2.5 bg-[#013b28] text-white rounded-xl text-[13px] font-medium hover:bg-[#022c22] transition-colors shadow-sm self-start sm:self-auto">
            <i class="bx bx-plus text-base"></i>
            Nouvelle culture
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse min-w-[600px]">
            <thead>
              <tr class="bg-gray-50/50">
                <th class="px-5 py-3 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100">Culture</th>
                <th class="px-5 py-3 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100">Superficie allouée</th>
                <th class="px-5 py-3 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100">Date de plantation</th>
                <th class="px-5 py-3 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100">Date de récolte</th>
                <th class="px-5 py-3 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100">Statut</th>
                <th class="px-5 py-3 text-[10px] font-bold text-gray-400 uppercase tracking-widest border-b border-gray-100 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-50/80">
              <tr v-for="crop in parcelCropsFromFullData" :key="crop.parcel_crop_id" class="hover:bg-gray-50/30 transition-colors">
                <td class="px-5 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-600 text-sm">
                      <i class="bx bxs-leaf"></i>
                    </div>
                    <span class="text-[13px] font-semibold text-gray-900">{{ crop.crop?.name }}</span>
                  </div>
                </td>
                <td class="px-5 py-4 text-[13px] text-gray-600 font-medium">
                  {{ crop.area }} m²
                </td>
                <td class="px-5 py-4 text-[13px] text-gray-500">
                  {{ crop.planting_date ? formatDate(crop.planting_date) : 'N/A' }}
                </td>
                <td class="px-5 py-4 text-[13px] text-gray-500">
                  {{ crop.harvest_date ? formatDate(crop.harvest_date) : 'Non planifiée' }}
                </td>
                <td class="px-5 py-4">
                  <span :class="[
                    'px-2.5 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider',
                    crop.status?.toLowerCase() === 'harvested' || crop.status?.toLowerCase() === 'récolté' ? 'bg-gray-100 text-gray-500' :
                    crop.status?.toLowerCase() === 'active' || crop.status?.toLowerCase() === 'en cours' ? 'bg-emerald-50 text-emerald-700 border border-emerald-100' :
                    'bg-amber-50 text-amber-700 border border-amber-100'
                  ]">
                    {{ crop.status || 'En cours' }}
                  </span>
                </td>
                <td class="px-5 py-4 text-right">
                  <div class="flex items-center justify-end gap-3 text-gray-500">
                    <button @click="openCropDetails(crop)" class="hover:text-[#013b28] transition-colors p-1" title="Voir détails">
                      <i class="bx bx-show text-base"></i>
                    </button>
                    <button @click="openEditCropModal(crop)" class="hover:text-emerald-600 transition-colors p-1" title="Modifier">
                      <i class="bx bx-pencil text-base"></i>
                    </button>
                    <button @click="confirmDeleteCrop(crop.parcel_crop_id)" class="hover:text-rose-500 transition-colors p-1" title="Supprimer">
                      <i class="bx bx-trash text-base"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="!parcelCropsFromFullData.length">
                <td colspan="6" class="px-5 py-8 text-center text-gray-400 text-sm">
                  Aucune plantation enregistrée sur cette parcelle.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal Détails Plantation -->
  <Teleport to="body">
    <transition name="pop-notification">
      <div v-if="showDetailsModal" class="fixed inset-0 flex items-center justify-center z-[100] px-4">
        <div class="absolute inset-0 bg-[#022c22]/80 backdrop-blur-sm" @click="showDetailsModal = false"></div>
        <div class="bg-white rounded-3xl p-8 w-full max-w-md text-left shadow-2xl relative z-10">
          <div class="flex justify-between items-start mb-6">
            <h3 class="text-xl font-bold text-[#022c22]">Détails de la plantation</h3>
            <button @click="showDetailsModal = false" class="text-gray-400 hover:text-gray-600">
              <i class="bx bx-x text-2xl"></i>
            </button>
          </div>
          
          <div class="space-y-4" v-if="selectedCropDetails">
            <div class="flex items-center gap-4 p-4 bg-emerald-50/50 rounded-2xl border border-emerald-100/50 mb-4">
              <div class="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center text-emerald-700 text-2xl">
                <i class="bx bxs-leaf"></i>
              </div>
              <div>
                <h4 class="text-lg font-bold text-gray-900">{{ selectedCropDetails.crop?.name }}</h4>
                <p class="text-xs text-gray-500 font-semibold uppercase tracking-wider">{{ selectedCropDetails.status || 'En cours' }}</p>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div class="bg-[#f8fafc] p-4 rounded-xl border border-gray-50">
                <span class="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Superficie</span>
                <span class="text-sm font-semibold text-gray-800">{{ selectedCropDetails.area }} m²</span>
              </div>
              
              <div class="bg-[#f8fafc] p-4 rounded-xl border border-gray-50">
                <span class="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Parcelle</span>
                <span class="text-sm font-semibold text-gray-800">{{ parcelData.name }}</span>
              </div>

              <div class="bg-[#f8fafc] p-4 rounded-xl border border-gray-50">
                <span class="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Date de plantation</span>
                <span class="text-sm font-semibold text-gray-800">{{ selectedCropDetails.planting_date ? formatDate(selectedCropDetails.planting_date) : 'N/A' }}</span>
              </div>

              <div class="bg-[#f8fafc] p-4 rounded-xl border border-gray-50">
                <span class="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Date de récolte</span>
                <span class="text-sm font-semibold text-gray-800">{{ selectedCropDetails.harvest_date ? formatDate(selectedCropDetails.harvest_date) : 'Non planifiée' }}</span>
              </div>
            </div>

            <div v-if="selectedCropDetails.crop?.variety" class="bg-[#f8fafc] p-4 rounded-xl border border-gray-50">
              <span class="block text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-1">Variété</span>
              <span class="text-sm font-semibold text-gray-800">{{ selectedCropDetails.crop.variety.name || 'N/A' }}</span>
            </div>
          </div>

          <div class="pt-6">
            <button @click="showDetailsModal = false" class="w-full py-3.5 bg-gray-50 text-gray-500 rounded-xl font-bold text-xs uppercase tracking-wider hover:bg-gray-100 transition-colors">
              Fermer
            </button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>

  <!-- Modal Ajouter / Modifier Plantation -->
  <Teleport to="body">
    <transition name="pop-notification">
      <div v-if="showCropModal" class="fixed inset-0 flex items-center justify-center z-[100] px-4">
        <div class="absolute inset-0 bg-[#022c22]/80 backdrop-blur-sm" @click="showCropModal = false"></div>
        <div class="bg-white rounded-3xl p-8 w-full max-w-md text-left shadow-2xl relative z-10">
          <h3 class="text-xl font-bold text-[#022c22] mb-6">
            {{ isEditingCrop ? 'Modifier la plantation' : 'Ajouter une plantation' }}
          </h3>
          
          <form @submit.prevent="saveCrop" class="space-y-5">
            <!-- Culture -->
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-400 mb-2">Culture</label>
              <select v-model="cropForm.crop_id" required class="w-full px-4 py-3 bg-[#f8fafc] border border-gray-200 rounded-xl text-sm font-semibold focus:ring-1 focus:ring-emerald-500 outline-none cursor-pointer">
                <option v-for="crop in cropsOptions" :key="crop.id" :value="crop.id">
                  {{ crop.display_name || crop.name }}
                </option>
              </select>
            </div>

            <!-- Superficie -->
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-400 mb-2">Superficie allouée (m²)</label>
              <input v-model="cropForm.area" type="number" step="any" required min="0" class="w-full px-4 py-3 bg-[#f8fafc] border border-gray-200 rounded-xl text-sm font-semibold focus:ring-1 focus:ring-emerald-500 outline-none" />
            </div>

            <!-- Date de plantation -->
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-400 mb-2">Date de plantation</label>
              <input v-model="cropForm.planting_date" type="date" required class="w-full px-4 py-3 bg-[#f8fafc] border border-gray-200 rounded-xl text-sm font-semibold focus:ring-1 focus:ring-emerald-500 outline-none" />
            </div>

            <!-- Date de récolte prévue -->
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-400 mb-2">Date de récolte prévue (optionnelle)</label>
              <input v-model="cropForm.harvest_date" type="date" class="w-full px-4 py-3 bg-[#f8fafc] border border-gray-200 rounded-xl text-sm font-semibold focus:ring-1 focus:ring-emerald-500 outline-none" />
            </div>

            <!-- Statut -->
            <div>
              <label class="block text-xs font-bold uppercase tracking-wider text-gray-400 mb-2">Statut</label>
              <select v-model="cropForm.status_id" required class="w-full px-4 py-3 bg-[#f8fafc] border border-gray-200 rounded-xl text-sm font-semibold focus:ring-1 focus:ring-emerald-500 outline-none cursor-pointer">
                <option v-for="status in statusOptions" :key="status.id" :value="status.id">
                  {{ status.name }}
                </option>
              </select>
            </div>

            <!-- Boutons d'action -->
            <div class="flex gap-3 pt-4">
              <button type="submit" class="flex-1 py-3.5 bg-[#013b28] text-white rounded-xl font-bold text-xs uppercase tracking-wider hover:bg-[#022c22] transition-colors">
                Enregistrer
              </button>
              <button type="button" @click="showCropModal = false" class="flex-1 py-3.5 bg-gray-50 text-gray-500 rounded-xl font-bold text-xs uppercase tracking-wider hover:bg-gray-100 transition-colors">
                Annuler
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </Teleport>

  <!-- Modal Confirmation Suppression Plantation -->
  <Teleport to="body">
    <transition name="pop-notification">
      <div v-if="showDeleteCropModal" class="fixed inset-0 flex items-center justify-center z-[100] px-4">
        <div class="absolute inset-0 bg-[#022c22]/80 backdrop-blur-sm" @click="showDeleteCropModal = false"></div>
        <div class="bg-white rounded-3xl p-10 w-full max-w-sm text-center shadow-2xl relative z-10">
          <div class="w-20 h-20 bg-rose-50 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <i class="bx bx-trash text-4xl text-rose-500"></i>
          </div>
          <h3 class="text-xl font-bold text-[#022c22] mb-3">Supprimer la plantation ?</h3>
          <p class="text-gray-500 text-[13px] mb-8">Cette action est irréversible. Toutes les données associées à cette plantation seront perdues.</p>
          <div class="flex flex-col gap-3">
            <button @click="deleteCropConfirmed" class="w-full py-3.5 bg-rose-500 text-white rounded-xl font-bold text-[12px] uppercase tracking-wider hover:bg-rose-600 transition-all">
              Supprimer définitivement
            </button>
            <button @click="showDeleteCropModal = false" class="w-full py-3.5 bg-gray-50 text-gray-500 rounded-xl font-bold text-[12px] uppercase tracking-wider hover:bg-gray-100 transition-all">
              Annuler
            </button>
          </div>
        </div>
      </div>
    </transition>
  </Teleport>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" })

import { reactive, ref, computed, onMounted, onUnmounted, watch, nextTick } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "~/stores/auth"
import { useApi } from "~/composables/useApi"
import Chart from "chart.js/auto"

const router = useRouter()
const authStore = useAuthStore()
const { apiFetch } = useApi()

const { t: nuxtT, locale } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);
const currentLocale = computed(() => locale.value)

const route = useRoute()
const fieldIdParam = route.params.id as string ?? null

// ===== MÉTÉO ======
const upcomingForecasts = computed(() => {
  if (!forecastDays.value) return [];
  const todayStr = new Date().toISOString().split('T')[0] ?? "";
  return forecastDays.value.filter((d: any) => d.date >= todayStr).slice(0, 5);
});

const todayWeather = computed(() => {
  return upcomingForecasts.value.length > 0 ? upcomingForecasts.value[0] : null;
});

// ===== ÉTAT =====
const currentWeather = ref<any>(null)
const forecastDays = ref<any[]>([])
const parcelPoints = ref<any[]>([])
const alerts = ref<any[]>([])
const translatedAlerts = ref<any[]>([])
const weatherAnalysis = ref<any>(null)
const weatherSummary = ref<any>(null)
const metadata = ref<any>({})
const selectedTab = ref("points")
const translatedCurrentCondition = ref("")
const currentTime = ref("")
const parcelFullData = reactive<any>({})
const parcelData = reactive<any>({})
const ownerData = reactive<any>({})
const soilQualities = reactive<any[]>([])
// ✅ FIX: tasks vient de fullData.tasks.tasks (tableau à la racine)
const tasks = ref<any[]>([])
const harvestHistory = ref<any[]>([])
const analyticsData = ref<any[]>([])
const selectedParcel = ref<any>(null)
const parcelCrops = ref<any[]>([])
const cropsOptions = ref<any[]>([])
const statusOptions = ref<any[]>([])

const showDetailsModal = ref(false)
const selectedCropDetails = ref<any>(null)

const showCropModal = ref(false)
const isEditingCrop = ref(false)
const currentCropId = ref<number | null>(null)

const cropForm = reactive({
  crop_id: "" as any,
  planting_date: "",
  harvest_date: "",
  area: 0,
  status_id: "" as any
})

const showDeleteCropModal = ref(false)
const cropToDeleteId = ref<number | null>(null)
const paginatedHarvest = ref<any[]>([])
const itemsPerPage = 5
const currentPage = ref(1)

const colorMap: Record<string, string> = {
  nitrogen: "#10b481",
  soc:      "#c99383",
  clay:     "#6d4c41",
  phh2o:    "#5fd4a2",
  sand:     "#f4a261",
  silt:     "#219ebc",
}

// ===== HORLOGE =====
let intervalId: ReturnType<typeof setInterval>

onMounted(() => {
  updateTime()
  intervalId = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  clearInterval(intervalId)
})

// ===== MAP INITIALIZATION =====
let L: any;
let map: any;

async function initMap() {
  if (!process.client || map) return;
  
  L = await import("leaflet");
  await import("leaflet/dist/leaflet.css");
  
  const satellite = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", { attribution: "Esri" });
  map = L.map("map", {
    center: [-18.8792, 47.5079],
    zoom: 6,
    layers: [satellite],
    zoomControl: false
  });

  if (parcelPoints.value.length >= 3) {
    const latlngs = parcelPoints.value.map(p => [p.lat, p.lng]);
    const poly = L.polygon(latlngs, {
      color: "#10b481",
      fillColor: "#10b481",
      fillOpacity: 0.2,
      weight: 3
    }).addTo(map);
    map.fitBounds(poly.getBounds(), { padding: [40, 40] });
  } else if (parcelPoints.value.length > 0) {
    map.setView([parcelPoints.value[0].lat, parcelPoints.value[0].lng], 15);
  }

  // Ajouter les alertes feu sur la carte
  alerts.value.forEach((alert: any) => {
    if (alert.type?.includes("FEU") && alert.latitude && alert.longitude) {
      // Icône de feu personnalisée
      const fireIcon = L.divIcon({
        className: 'bg-transparent',
        html: `<div class="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center text-white shadow-[0_0_15px_rgba(239,68,68,0.8)] border-2 border-white animate-pulse"><i class='bx bxs-flame'></i></div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      });
      
      // Ajouter le marqueur du feu
      L.marker([alert.latitude, alert.longitude], { icon: fireIcon })
        .addTo(map)
        .bindPopup(`<div class="text-center"><b class="text-red-600">🔥 Foyer d'Incendie</b><br><span class="text-xs">Distance: ${alert.distance_km} km</span></div>`);
      
      // Ajouter un cercle de danger (rayon d'alerte)
      L.circle([alert.latitude, alert.longitude], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0.05,
        radius: 5000 // 5km radius visuel
      }).addTo(map);
    }
  });
}

function updateTime() {
  const now = new Date()
  currentTime.value = `${now.getHours().toString().padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}`
}

// ===== MÉTÉO =====
// ✅ FIX: mapping complet depuis la vraie structure API
function updateWeatherForecast(data: any) {
  const weatherData = data?.weather_data?.data
  if (!weatherData) {
    currentWeather.value = null
    forecastDays.value = []
    parcelPoints.value = []
    alerts.value = []
    metadata.value = {}
    return
  }

  // ✅ current est directement weatherData.current (temp_c, wind_kph, humidity, uv, condition.text)
  currentWeather.value = weatherData.current ?? null

  // ✅ forecastday est dans weatherData.forecast.forecastday (pas daily_forecast)
  forecastDays.value = weatherData.forecast?.forecastday ?? []

  parcelPoints.value = data?.parcel?.points ?? []

  alerts.value = data?.weather_data?.alerts ?? []

  const meta = data?.weather_data?.metadata
  metadata.value = meta ? {
    location:        meta.location_name,
    forecast_period: `${meta.start} → ${meta.end}`,
    risk_level:      meta.risk_level,
  } : {}

  // Ajout de l'analyse et du résumé
  weatherAnalysis.value = data?.weather_data?.analysis ?? null
  weatherSummary.value = data?.weather_data?.summary ?? null
}

// ✅ FIX: todayForecast cherche dans forecastday[] qui sont des objets { date, day, hour, astro }
const todayForecast = computed(() => {
  if (!forecastDays.value.length) return null
  const today = new Date().toISOString().split("T")[0]
  return forecastDays.value.find((d: any) => d.date === today) ?? forecastDays.value[0] ?? null
})

function getAlertTitle(type: string) {
  const map: Record<string, string> = {
    'DROUGHT_RISK': 'waterStress',
    'HEAVY_RAIN':   'heavyRain',
    'FROST_RISK':   'frostRisk',
    'STRONG_WIND':  'strongWind',
    'HIGH_HUMIDITY': 'highHumidity',
  }
  const cleanType = type.replace(/^[\u2300-\u27BF\uD83C-\uDBFF\uDC00-\uDFFF\u2000-\u32FF⏰🔔🧪🌱🔥🌧️❄️💨💧🌵]+\s*/, "")
  return map[type] ? t(map[type]) : (cleanType || type)
}

function getAlertIcon(type: string) {
  const t = type.toLowerCase()
  if (t.includes('feu') || t.includes('fire')) return 'bxs-flame text-red-500 animate-pulse'
  if (t.includes('pluie') || t.includes('rain')) return 'bx-cloud-rain text-blue-500'
  if (t.includes('gel') || t.includes('frost')) return 'bx-snowflake text-sky-400'
  if (t.includes('vent') || t.includes('wind')) return 'bx-wind text-blue-400'
  if (t.includes('humidité') || t.includes('humidity')) return 'bx-water text-teal-400'
  if (t.includes('sécheresse') || t.includes('drought') || t.includes('stress')) return 'bx-sun text-amber-600'
  if (t.includes('tâche') || t.includes('task')) return 'bx-time-five text-amber-500'
  if (t.includes('ph') || t.includes('acide')) return 'bx-vial text-emerald-500'
  if (t.includes('azote') || t.includes('nitrogen')) return 'bx-leaf text-emerald-600'
  return 'bx-error-circle text-gray-400'
}

function getSeverityClass(severity: string) {
  const s = severity?.toUpperCase() || 'LOW'
  if (s === 'CRITICAL' || s === 'CRITIQUE') {
    return {
      bg: 'bg-red-50/40 border-red-600',
      badge: 'bg-red-600 text-white',
      text: 'text-red-800'
    }
  } else if (s === 'HIGH' || s === 'ÉLEVÉE' || s === 'ÉLEVÉ') {
    return {
      bg: 'bg-orange-50/40 border-orange-400',
      badge: 'bg-orange-400 text-white',
      text: 'text-orange-800'
    }
  } else if (s === 'MEDIUM' || s === 'MOYEN') {
    return {
      bg: 'bg-amber-50/40 border-amber-400',
      badge: 'bg-amber-400 text-white',
      text: 'text-amber-800'
    }
  } else {
    return {
      bg: 'bg-blue-50/40 border-blue-500',
      badge: 'bg-blue-500 text-white',
      text: 'text-blue-800'
    }
  }
}

function getDayName(dateStr: string) {
  return new Date(dateStr).toLocaleDateString(currentLocale.value, { weekday: "long" })
}

function getDayNameShort(dateStr: string) {
  return new Date(dateStr).toLocaleDateString(currentLocale.value, { weekday: "short" })
}

// Dictionnaire complet des 65 conditions officielles WeatherAPI en français
const weatherIconMap: Record<string, string> = {
  // ☀️ Soleil / Ciel clair
  "Ensoleillé":                               "☀️",
  "Clair":                                    "🌙",

  // ⛅ Partiellement nuageux
  "Partiellement nuageux":                    "⛅",

  // ☁️ Nuageux / Couvert
  "Nuageux":                                  "☁️",
  "Couvert":                                  "☁️",

  // 🌫️ Brume / Brouillard
  "Brume":                                    "🌫️",
  "Brouillard":                               "🌫️",
  "Brouillard givrant":                       "🌫️",

  // 🌦️ Pluie légère / Bruine
  "Pluie éparse à proximité":                 "🌦️",
  "Bruine légère éparse":                     "🌦️",
  "Bruine légère":                            "🌦️",
  "Pluie légère éparse":                      "🌦️",
  "Pluie légère":                             "🌦️",
  "Averses légères":                          "🌦️",

  // 🌧️ Pluie modérée à forte
  "Pluie modérée par moments":                "🌧️",
  "Pluie modérée":                            "🌧️",
  "Pluie forte par moments":                  "🌧️",
  "Pluie forte":                              "🌧️",
  "Averses modérées ou fortes":               "🌧️",
  "Averses torrentielles":                    "🌧️",

  // ❄️ Neige / Verglas / Grésil
  "Neige éparse à proximité":                 "❄️",
  "Grésil épars à proximité":                 "🌨️",
  "Bruine verglaçante éparse à proximité":    "❄️",
  "Rafales de neige":                         "🌨️",
  "Blizzard":                                 "🌨️",
  "Bruine verglaçante":                       "❄️",
  "Forte bruine verglaçante":                 "❄️",
  "Pluie verglaçante légère":                 "❄️",
  "Pluie verglaçante modérée à forte":        "❄️",
  "Léger grésil":                             "🌨️",
  "Grésil modéré à fort":                     "🌨️",
  "Neige légère éparse":                      "❄️",
  "Neige légère":                             "❄️",
  "Neige modérée éparse":                     "❄️",
  "Neige modérée":                            "❄️",
  "Neige forte éparse":                       "❄️",
  "Neige forte":                              "❄️",
  "Averses de grésil léger":                  "🌨️",
  "Averses de grésil modéré ou fort":         "🌨️",
  "Averses de neige légère":                  "❄️",
  "Averses de neige modérée ou forte":        "❄️",

  // ⛈️ Orages / Grêle
  "Foyers orageux à proximité":               "⛈️",
  "Grêle":                                    "⛈️",
  "Averses de grêle légère":                  "⛈️",
  "Averses de grêle modérée ou forte":        "⛈️",
  "Pluie légère éparse avec orages":          "⛈️",
  "Pluie modérée ou forte avec orages":       "⛈️",
  "Neige légère éparse avec orages":          "⛈️",
  "Neige modérée ou forte avec orages":       "⛈️",
}

function getWeatherIcon(condition?: string): string {
  if (!condition) return "🌡️"

  // 1. Correspondance exacte (conditions officielles WeatherAPI FR)
  if (weatherIconMap[condition]) return weatherIconMap[condition]

  // 2. Fallback par mots-clés pour variantes non officielles (ex: "Orage", "Orage avec grêle légère")
  const c = condition.toLowerCase()
  if (c.includes("orage") || c.includes("grêle") || c.includes("tempête")) return "⛈️"
  if (c.includes("neige") || c.includes("grésil") || c.includes("blizzard"))  return "❄️"
  if (c.includes("averse") || c.includes("bruine"))                            return "🌦️"
  if (c.includes("pluie forte") || c.includes("forte pluie"))                 return "🌧️"
  if (c.includes("pluie"))                                                     return "🌧️"
  if (c.includes("brouillard") || c.includes("brume"))                        return "🌫️"
  if (c.includes("partiellement") || c.includes("partly"))                    return "⛅"
  if (c.includes("couvert") || c.includes("nuageux") || c.includes("cloudy")) return "☁️"
  if (c.includes("clair") || c.includes("clear"))                             return "🌙"
  if (c.includes("ensoleillé") || c.includes("sunny") || c.includes("sun"))  return "☀️"

  return "🌡️"
}

// ===== TRADUCTIONS =====
const translationCache = useState("translationCache", () => ({} as Record<string, string>))

const removeEmojis = (text: string) =>
  text.replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|[\uD83C-\uDBFF\uDC00-\uDFFF])/g, "")

async function translateText(text: string, sourceLang = "fr") {
  const targetLang = currentLocale.value || "en"
  if (sourceLang === targetLang) return { translated: text, original: text }
  if (translationCache.value[text]) return { translated: translationCache.value[text], original: text }

  try {
    const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(text)}&langpair=${sourceLang}|${targetLang}`
    const res = await fetch(url)
    const json = await res.json()
    const translatedText = json?.responseData?.translatedText || text
    translationCache.value[text] = translatedText
    return { translated: translatedText, original: text }
  } catch {
    translationCache.value[text] = text
    return { translated: text, original: text }
  }
}

async function translateAlerts(alertList: any[]) {
  if (!alertList || !alertList.length) {
    translatedAlerts.value = []
    return
  }
  translatedAlerts.value = await Promise.all(
    alertList.map(async (alert) => {
      const messageRes = await translateText(removeEmojis(alert.message))
      const actionRes  = await translateText(removeEmojis(alert.action))
      return {
        ...alert,
        message:         messageRes.translated,
        messageOriginal: messageRes.original,
        action:          actionRes.translated,
        actionOriginal:  actionRes.original,
      }
    })
  )
}

async function translateCurrentWeatherCondition() {
  // ✅ FIX: condition est un objet { text, code, icon } dans l'API WeatherAPI
  const conditionText = currentWeather.value?.condition?.text
  if (conditionText) {
    const res = await translateText(removeEmojis(conditionText))
    translatedCurrentCondition.value = res.translated
    currentWeather.value.conditionOriginal = res.original
  } else {
    translatedCurrentCondition.value = ""
  }
}

watch(alerts, (val) => { translateAlerts(val) }, { immediate: true })
watch(currentWeather, () => { translateCurrentWeatherCondition() })

// ===== SOL =====
function updateSoilQualities(layers: any[]) {
  if (!layers || !Array.isArray(layers)) return
  soilQualities.length = 0
  layers.forEach((layer) => {
    soilQualities.push({
      name:  layer.name,
      value: layer.depths?.[0]?.values?.mean ?? null,
      unit:  layer.unit_measure?.mapped_units ?? "",
    })
  })
}

const soilSynthesis = computed(() => {
  if (!soilQualities.length) {
    return "Données de sol insuffisantes pour formuler une synthèse agronomique."
  }

  const getVal = (name: string) => {
    const q = soilQualities.find(item => item.name.toLowerCase() === name.toLowerCase())
    return q && q.value !== null ? Number(q.value) : null
  }

  const ph = getVal("phh2o")
  const nitrogen = getVal("nitrogen")
  const clay = getVal("clay")
  const sand = getVal("sand")
  const soc = getVal("soc")

  let phDesc = ""
  if (ph !== null) {
    const realPh = ph > 15 ? ph / 10 : ph
    if (realPh < 6.0) {
      phDesc = "Le sol est acide, ce qui peut limiter l'assimilation de certains nutriments."
    } else if (realPh > 7.5) {
      phDesc = "Le sol est calcaire, bloquant potentiellement le phosphore."
    } else {
      phDesc = "Le pH du sol est optimal et neutre, idéal pour la plupart des cultures."
    }
  }

  let fertilityDesc = ""
  if (nitrogen !== null && soc !== null) {
    if (nitrogen < 30 || soc < 20) {
      fertilityDesc = "Un apport organique (compost ou engrais vert) est vivement recommandé pour stimuler la fertilité."
    } else {
      fertilityDesc = "Les niveaux de fertilité et de carbone organique sont bien équilibrés."
    }
  }

  let textureDesc = ""
  if (clay !== null && sand !== null) {
    if (clay > 35) {
      textureDesc = "La texture argileuse retient bien l'eau, surveillez le drainage."
    } else if (sand > 50) {
      textureDesc = "La texture sableuse est très drainante ; irriguez fréquemment à faible dose."
    } else {
      textureDesc = "La structure du sol est équilibrée et favorable au développement racinaire."
    }
  }

  const parts = [phDesc, textureDesc, fertilityDesc].filter(Boolean)
  if (parts.length > 0) {
    return parts.join(" ")
  }

  return "Sol globalement sain et propice aux cultures standard."
})

// ===== TÂCHES =====
// ✅ FIX: tasks viennent de fullData.tasks.tasks (pas parcel_crops[].tasks)
function updateTasks(fullData: any) {
  tasks.value = fullData.tasks?.tasks ?? []
}

const formatDate = (date: string) => {
  if (!date) return ""
  try {
    return new Date(date).toLocaleDateString(currentLocale.value === "fr" ? "fr-FR" : "en-GB", { day: "2-digit", month: "short", year: "numeric" })
  } catch {
    return date
  }
}

const nearestTasks = computed(() =>
  [...tasks.value]
    .filter((t) => t.status !== "Cancelled" && t.status !== "Done")
    .sort((a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime())
    .slice(0, 3)
)

// ===== CULTURES depuis fullData =====
// ✅ FIX: parcel_crops est à la racine de fullData avec parcel_crop_id, crop.name, area
const parcelCropsFromFullData = computed(() =>
  Array.isArray(parcelFullData.parcel_crops) ? parcelFullData.parcel_crops : []
)

// ===== GRAPHIQUES =====
let taskChart: Chart | null = null
let yieldChart: Chart | null = null

function updateTaskChart() {
  // ✅ FIX: utilise tasks.value directement
  const statusCount = tasks.value.reduce((acc: Record<string, number>, t) => {
    acc[t.status] = (acc[t.status] || 0) + 1
    return acc
  }, {})

  const ctx = document.getElementById("taskPerformanceChart") as HTMLCanvasElement
  if (!ctx) return
  if (taskChart) taskChart.destroy()

  taskChart = new Chart(ctx.getContext("2d")!, {
    type: "doughnut",
    data: {
      labels: Object.keys(statusCount).map((s) => t(`status${s.replace(/\s+/g, "")}`)),
      datasets: [{
        label: t("chartTasksByStatus"),
        data: Object.values(statusCount),
        backgroundColor: ["#10b481", "#112830", "#f43f5e", "#fbbf24"],
        borderWidth: 0,
        hoverOffset: 10
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "80%",
      plugins: { 
        legend: { display: false } 
      },
    },
  })
}

function updateYieldEvolutionChart() {
  // ✅ FIX: yield_records à la racine de fullData, champ "yield" (pas r.yield → r.yield)
  const records = parcelFullData.yield_records ?? []
  if (!records.length) return

  const grouped: Record<string, number> = {}
  records.forEach((r: any) => {
    const monthYear = new Date(r.date).toLocaleString("default", { month: "short", year: "numeric" })
    grouped[monthYear] = (grouped[monthYear] || 0) + (r.yield ?? 0)
  })

  const labels = Object.keys(grouped).sort((a, b) => new Date(a).getTime() - new Date(b).getTime())
  const data   = labels.map((l) => grouped[l] ?? 0)

  const ctx = document.getElementById("yieldEvolutionChart") as HTMLCanvasElement
  if (!ctx) return
  if (yieldChart) yieldChart.destroy()

  yieldChart = new Chart(ctx.getContext("2d")!, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: t("chartYieldEvolution"),
        data,
        backgroundColor: "#10b481",
        borderRadius: 12,
        borderSkipped: false,
        barThickness: 24,
        hoverBackgroundColor: "#ffffff",
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "#ffffff",
          titleColor: "#112830",
          bodyColor: "#112830",
          titleFont: { weight: 'bold' },
          padding: 12,
          cornerRadius: 12,
          displayColors: false
        },
      },
      scales: {
        x: { 
          grid: { display: false }, 
          ticks: { color: "rgba(255,255,255,0.4)", font: { size: 10, weight: "bold" } } 
        },
        y: { 
          beginAtZero: true, 
          grid: { color: "rgba(255,255,255,0.05)" },
          ticks: { color: "rgba(255,255,255,0.4)", font: { size: 10, weight: "bold" } } 
        },
      },
    },
  })
}

// ===== HARVEST =====
function calculateTrends() {
  if (!harvestHistory.value.length) return

  const grouped = harvestHistory.value.reduce((acc: Record<string, any[]>, r) => {
    const key = r.parcel_crop_id
    if (!acc[key]) acc[key] = []
    acc[key].push(r)
    return acc
  }, {})

  Object.values(grouped).forEach((records) => {
    records.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    records.forEach((r, i) => {
      if (i === 0) { r.trend = "neutral"; r.trendValue = 0; return }
      const diff = r.yield - records[i - 1].yield
      r.trend      = diff > 0 ? "up" : diff < 0 ? "down" : "neutral"
      r.trendValue = Math.abs(diff)
    })
  })

  harvestHistory.value = Object.values(grouped).flat()
}

function updatePaginatedHarvest() {
  const start = (currentPage.value - 1) * itemsPerPage
  paginatedHarvest.value = (harvestHistory.value ?? []).slice(start, start + itemsPerPage).map((r, idx) => ({
    // ✅ FIX: yield_records n'a pas d'id → on génère un id stable
    id:         r.id ?? `${r.parcel_crop_id}-${r.date}-${idx}`,
    date:       r.date,
    quantity:   r.yield,
    observation:r.notes,
    trend:      r.trend ?? "neutral",
    trendValue: r.trendValue ?? 0,
  }))
}

const totalPages = computed(() =>
  Math.max(1, Math.ceil((harvestHistory.value ?? []).length / itemsPerPage))
)

const visiblePages = computed(() => {
  const pages: (number | string)[] = []
  for (let i = 1; i <= totalPages.value; i++) pages.push(i)
  return pages
})

watch(harvestHistory, updatePaginatedHarvest, { immediate: true })
watch(currentPage,   updatePaginatedHarvest)

function prevPage()  { if (currentPage.value > 1) currentPage.value-- }
function nextPage()  { if (currentPage.value < totalPages.value) currentPage.value++ }
function goToPage(p: number | string) { if (typeof p === "number") currentPage.value = p }

async function deleteRecord(id: string) {
  try {
    await apiFetch(`/api/yield-records/${id}/`, { method: "DELETE" })
    harvestHistory.value = harvestHistory.value.filter((r) => r.id !== id)
  } catch (e) {
    console.error("Erreur suppression record:", e)
  }
}

function exportCSV() {
  const data = paginatedHarvest.value
  if (!data.length) return
  const headers = Object.keys(data[0])
  const csv = [headers.join(","), ...data.map((r) => headers.map((h) => `"${(r as any)[h]}"`).join(","))].join("\n")
  const link = Object.assign(document.createElement("a"), {
    href: URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8;" })),
    download: "harvest_history.csv",
  })
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// ===== SURFACE =====
// ✅ FIX: parcel.points utilise lat/lng (pas latitude/longitude)
const parcelAreaHa = computed(() => calculateParcelArea(parcelData.points))

function calculateParcelArea(points: any[]) {
  if (!points || points.length < 3) return 0
  let area = 0
  const n = points.length
  for (let i = 0; i < n; i++) {
    // ✅ FIX: lat/lng (pas latitude/longitude)
    const { lat: x1, lng: y1 } = points[i]
    const { lat: x2, lng: y2 } = points[(i + 1) % n]
    area += x1 * y2 - x2 * y1
  }
  area = Math.abs(area / 2)
  const avgLat = points.reduce((s, p) => s + p.lat, 0) / points.length
  const areaM2 = area * 111_000 * 111_000 * Math.cos((avgLat * Math.PI) / 180)
  return (areaM2 / 10_000).toFixed(2)
}

function formatM2(areaInHa: any) {
  if (!areaInHa) return "- m²"
  return `${(Number(areaInHa) * 10000).toLocaleString()} m²`
}

// ===== ANALYTICS =====
async function fetchAnalyticsData() {
  if (!authStore.isAuthenticated) return
  try {
    const data: any = await apiFetch("/api/analytics/yields/")
    analyticsData.value = Object.values(data).map((parcel: any) => ({
      ...parcel,
      mean_yield:          parcel.mean_yield ?? 0,
      mean_yield_per_area: parcel.mean_yield_per_area ?? 0,
      parcel_name:         parcel.parcel_name ?? "Unknown Parcel",
    }))
  } catch (e) {
    console.error("Erreur fetchAnalyticsData:", e)
  }
}

// ✅ FIX: parcelData.name au lieu de parcelData.parcel_name
watch(() => parcelData.name, (name) => {
  if (!name) return
  selectedParcel.value = analyticsData.value.find(
    (p) => p.parcel_name?.trim().toLowerCase() === String(name).trim().toLowerCase()
  ) ?? null
})

// ===== GESTION DES PLANTATIONS =====
async function fetchCropOptions() {
  try {
    const cropsData: any = await apiFetch("/api/crops/")
    cropsOptions.value = cropsData?.results || cropsData || []
    
    const statusData: any = await apiFetch("/api/status-crops/")
    statusOptions.value = statusData?.results || statusData || []
  } catch (e) {
    console.error("Erreur lors du chargement des options de culture :", e)
  }
}

function openCropDetails(crop: any) {
  selectedCropDetails.value = crop
  showDetailsModal.value = true
}

function openAddCropModal() {
  isEditingCrop.value = false
  currentCropId.value = null
  cropForm.crop_id = cropsOptions.value[0]?.id || ""
  cropForm.planting_date = new Date().toISOString().split('T')[0] ?? ""
  cropForm.harvest_date = ""
  cropForm.area = 500
  cropForm.status_id = statusOptions.value[0]?.id || ""
  showCropModal.value = true
}

function openEditCropModal(crop: any) {
  isEditingCrop.value = true
  currentCropId.value = crop.parcel_crop_id
  cropForm.crop_id = crop.crop?.id || ""
  cropForm.planting_date = crop.planting_date || ""
  cropForm.harvest_date = crop.harvest_date || ""
  cropForm.area = crop.area || 0
  cropForm.status_id = statusOptions.value.find(s => s.name === crop.status)?.id || ""
  showCropModal.value = true
}

async function saveCrop() {
  try {
    const payload = {
      crop_id: cropForm.crop_id,
      planting_date: cropForm.planting_date,
      harvest_date: cropForm.harvest_date || null,
      area: parseFloat(cropForm.area as any) || 0,
      status_id: cropForm.status_id || null,
    }
    
    if (isEditingCrop.value && currentCropId.value) {
      await apiFetch(`/api/parcel-crops/${currentCropId.value}/`, {
        method: "PATCH",
        body: payload
      })
    } else {
      await apiFetch("/api/parcel-crops/", {
        method: "POST",
        body: {
          ...payload,
          parcel: fieldIdParam
        }
      })
    }
    
    showCropModal.value = false
    await fetchParcelData()
  } catch (e) {
    console.error("Erreur lors de l'enregistrement de la culture :", e)
    alert("Impossible d'enregistrer la culture. Veuillez vérifier les informations.")
  }
}

function confirmDeleteCrop(id: number) {
  cropToDeleteId.value = id
  showDeleteCropModal.value = true
}

async function deleteCropConfirmed() {
  if (!cropToDeleteId.value) return
  try {
    await apiFetch(`/api/parcel-crops/${cropToDeleteId.value}/`, {
      method: "DELETE"
    })
    showDeleteCropModal.value = false
    cropToDeleteId.value = null
    await fetchParcelData()
  } catch (e) {
    console.error("Erreur lors de la suppression de la culture :", e)
    alert("Impossible de supprimer la culture.")
  }
}

// ===== CHARGEMENT PRINCIPAL =====
async function fetchParcelData() {
  if (!authStore.isAuthenticated || !fieldIdParam) return

  try {
    const fullData: any = await apiFetch(`/api/parcels/${fieldIdParam}/full_data/`)

    Object.assign(parcelFullData, fullData)
    // ✅ FIX: parcel est directement fullData.parcel (name, points, uuid, created_at)
    Object.assign(parcelData, fullData.parcel ?? {})

    if (fullData.weather_data) updateWeatherForecast(fullData)

    // ✅ FIX: soil layers dans fullData.soil_data.data.properties.layers
    updateSoilQualities(fullData.soil_data?.data?.properties?.layers)

    // ✅ FIX: tasks depuis fullData.tasks.tasks
    updateTasks(fullData)

    await nextTick()
    updateTaskChart()
    updateYieldEvolutionChart()
    await initMap()

    // ✅ FIX: yield_records à la racine de fullData
    harvestHistory.value = fullData.yield_records ?? []
    calculateTrends()
    updatePaginatedHarvest()

    // ✅ FIX: parcel n'a pas de champ owner → on ne fait pas l'appel si undefined
    const ownerId = fullData.parcel?.owner
    if (ownerId) {
      try {
        const uData: any = await apiFetch(`/api/users/${ownerId}/`)
        Object.assign(ownerData, uData)
      } catch {
        // owner endpoint peut ne pas exister
      }
    }

  } catch (error) {
    console.error("Erreur fetchParcelData:", error)
  }
}

async function fetchParcelCrops() {
  // ✅ parcel_crops vient déjà de fullData → cet appel reste pour la compatibilité filteredParcelCrops
  if (!authStore.isAuthenticated || !fieldIdParam) return
  try {
    const data: any = await apiFetch("/api/parcel-crops/")
    parcelCrops.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error("Erreur fetchParcelCrops:", e)
    parcelCrops.value = []
  }
}

onMounted(() => {
  fetchParcelData()
  fetchAnalyticsData()
  fetchParcelCrops()
  fetchCropOptions()
})
</script>

<style scoped>
.scrollbar-hidden::-webkit-scrollbar {
  display: none;
}
.scrollbar-hidden {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

#map {
  height: 100%;
  width: 100%;
}

:deep(.leaflet-bar) {
  border: none;
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}

:deep(.leaflet-bar a) {
  background-color: white;
  color: #112830;
  border-radius: 12px !important;
  margin-bottom: 5px;
  border: none;
}

.pop-notification-enter-active,
.pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
.pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px) scale(0.9);
}
</style>