<template>
  <div class="p-6 space-y-8 text-[#112830]">
    
    <!-- ===== BREADCRUMB & HEADER ===== -->
    <div class="space-y-2">
      <nav class="flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-gray-400" aria-label="Breadcrumb">
        <NuxtLink to="/farmer/dashboard" class="hover:text-[#10b481] transition-colors flex items-center gap-1">
          <i class="bx bx-home text-xs"></i> Home
        </NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">
          {{ t("parcels") }}
        </NuxtLink>
        <i class="bx bx-chevron-right text-[8px]"></i>
        <span class="text-[#10b481]">{{ t("breadcrumb_create") }}</span>
      </nav>
      <h1 class="text-4xl font-black tracking-tighter">Nouvelle Parcelle</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
      
      <!-- ===== FORM PANEL (5/12) ===== -->
      <div class="lg:col-span-5 space-y-8 order-2 lg:order-1">
        
        <!-- Instructions Panel -->
        <div class="bg-amber-50/50 rounded-[2rem] border border-amber-100 overflow-hidden shadow-sm transition-all">
          <button 
            @click="showInstructions = !showInstructions"
            class="w-full px-8 py-5 flex items-center justify-between text-amber-700 hover:bg-amber-100/50 transition-colors"
          >
            <div class="flex items-center gap-3">
              <i class="bx bx-info-circle text-xl"></i>
              <span class="text-xs font-black uppercase tracking-widest">{{ t("instructions") }}</span>
            </div>
            <i :class="['bx bx-chevron-down transition-transform duration-300', showInstructions ? 'rotate-180' : '']"></i>
          </button>
          <transition 
            enter-active-class="transition-all duration-300 ease-out"
            leave-active-class="transition-all duration-200 ease-in"
            enter-from-class="max-h-0 opacity-0"
            enter-to-class="max-h-96 opacity-100"
            leave-from-class="max-h-96 opacity-100"
            leave-to-class="max-h-0 opacity-0"
          >
            <div v-show="showInstructions" class="px-8 pb-6">
              <ul class="space-y-3 text-xs font-medium text-amber-900/70 leading-relaxed">
                <li v-for="(step, i) in ['step1','step2','step3','step4','step5']" :key="i" class="flex gap-3">
                  <span class="font-black text-amber-400">0{{ i+1 }}.</span>
                  <span v-html="formatBold(t(step))"></span>
                </li>
              </ul>
            </div>
          </transition>
        </div>

        <!-- Create Form -->
        <form @submit.prevent="submitForm" class="bg-white p-10 rounded-[3rem] border border-gray-100 shadow-sm space-y-8">
          
          <!-- Search Address -->
          <div class="space-y-3">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">{{ t("searchonmap") }}</label>
            <div class="relative group">
              <i class="bx bx-search absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
              <input
                v-model="form.search"
                type="text"
                :placeholder="t('searchonmap')"
                @input="onSearchInput"
                class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-medium placeholder:text-gray-300"
              />
            </div>
          </div>

          <!-- Parcel Name -->
          <div class="space-y-3">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">{{ t("thparcelname") }} *</label>
            <div class="relative group">
              <i class="bx bx-rename absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
              <input
                v-model="form.parcel"
                type="text"
                required
                :placeholder="t('parcel_name_placeholder')"
                class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-medium placeholder:text-gray-300"
              />
            </div>
          </div>

          <!-- Surface Read-only -->
          <div class="bg-gray-50 p-6 rounded-[2rem] border border-gray-100 flex items-center justify-between">
            <div>
              <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ t("parcel_area") }}</p>
              <p class="text-2xl font-black text-[#112830] tracking-tighter">{{ formatM2(form.area) }}</p>
            </div>
            <div class="w-12 h-12 bg-white rounded-2xl flex items-center justify-center text-[#10b481] shadow-sm">
              <i class="bx bx-area text-2xl"></i>
            </div>
          </div>

          <!-- Points Display (Mini Table) -->
          <div class="space-y-3">
            <div class="flex items-center justify-between ml-4">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ t("points") }}</label>
              <span class="text-[10px] font-black px-2 py-0.5 bg-[#112830] text-white rounded-full">{{ form.points.length }}</span>
            </div>
            
            <div v-if="form.points.length > 0" class="max-h-52 overflow-y-auto scrollbar-hidden rounded-2xl border border-gray-100">
              <table class="w-full text-left text-[10px] font-black uppercase tracking-widest">
                <thead class="bg-gray-50/50 sticky top-0 backdrop-blur-md">
                  <tr>
                    <th class="p-4 text-gray-300">#</th>
                    <th class="p-4 text-gray-400">Latitude</th>
                    <th class="p-4 text-gray-400">Longitude</th>
                    <th class="p-4"></th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-50 italic">
                  <tr v-for="(p, i) in form.points" :key="i" class="hover:bg-gray-50/50">
                    <td class="p-4 text-[#10b481]">{{ i + 1 }}</td>
                    <td class="p-4 text-gray-400 font-mono">{{ p.lat.toFixed(5) }}</td>
                    <td class="p-4 text-gray-400 font-mono">{{ p.lng.toFixed(5) }}</td>
                    <td class="p-4 text-right">
                      <button @click.prevent="removePoint(i)" class="text-rose-500 hover:scale-125 transition-transform">
                        <i class="bx bx-x text-xl"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="p-8 text-center bg-gray-50 rounded-[2rem] border border-dashed border-gray-200">
              <p class="text-[10px] font-black uppercase tracking-widest text-gray-300 italic">{{ t("nopoinntsfound") }}</p>
            </div>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            :disabled="isLoading || form.points.length < 3"
            class="w-full group bg-[#112830] hover:bg-[#10b481] py-5 rounded-2xl text-white font-black uppercase tracking-widest text-xs flex justify-center items-center gap-3 transition-all duration-500 shadow-xl shadow-[#112830]/10 hover:shadow-[#10b481]/20 hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <template v-if="isLoading">
              <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              {{ t("loading") }}
            </template>
            <template v-else>
              {{ t("btnsaveparcel") }}
              <i class="bx bx-right-arrow-alt text-xl group-hover:translate-x-1 transition-transform"></i>
            </template>
          </button>
        </form>
      </div>

      <!-- ===== MAP PANEL (7/12) ===== -->
      <div class="lg:col-span-7 h-[600px] lg:h-[800px] rounded-[3.5rem] border-8 border-white shadow-2xl relative overflow-hidden order-1 lg:order-2 group">
        <div id="map" class="h-full w-full z-10 transition-transform duration-700 group-hover:scale-[1.02]"></div>
        <!-- Status Overlay -->
        <div class="absolute bottom-10 left-10 z-20 pointer-events-none">
          <div class="bg-[#112830]/90 backdrop-blur-md px-6 py-3 rounded-2xl flex items-center gap-4 text-white shadow-2xl border border-white/10">
            <div :class="['w-3 h-3 rounded-full animate-pulse', form.points.length >= 3 ? 'bg-[#10b481]' : 'bg-rose-500']"></div>
            <span class="text-[10px] font-black uppercase tracking-widest">
              {{ form.points.length < 3 ? `Besoin de ${3 - form.points.length} points de plus` : 'Polygone valide' }}
            </span>
          </div>
        </div>

        <!-- Custom Map Controls (Styling placeholder if needed) -->
         <div v-if="isLoading" class="absolute inset-0 bg-[#112830]/40 backdrop-blur-sm flex items-center justify-center z-[100]">
           <div class="w-16 h-16 border-4 border-white/20 border-t-[#10b481] rounded-full animate-spin"></div>
         </div>
      </div>

    </div>

    <!-- Notification System -->
    <transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-10 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="['bg-white rounded-[2rem] shadow-2xl p-6 flex items-center gap-5 border border-gray-100', notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500']">
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center text-2xl flex-shrink-0', notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500']">
            <i :class="notification.type === 'success' ? 'bx bx-check' : 'bx bx-error'"></i>
          </div>
          <div class="flex-1">
            <p class="text-sm font-black text-[#112830] tracking-tight">{{ notification.message }}</p>
            <p class="text-[10px] font-medium text-gray-400">{{ notification.type === 'success' ? 'Redirection en cours...' : 'Veuillez corriger les points.' }}</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

definePageMeta({ layout: "dashboard" });

let L: any;
const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const showInstructions = ref(false);
const isLoading = ref(false);
const notification = ref({ visible: false, message: "", type: "success" });

const showNotification = (message: string, type: "success" | "error" = "success", duration = 3000) => {
  notification.value.message = message;
  notification.value.type = type;
  notification.value.visible = true;
  setTimeout(() => (notification.value.visible = false), duration);
};

const form = reactive({
  parcel: "",
  search: "",
  points: [] as { lat: number; lng: number; order: number }[],
  area: "",
});

let map: any;
let drawnPolygon: any = null;
let marker: any = null;
let turf: any = null;
let searchTimeout: any = null;

function onSearchInput() {
  if (searchTimeout) clearTimeout(searchTimeout);
  searchTimeout = setTimeout(searchLocation, 500);
}

function calculateParcelArea(points: { lat: number; lng: number }[]) {
  if (!points || points.length < 3 || !turf) return 0;
  const coords = points.map((p) => [p.lng, p.lat]);
  coords.push([points[0].lng, points[0].lat]);
  const polygon = turf.polygon([coords]);
  const areaM2 = turf.area(polygon);
  return areaM2 / 10000;
}

function updatePolygon() {
  if (!map || !L) return;
  if (drawnPolygon) map.removeLayer(drawnPolygon);
  if (form.points.length > 0) {
    drawnPolygon = L.polygon(
      form.points.map((p) => [p.lat, p.lng]),
      { color: "blue" }
    ).addTo(map);
  }
  form.area = form.points.length < 3 ? "" : calculateParcelArea(form.points).toFixed(2);
}

async function searchLocation() {
  if (!form.search) return;
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(form.search)}`, {
      headers: { "User-Agent": "ParcelApp/1.0", "Accept-Language": "mg,fr,en" }
    });
    const results = await response.json();
    if (!results?.length) return;
    const place = results[0];
    const lat = parseFloat(place.lat);
    const lon = parseFloat(place.lon);
    map.setView([lat, lon], 14);
    if (marker) map.removeLayer(marker);
    marker = L.marker([lat, lon]).addTo(map);
  } catch (err) {
    console.error("Erreur recherche:", err);
  }
}

async function submitForm() {
  if (!authStore.isAuthenticated) return;
  isLoading.value = true;
  try {
    const parcel_points = form.points.map((p) => ({
      latitude: p.lat,
      longitude: p.lng,
      order: p.order,
    }));
    const payload = { owner: authStore.uuid, parcel_name: form.parcel, parcel_points };
    await apiFetch("/api/parcels/", { method: "POST", body: payload });
    showNotification(t("success_save"), "success");
    setTimeout(() => router.push("/farmer/parcels"), 3000);
  } catch (err) {
    console.error(err);
    showNotification(t("error_save"), "error");
  } finally {
    isLoading.value = false;
  }
}

function removePoint(index: number) {
  if (!L) return;
  form.points.splice(index, 1);
  form.points.forEach((p, i) => (p.order = i + 1));

  map.eachLayer((layer: any) => {
    if (layer instanceof L.CircleMarker || layer instanceof L.Tooltip || layer instanceof L.Polygon) {
      map.removeLayer(layer);
    }
  });

  form.points.forEach((p) => {
    L.circleMarker([p.lat, p.lng], { radius: 6, color: "#1d4ed8", fillColor: "#3b82f6", fillOpacity: 0.8, weight: 2 }).addTo(map);
    L.tooltip({ permanent: true, direction: "top", offset: [0, -5] }).setContent(`Point ${p.order}`).setLatLng([p.lat, p.lng]).addTo(map);
  });
  updatePolygon();
}

onMounted(async () => {
  if (!process.client) return;
  L = await import("leaflet");
  await import("leaflet/dist/leaflet.css");
  turf = await import("@turf/turf");

  delete (L.Icon.Default.prototype as any)._getIconUrl;
  L.Icon.Default.mergeOptions({ iconRetinaUrl: markerIcon2x, iconUrl: markerIcon, shadowUrl: markerShadow });

  const satellite = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", { attribution: "Esri" });
  const streets = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "OSM" });

  map = L.map("map", { center: [-18.8792, 47.5079], zoom: 6, layers: [satellite] });
  L.control.layers({ Satellite: satellite, "Street Map": streets }).addTo(map);

  map.on("click", (e: any) => {
    form.points.push({ lat: e.latlng.lat, lng: e.latlng.lng, order: form.points.length + 1 });
    map.eachLayer((layer: any) => {
      if (layer instanceof L.CircleMarker || layer instanceof L.Tooltip || layer instanceof L.Polygon) {
        map.removeLayer(layer);
      }
    });
    form.points.forEach((p) => {
      L.circleMarker([p.lat, p.lng], { radius: 6, color: "#1d4ed8", fillColor: "#3b82f6", fillOpacity: 0.8, weight: 2 }).addTo(map);
      L.tooltip({ permanent: true, direction: "top", offset: [0, -5] }).setContent(`${t('point')} ${p.order}`).setLatLng([p.lat, p.lng]).addTo(map);
    });
    updatePolygon();
  });
});

const formatM2 = (areaInHa) => areaInHa ? `${(parseFloat(areaInHa) * 10000).toLocaleString()} m²` : "- m²";
const formatBold = (text: string) => text.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
</script>

<style scoped>
#map {
  height: 100%;
  width: 100%;
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

.scrollbar-hidden::-webkit-scrollbar {
  display: none;
}
.scrollbar-hidden {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

:deep(.leaflet-popup-content-wrapper) {
  border-radius: 1rem;
  padding: 0.5rem;
}

:deep(.leaflet-control-layers) {
  border-radius: 1rem;
  border: none;
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
</style>
