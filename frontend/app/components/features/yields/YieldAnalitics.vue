<template>
<div class="mt-12 mb-20">
  <h2 class="text-xl sm:text-2xl font-bold text-gray-800 mb-6">
    {{ t("titleanalytics") }}
  </h2>


  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4 mb-6">
  <label for="parcelFilter" class="font-medium text-gray-700 sr-only">
    {{ t('selectParcel') }}
  </label>
  <select
    id="parcelFilter"
    v-model="selectedParcel"
    class="rounded px-3 py-2 text-gray-700 w-full sm:w-auto"
  >
    <option value="">{{ t("allParcel") }}</option>
    <option v-for="(p, idx) in analyticsData" :key="idx" :value="p.parcel_name">
      {{ p.parcel_name }}
    </option>
  </select>

  <button
    @click="downloadChart"
    class="mt-2 sm:mt-0 ml-auto px-4 py-2 bg-[#10b481] text-white rounded hover:bg-[#0f9e72] transition"
  >
    {{ t("exportChart") }}
  </button>
</div>


    <div class="flex flex-col md:flex-row gap-6">
      <div class="flex-1 h-64 md:h-64 bg-white">
        <canvas ref="yieldCanvas"></canvas>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
        <div class="relative gap-4 p-3 bg-gray-100 rounded shadow-sm transition border border-gray-100 text-center">
          <h3 class="text-gray-500 tracking-wide text-sm">
            {{ t("totalyield") }}
          </h3>
          <p class="text-lg font-bold text-gray-800">{{ totalYield.toFixed(2) }}</p>
        </div>
        <div class="relative gap-4 p-3 bg-gray-100 rounded shadow-sm transition border border-gray-100 text-center">
          <h3 class="text-gray-500 tracking-wide text-sm">
            {{ t("averageyield") }} (kg)
          </h3>
          <p class="text-lg font-bold text-gray-800">
            {{ averageYield.toFixed(2) }}
          </p>
        </div>
        <div class="relative gap-4 p-3 bg-gray-100 rounded shadow-sm transition border border-gray-100 text-center">
          <h3 class="text-gray-500 tracking-wide text-sm">
            {{ t("cumulativeYield") }} (kg)
          </h3>
          <p class="text-lg font-bold text-gray-800">
            {{ cumulativeYield.toFixed(2) }} 
          </p>
        </div>
        <div class="relative gap-4 p-3 bg-gray-100 rounded shadow-sm transition border border-gray-100 text-center">
          <h3 class="text-gray-500 tracking-wide text-sm">
            {{ t("volatility") }} 
          </h3>
          <p class="text-lg font-bold text-gray-800">
            {{ volatility.toFixed(2) }} 
          </p>
        </div>
        <div class="relative gap-4 p-3 bg-gray-100 rounded shadow-sm transition border border-gray-100 text-center">
          <h3 class="text-gray-500 tracking-wide text-sm">
            {{ t("yieldRelative") }}
          </h3>
          <p class="text-lg font-bold text-gray-800">
            {{ relativeYield }}  %
          </p>
        </div>
        <div
          class="p-3 border border-[#f4a261]/80 bg-[#f4a261]/10 rounded text-center"
        >
          <h3 class="text-gray-500 tracking-wide text-sm text-[#f4a261]/80">
            {{ t("anomalies") }}
          </h3>
          <p class="text-lg font-bold text-[#f4a261]">{{ anomalies.length }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick, computed } from "vue";
import Chart from "chart.js/auto";
import { useAuthStore } from "~/stores/auth";
const { t: nuxtT, locale } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);
const authStore = useAuthStore();
const { apiFetch } = useApi();

const yieldChart = ref<Chart | null>(null);
const yieldCanvas = ref<HTMLCanvasElement | null>(null);
  const analyticsData = useState<any[]>("analyticsData", () => []);
const selectedParcel = ref<string>("");

async function fetchAnalytics() {
  if (!authStore.isAuthenticated) return;

  if (!Array.isArray(analyticsData.value)) analyticsData.value = [];

  if (analyticsData.value.length > 0) {
    console.log("Using cached analytics data");
    await nextTick();
    createChart();
    return;
  }

  try {
    const resData: any = await apiFetch("/analytics/yields/");

    analyticsData.value = Array.isArray(resData)
      ? resData
      : Object.values(resData);
    await nextTick();
    createChart();
  } catch (err) {
    console.error(err);
  }
}

function createChart() {
  if (!analyticsData.value.length || !yieldCanvas.value) return;

  const dataToUse = selectedParcel.value
    ? analyticsData.value.filter((p) => p.parcel_name === selectedParcel.value)
    : analyticsData.value;

  if (!dataToUse.length) {
    if (yieldChart.value) yieldChart.value.destroy();
    yieldChart.value = null;
    return;
  }

  const allDatesSet = new Set<string>();
  dataToUse.forEach((p) =>
    p.dates.forEach((d) => allDatesSet.add(d.split("T")[0]))
  );
  const labels = Array.from(allDatesSet)
  .sort()
  .map((d) => {
    const date = new Date(d);
    return date.toLocaleDateString(
      locale.value === "fr" ? "fr-FR" : locale.value === "mg" ? "mg-MG" : "en-US",
      {
        year: "numeric",
        month: "short",
      }
    );
  });


  const colors = [
    "#112830",
    "#f4a261",
    "#10b481",
    "#6d4c41",
    "#222831",
    "#f4a261",
    "#219ebc",
  ];
  const datasets = dataToUse.map((p, idx) => {
    const ctx = yieldCanvas.value!.getContext("2d")!;
    const gradient = ctx.createLinearGradient(
      0,
      0,
      0,
      yieldCanvas.value!.height
    );
    gradient.addColorStop(0, colors[idx % colors.length] + "33");
    gradient.addColorStop(1, colors[idx % colors.length] + "05");

    return {
  label: p.parcel_name,
  data: labels.map((label) => {
  const originalDate = p.dates.find((dateStr) => {
    const d = new Date(dateStr);
    const formatted = d.toLocaleDateString(
      locale.value === "fr" ? "fr-FR" : locale.value === "mg" ? "mg-MG" : "en-US",
      { year: "numeric", month: "short" }
    );
    return formatted === label;
  });

  if (!originalDate) return null;

  const index = p.dates.findIndex((dateStr) => dateStr === originalDate);
  return p.yield_amount[index];
}),

backgroundColor: colors[idx % colors.length],
    borderColor: colors[idx % colors.length],

    borderRadius: 3,
    borderSkipped: false,
};

  });

  if (yieldChart.value) yieldChart.value.destroy();

  yieldChart.value = new Chart(yieldCanvas.value, {
  type: "bar",
  data: { labels, datasets },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    layout: { padding: { left: 10, right: 10, top: 5, bottom: 5 } },

    plugins: {
      legend: {
        display: false,
        position: "top",
        labels: {
          usePointStyle: true,
          pointStyle: "rectRounded",
          color: "#374151",
          font: { size: 11 },
        },
      },
      tooltip: {
        backgroundColor: "#1f2937",
        titleFont: { size: 12, weight: "bold" },
        bodyFont: { size: 11 },
        padding: 8,
        cornerRadius: 3,
        displayColors: false,
      },
    },

    scales: {
      x: {
        ticks: { color: "#6b7280", font: { size: 11 } },
        grid: { display: false },
        border: { display: false },
      },
      y: {
        beginAtZero: true,
        ticks: { color: "#6b7280", font: { size: 11 } },
        grid: {
          color: "#f2f2f2",
          borderDash: [4, 4],
        },
        border: { display: false },
      },
    },
  },
});

}

function downloadChart() {
  if (!yieldChart.value) return;
  const link = document.createElement("a");
  link.href = yieldChart.value.toBase64Image();
  link.download = "parcel_yields_chart.png";
  link.click();
}

watch(selectedParcel, () => createChart());
onMounted(() => fetchAnalytics());

// Assurer que filteredData est un tableau
const filteredData = computed(() =>
  Array.isArray(analyticsData.value)
    ? selectedParcel.value
      ? analyticsData.value.filter((p) => p.parcel_name === selectedParcel.value)
      : analyticsData.value
    : []
);

// Assurer que yield_amount est un tableau
const allYields = computed(() =>
  filteredData.value.flatMap((p) => Array.isArray(p.yield_amount) ? p.yield_amount : [])
);

const totalYield = computed(() =>
  allYields.value.reduce((acc, v) => acc + v, 0)
);

const averageYield = computed(() =>
  allYields.value.length ? totalYield.value / allYields.value.length : 0
);

const cumulativeYield = computed(() =>
  filteredData.value.reduce(
    (acc, p) => acc + (Array.isArray(p.yield_amount) ? p.yield_amount.reduce((a, b) => a + b, 0) : 0),
    0
  )
);

const volatility = computed(() => {
  const mean = averageYield.value;
  const n = allYields.value.length;
  if (!n) return 0;
  const variance =
    allYields.value.reduce((sum, y) => sum + (y - mean) ** 2, 0) / n;
  return Math.sqrt(variance);
});

const relativeYield = computed(() => {
  if (!filteredData.value.length) return 0;
  const maxTotal = Math.max(
    ...analyticsData.value.map((p) => Array.isArray(p.yield_amount) ? p.yield_amount.reduce((a, b) => a + b, 0) : 0)
  );
  const thisTotal = Array.isArray(filteredData.value[0].yield_amount)
    ? filteredData.value[0].yield_amount.reduce((a, b) => a + b, 0)
    : 0;
  return maxTotal ? (thisTotal / maxTotal) * 100 : 0;
});

const anomalies = computed(() => {
  const mean = averageYield.value;
  const std = volatility.value;
  return allYields.value.filter(
    (y) => y > mean + 2 * std || y < mean - 2 * std
  );
});

</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: #d0d0d0;
  border-radius: 10px;
}
</style>
