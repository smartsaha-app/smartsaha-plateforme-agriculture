<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 text-[#112830]">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Nouvelle parcelle">
      <template #subtitle>
        <i class="bx bx-map-pin"></i>
        Dessinez votre parcelle en cliquant sur les points de la carte
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">Parcelles</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Nouvelle</span>
      </template>
    </PageHeader>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- ===== FORM PANEL (5/12) ===== -->
      <div class="lg:col-span-5 space-y-4 order-2 lg:order-1">

        <!-- Instructions collapsible -->
        <div class="bg-amber-50 rounded-2xl border border-amber-100 overflow-hidden">
          <button
            @click="showInstructions = !showInstructions"
            class="w-full px-5 py-4 flex items-center justify-between text-amber-700 hover:bg-amber-100/50 transition-colors"
          >
            <div class="flex items-center gap-2.5">
              <div class="w-7 h-7 bg-amber-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <i class="bx bx-bulb text-amber-600 text-sm"></i>
              </div>
              <span class="text-[12px] font-semibold">{{ t("instructions") }}</span>
            </div>
            <i :class="['bx bx-chevron-down text-amber-500 text-lg transition-transform duration-300', showInstructions ? 'rotate-180' : '']"></i>
          </button>
          <transition
            enter-active-class="transition-all duration-300 ease-out"
            leave-active-class="transition-all duration-200 ease-in"
            enter-from-class="opacity-0 max-h-0"
            enter-to-class="opacity-100 max-h-96"
            leave-from-class="opacity-100 max-h-96"
            leave-to-class="opacity-0 max-h-0"
          >
            <div v-show="showInstructions" class="px-5 pb-5">
              <ol class="space-y-2.5">
                <li v-for="(step, i) in ['step1','step2','step3','step4','step5']" :key="i"
                  class="flex gap-3 text-[12px] text-amber-800/80 leading-relaxed">
                  <span class="w-5 h-5 rounded-full bg-amber-200 text-amber-700 flex items-center justify-center text-[10px] font-bold flex-shrink-0 mt-0.5">{{ i + 1 }}</span>
                  <span v-html="formatBold(t(step))"></span>
                </li>
              </ol>
            </div>
          </transition>
        </div>

        <!-- Main form card -->
        <form @submit.prevent="submitForm" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-5">

          <!-- Search address -->
          <div class="space-y-2">
            <label class="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider">{{ t("searchonmap") }}</label>
            <div class="relative">
              <i class="bx bx-search absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
              <input
                v-model="form.search"
                type="text"
                :placeholder="t('searchonmap')"
                @input="onSearchInput"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
              />
            </div>
          </div>

          <div class="border-t border-gray-50"></div>

          <!-- Parcel name -->
          <div class="space-y-2">
            <label class="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider">
              {{ t("thparcelname") }} <span class="text-rose-400">*</span>
            </label>
            <div class="relative">
              <i class="bx bx-map-pin absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
              <input
                v-model="form.parcel"
                type="text"
                required
                :placeholder="t('parcel_name_placeholder')"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
              />
            </div>
          </div>

          <!-- Area display -->
          <div class="flex items-center justify-between px-4 py-3.5 bg-gradient-to-r from-emerald-50 to-teal-50/60 rounded-xl border border-emerald-100">
            <div>
              <p class="text-[10px] font-semibold text-emerald-600 uppercase tracking-wider mb-0.5">{{ t("parcel_area") }}</p>
              <p class="text-[22px] font-black text-[#112830] tracking-tight leading-none">{{ formatM2(form.area) }}</p>
            </div>
            <div class="w-10 h-10 bg-emerald-100 rounded-xl flex items-center justify-center">
              <i class="bx bx-area text-emerald-600 text-xl"></i>
            </div>
          </div>

          <div class="border-t border-gray-50"></div>

          <!-- Points section -->
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="w-6 h-6 bg-[#112830] rounded-md flex items-center justify-center">
                  <i class="bx bx-map-alt text-white text-xs"></i>
                </div>
                <span class="text-[12px] font-semibold text-gray-700">{{ t("points") }}</span>
              </div>
              <span :class="[
                'text-[10px] font-bold px-2.5 py-0.5 rounded-full',
                form.points.length >= 3 ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'
              ]">{{ form.points.length }} / min 3</span>
            </div>

            <!-- Points list -->
            <div v-if="form.points.length > 0" class="max-h-44 overflow-y-auto space-y-1.5 scrollbar-hidden">
              <div
                v-for="(p, i) in form.points"
                :key="i"
                class="flex items-center gap-3 px-3 py-2.5 bg-gray-50 rounded-xl border border-gray-50 hover:border-gray-100 transition-colors group"
              >
                <span class="w-6 h-6 bg-[#10b481] rounded-lg text-white text-[10px] font-bold flex items-center justify-center flex-shrink-0">{{ i + 1 }}</span>
                <div class="flex-1 grid grid-cols-2 gap-1 font-mono text-[11px] text-gray-500">
                  <span><span class="text-gray-300 mr-1">lat</span>{{ p.lat.toFixed(5) }}</span>
                  <span><span class="text-gray-300 mr-1">lng</span>{{ p.lng.toFixed(5) }}</span>
                </div>
                <button
                  @click.prevent="removePoint(i)"
                  class="w-6 h-6 rounded-lg text-gray-300 hover:text-rose-500 hover:bg-rose-50 transition-all opacity-0 group-hover:opacity-100 flex items-center justify-center"
                >
                  <i class="bx bx-x text-base"></i>
                </button>
              </div>
            </div>

            <!-- Empty state -->
            <div v-else class="py-8 text-center bg-gray-50 rounded-xl border border-dashed border-gray-200">
              <i class="bx bx-map-alt text-gray-200 text-3xl mb-2 block"></i>
              <p class="text-[12px] text-gray-400 font-medium">{{ t("nopoinntsfound") }}</p>
              <p class="text-[11px] text-gray-300 mt-0.5">Cliquez sur la carte pour commencer</p>
            </div>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="isLoading || form.points.length < 3"
            class="w-full py-3.5 bg-[#112830] text-white rounded-xl font-semibold text-[14px] hover:bg-[#10b481] transition-all duration-300 shadow-lg shadow-[#112830]/10 hover:shadow-[#10b481]/20 flex items-center justify-center gap-2.5 disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <template v-if="isLoading">
              <i class="bx bx-loader-alt animate-spin text-lg"></i>
              {{ t("loading") }}
            </template>
            <template v-else>
              <i class="bx bx-save text-lg group-hover:scale-110 transition-transform"></i>
              {{ t("btnsaveparcel") }}
            </template>
          </button>
        </form>
      </div>

      <!-- ===== MAP PANEL (7/12) ===== -->
      <div class="lg:col-span-7 order-1 lg:order-2">
        <div class="relative h-[480px] lg:h-full min-h-[600px] rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
          <div id="map" class="h-full w-full z-10"></div>

          <!-- Map hint badge -->
          <!-- <div class="absolute top-4 left-4 z-20 pointer-events-none">
            <div class="flex items-center gap-2 bg-white/90 backdrop-blur-sm px-3.5 py-2 rounded-xl shadow-sm border border-gray-100 text-[12px] font-medium text-gray-600">
              <i class="bx bx-pointer text-[#10b481] text-base"></i>
              Cliquez sur la carte pour placer des points
            </div>
          </div> -->

          <!-- Status overlay -->
          <div class="absolute bottom-5 left-5 z-20 pointer-events-none">
            <div :class="[
              'flex items-center gap-2.5 px-4 py-2.5 rounded-xl backdrop-blur-md border shadow-lg text-[12px] font-semibold',
              form.points.length >= 3
                ? 'bg-emerald-900/85 border-emerald-700/30 text-emerald-300'
                : 'bg-[#112830]/85 border-white/10 text-white'
            ]">
              <span :class="['w-2 h-2 rounded-full flex-shrink-0', form.points.length >= 3 ? 'bg-emerald-400' : 'bg-amber-400 animate-pulse']"></span>
              {{ form.points.length >= 3 ? `Polygone valide — ${form.points.length} points` : `Besoin de ${3 - form.points.length} point(s) de plus` }}
            </div>
          </div>

          <!-- Loading overlay -->
          <div v-if="isLoading" class="absolute inset-0 bg-[#112830]/40 backdrop-blur-sm flex items-center justify-center z-[100]">
            <div class="w-12 h-12 border-4 border-white/20 border-t-[#10b481] rounded-full animate-spin"></div>
          </div>
        </div>
      </div>

    </div>

    <!-- ===== TOAST ===== -->
    <Transition name="pop-notification">
      <div v-if="notification.visible" class="fixed top-6 left-1/2 -translate-x-1/2 z-[200] w-full max-w-sm px-4">
        <div :class="[
          'bg-white rounded-2xl shadow-2xl p-5 flex items-center gap-4 border border-gray-100',
          notification.type === 'success' ? 'border-l-4 border-l-[#10b481]' : 'border-l-4 border-l-rose-500'
        ]">
          <div :class="[
            'w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0',
            notification.type === 'success' ? 'bg-emerald-50 text-[#10b481]' : 'bg-rose-50 text-rose-500'
          ]">
            <i :class="notification.type === 'success' ? 'bx bx-check-circle' : 'bx bx-error-circle'"></i>
          </div>
          <div class="flex-1">
            <p class="text-[13px] font-semibold text-[#112830]">{{ notification.message }}</p>
            <p class="text-[11px] text-gray-400 mt-0.5">{{ notification.type === 'success' ? 'Redirection en cours…' : 'Vérifiez les informations' }}</p>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from "vue";
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
const showInstructions = ref(true);
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
  const first = points[0];
  if (first) coords.push([first.lng, first.lat]);
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
      { color: "#10b481", fillColor: "#10b481", fillOpacity: 0.15, weight: 2 }
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
    L.circleMarker([p.lat, p.lng], { radius: 7, color: "#10b481", fillColor: "#ffffff", fillOpacity: 1, weight: 2.5 }).addTo(map);
    L.tooltip({ permanent: true, direction: "top", offset: [0, -5], className: 'custom-map-label' }).setContent(`${p.order}`).setLatLng([p.lat, p.lng]).addTo(map);
  });
  updatePolygon();
}

onMounted(async () => {
  if (!import.meta.client) return;
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
      L.circleMarker([p.lat, p.lng], { radius: 7, color: "#10b481", fillColor: "#ffffff", fillOpacity: 1, weight: 2.5 }).addTo(map);
      L.tooltip({ permanent: true, direction: "top", offset: [0, -5], className: 'custom-map-label' }).setContent(`${t('point')} ${p.order}`).setLatLng([p.lat, p.lng]).addTo(map);
    });
    updatePolygon();
  });
});

const formatM2 = (areaInHa: string | number) => areaInHa ? `${(parseFloat(String(areaInHa)) * 10000).toLocaleString()} m²` : "— m²";
const formatBold = (text: string) => text.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
</script>

<style scoped>
#map { height: 100%; width: 100%; }

.pop-notification-enter-active,
.pop-notification-leave-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.pop-notification-enter-from,
.pop-notification-leave-to {
  opacity: 0;
  transform: translate(-50%, -16px) scale(0.95);
}

.scrollbar-hidden::-webkit-scrollbar { display: none; }
.scrollbar-hidden { -ms-overflow-style: none; scrollbar-width: none; }

:deep(.custom-map-label) {
  background: #112830;
  border: none;
  border-radius: 6px;
  color: white;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 6px;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.2);
}

:deep(.leaflet-control-layers) {
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
}
</style>