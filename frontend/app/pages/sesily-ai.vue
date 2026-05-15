<template>
  <div class="h-screen bg-white text-gray-900 font-sans selection:bg-[#10b481]/30 flex flex-col overflow-hidden">
    
    <!-- Notification Toast -->
    <transition name="slide-down">
      <div v-if="showToast" class="fixed top-20 left-1/2 -translate-x-1/2 z-[100] w-[90%] max-w-md">
        <div class="bg-red-600 text-white px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-4 border border-red-400/30">
          <div class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center flex-shrink-0">
            <i class="bx bx-time-five text-2xl"></i>
          </div>
          <div class="flex-1">
            <p class="font-bold text-sm">Action limitée</p>
            <p class="text-xs opacity-90">Désolé ! 1 question par heure. Reviens dans <span class="font-bold underline">{{ timeLeft }}</span>.</p>
          </div>
          <button @click="showToast = false" class="text-white/60 hover:text-white transition-colors">
            <i class="bx bx-x text-2xl"></i>
          </button>
        </div>
      </div>
    </transition>

    <!-- Header (Fixed) -->
    <header class="flex-shrink-0 z-30 flex items-center justify-between p-4 md:px-8 border-b border-gray-100 bg-white/80 backdrop-blur-md">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-lg bg-[#10b481] flex items-center justify-center shadow-sm">
           <i class="bx bx-bot text-xl text-white"></i>
        </div>
        <span class="text-lg font-bold tracking-tight text-gray-900">Sesily AI</span>
      </div>

      <div class="flex items-center gap-3">
        <NuxtLink :to="localePath('/login')" class="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
          Connexion
        </NuxtLink>
        <NuxtLink :to="localePath('/signup')" class="px-4 py-2 text-sm font-medium bg-[#10b481] text-white rounded-full hover:bg-[#0d9469] transition-all shadow-sm">
          S'inscrire
        </NuxtLink>
      </div>
    </header>

    <!-- Main Content (Only Discussion is Scrollable) -->
    <main class="flex-1 relative flex flex-col overflow-hidden">
      
      <!-- Center Hero Section (Initially visible if no messages) -->
      <transition name="fade">
        <div v-if="messages.length === 0 && !isTyping" class="flex-1 flex flex-col items-center justify-center px-4 -mt-16">
          <h1 class="text-3xl md:text-4xl font-bold mb-8 text-center tracking-tight text-gray-900 animate-in slide-up">
            Que puis-je faire pour vous ?
          </h1>
          
          <!-- Search Bar (ChatGPT Style) -->
          <div class="w-full max-w-2xl group relative animate-in slide-up [animation-delay:100ms]">
            <div class="relative bg-gray-50 border border-gray-200 rounded-3xl p-2 flex flex-col shadow-sm transition-all duration-300 focus-within:border-[#10b481]/50 focus-within:bg-white focus-within:shadow-md">
              <textarea 
                v-model="userInput" 
                @keydown.enter.prevent="sendMessage"
                placeholder="Posez votre question sur l'agriculture..."
                class="w-full bg-transparent border-none focus:outline-none text-lg py-4 px-6 resize-none min-h-[60px] max-h-[200px] scrollbar-hide text-gray-900 placeholder:text-gray-400"
                rows="1"
              ></textarea>
              
              <div class="flex items-center justify-between px-4 pb-2 pt-1">
                <div class="flex items-center gap-2">
                  <button 
                    @click="newChat"
                    title="Nouvelle discussion"
                    class="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-100"
                  >
                    <i class="bx bx-plus text-xl"></i>
                  </button>
                  <button 
                    @click="isSearchMode = !isSearchMode"
                    :class="[
                      'flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold transition-all',
                      isSearchMode ? 'bg-[#10b481]/10 text-[#10b481] border border-[#10b481]/20' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    ]"
                  >
                    <i class="bx bx-globe text-sm"></i>
                    Recherche
                  </button>
                </div>
                
                <button 
                  @click="sendMessage"
                  :disabled="!userInput.trim() || isTyping"
                  class="w-10 h-10 bg-[#10b481] text-white rounded-full flex items-center justify-center disabled:bg-gray-200 disabled:text-gray-400 transition-all shadow-sm hover:scale-105 active:scale-95"
                >
                  <i class="bx bx-up-arrow-alt text-2xl font-bold"></i>
                </button>
              </div>
            </div>
          </div>

        </div>
      </transition>

      <!-- Scrollable Discussion -->
      <div v-if="messages.length > 0 || isTyping" class="flex-1 overflow-y-auto px-4 py-8 scroll-smooth" ref="chatContainer">
        <div class="max-w-2xl mx-auto space-y-10 pb-40">
          <div v-for="(msg, i) in messages" :key="i" class="animate-in fade-in slide-up duration-500">
            <!-- User Message -->
            <div v-if="msg.role === 'user'" class="flex justify-end">
              <div class="bg-gray-100 px-5 py-3 rounded-2xl max-w-[85%] text-gray-900 border border-gray-200">
                <p class="leading-relaxed">{{ msg.content }}</p>
              </div>
            </div>

            <!-- Assistant Message -->
            <div v-else class="flex gap-4">
              <div class="w-8 h-8 rounded-full bg-[#10b481]/10 flex-shrink-0 flex items-center justify-center border border-[#10b481]/20">
                 <i class="bx bx-bot text-lg text-[#10b481]"></i>
              </div>
              <div class="flex-1">
                <p class="text-gray-800 leading-relaxed text-lg whitespace-pre-wrap">{{ msg.content }}</p>
                
                <!-- Display Sources if any -->
                <div v-if="msg.sources && msg.sources.length > 0" class="mt-4 pt-4 border-t border-gray-100">
                  <p class="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Sources consultées :</p>
                  <div class="flex flex-wrap gap-2">
                    <a v-for="(source, idx) in msg.sources" :key="idx" :href="source" target="_blank" 
                       class="text-[10px] bg-gray-50 hover:bg-gray-100 border border-gray-200 px-2 py-1 rounded-md text-[#10b481] transition-all flex items-center gap-1">
                      <i class="bx bx-link-external"></i>
                      {{ formatSource(source) }}
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="flex gap-4 animate-in fade-in">
            <div class="w-8 h-8 rounded-full bg-[#10b481]/10 flex-shrink-0 flex items-center justify-center border border-[#10b481]/20">
               <i class="bx bx-bot text-lg text-[#10b481]"></i>
            </div>
            <div class="flex items-center gap-1.5 pt-3">
              <span class="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce"></span>
              <span class="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce [animation-delay:0.2s]"></span>
              <span class="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce [animation-delay:0.4s]"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Fixed Bottom Input Area -->
      <transition name="slide-up">
        <div v-if="messages.length > 0 || isTyping" class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-white via-white/95 to-transparent p-4 md:p-8 pt-10 pointer-events-none">
          <div class="max-w-2xl mx-auto w-full pointer-events-auto">
            <div class="relative bg-gray-50 border border-gray-200 rounded-3xl p-2 flex flex-col shadow-sm transition-all duration-300 focus-within:border-[#10b481]/50 focus-within:bg-white focus-within:shadow-md">
              <textarea 
                v-model="userInput" 
                @keydown.enter.prevent="sendMessage"
                placeholder="Posez votre question sur l'agriculture..."
                class="w-full bg-transparent border-none focus:outline-none text-lg py-4 px-6 resize-none min-h-[60px] max-h-[200px] scrollbar-hide text-gray-900 placeholder:text-gray-400"
                rows="1"
              ></textarea>
              
              <div class="flex items-center justify-between px-4 pb-2 pt-1">
                <div class="flex items-center gap-2">
                  <button 
                    @click="newChat"
                    title="Nouvelle discussion"
                    class="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-100"
                  >
                    <i class="bx bx-plus text-xl"></i>
                  </button>
                  <button 
                    @click="isSearchMode = !isSearchMode"
                    :class="[
                      'flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold transition-all',
                      isSearchMode ? 'bg-[#10b481]/10 text-[#10b481] border border-[#10b481]/20' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    ]"
                  >
                    <i class="bx bx-globe text-sm"></i>
                    Recherche
                  </button>
                </div>
                
                <button 
                  @click="sendMessage"
                  :disabled="!userInput.trim() || isTyping"
                  class="w-10 h-10 bg-[#10b481] text-white rounded-full flex items-center justify-center disabled:bg-gray-200 disabled:text-gray-400 transition-all shadow-sm hover:scale-105 active:scale-95"
                >
                  <i class="bx bx-up-arrow-alt text-2xl font-bold"></i>
                </button>
              </div>
            </div>
            <div class="mt-3 flex justify-center flex-col items-center gap-1">
               <p v-if="!canAsk" class="text-red-500 text-[10px] uppercase font-black tracking-widest bg-red-50 px-3 py-1 rounded-full border border-red-100">
                  Verrouillé • Prochain message dans {{ timeLeft }}
               </p>
               <p class="text-gray-400 text-[10px] tracking-wide opacity-80">
                 Sesily AI peut faire des erreurs.
               </p>
            </div>
          </div>
        </div>
      </transition>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, nextTick, onUnmounted } from 'vue';

const localePath = useLocalePath();
const { apiFetch } = useApi();

const userInput = ref('');
const messages = ref<any[]>([]);
const isTyping = ref(false);
const isSearchMode = ref(false);
const lastQuestionTime = ref<number | null>(null);
const currentTime = ref(Date.now());
const chatContainer = ref<HTMLElement | null>(null);
const showToast = ref(false);

const STORAGE_KEY = 'sesily_last_question_time';
const COOLDOWN_MS = 60 * 60 * 1000; // 1 hour

onMounted(() => {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    lastQuestionTime.value = parseInt(saved);
  }
  
  const timer = setInterval(() => {
    currentTime.value = Date.now();
  }, 1000);

  const savedMessages = sessionStorage.getItem('sesily_messages');
  if (savedMessages) {
    messages.value = JSON.parse(savedMessages);
    scrollToBottom();
  }

  onUnmounted(() => clearInterval(timer));
});

const canAsk = computed(() => {
  if (!lastQuestionTime.value) return true;
  const elapsed = currentTime.value - lastQuestionTime.value;
  return elapsed >= COOLDOWN_MS;
});

const timeLeft = computed(() => {
  if (!lastQuestionTime.value) return '';
  const remaining = COOLDOWN_MS - (currentTime.value - lastQuestionTime.value);
  if (remaining <= 0) return '';
  
  const minutes = Math.floor(remaining / 60000);
  const seconds = Math.floor((remaining % 60000) / 1000);
  return `${minutes}m ${seconds}s`;
});

const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTo({
      top: chatContainer.value.scrollHeight,
      behavior: 'smooth'
    });
  }
};


const newChat = () => {
  if (confirm('Voulez-vous effacer cette discussion et en recommencer une nouvelle ?')) {
    messages.value = [];
    sessionStorage.removeItem('sesily_messages');
  }
};

const formatSource = (url: string) => {
  try {
    const domain = new URL(url).hostname;
    return domain.replace('www.', '');
  } catch {
    return 'Lien';
  }
};

const sendMessage = async () => {
  if (!userInput.value.trim() || isTyping.value) return;

  // Check rate limit
  if (!canAsk.value) {
    showToast.value = true;
    setTimeout(() => {
      showToast.value = false;
    }, 5000);
    return;
  }

  const question = userInput.value;
  messages.value.push({ role: 'user', content: question });
  userInput.value = '';
  
  // Set cooldown
  lastQuestionTime.value = Date.now();
  localStorage.setItem(STORAGE_KEY, lastQuestionTime.value.toString());
  
  sessionStorage.setItem('sesily_messages', JSON.stringify(messages.value));

  await scrollToBottom();
  isTyping.value = true;

  try {
    const payload = { 
      question,
      search_enabled: isSearchMode.value,
      chat_history: messages.value.slice(-6).map(m => ({ role: m.role, content: m.content }))
    };

    const data: any = await apiFetch('/api/v2/smart-assistant/ask-public/', {
      method: 'POST',
      body: payload
    });
    
    isTyping.value = false;

    messages.value.push({ 
      role: 'assistant', 
      content: data.answer || "Désolé, je n'ai pas pu traiter votre demande.",
      sources: data.sources || []
    });
    
    sessionStorage.setItem('sesily_messages', JSON.stringify(messages.value));
    await scrollToBottom();
  } catch (error) {
    isTyping.value = false;
    messages.value.push({ 
      role: 'assistant', 
      content: "Une erreur est survenue lors de la communication avec l'IA. Veuillez réessayer plus tard."
    });
    await scrollToBottom();
  }
};
</script>

<style scoped>
@import url('https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css');

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.animate-in {
  animation-fill-mode: forwards;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active, .slide-up-leave-active {
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(30px);
  opacity: 0;
}

.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-down-enter-from, .slide-down-leave-to {
  transform: translate(-50%, -100%);
  opacity: 0;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.slide-up {
  animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in {
  animation: fadeIn 0.8s ease-out;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.animate-bounce {
  animation: bounce 1s infinite;
}
</style>
