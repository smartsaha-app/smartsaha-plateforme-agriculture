<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 text-[#112830]">

    <!-- ===== HEADER ===== -->
    <PageHeader title="Modifier la parcelle">
      <template #subtitle>
        <i class="bx bx-edit"></i>
        Mettez à jour le nom ou repositionnez les points de la parcelle
      </template>
      <template #breadcrumb>
        <NuxtLink to="/farmer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>Accueil</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <NuxtLink to="/farmer/parcels" class="hover:text-[#10b481] transition-colors">Parcelles</NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">Modifier</span>
      </template>
    </PageHeader>
    <!-- Polygon status badge -->
    <div class="flex justify-end -mt-2 mb-6">
      <div :class="[
        'flex items-center gap-2 px-3.5 py-2 rounded-xl text-[12px] font-semibold border',
        form.parcel_points.length >= 3
          ? 'bg-emerald-50 border-emerald-100 text-emerald-700'
          : 'bg-amber-50 border-amber-100 text-amber-700'
      ]">
        <span :class="['w-2 h-2 rounded-full flex-shrink-0', form.parcel_points.length >= 3 ? 'bg-emerald-500' : 'bg-amber-400 animate-pulse']"></span>
        {{ form.parcel_points.length >= 3 ? `${form.parcel_points.length} points` : `${3 - form.parcel_points.length} point(s) manquant(s)` }}
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading && !form.parcel_name" class="flex flex-col items-center justify-center py-24 gap-4 text-gray-400">
      <div class="w-10 h-10 border-4 border-gray-200 border-t-[#10b481] rounded-full animate-spin"></div>
      <p class="text-[13px]">Chargement de la parcelle…</p>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-6">

      <!-- ===== FORM PANEL (5/12) ===== -->
      <div class="lg:col-span-5 space-y-4 order-2 lg:order-1">

        <!-- Owner card -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 flex items-center gap-4">
          <div class="w-10 h-10 bg-[#112830] rounded-xl flex items-center justify-center flex-shrink-0">
            <i class="bx bx-user text-white text-lg"></i>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">{{ t("parcel_owner") }}</p>
            <p class="text-[14px] font-semibold text-[#112830] truncate">{{ ownerName || '—' }}</p>
          </div>
          <span class="text-[10px] font-semibold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-100">
            Propriétaire
          </span>
        </div>

        <!-- Edit form card -->
        <form @submit.prevent="submitParcel" class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 space-y-5">

          <!-- Parcel name -->
          <div class="space-y-2">
            <label class="block text-[11px] font-semibold text-gray-400 uppercase tracking-wider">
              {{ t("thparcelname") }} <span class="text-rose-400">*</span>
            </label>
            <div class="relative">
              <i class="bx bx-map-pin absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-lg pointer-events-none"></i>
              <input
                v-model="form.parcel_name"
                type="text"
                required
                placeholder="Nom de la parcelle"
                class="w-full pl-11 pr-4 py-3 bg-gray-50 border border-gray-100 rounded-xl text-[14px] focus:outline-none focus:ring-2 focus:ring-[#10b481]/20 focus:border-[#10b481]/40 focus:bg-white transition-all placeholder:text-gray-300"
              />
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
                <span class="text-[12px] font-semibold text-gray-700">{{ t("pointsParcel") }}</span>
              </div>
              <span :class="[
                'text-[10px] font-bold px-2.5 py-0.5 rounded-full',
                form.parcel_points.length >= 3 ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'
              ]">{{ form.parcel_points.length }} pts</span>
            </div>

            <div class="max-h-52 overflow-y-auto space-y-1.5 scrollbar-hidden">
              <div
                v-for="(point, index) in form.parcel_points"
                :key="index"
                class="flex items-center gap-2.5 px-3 py-2 bg-gray-50 rounded-xl border border-gray-50 hover:border-gray-100 transition-colors group"
              >
                <span class="w-6 h-6 bg-[#10b481] rounded-lg text-white text-[10px] font-bold flex items-center justify-center flex-shrink-0">{{ index + 1 }}</span>
                <div class="flex-1 grid grid-cols-2 gap-2">
                  <div class="relative">
                    <span class="absolute left-2 top-1/2 -translate-y-1/2 text-[9px] text-gray-300 font-semibold pointer-events-none">lat</span>
                    <input
                      v-model.number="point.latitude"
                      type="number"
                      step="any"
                      @input="updateMapFromInputs"
                      class="w-full pl-7 pr-2 py-1.5 bg-white border border-gray-100 rounded-lg font-mono text-[11px] text-gray-600 focus:outline-none focus:ring-1 focus:ring-[#10b481]/30 focus:border-[#10b481]/40 transition-all"
                    />
                  </div>
                  <div class="relative">
                    <span class="absolute left-2 top-1/2 -translate-y-1/2 text-[9px] text-gray-300 font-semibold pointer-events-none">lng</span>
                    <input
                      v-model.number="point.longitude"
                      type="number"
                      step="any"
                      @input="updateMapFromInputs"
                      class="w-full pl-7 pr-2 py-1.5 bg-white border border-gray-100 rounded-lg font-mono text-[11px] text-gray-600 focus:outline-none focus:ring-1 focus:ring-[#10b481]/30 focus:border-[#10b481]/40 transition-all"
                    />
                  </div>
                </div>
                <button
                  @click.prevent="removePoint(index)"
                  class="w-6 h-6 rounded-lg text-gray-300 hover:text-rose-500 hover:bg-rose-50 transition-all opacity-0 group-hover:opacity-100 flex items-center justify-center flex-shrink-0"
                >
                  <i class="bx bx-trash text-sm"></i>
                </button>
              </div>
            </div>

            <p class="text-[11px] text-gray-300 text-center">Cliquez sur la carte pour ajouter un point</p>
          </div>

          <!-- Actions -->
          <div class="flex gap-3 pt-1">
            <button
              type="button"
              @click="resetToOriginal"
              class="flex-1 py-3 bg-gray-50 border border-gray-100 text-gray-500 rounded-xl text-[13px] font-semibold hover:bg-gray-100 transition-colors flex items-center justify-center gap-2"
            >
              <i class="bx bx-reset text-base"></i>
              Réinitialiser
            </button>
            <button
              type="submit"
              :disabled="isLoading || form.parcel_points.length < 3"
              class="flex-1 py-3 bg-[#112830] text-white rounded-xl text-[13px] font-semibold hover:bg-[#10b481] transition-all duration-300 shadow-lg shadow-[#112830]/10 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed group"
            >
              <template v-if="isLoading">
                <i class="bx bx-loader-alt animate-spin text-base"></i>
                Enregistrement…
              </template>
              <template v-else>
                <i class="bx bx-save text-base group-hover:scale-110 transition-transform"></i>
                {{ t("btnsaveparcel") }}
              </template>
            </button>
          </div>
        </form>
      </div>

      <!-- ===== MAP PANEL (7/12) ===== -->
      <div class="lg:col-span-7 order-1 lg:order-2">
        <div class="relative h-[480px] lg:h-full min-h-[600px] rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
          <div id="map" class="h-full w-full z-10"></div>

          <!-- Hint badge -->
          <div class="absolute top-4 left-4 z-20 pointer-events-none">
            <div class="flex items-center gap-2 bg-white/90 backdrop-blur-sm px-3.5 py-2 rounded-xl shadow-sm border border-gray-100 text-[12px] font-medium text-gray-600">
              <i class="bx bx-pointer text-[#10b481] text-base"></i>
              Cliquez pour ajouter un point
            </div>
          </div>

          <!-- Status overlay -->
          <div class="absolute bottom-5 left-5 z-20 pointer-events-none">
            <div :class="[
              'flex items-center gap-2.5 px-4 py-2.5 rounded-xl backdrop-blur-md border shadow-lg text-[12px] font-semibold',
              form.parcel_points.length >= 3
                ? 'bg-emerald-900/85 border-emerald-700/30 text-emerald-300'
                : 'bg-[#112830]/85 border-white/10 text-white'
            ]">
              <span :class="['w-2 h-2 rounded-full flex-shrink-0', form.parcel_points.length >= 3 ? 'bg-emerald-400' : 'bg-amber-400 animate-pulse']"></span>
              {{ form.parcel_points.length >= 3 ? `Polygone valide — ${form.parcel_points.length} points` : `Besoin de ${3 - form.parcel_points.length} point(s) de plus` }}
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
            <p class="text-[11px] text-gray-400 mt-0.5">Mise à jour réussie</p>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });

import { ref, onMounted, reactive } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const { apiFetch } = useApi();
const id = route.params.id as string;

const isLoading = ref(false);
const originalData = ref<any>(null);
const ownerName = ref("");
const ownerUUID = ref("");

const notification = ref({ visible: false, message: "", type: "success" });

const form = reactive({
  parcel_name: "",
  parcel_points: [] as { latitude: number; longitude: number; order: number }[],
});

let L: any;
let map: any;
let drawnPolygon: any = null;

const showNotification = (message: string, type: "success" | "error" = "success") => {
  notification.value.message = message;
  notification.value.type = type;
  notification.value.visible = true;
  setTimeout(() => (notification.value.visible = false), 3000);
};

async function fetchParcelData() {
  if (!authStore.isAuthenticated) return;
  isLoading.value = true;
  try {
    const data: any = await apiFetch(`/api/parcels/${id}/`);
    originalData.value = JSON.parse(JSON.stringify(data));
    ownerUUID.value = data.owner;

    form.parcel_name = data.parcel_name || "";
    form.parcel_points = data.parcel_points?.length
      ? data.parcel_points.map((p: any) => ({
          latitude: p.latitude,
          longitude: p.longitude,
          order: p.order,
        }))
      : [];

    if (data.owner) {
      try {
        const uData: any = await apiFetch(`/api/users/${data.owner}/`);
        ownerName.value = `${uData.first_name || ""} ${uData.last_name || ""}`.trim() || data.owner;
      } catch {
        ownerName.value = data.owner;
      }
    }

    await initMap();
  } catch (err) {
    console.error(err);
    showNotification("Erreur lors du chargement de la parcelle", "error");
  } finally {
    isLoading.value = false;
  }
}

async function initMap() {
  if (!import.meta.client || map) return;

  L = await import("leaflet");
  await import("leaflet/dist/leaflet.css");

  delete (L.Icon.Default.prototype as any)._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
  });

  const satellite = L.tileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", { attribution: "Esri" });
  const streets = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "OSM" });

  map = L.map("map", { center: [-18.8792, 47.5079], zoom: 6, layers: [satellite] });
  L.control.layers({ "Satellite": satellite, "Rues": streets }).addTo(map);

  map.on("click", (e: any) => {
    form.parcel_points.push({
      latitude: e.latlng.lat,
      longitude: e.latlng.lng,
      order: form.parcel_points.length + 1
    });
    refreshMapLayers();
  });

  refreshMapLayers(true);
}

function refreshMapLayers(fit = false) {
  if (!map || !L) return;

  map.eachLayer((layer: any) => {
    if (layer instanceof L.CircleMarker || layer instanceof L.Tooltip || layer instanceof L.Polygon) {
      map.removeLayer(layer);
    }
  });

  if (form.parcel_points.length === 0) return;

  const latlngs = form.parcel_points.map(p => [p.latitude, p.longitude]);

  form.parcel_points.forEach((p, i) => {
    L.circleMarker([p.latitude, p.longitude], {
      radius: 7,
      color: "#10b481",
      fillColor: "#ffffff",
      fillOpacity: 1,
      weight: 2.5
    }).addTo(map);

    L.tooltip({ permanent: true, direction: "top", offset: [0, -8], className: 'custom-map-label' })
      .setContent(`${i + 1}`)
      .setLatLng([p.latitude, p.longitude])
      .addTo(map);
  });

  if (form.parcel_points.length >= 3) {
    drawnPolygon = L.polygon(latlngs, {
      color: "#10b481",
      fillColor: "#10b481",
      fillOpacity: 0.15,
      weight: 2
    }).addTo(map);

    if (fit) map.fitBounds(drawnPolygon.getBounds(), { padding: [50, 50] });
  } else if (fit && latlngs[0]) {
    map.setView(latlngs[0] as [number, number], 15);
  }
}

function updateMapFromInputs() {
  refreshMapLayers();
}

function removePoint(index: number) {
  form.parcel_points.splice(index, 1);
  form.parcel_points.forEach((p, i) => (p.order = i + 1));
  refreshMapLayers();
}

function resetToOriginal() {
  if (!originalData.value) return;
  form.parcel_name = originalData.value.parcel_name;
  form.parcel_points = originalData.value.parcel_points.map((p: any) => ({
    latitude: p.latitude,
    longitude: p.longitude,
    order: p.order
  }));
  refreshMapLayers(true);
}

async function submitParcel() {
  isLoading.value = true;
  try {
    const payload = {
      owner: ownerUUID.value,
      parcel_name: form.parcel_name,
      parcel_points: form.parcel_points.map((p, i) => ({
        latitude: p.latitude,
        longitude: p.longitude,
        order: i + 1,
      })),
    };

    await apiFetch(`/api/parcels/${id}/`, { method: "PUT", body: payload });
    showNotification("Parcelle mise à jour avec succès !", "success");
    setTimeout(() => router.push("/farmer/parcels"), 2500);
  } catch (err) {
    console.error(err);
    showNotification("Erreur lors de la mise à jour", "error");
  } finally {
    isLoading.value = false;
  }
}

onMounted(fetchParcelData);
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