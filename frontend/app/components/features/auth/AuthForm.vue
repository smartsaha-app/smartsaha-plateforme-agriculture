<template>
  <div class="relative w-full max-w-md mx-auto my-4">
    <div class="w-full relative z-0">
      <h2 class="text-2xl font-black mb-2 text-center text-[#112830]">
        {{ title }}
      </h2>

      <slot name="under-title"></slot>

      <form @submit.prevent="submit" class="space-y-3">
        <!-- Name Grid -->
        <div v-if="fields.includes('first_name') && fields.includes('last_name')" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div v-for="field in ['first_name', 'last_name']" :key="field" class="relative">
            <i :class="icons[field] + ' text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2 text-lg'"></i>
            <input
              v-model="formData[field]"
              type="text"
              placeholder=" "
              class="peer w-full p-3 pl-10 pr-4 rounded border border-gray-400 bg-transparent text-gray-600 placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-[#10b481] text-sm"
            />
            <label
              :for="field"
              class="absolute left-10 text-gray-400 text-sm pointer-events-none transition-all duration-200"
              :class="[
                formData[field] || fieldHasFocus[field]
                  ? '-top-3 text-xs text-[#10b481] bg-[#f9f9f9] px-2 rounded font-bold'
                  : 'top-3 text-sm text-[#10b481]',
              ]"
            >
              {{ labels[field] }}
            </label>
          </div>
        </div>

        <!-- Other Fields -->
        <div v-for="field in fields.filter(f => !['first_name', 'last_name'].includes(f))" :key="field" class="w-full">
          <div class="relative">
            <i
              :class="
                icons[field] +
                ' text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2 text-lg'
              "
            ></i>

            <input
              v-model="formData[field]"
              :type="getInputType(field)"
              placeholder=" "
              class="peer w-full p-3 pl-10 pr-10 rounded border border-gray-400 bg-transparent text-gray-600 placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-[#10b481] text-sm"
            />

            <label
              :for="field"
              class="absolute left-10 text-gray-400 text-sm pointer-events-none transition-all duration-200"
              :class="[
                formData[field] || fieldHasFocus[field]
                  ? '-top-3 text-xs text-[#10b481] bg-[#f9f9f9] px-2 rounded font-bold'
                  : 'top-3 text-sm text-[#10b481]',
              ]"
            >
              {{ labels[field] || passwordLabel }}
            </label>

            <i
              v-if="field === 'password'"
              :class="[
                showPassword ? 'bx bx-hide' : 'bx bx-show',
                'absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-lg cursor-pointer hover:text-[#10b481] transition',
              ]"
              @click="togglePassword"
            ></i>
          </div>

          <!-- Forgot Password Link -->
          <div v-if="field === 'password' && showForgotPassword" class="flex justify-end mt-2">
            <NuxtLink to="/reset-password" class="text-[12px] text-[#10b481] hover:underline font-bold">
              Mot de passe oublié ?
            </NuxtLink>
          </div>
        </div>

        <div
          v-if="
            buttonText.toLowerCase().includes('sign') ||
            buttonText === 'S\'inscrire'
          "
          class="mt-2 text-sm text-gray-700"
        >
          <label class="flex items-center space-x-2">
            <input
              type="checkbox"
              v-model="acceptedPolicy"
              class="h-4 w-4 accent-[#10b481]"
              required
            />
            <span>
              I agree to the
              <NuxtLink
                to="/privacy-policy"
                class="underline hover:text-[#10b481]"
              >
                Privacy Policy
              </NuxtLink>
              and
              <NuxtLink
                to="/terms-of-service"
                class="underline hover:text-[#10b481]"
              >
                Terms of Service
              </NuxtLink>
            </span>
          </label>
        </div>

        <button
          type="submit"
          :disabled="
            (buttonText.toLowerCase().includes('sign') ||
              buttonText === 'S\'inscrire') &&
            !acceptedPolicy
          "
          class="w-full py-3 bg-gradient-to-r from-[#10b481] uppercase text-md to-[#0a8f6e] text-white rounded hover:bg-[#0da06a] transition-all duration-300 shadow-md disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {{ buttonText }}
        </button>
      </form>

      <div class="mt-6 text-center text-gray-500 space-x-4">
        <slot name="footer-links"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";

const props = defineProps<{
  title: string;
  buttonText: string;
  fields: string[];
  passwordLabel?: string;
  showForgotPassword?: boolean;
}>();

const emit = defineEmits<{
  (e: "submit", formData: Record<string, string>): void;
}>();

const acceptedPolicy = ref(false);
const formData = reactive<Record<string, string>>({});
props.fields.forEach((f) => (formData[f] = ""));

const fieldHasFocus = reactive<Record<string, boolean>>({});
props.fields.forEach((f) => (fieldHasFocus[f] = false));

const icons: Record<string, string> = {
  username: "bx bx-user",
  first_name: "bx bx-id-card",
  last_name: "bx bx-id-card",
  email: "bx bx-envelope",
  password: "bx bx-lock-alt",
};

const labels: Record<string, string> = {
  username: "Username",
  first_name: "First name",
  last_name: "Last name",
  email: "Email",
};

const showPassword = ref(false);
function togglePassword() {
  showPassword.value = !showPassword.value;
}
function getInputType(field: string) {
  return field === "password"
    ? showPassword.value
      ? "text"
      : "password"
    : "text";
}

function submit() {
  emit("submit", { ...formData });
}
</script>
