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
        <span class="text-[#10b481]">{{ t("titleeditparcel") }}</span>
      </nav>
      <h1 class="text-4xl font-black tracking-tighter">Éditer la Parcelle</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-10">
      
      <!-- ===== FORM PANEL (5/12) ===== -->
      <div class="lg:col-span-5 space-y-8 order-2 lg:order-1">
        
        <!-- Owner Info (Read-only) -->
        <div class="bg-gray-50/50 p-6 rounded-[2rem] border border-gray-100 flex items-center justify-between shadow-sm">
          <div>
            <p class="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-1">{{ t("parcel_owner") }}</p>
            <p class="text-lg font-black text-[#112830] tracking-tighter">{{ ownerName }}</p>
          </div>
          <div class="w-12 h-12 bg-white rounded-2xl flex items-center justify-center text-gray-300 shadow-sm border border-gray-50">
            <i class="bx bx-user text-2xl"></i>
          </div>
        </div>

        <!-- Edit Form -->
        <form @submit.prevent="submitParcel" class="bg-white p-10 rounded-[3rem] border border-gray-100 shadow-sm space-y-8">
          
          <!-- Parcel Name -->
          <div class="space-y-3">
            <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest ml-4">{{ t("thparcelname") }} *</label>
            <div class="relative group">
              <i class="bx bx-rename absolute left-5 top-1/2 -translate-y-1/2 text-xl text-gray-300 group-focus-within:text-[#10b481] transition-colors"></i>
              <input
                v-model="form.parcel_name"
                type="text"
                required
                class="w-full pl-14 pr-6 py-4 bg-gray-50 border-none rounded-2xl focus:ring-2 focus:ring-[#10b481]/20 outline-none transition-all font-medium placeholder:text-gray-300 shadow-inner"
              />
            </div>
          </div>

          <!-- Points Display & Edit -->
          <div class="space-y-4">
            <div class="flex items-center justify-between ml-4">
              <label class="text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ t("pointsParcel") }}</label>
              <span class="text-[10px] font-black px-2 py-0.5 bg-[#10b481] text-white rounded-full transition-all scale-110 shadow-lg shadow-[#10b481]/20">{{ form.parcel_points.length }} pts</span>
            </div>
            
            <div class="max-h-72 overflow-y-auto scrollbar-hidden rounded-[2rem] border border-gray-50 bg-gray-50/30 p-2">
              <table class="w-full text-left text-[10px] font-black uppercase tracking-widest">
                <thead class="bg-white/50 sticky top-0 backdrop-blur-md">
                  <tr>
                    <th class="p-4 text-gray-300">#</th>
                    <th class="p-4 text-gray-400">Lat</th>
                    <th class="p-4 text-gray-400">Lng</th>
                    <th class="p-4"></th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-white/50">
                  <tr v-for="(point, index) in form.parcel_points" :key="index" class="hover:bg-white/80 transition-colors group">
                    <td class="p-4 text-[#10b481]">
                      <span class="w-6 h-6 flex items-center justify-center bg-emerald-50 rounded-lg">{{ index + 1 }}</span>
                    </td>
                    <td class="p-2">
                      <input 
                        v-model.number="point.latitude" 
                        type="number" 
                        step="any"
                        @input="updateMapFromInputs"
                        class="w-full bg-transparent border-none p-2 font-mono text-[10px] focus:ring-0 text-gray-500"
                      />
                    </td>
                    <td class="p-2">
                      <input 
                        v-model.number="point.longitude" 
                        type="number" 
                        step="any"
                        @input="updateMapFromInputs"
                        class="w-full bg-transparent border-none p-2 font-mono text-[10px] focus:ring-0 text-gray-500"
                      />
                    </td>
                    <td class="p-4 text-right">
                      <button @click.prevent="removePoint(index)" class="text-rose-500 opacity-0 group-hover:opacity-100 hover:scale-125 transition-all">
                        <i class="bx bx-trash text-lg"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <p class="text-[8px] font-black uppercase text-gray-300 text-center tracking-widest">Cliquez sur la carte pour ajouter un point</p>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            :disabled="isLoading || form.parcel_points.length < 3"
            class="w-full group bg-[#112830] hover:bg-[#10b481] py-5 rounded-2xl text-white font-black uppercase tracking-widest text-xs flex justify-center items-center gap-3 transition-all duration-500 shadow-xl shadow-[#112830]/10 hover:shadow-[#10b481]/20 hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <template v-if="isLoading">
              <div class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
              {{ t("loading") }}
            </template>
            <template v-else>
              {{ t("btnsaveparcel") }}
              <i class="bx bx-check-double text-xl group-hover:translate-x-1 transition-transform"></i>
            </template>
          </button>
        </form>
      </div>

      <!-- ===== MAP PANEL (Interactive) ===== -->
      <div class="lg:col-span-7 h-[600px] lg:h-[800px] rounded-[3.5rem] border-8 border-white shadow-2xl relative overflow-hidden order-1 lg:order-2">
        <div id="map" class="h-full w-full z-10"></div>
        
        <!-- Interactive Overlay -->
        <div class="absolute top-10 right-10 z-20">
          <button @click="resetToOriginal" class="bg-white/90 backdrop-blur px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest shadow-xl border border-gray-100 hover:bg-[#112830] hover:text-white transition-all">
            Réinitialiser
          </button>
        </div>

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
            <p class="text-[10px] font-medium text-gray-400">Mise à jour réussie</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });

import { ref, onMounted, reactive, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

// Leaflet imports
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

const notification = ref({
  visible: false,
  message: "",
  type: "success",
});

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
    
    // Initialize map after data is loaded
    await initMap();
  } catch (err) {
    console.error(err);
    showNotification("Erreur lors du chargement de la parcelle", "error");
  } finally {
    isLoading.value = false;
  }
}

async function initMap() {
  if (!process.client || map) return;
  
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

  map = L.map("map", {
    center: [-18.8792, 47.5079],
    zoom: 6,
    layers: [satellite]
  });

  L.control.layers({ "Satellite": satellite, "Rues": streets }).addTo(map);

  map.on("click", (e: any) => {
    form.parcel_points.push({
      latitude: e.latlng.lat,
      longitude: e.latlng.lng,
      order: form.parcel_points.length + 1
    });
    refreshMapLayers();
  });

  refreshMapLayers(true); // Fit bounds on first load
}

function refreshMapLayers(fit = false) {
  if (!map || !L) return;

  // Clear previous layers (CircleMarkers, Tooltips, Polygons)
  map.eachLayer((layer: any) => {
    if (layer instanceof L.CircleMarker || layer instanceof L.Tooltip || layer instanceof L.Polygon) {
      map.removeLayer(layer);
    }
  });

  if (form.parcel_points.length === 0) return;

  const latlngs = form.parcel_points.map(p => [p.latitude, p.longitude]);

  // Draw Points
  form.parcel_points.forEach((p, i) => {
    L.circleMarker([p.latitude, p.longitude], {
      radius: 6,
      color: "#10b481",
      fillColor: "#ffffff",
      fillOpacity: 1,
      weight: 3
    }).addTo(map);

    L.tooltip({ permanent: true, direction: "top", offset: [0, -8], className: 'custom-map-label' })
      .setContent(`${i + 1}`)
      .setLatLng([p.latitude, p.longitude])
      .addTo(map);
  });

  // Draw Polygon
  if (form.parcel_points.length >= 3) {
    drawnPolygon = L.polygon(latlngs, {
      color: "#10b481",
      fillColor: "#10b481",
      fillOpacity: 0.2,
      weight: 2
    }).addTo(map);

    if (fit) map.fitBounds(drawnPolygon.getBounds(), { padding: [50, 50] });
  } else if (fit) {
    map.setView(latlngs[0], 15);
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

    await apiFetch(`/api/parcels/${id}/`, {
      method: "PUT",
      body: payload,
    });
    
    showNotification("Parcelle mise à jour avec succès !", "success");
    setTimeout(() => {
      router.push("/farmer/parcels");
    }, 2500);
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

:deep(.custom-map-label) {
  background: #112830;
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 8px;
  font-weight: 900;
  padding: 2px 5px;
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

:deep(.leaflet-control-layers) {
  border-radius: 1rem;
  border: none;
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
</style>
