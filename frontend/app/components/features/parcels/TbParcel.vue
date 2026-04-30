<template>
  <div>
    <div class="mb-6">
      <h2
        class="text-xl sm:text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2"
      >
        <i class="bxr bx-list-ul text-2xl sm:text-3xl"></i>
        {{ t("titleparcellist") }}
      </h2>

      <div class="flex justify-between items-center flex-wrap gap-4 hidden">
        <div class="flex items-center space-x-2">
          <label for="rows" class="text-sm">{{ t("rowperpage") }}</label>
          <select
            id="rows"
            v-model.number="rowsPerPage"
            class="p-1 border rounded"
          >
            <option :value="4">4</option>
            <option :value="8">8</option>
            <option :value="12">12</option>
            <option :value="16">16</option>
          </select>
        </div>
        <div class="flex items-center sm:hidden">
          <button
            @click="showFilters = !showFilters"
            class="p-2 bg-gray-200 rounded hover:bg-gray-300"
          >
            <i class="bx bx-filter-alt text-xl"></i>
          </button>
        </div>

        <div
          :class="[
            'flex space-x-4 items-center flex-wrap mt-2 sm:mt-0',
            showFilters ? 'block w-full' : 'hidden sm:flex',
          ]"
        >
          <input
            v-model="filters.owner"
            type="text"
            :placeholder="t('filterbyowner')"
            class="p-2 border border-gray-300 rounded w-full sm:w-60"
          />
          <input
            v-model="filters.parcel_name"
            type="text"
            :placeholder="t('filterbyparcel')"
            class="p-2 border border-gray-300 rounded w-full sm:w-60"
          />
          <button
            @click="resetFilters"
            class="p-2 bg-gray-200 rounded hover:bg-gray-300 flex items-center justify-center"
          >
            <i class="bxr bx-refresh-cw text-lg"></i>
          </button>
        </div>

        <div class="flex space-x-3 flex-nowrap mt-2 sm:mt-0">
          <div class="relative inline-block group">
            <button
              class="flex items-center bg-white text-[#222831] px-4 py-2 rounded-xl shadow hover:bg-gray-100"
            >
              <i class="bx bx-export mr-2 text-xl"></i> {{ t("export") }}
              <i class="bx bx-chevron-down ml-2"></i>
            </button>
            <div
              class="absolute -mt-1 bg-white rounded shadow-lg w-32 hidden group-hover:block z-50"
            >
              <button
                @click="exportData('pdf')"
                class="block px-4 py-2 w-full text-left hover:bg-gray-100"
              >
                PDF
              </button>
              <button
                @click="exportData('csv')"
                class="block px-4 py-2 w-full text-left hover:bg-gray-100"
              >
                CSV
              </button>
            </div>
          </div>

          <NuxtLink
            to="/parcels/create"
            class="flex items-center bg-[#10b481] text-white px-6 py-2 rounded-xl shadow hover:bg-[#0da06a]"
          >
            <i class="bx bx-plus mr-2 text-xl"></i> {{ t("addparcel") }}
          </NuxtLink>
        </div>
      </div>
    </div>

    <div class="pb-2">
      <div class="overflow-x-auto bg-white">
        <table class="min-w-[700px] w-full text-left border-collapse">
          <thead class="bg-gray-100 text-gray-800">
            <tr>
              <th class="px-6 py-2 border-b hidden">Owner</th>
              <th class="px-6 py-2 border-b">{{ t("thparcelname") }}</th>
              <th class="px-6 py-2 border-b hidden sm:table-cell">
                {{ t("thlatitude") }}
              </th>
              <th class="px-6 py-2 border-b hidden sm:table-cell">
                {{ t("thlongitude") }}
              </th>
              <th class="px-6 py-2 border-b text-center">
                {{ t("thactions") }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="field in paginatedFields"
              :key="field.id"
              class="hover:bg-gray-50 text-gray-800"
            >
              <td class="px-6 py-2 border-b hidden">{{ field.owner }}</td>

              <td class="px-6 py-2 border-b">
                <NuxtLink
                  :to="`/parcels/show/${field.fieldId}`"
                  class="hover:text-[#10b481] transition-colors"
                >
                  {{ field.parcel_name }}
                </NuxtLink>
              </td>

              <td class="px-6 py-2 border-b hidden sm:table-cell">
                {{ field.latitude.toFixed(6) }}
              </td>
              <td class="px-6 py-2 border-b hidden sm:table-cell">
                {{ field.longitude.toFixed(6) }}
              </td>

              <td class="p-3 border-b text-center flex justify-center gap-2">
                <NuxtLink
                  :to="`/parcels/show/${field.fieldId}`"
                  class="p-2 rounded-full hover:bg-[#10b481]/20"
                >
                  <i class="bx bx-show text-[#10b481] text-xl"></i>
                </NuxtLink>

                <NuxtLink
                  :to="`/parcels/edit/${field.fieldId}`"
                  class="p-2 rounded-full hover:bg-[#f4a261]/10"
                >
                  <i class="bx bx-edit text-[#f4a261] text-xl"></i>
                </NuxtLink>
                <button
                  @click="confirmDelete(field.fieldId)"
                  class="p-2 rounded-full hover:bg-[#e63946]/10"
                >
                  <i class="bx bx-trash text-[#e63946] text-xl"></i>
                </button>
              </td>
            </tr>
            <tr v-if="paginatedFields.length === 0">
              <td colspan="6" class="p-6 text-center text-gray-500">
                {{ t("noparcelsfound") }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex justify-between items-center mt-4 mb-2">
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="flex items-center px-3 py-1 rounded disabled:opacity-50"
        >
          <i class="bx bx-chevron-left"></i> {{ t("prev") }}
        </button>

        <div class="flex items-center space-x-2">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="goToPage(page)"
            :class="[
              'px-3 py-1 rounded',
              currentPage === page
                ? 'bg-[#10b481] text-white'
                : 'bg-gray-100 hover:bg-gray-200',
            ]"
            v-if="page !== '...'"
          >
            {{ page }}
          </button>
          <span v-else class="px-2">...</span>
        </div>

        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="flex items-center px-3 py-1 rounded disabled:opacity-50"
        >
          {{ t("next") }} <i class="bx bx-chevron-right"></i>
        </button>
      </div>
    </div>
  </div>

  <div
    v-if="showDeleteModal"
    class="fixed inset-0 flex items-center justify-center bg-black/40 z-50"
  >
    <div class="bg-white rounded p-6 w-80 text-center shadow-lg">
      <h3 class="text-xl font-bold mb-4">Delete Parcel</h3>
      <p class="mb-6">Are you sure you want to delete this parcel?</p>
      <div class="flex justify-center gap-4">
        <button
          @click="deleteParcelConfirmed"
          class="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Yes
        </button>
        <button
          @click="cancelDelete"
          class="bg-gray-300 px-4 py-2 rounded hover:bg-gray-400"
        >
          No
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from "vue";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const authStore = useAuthStore();
const { apiFetch } = useApi();
const showFilters = ref(false);

const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

definePageMeta({
  layout: "dashboard",
});

async function exportData(type: "pdf" | "csv") {
  const data = filteredFields.value.map((f) => ({
    Owner: f.owner,
    FieldID: f.fieldId,
    ParcelName: f.parcel_name,
    Latitude: f.latitude,
    Longitude: f.longitude,
  }));

  if (type === "pdf") {
    if (process.client) {
      const { jsPDF } = await import("jspdf");
      const autoTableModule = await import("jspdf-autotable");

      const doc = new jsPDF();
      autoTableModule.default(doc, {
        head: [["Owner", "FieldID", "ParcelName", "Latitude", "Longitude"]],
        body: data.map(Object.values),
        startY: 20,
      });

      doc.save("parcels.pdf");
    }
  } else {
    if (!data.length) return;
    const headers = Object.keys(data[0]);
    const csvRows = [
      headers.join(","),
      ...data.map((row) => headers.map((h) => `"${row[h]}"`).join(",")),
    ];
    const csvString = csvRows.join("\n");
    const blob = new Blob([csvString], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", "parcels.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }
}

const filters = reactive({
  owner: "",
  parcel_name: "",
});

const fields = ref<any[]>([]);
const totalCount = ref(0);
const rowsPerPage = ref(10); // Augmenté pour correspondre à la PAGE_SIZE par défaut
const currentPage = ref(1);
const activeMenu = ref<string | null>(null);
const menuPosition = reactive({ top: 0, right: 0 });

const fieldsState = useState("fieldsData", () => ({
  data: [] as any[],
  timestamp: 0,
}));

async function loadData() {
  if (!authStore.isAuthenticated) return;

  try {
    const data: any = await apiFetch(`/api/parcels/?page=${currentPage.value}`);
    const parcels = data.results || data;
    totalCount.value = data.count || parcels.length;

    const ownerUUIDs = [...new Set(parcels.map((p: any) => p.owner))];
    const ownersMap: Record<string, string> = {};

    await Promise.all(
      ownerUUIDs.map(async (uuid: any) => {
        try {
          const ownerData: any = await apiFetch(`/api/users/${uuid}/`);
          ownersMap[uuid] = `${ownerData.first_name}`.trim() || "Unknown";
        } catch (err) {
          ownersMap[uuid] = "Unknown";
        }
      })
    );

    fields.value = parcels.map((parcel: any, idx: number) => ({
      id: idx + 1,
      fieldId: parcel.uuid,
      owner: ownersMap[parcel.owner] || "Unknown Owner",
      parcel_name: parcel.parcel_name,
      latitude: parcel.parcel_points?.[0]?.latitude ?? 0,
      longitude: parcel.parcel_points?.[0]?.longitude ?? 0,
    }));
  } catch (err) {
    console.error("Erreur réseau:", err);
  }
}

watch(currentPage, () => {
  loadData();
});

onMounted(() => {
  loadData();
});

const filteredFields = computed(() =>
  fields.value.filter(
    (f) =>
      f.owner.toLowerCase().includes(filters.owner.toLowerCase()) &&
      f.parcel_name.toLowerCase().includes(filters.parcel_name.toLowerCase())
  )
);

const totalPages = computed(() =>
  Math.ceil(totalCount.value / rowsPerPage.value)
);
const paginatedFields = computed(() => {
  return filteredFields.value; // Déjà paginé par le backend
});

const visiblePages = computed(() => {
  const pages: (number | string)[] = [];
  if (totalPages.value <= 15) {
    for (let i = 1; i <= totalPages.value; i++) pages.push(i);
  } else {
    if (currentPage.value <= 7) {
      pages.push(
        ...Array.from({ length: 8 }, (_, i) => i + 1),
        "...",
        totalPages.value
      );
    } else if (currentPage.value >= totalPages.value - 6) {
      pages.push(
        1,
        "...",
        ...Array.from({ length: 8 }, (_, i) => totalPages.value - 7 + i)
      );
    } else {
      pages.push(
        1,
        "...",
        currentPage.value - 2,
        currentPage.value - 1,
        currentPage.value,
        currentPage.value + 1,
        currentPage.value + 2,
        "...",
        totalPages.value
      );
    }
  }
  return pages;
});

function resetFilters() {
  filters.owner = "";
  filters.parcel_name = "";
  currentPage.value = 1;
}

function toggleMenu(id: string, event: MouseEvent) {
  if (activeMenu.value === id) {
    activeMenu.value = null;
  } else {
    activeMenu.value = id;
    const button = event.currentTarget as HTMLElement;
    const rect = button.getBoundingClientRect();
    menuPosition.top = rect.bottom + window.scrollY;
    menuPosition.right = rect.right + window.scrollX;
  }
}

const showDeleteModal = ref(false);
const parcelToDelete = ref<string | null>(null);

function confirmDelete(uuid: string) {
  parcelToDelete.value = uuid;
  showDeleteModal.value = true;
}

async function deleteParcelConfirmed() {
  if (!parcelToDelete.value) return;

  try {
    await apiFetch(`/api/parcels/${parcelToDelete.value}/`, {
      method: "DELETE"
    });
    fields.value = fields.value.filter(
      (f) => f.fieldId !== parcelToDelete.value
    );
    showDeleteModal.value = false;
    parcelToDelete.value = null;
  } catch (err) {
    console.error(err);
    alert("Failed to delete parcel");
  }
}

function cancelDelete() {
  showDeleteModal.value = false;
  parcelToDelete.value = null;
}

function prevPage() {
  if (currentPage.value > 1) currentPage.value--;
}
function nextPage() {
  if (currentPage.value < totalPages.value) currentPage.value++;
}
function goToPage(page: number | string) {
  if (page !== "...") currentPage.value = page as number;
}
</script>
