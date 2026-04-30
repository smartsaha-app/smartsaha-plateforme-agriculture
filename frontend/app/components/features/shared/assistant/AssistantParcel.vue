<template>
  <div class="relative flex flex-col h-full bg-gray-50 overflow-hidden">
    <!-- Header with Back Button (Specific to Parcel view) -->
    <div class="absolute top-4 right-4 z-50">
      <button
        @click="$router.back()"
        class="flex items-center justify-center w-10 h-10 bg-white/80 backdrop-blur-md rounded-full shadow-lg hover:bg-white transition-all duration-300 border border-gray-100"
      >
        <i class="bx bx-x text-2xl text-gray-800"></i>
      </button>
    </div>

    <!-- Chat Messages Container -->
    <div
      ref="chatContainer"
      class="flex-1 overflow-y-auto p-4 sm:px-12 md:px-24 space-y-4 pt-16 pb-64 scroll-behavior-smooth"
    >
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="flex"
        :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
          :class="[
            'px-5 py-3 rounded-2xl max-w-2xl break-words shadow-sm',
            msg.sender === 'user'
              ? 'bg-[#10b481] text-white rounded-br-none'
              : 'bg-white text-gray-800 rounded-bl-none border border-gray-100',
          ]"
        >
          <span v-html="formatMessage(msg.text)"></span>
        </div>
      </div>

      <!-- Typing Indicator -->
      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-white px-5 py-3 rounded-2xl shadow-sm border border-gray-100 flex items-center gap-2">
          <div class="flex gap-1">
            <span class="w-1.5 h-1.5 bg-[#10b481] rounded-full animate-bounce [animation-delay:-0.3s]"></span>
            <span class="w-1.5 h-1.5 bg-[#10b481] rounded-full animate-bounce [animation-delay:-0.15s]"></span>
            <span class="w-1.5 h-1.5 bg-[#10b481] rounded-full animate-bounce"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Welcome Message -->
    <div
      v-if="showWelcome && messages.length === 0"
      class="absolute inset-0 flex flex-col items-center justify-center text-center p-8 pointer-events-none"
    >
      <h1 class="text-4xl md:text-5xl font-black text-[#112830] leading-tight animate-fade-in max-w-3xl">
        Je suis <span class="text-[#10b481]">Sesily</span>, votre assistant agronome. <br />
        <span class="text-gray-400 text-3xl font-bold">Posez-moi vos questions sur cette parcelle !</span>
      </h1>
    </div>

    <!-- Context/Modules Selector -->
    <div class="absolute left-0 right-0 bottom-24 p-4 bg-white/80 backdrop-blur-lg border-t border-gray-100 shadow-[0_-10px_20px_-5px_rgba(0,0,0,0.05)] flex flex-wrap justify-center gap-2 z-10 transition-all">
      <label
        v-for="module in modulesList"
        :key="module"
        class="flex items-center gap-2 px-3 py-1.5 rounded-full cursor-pointer transition-all border"
        :class="selectedModules.includes(module) ? 'bg-[#10b481] border-[#10b481] text-white' : 'bg-white border-gray-200 text-gray-600 hover:border-[#10b481]'"
      >
        <input
          type="checkbox"
          v-model="selectedModules"
          :value="module"
          class="hidden"
        />
        <i v-if="selectedModules.includes(module)" class="bx bx-check-circle text-sm"></i>
        <span class="text-xs font-bold uppercase tracking-wider">{{ module }}</span>
      </label>
    </div>

    <!-- Input Bar -->
    <div class="absolute left-0 right-0 bottom-0 p-4 bg-white border-t border-gray-100 shadow-2xl flex items-center justify-center z-20">
      <div class="max-w-4xl w-full flex items-center bg-gray-50 rounded-2xl border border-gray-200 p-1 focus-within:border-[#10b481] focus-within:ring-4 focus-within:ring-[#10b481]/5 transition-all">
        <input
          v-model="inputMessage"
          @keyup.enter="sendMessage"
          type="text"
          placeholder="Écris un message pour Sesily..."
          class="flex-1 p-3 bg-transparent text-gray-800 placeholder-gray-400 outline-none font-medium"
        />
        <button
          @click="sendMessage"
          :disabled="!inputMessage.trim() || isLoading"
          class="bg-[#112830] text-white p-3 rounded-xl hover:bg-black transition-all flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed group"
        >
          <i class="bx bx-up-arrow-alt text-2xl group-hover:scale-110 transition-transform"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from "vue";
import { useApi } from "~/composables/useApi";

const props = defineProps<{
  parcelId: string | string[];
}>();

const { apiFetch } = useApi();

const messages = ref<{ sender: string; text: string }[]>([]);
const inputMessage = ref("");
const chatContainer = ref<HTMLElement | null>(null);
const isLoading = ref(false);
const showWelcome = ref(true);

const modulesList = [
  "Parcelle",
  "Sol",
  "Tâches",
  "Culture",
  "Météo",
  "Rendement",
];
const selectedModules = ref<string[]>(["Parcelle", "Culture", "Météo"]);

function formatMessage(text: string) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/^- (.*)$/gm, "• $1")
    .replace(/\n/g, "<br>");
}

function buildModulesPayload() {
  const payload: Record<string, boolean> = {};
  modulesList.forEach((module) => {
    payload[module] = selectedModules.value.includes(module);
  });
  return payload;
}

async function sendMessage() {
  if (!inputMessage.value.trim() || isLoading.value) return;

  if (showWelcome.value) {
    messages.value.push({
      sender: "ai",
      text: "Bonjour ! Je suis **Sesily**, votre assistant agronome. Je suis prêt à analyser les données de cette parcelle avec vous.",
    });
    showWelcome.value = false;
  }

  const userMessage = inputMessage.value;
  messages.value.push({ sender: "user", text: userMessage });
  inputMessage.value = "";

  await nextTick();
  chatContainer.value?.scrollTo({
    top: chatContainer.value.scrollHeight,
    behavior: "smooth",
  });

  try {
    isLoading.value = true;
    const res: any = await apiFetch('/api/v2/smart-assistant/', {
      method: "POST",
      body: {
        question: userMessage,
        session_id: null, // On reste en continu sur cette vue spécialisée
        parcel_id: props.parcelId,
        crop_name: null,
        user_modules: buildModulesPayload(),
      },
    });

    messages.value.push({ sender: "ai", text: res.answer || "Désolé, je n'ai pas pu obtenir de réponse." });
  } catch (err: any) {
    console.error("Erreur API :", err);
    messages.value.push({
      sender: "ai",
      text: "⚠️ Une erreur est survenue lors de la communication avec Sesily.",
    });
  } finally {
    isLoading.value = false;
    await nextTick();
    chatContainer.value?.scrollTo({
      top: chatContainer.value.scrollHeight,
      behavior: "smooth",
    });
  }
}
</script>

<style scoped>
.scroll-behavior-smooth {
  scroll-behavior: smooth;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}
</style>
