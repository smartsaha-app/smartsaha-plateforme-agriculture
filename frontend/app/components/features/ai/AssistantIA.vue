<template>
    <div class="flex flex-col h-full">
      <!-- Messages scrollables -->
      <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 space-y-3">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="flex"
          :class="msg.sender === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            :class="[
              'px-4 py-3 rounded-2xl max-w-[80%] break-words shadow-md',
              msg.sender === 'user'
                ? 'bg-[#10b481] text-white rounded-br-none'
                : 'bg-white text-gray-800 rounded-bl-none'
            ]"
          >
            <span v-html="formatMessage(msg.text)"></span>
          </div>
        </div>
  
        <!-- Loading / typing dots -->
        <div v-if="isLoading" class="flex justify-start">
          <div class="bg-white text-gray-800 px-4 py-2 rounded-2xl shadow flex items-center">
            <span class="typing-dots flex space-x-1">
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300"></span>
            </span>
          </div>
        </div>
      </div>
  
      <!-- Footer fixe -->
      <div class="flex-none p-3 bg-[#1E1E1E] border-t border-gray-700 flex gap-2 rounded-t-2xl">
        <input
          v-model="inputMessage"
          @keyup.enter="sendMessage"
          type="text"
          placeholder="Posez votre question"
          :disabled="demoRunning"
          class="flex-1 p-3 rounded-l-full bg-gray-800 text-white text-sm sm:text-base focus:outline-none disabled:opacity-50"
        />
        <button
          @click="sendMessage"
          :disabled="demoRunning"
          class="bg-[#10b481] text-white p-3 rounded-r-full hover:bg-green-600 transition flex items-center justify-center disabled:opacity-50"
        >
          <i class="bx bx-up-arrow-alt text-xl sm:text-2xl"></i>
        </button>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, nextTick, onMounted } from "vue";
  import { useAuthStore } from "~/stores/auth";
  import { useApi } from "~/composables/useApi";
  const authStore = useAuthStore();
  const { apiFetch } = useApi();
  const { t: nuxtT } = useI18n();
  const t = (key: string) => nuxtT(`dashboard.${key}`);
  
  const messages = ref<{ sender: string; text: string }[]>([]);
  const inputMessage = ref("");
  const chatContainer = ref<HTMLElement | null>(null);
  const isLoading = ref(false);
  const demoRunning = ref(true); // bloque le champ pendant la démo
  
  function formatMessage(text: string) {
    return text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/^- (.*)$/gm, "• $1")
      .replace(/\n/g, "<br>");
  }
  
  function scrollToBottom() {
    if (chatContainer.value) {
      chatContainer.value.scrollTo({
        top: chatContainer.value.scrollHeight,
        behavior: "smooth",
      });
    }
  }
  
  // Démo automatique
  async function demoMessage(userText: string, aiText: string, delay = 1500) {
    messages.value.push({ sender: "user", text: userText });
    await nextTick();
    scrollToBottom();
  
    isLoading.value = true;
    await new Promise((r) => setTimeout(r, delay));
    isLoading.value = false;
  
    messages.value.push({ sender: "ai", text: aiText });
    await nextTick();
    scrollToBottom();
  }
  
  onMounted(async () => {
    // Démo initiale
    await demoMessage(
      "Bonjour, peux-tu m'aider avec mes cultures ?",
      "Bien sûr ! Je peux vous conseiller sur la plantation, l'irrigation et la fertilisation."
    );
    await demoMessage(
      "Quels engrais recommandes-tu pour le maïs ?",
      "Pour le maïs, un engrais riche en azote et en phosphore est recommandé."
    );
    await demoMessage(
      "Merci ! Et pour les maladies ?",
      "Surveillez les signes de rouille ou de mildiou et appliquez des traitements biologiques si nécessaire."
    );
  
    demoRunning.value = false; // débloque le champ pour l'utilisateur
  });
  
  async function sendMessage() {
    if (!inputMessage.value.trim() || demoRunning.value) return;
  
    messages.value.push({ sender: "user", text: inputMessage.value });
    const userMessage = inputMessage.value;
    inputMessage.value = "";
  
    await nextTick();
    scrollToBottom();
  
    try {
      isLoading.value = true;
      const data: any = await apiFetch("/api/v2/smart-assistant/", {
        method: "POST",
        body: {
          question: userMessage,
          session_id: null,
          parcel_id: null,
          crop_name: null,
          user_modules: {},
        },
      });
  
      isLoading.value = false;
      messages.value.push({ sender: "ai", text: data.answer || "Désolé, je n'ai pas pu générer de réponse." });
      await nextTick();
      scrollToBottom();
    } catch (err: any) {
      console.error(err);
      isLoading.value = false;
      messages.value.push({ sender: "ai", text: "Erreur de communication avec Sesily AI." });
      await nextTick();
      scrollToBottom();
    }
  }
  </script>
  
  <style scoped>
  .typing-dots span {
    display: inline-block;
    animation: bounce 0.6s infinite alternate;
  }
  .typing-dots span.delay-150 { animation-delay: 0.15s; }
  .typing-dots span.delay-300 { animation-delay: 0.3s; }
  
  @keyframes bounce {
    from { transform: translateY(0); opacity: 0.3; }
    to { transform: translateY(-6px); opacity: 1; }
  }

  ::-webkit-scrollbar {
  width: 3px;
}
::-webkit-scrollbar-thumb {
  background-color: transparent;
  border-radius: 10px;
}
  </style>
  