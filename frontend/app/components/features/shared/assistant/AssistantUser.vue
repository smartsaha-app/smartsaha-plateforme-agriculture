<template>
  <div class="relative flex flex-col p-10 h-full overflow-hidden">
    <div
      v-if="isMounted"
      ref="chatContainer"
      class="flex-1 overflow-y-auto px-3 sm:px-32 pt-4 pb-28 space-y-3 scroll-behavior-smooth"
    >
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="flex"
        :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
          :class="[
            'px-4 py-2 rounded-lg max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg shadow-sm',
            msg.sender === 'user'
              ? 'bg-[#10b481] text-white rounded-br-none'
              : 'bg-white text-gray-800 rounded-bl-none border border-gray-100',
          ]"
        >
          <span v-html="formatMessage(msg.text)"></span>
        </div>
      </div>

      <div v-if="isLoading" class="flex justify-start">
        <div
          class="bg-white text-gray-800 px-4 py-2 rounded-lg shadow-sm flex items-center border border-gray-100"
        >
          <span class="typing-dots flex space-x-1">
            <span
              class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
            ></span>
            <span
              class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"
            ></span>
            <span
              class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300"
            ></span>
          </span>
        </div>
      </div>
    </div>

    <div
      v-if="showWelcome && messages.length === 0"
      class="absolute inset-0 flex flex-col items-center justify-center text-center space-y-6 pointer-events-none px-4 sm:px-24"
    >
      <h1
        class="text-2xl sm:text-4xl md:text-5xl font-extrabold text-[#112830] animate-fade-in"
      >
        Bonjour ! Je suis Sesily AI, votre assistant agronome. Posez-moi vos
        questions !
      </h1>
      <div
        class="flex flex-wrap gap-2 sm:gap-3 justify-center pointer-events-auto"
      >
        <button
          v-for="(q, i) in suggestedQuestions"
          :key="i"
          @click="askSuggestedQuestion(q)"
          class="px-3 sm:px-4 py-2 text-sm sm:text-base bg-white border rounded-full shadow hover:bg-gray-50 transition"
        >
          {{ q }}
        </button>
      </div>
    </div>

    <div
      ref="footer"
      class="fixed bottom-10 left-1/2 p-2 -translate-x-1/2 max-w-[800px] w-full bg-[#112830] rounded-xl border border-gray-700 shadow-2xl flex items-center gap-2 z-20 mx-4"
    >
      <input
        v-model="inputMessage"
        @keyup.enter="sendMessage"
        type="text"
        placeholder="Posez votre question..."
        class="bg-transparent text-white flex-1 p-3 text-sm outline-none"
      />
      <button
        @click="sendMessage"
        class="bg-[#10b481] text-white rounded-lg p-2 px-4 hover:bg-[#0d946b] transition flex items-center justify-center"
      >
        <i class="bx bx-up-arrow-alt text-xl"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from "vue";
import { useApi } from "~/composables/useApi";

const { apiFetch } = useApi();
const messages = ref<{ sender: string; text: string }[]>([]);
const inputMessage = ref("");
const chatContainer = ref<HTMLElement | null>(null);
const footer = ref<HTMLElement | null>(null);
const isLoading = ref(false);
const showWelcome = ref(true);
const suggestedQuestions = ref([
  "Comment planter du maïs ?",
  "Comment reconnaître une maladie des plantes ?",
  "Quels sont les signes de carences en nutriments ?",
  "Comment améliorer la fertilité du sol ?",
  "Comment protéger mes plantes contre les insectes ?",
  "Quels sont les meilleurs engrais pour le manioc ?",
  "Comment faire une rotation des cultures ?",
  "Comment savoir si une plante a besoin d’eau ?",
]);

const isMounted = ref(false);

onMounted(() => {
  isMounted.value = true;
});

function formatMessage(text: string) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/^- (.*)$/gm, "• $1")
    .replace(/\n/g, "<br>");
}

async function sendMessage() {
  if (!inputMessage.value.trim()) return;

  if (showWelcome.value) {
    messages.value.push({
      sender: "ai",
      text: "Bonjour ! Je suis **Sesily AI**, votre assistant agricole. Comment puis-je vous aider ?",
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
      method: 'POST',
      body: { 
        question: userMessage,
        session_id: null,
        parcel_id: null,
        crop_name: null,
        user_modules: {}
      },
    });
    messages.value.push({
      sender: "ai",
      text: res.answer || "Pas de réponse disponible.",
    });
  } catch (err: any) {
    console.error("Erreur API:", err);
    messages.value.push({
      sender: "ai",
      text: "Erreur lors de la communication avec l’assistant.",
    });
  } finally {
    isLoading.value = false;
  }

  await nextTick();
  chatContainer.value?.scrollTo({
    top: chatContainer.value.scrollHeight,
    behavior: "smooth",
  });
}

function askSuggestedQuestion(question: string) {
  inputMessage.value = question;
  sendMessage();
}
</script>

<style scoped>
.typing-dots span {
  display: inline-block;
  animation: bounce 0.6s infinite alternate;
}
.typing-dots span.delay-150 {
  animation-delay: 0.15s;
}
.typing-dots span.delay-300 {
  animation-delay: 0.3s;
}
@keyframes bounce {
  from {
    transform: translateY(0);
    opacity: 0.3;
  }
  to {
    transform: translateY(-6px);
    opacity: 1;
  }
}
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fade-in 0.6s ease-out forwards;
}

.scroll-behavior-smooth {
  scroll-behavior: smooth;
}
</style>
