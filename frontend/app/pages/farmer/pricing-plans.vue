<template>
  <section class="bg-gray-50 py-20">
    <div class="max-w-7xl mx-auto px-6 text-center">
      <h2 class="text-3xl font-bold text-gray-900 mb-4">
        {{ t('pricing.title') }}
      </h2>
      <p class="text-gray-600 mb-12">
        {{ t('pricing.subtitle') }}
      </p>

      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        <div
          v-for="(plan, index) in localizedPlans"
          :key="index"
          :class="[
            'rounded-2xl shadow p-8 hover:shadow-lg transition flex flex-col justify-between border',
            plan.highlight
              ? 'bg-[#f1fcf8] border-[#10b481]'
              : 'bg-white border-gray-100',
          ]"
        >
          <div>
            <div class="text-3xl text-[#10b481] mb-4">
              <i :class="plan.icon"></i>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-4">
              {{ plan.title }}
            </h3>
            <p class="text-gray-500 mb-6">{{ plan.description }}</p>

            <p class="text-3xl font-bold mb-4 text-gray-800">
              {{ plan.price }}
              <span v-if="plan.limit" class="text-sm text-gray-500"
                >({{ plan.limit }})</span
              >
            </p>

            <ul class="text-left text-gray-700 space-y-2 mb-8">
              <li v-for="(feature, i) in plan.features" :key="i">
                <i class="bx bx-check text-[#10b481] mr-2"></i> {{ feature }}
              </li>
            </ul>
          </div>

          <button
            class="bg-[#10b481] text-white px-6 py-2 rounded-xl hover:bg-[#0b7a58] mt-auto"
          >
            {{ plan.button }}
          </button>
        </div>
      </div>

      <p class="text-gray-500 mt-12">
        {{ t('pricing.dataNotice') }}
      </p>
    </div>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "dashboard",
});

const { t } = useI18n();

const localizedPlans = computed(() => [
  {
    title: t('pricing.free.title'),
    icon: "bx bx-leaf",
    description: t('pricing.free.desc'),
    price: t('pricing.free.price'),
    limit: t('pricing.free.limit'),
    button: t('pricing.free.btn'),
    highlight: false,
    features: [
      t('pricing.features.soil'),
      t('pricing.features.moisture'),
      t('pricing.features.weather7'),
      t('pricing.features.agronomist'),
      t('pricing.features.forecast'),
      t('pricing.features.yieldHistory'),
      t('pricing.features.taskMgmt'),
      t('pricing.features.map'),
      t('pricing.features.fireLimited'),
    ],
  },
  {
    title: t('pricing.standard.title'),
    icon: "bx bx-seedling",
    description: t('pricing.standard.desc'),
    price: t('pricing.standard.price'),
    button: t('pricing.standard.btn'),
    highlight: false,
    features: [
      t('pricing.features.allFree'),
      t('pricing.features.unlimitedParcels'),
      t('pricing.features.remoteSensing'),
      t('pricing.features.fireFull'),
      t('pricing.features.agronomistAdv'),
      t('pricing.features.taskMgmtFull'),
      t('pricing.features.weatherDetailed'),
      t('pricing.features.dataMgmt'),
    ],
  },
  {
    title: t('pricing.advanced.title'),
    icon: "bx bx-briefcase-alt-2",
    description: t('pricing.advanced.desc'),
    price: t('pricing.advanced.price'),
    button: t('pricing.advanced.btn'),
    highlight: true,
    features: [
      t('pricing.features.allStandard'),
      t('pricing.features.multiUser'),
      t('pricing.features.biDashboard'),
      t('pricing.features.advMapping'),
      t('pricing.features.iaDecision'),
      t('pricing.features.customReports'),
      t('pricing.features.fireLargeScale'),
      t('pricing.features.carbon'),
    ],
  },
  {
    title: t('pricing.premium.title'),
    icon: "bx bx-diamond",
    description: t('pricing.premium.desc'),
    price: t('pricing.premium.price'),
    button: t('pricing.premium.btn'),
    highlight: false,
    features: [
      t('pricing.features.allAdvanced'),
      t('pricing.features.certifications'),
      t('pricing.features.multiParcelReports'),
      t('pricing.features.dynamicDashboards'),
      t('pricing.features.iaStrategic'),
      t('pricing.features.apiAccess'),
      t('pricing.features.support'),
    ],
  },
]);
</script>
