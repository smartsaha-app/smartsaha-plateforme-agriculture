<template>
  <div class="max-w-5xl mx-auto px-4 py-10">
    <div class="flex items-center justify-between mb-10">
      <h1
        class="text-2xl sm:text-3xl font-semibold text-gray-800 tracking-tight"
      >
        {{ t('stepTittle') }}
      </h1>
      <p class="text-sm text-gray-500">
        {{ t('step') }} {{ currentStep + 1 }} / {{ steps.length }}
      </p>
    </div>

    <div class="relative mb-12">
      <div class="absolute top-1/2 left-0 w-full h-[2px] bg-gray-200"></div>
      <div
        class="absolute top-1/2 left-0 h-[2px] bg-[#10b481] transition-all duration-500"
        :style="{ width: `${((currentStep + 1) / steps.length) * 100}%` }"
      ></div>
      <div class="flex justify-between">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="flex flex-col items-center text-center group"
        >
          <div
            :class="[
              'w-3 h-3 rounded-full transition-all duration-300',
              currentStep === index
                ? 'bg-[#10b481] scale-125'
                : completedSteps.includes(index)
                ? 'bg-[#10b481]'
                : 'bg-gray-300',
            ]"
          ></div>
          <span
            class="mt-2 text-xs text-gray-500 group-hover:text-[#10b481] transition-colors duration-200"
          >
            {{ step }}
          </span>
        </div>
      </div>
    </div>

    <div
      class="transition-all duration-500"
    >
      <transition name="fade" mode="out-in">
        <div :key="currentStep">
          <ParcelForm v-if="currentStep === 0" @next="handleNextStep" />
          <CropForm
            v-else-if="currentStep === 1"
            @next="handleNextStep"
            @skip="skipStep"
          />
          <ParcelCropForm
            v-else-if="currentStep === 2"
            @next="handleNextStep"
          />
          <YieldForm
            v-else-if="currentStep === 3"
            @next="handleNextStep"
            @skip="skipStep"
          />
          <TaskForm
            v-else-if="currentStep === 4"
            @next="handleNextStep"
            @skip="skipStep"
          />
        </div>
      </transition>
    </div>

    <div class="mt-10 flex gap-4 justify-start items-center">
      
      <button
        v-if="currentStep < steps.length - 1"
        @click="skipStep"
        class="text-sm text-gray-500 hover:text-[#10b481] transition font-medium"
      >
        {{ t('skip') }}
      </button>

      <button
        @click="prevStep"
        :disabled="currentStep === 0"
        class="text-sm px-5 py-2 rounded bg-gray-100 text-gray-700 hover:bg-gray-200 disabled:opacity-0 font-medium transition shadow-sm"
      >
        {{ t('back') }}
      </button>

    </div>

    <transition name="fade">
      <div
        v-if="notification.visible"
        :class="[
          'fixed top-5 left-1/2 -translate-x-1/2 px-6 py-3 rounded-lg shadow-md text-white font-medium z-50',
          notification.type === 'success' ? 'bg-[#10b481]' : 'bg-red-500',
        ]"
      >
        {{ notification.message }}
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dashboard" });

import { ref } from "vue";
import ParcelForm from "~/components/forms/ParcelForm.vue";
import CropForm from "~/components/forms/CropForm.vue";
import ParcelCropForm from "~/components/forms/ParcelCropForm.vue";
import YieldForm from "~/components/forms/YieldForm.vue";
import TaskForm from "~/components/forms/TaskForm.vue";
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const steps = [t('parcels'), t('crops'), t('parcelcrop'), t('yields'), t('tasks')];

const currentStep = ref(0);
const completedSteps = ref([]);
const notification = ref({ visible: false, message: "", type: "success" });

const showNotification = (message, type = "success", duration = 2500) => {
  notification.value = { visible: true, message, type };
  setTimeout(() => (notification.value.visible = false), duration);
};

const handleNextStep = () => {
  if (!completedSteps.value.includes(currentStep.value))
    completedSteps.value.push(currentStep.value);

  if (currentStep.value < steps.length - 1) currentStep.value++;
  else showNotification("Setup completed successfully!");
};

const skipStep = () => {
  if (currentStep.value < steps.length - 1) currentStep.value++;
};

const prevStep = () => {
  if (currentStep.value > 0) currentStep.value--;
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(5px);
}
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
