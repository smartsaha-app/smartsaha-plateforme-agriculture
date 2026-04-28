<template>
  <div
    class="flex flex-col lg:flex-row gap-6 relative mb-10 sm:mb-1"
  >
    <div class="w-full lg:w-2/5 space-y-4">
      <form class="space-y-4">
        <div class="space-y-4 rounded">
          <h2
            class="text-2xl sm:text-3xl font-extrabold text-[#222831] mb-4"
          >
            {{ t("titlesaveparcel") }}
          </h2>

          <div class="hidden">
            <label class="text-gray-700 text-sm font-medium mb-1">Owner</label>
            <input
              v-model="user.username"
              type="text"
              class="w-full p-2 border rounded bg-gray-100"
              readonly
            />
          </div>

          <p class="text-gray-700 text-sm font-medium mb-1">
            {{ t("searchintruction") }}
          </p>

          <div class="relative">
            <i
              class="bx bx-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-lg"
            ></i>
            <input
              v-model="form.search"
              type="text"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#10b481] transition"
              :placeholder="t('searchonmap')"
              @input="onSearchInput"
            />
          </div>

          <div>
            <label class="text-gray-700 text-sm font-medium mb-1">{{
              t("points")
            }}</label>

            <div
              v-if="form.points.length"
              class="max-h-56 overflow-y-auto border rounded bg-gray-50"
            >
              <table class="w-full text-sm text-left">
                <thead class="bg-gray-100 sticky top-0">
                  <tr>
                    <th
                      class="px-3 py-2 font-medium text-gray-700 border-b text-center"
                    >
                      #
                    </th>
                    <th class="px-3 py-2 font-medium text-gray-700 border-b">
                      {{ t("thlatitude") }}
                    </th>
                    <th class="px-3 py-2 font-medium text-gray-700 border-b">
                      {{ t("thlongitude") }}
                    </th>
                    <th class="px-3 py-2 font-medium text-gray-700 border-b">
                      {{ t("thactions") }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(p, index) in form.points"
                    :key="index"
                    class="hover:bg-white transition"
                  >
                    <td
                      class="text-gray-700 text-sm font-medium mb-1 text-center"
                    >
                      {{ index + 1 }}
                    </td>
                    <td class="px-3 py-2 border-t">{{ p.lat.toFixed(6) }}</td>
                    <td class="px-3 py-2 border-t">{{ p.lng.toFixed(6) }}</td>
                    <td class="px-3 py-2 border-t text-center">
                      <button
                        type="button"
                        @click="removePoint(index)"
                        class="text-red-500 hover:text-red-700 transition"
                        title="Supprimer le point"
                      >
                        <i class="bx bx-trash text-lg"></i>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <p v-else class="text-xs text-gray-400 italic mt-2">
              {{ t("nopoinntsfound") }}
            </p>
          </div>

          <div>
            <label class="text-gray-700 text-sm font-medium mb-1">
              {{ t("parcelarea") }}
            </label>
            <input
              :value="formatM2(form.area)"
              type="text"
              readonly
              class="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label class="text-gray-700 text-sm font-medium mb-1">
              {{ t("thparcelname") }}
            </label>
            <input
              v-model="form.parcel"
              type="text"
              class="w-full p-2 border rounded"
              placeholder="Parcel name"
            />
          </div>

          <button
            type="button"
            class="bg-[#10b481] text-white px-4 py-3 rounded shadow hover:bg-[#0da06a] w-full transition"
            @click="submitForm"
          >
            {{ t("btnsaveparcel") }}
          </button>
        </div>
      </form>
    </div>

    <div
      class="w-full lg:flex-1 bg-gray-200 rounded shadow-sm h-[350px] sm:h-[400px] lg:h-auto overflow-hidden z-40"
    >
      <div id="map" class="h-full w-full rounded"></div>
    </div>

    <transition name="fade">
      <div
        v-if="notification.visible"
        class="fixed inset-0 flex items-center justify-center z-50 bg-black/20 backdrop-blur-sm"
      >
        <div
          :class="[
            'bg-white rounded-2xl shadow-2xl px-8 py-6 flex flex-col items-center gap-4 w-[340px] text-center transition-all duration-300',
            notification.type === 'success'
              ? 'border-t-4 border-[#10b481]'
              : 'border-t-4 border-red-500',
          ]"
        >
          <div
            v-if="notification.type === 'success'"
            class="w-16 h-16 rounded-full bg-[#10b481] flex items-center justify-center"
          >
            <i class="bx bx-check text-4xl font-extrabold text-white"></i>
          </div>
          <div
            v-else
            class="w-16 h-16 rounded-full bg-red-500 flex items-center justify-center"
          >
            <i class="bx bx-x text-4xl font-extrabold text-white"></i>
          </div>

          <p
            :class="[
              'text-lg font-semibold',
              notification.type === 'success'
                ? 'text-[#10b481]'
                : 'text-red-500',
            ]"
          >
            {{ notification.message }}
          </p>

          <p class="text-gray-500 text-sm">
            {{
              notification.type === "success"
                ? "Redirecting to your dashboard..."
                : "Please try again."
            }}
          </p>
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
import markerIcon from "leaflet/dist/images/marker-icon.png";
import markerIcon2x from "leaflet/dist/images/marker-icon-2x.png";
import markerShadow from "leaflet/dist/images/marker-shadow.png";

let L: any;

const router = useRouter();
const authStore = useAuthStore();
const { apiFetch } = useApi();

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const isLoading = ref(false);
const notification = ref({ visible: false, message: "", type: "success" });

const showNotification = (
  message: string,
  type: "success" | "error" = "success",
  duration = 3000
) => {
  notification.value.message = message;
  notification.value.type = type;
  notification.value.visible = true;
  setTimeout(() => (notification.value.visible = false), duration);
};

const mode = ref<"polygon" | "point">("polygon");
const form = reactive({
  parcel: "",
  search: "",
  latitude: "",
  longitude: "",
  points: [] as { lat: number; lng: number; order: number }[],
  area: "",
});
const user = reactive<{ uuid: string; username: string }>({
  uuid: "",
  username: "",
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
  if (!points || points.length < 3) return 0;
  const coords = points.map((p) => [p.lng, p.lat]);
  coords.push([points[0].lng, points[0].lat]);
  const polygon = turf.polygon([coords]);
  const areaM2 = turf.area(polygon);
  return areaM2 / 10000;
}

function updatePolygon() {
  if (!map) return;
  if (drawnPolygon) map.removeLayer(drawnPolygon);
  if (form.points.length > 0) {
    drawnPolygon = L.polygon(
      form.points.map((p) => [p.lat, p.lng]),
      { color: "blue" }
    ).addTo(map);
  }
  form.area =
    form.points.length < 3
      ? "---"
      : calculateParcelArea(form.points).toFixed(2);
}

function removeLastPoint() {
  if (form.points.length > 0) {
    form.points.pop();
    updatePolygon();
  }
}

async function searchLocation() {
  if (!form.search) return;
  try {
    const response = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
        form.search
      )}`,
      {
        headers: {
          "User-Agent": "ParcelApp/1.0 (contact@tonapp.com)",
          "Accept-Language": "mg,fr,en",
        },
      }
    );
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
  isLoading.value = true;
  try {
    if (!authStore.isAuthenticated) return;

    const parcel_points = form.points.map((p) => ({
      latitude: p.lat,
      longitude: p.lng,
      order: p.order,
    }));

    const payload = { owner: authStore.user?.uuid, parcel_name: form.parcel, parcel_points };

    const data: any = await apiFetch('/api/parcels/', {
      method: "POST",
      body: payload,
    });

    showNotification("Parcel saved successfully!", "success");
    // router.push("/parcels");
  } catch (err) {
    console.error(err);
    showNotification("Network error", "error");
  } finally {
    isLoading.value = false;
  }
}

function removePoint(index: number) {
  const removedPoint = form.points[index];
  if (!removedPoint) return;

  form.points.splice(index, 1);

  form.points.forEach((p, i) => (p.order = i + 1));

  map.eachLayer((layer: any) => {
    if (
      layer instanceof L.CircleMarker ||
      layer instanceof L.Tooltip ||
      layer instanceof L.Polygon
    ) {
      map.removeLayer(layer);
    }
  });

  form.points.forEach((p) => {
    const circle = L.circleMarker([p.lat, p.lng], {
      radius: 6,
      color: "#1d4ed8",
      fillColor: "#3b82f6",
      fillOpacity: 0.8,
      weight: 2,
    }).addTo(map);

    L.tooltip({
      permanent: true,
      direction: "top",
      className: "custom-label",
      offset: [0, -5],
    })
      .setContent(`Point ${p.order}`)
      .setLatLng([p.lat, p.lng])
      .addTo(map);
  });

  if (form.points.length >= 3) {
    drawnPolygon = L.polygon(
      form.points.map((p) => [p.lat, p.lng]),
      { color: "blue" }
    ).addTo(map);
  }

  updatePolygon();
}

onMounted(async () => {
  if (!process.client) return;

  L = await import("leaflet");
  await import("leaflet/dist/leaflet.css");
  turf = await import("@turf/turf");

  delete (L.Icon.Default.prototype as any)._getIconUrl;
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: markerIcon2x,
    iconUrl: markerIcon,
    shadowUrl: markerShadow,
  });

  const satellite = L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    { attribution: "Tiles &copy; Esri" }
  );
  const streets = L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    { attribution: "&copy; OpenStreetMap contributors" }
  );

  map = L.map("map", {
    center: [-18.8792, 47.5079],
    zoom: 6,
    layers: [satellite],
  });

  L.control.layers({ Satellite: satellite, "Street Map": streets }).addTo(map);

  map.on("click", (e: any) => {
    form.points.push({
      lat: e.latlng.lat,
      lng: e.latlng.lng,
      order: form.points.length + 1,
    });

    map.eachLayer((layer: any) => {
      if (
        layer instanceof L.CircleMarker ||
        layer instanceof L.Tooltip ||
        layer instanceof L.Polygon
      ) {
        map.removeLayer(layer);
      }
    });

    form.points.forEach((p) => {
      const circle = L.circleMarker([p.lat, p.lng], {
        radius: 6,
        color: "#1d4ed8",
        fillColor: "#3b82f6",
        fillOpacity: 0.8,
        weight: 2,
      }).addTo(map);

      L.tooltip({
        permanent: true,
        direction: "top",
        className: "custom-label",
        offset: [0, -5],
      })
        .setContent(`Point ${p.order}`)
        .setLatLng([p.lat, p.lng])
        .addTo(map);
    });

    if (form.points.length >= 3) {
      drawnPolygon = L.polygon(
        form.points.map((p) => [p.lat, p.lng]),
        { color: "blue" }
      ).addTo(map);
    }

    updatePolygon();
  });
});

const formatM2 = (areaInHa) => {
  if (!areaInHa) return "- m²";
  return `${(areaInHa * 10000).toLocaleString()} m²`;
};

import { defineEmits } from "vue";
const emit = defineEmits<{
  (e: "next"): void;
}>();

const handleNext = async () => {
  await submitForm(); // Enregistre dans la base de données
  emit("next"); // Passe à l'étape suivante
};
</script>

<style scoped>
#map {
  height: 100%;
  width: 100%;
}
</style>
