<template>
  <div class="chat-wrapper" :class="{ 'sidebar-open': isHistoryOpen }">
    <!-- Sidebar History -->
    <aside class="chat-sidebar">
      <div class="sidebar-header">
        <h2 class="sidebar-title">{{ t("chatHistory") }}</h2>
        <button @click="createNewChat" class="btn-new-chat" :title="t('newChat')">
          <i class="bx bx-plus"></i>
        </button>
      </div>
      
      <div class="sessions-list">
        <div v-if="loadingSessions" class="loading-state">
          <i class="bx bx-loader-alt bx-spin"></i>
        </div>
        <button
          v-for="session in sessions"
          :key="session.id"
          @click="loadSessionDetail(session.id)"
          class="session-item"
          :class="{ 'session-item--active': currentSessionId === session.id }"
        >
          <i class="bx bx-message-square-detail"></i>
          <span class="session-label">{{ session.title || 'Sans titre' }}</span>
        </button>
        <div v-if="!loadingSessions && sessions.length === 0" class="empty-sessions">
          {{ t("noHistoryFound") }}
        </div>
      </div>
    </aside>

    <div class="chat-page">
      <!-- Main Header -->
      <header class="chat-header">
        <div class="header-left">
          <button @click="isHistoryOpen = !isHistoryOpen" class="btn-toggle-sidebar" title="Menu">
            <i class="bx" :class="isHistoryOpen ? 'bx-chevron-left' : 'bx-menu'"></i>
          </button>
          <div class="brand">
            <div class="ai-avatar-mini">
              <i class="bx bx-leaf"></i>
            </div>
            <span class="brand-name">Sesily AI</span>
          </div>
        </div>
        
        <div class="header-right">
          <button @click="createNewChat" class="btn-action-mobile" :title="t('newChat')">
            <i class="bx bx-plus"></i>
          </button>
        </div>
      </header>

      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>

      <!-- Messages area -->
      <div
        v-if="isMounted"
        ref="chatContainer"
        class="messages-area"
      >
        <div class="messages-inner">
          <transition-group name="msg" tag="div" class="msg-list">
            <div
              v-for="(msg, index) in messages"
              :key="index"
              class="msg-row"
              :class="msg.role === 'user' ? 'msg-row--user' : 'msg-row--ai'"
            >
              <!-- AI avatar -->
              <div v-if="msg.role === 'assistant'" class="ai-avatar">
                <i class="bx bx-leaf"></i>
              </div>

              <div class="message-content-wrapper">
                <div
                  class="bubble"
                  :class="msg.role === 'user' ? 'bubble--user' : 'bubble--ai'"
                >
                  <span v-html="formatMessage(msg.content)"></span>
                </div>
                
                <!-- AI Message Tools (Feedback + Metadata) -->
                <div v-if="msg.role === 'assistant'" class="message-tools">
                  <div class="metadata-tags">
                    <span v-if="msg.metadata?.intent" class="tag tag--intent">
                      {{ t('detectedIntent') }}: {{ msg.metadata.intent }}
                    </span>
                    <span class="tag tag--provider">{{ t('aiProvider') }}</span>
                  </div>
                  
                  <div class="feedback-tools">
                    <button 
                      @click="handleFeedback(msg.id, 2)" 
                      class="btn-feedback"
                      :class="{ 'btn-feedback--active': msg.feedback?.rating === 2 }"
                      title="Utile"
                    >
                      <i class="bx bx-like"></i>
                    </button>
                    <button 
                      @click="handleFeedback(msg.id, 1)" 
                      class="btn-feedback"
                      :class="{ 'btn-feedback--active': msg.feedback?.rating === 1 }"
                      title="Pas utile"
                    >
                      <i class="bx bx-dislike"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </transition-group>

          <!-- Typing indicator -->
          <div v-if="isLoading" class="msg-row msg-row--ai">
            <div class="ai-avatar">
              <i class="bx bx-leaf"></i>
            </div>
            <div class="bubble bubble--ai bubble--typing">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Welcome screen -->
      <transition name="fade">
        <div v-if="showWelcome && messages.length === 0" class="welcome-screen">
          <div class="welcome-icon">
            <i class="bx bx-leaf"></i>
          </div>
          <h1 class="welcome-title" v-html="formatBold(t('heroTitle'))"></h1>
          <p class="welcome-sub">{{ t("ask") }}</p>
        </div>
      </transition>


      <!-- Input bar -->
      <div ref="footer" class="input-bar">
        <!-- Options panel -->
        <transition name="slide-up">
          <div v-if="showOptions" class="options-panel">
            <div class="options-header">
              <span class="options-title">
                <i class="bx bx-slider-alt"></i>
                {{ t('optionsTitle') }}
              </span>
              <button @click="showOptions = false" class="options-close">
                <i class="bx bx-x"></i>
              </button>
            </div>

            <div class="options-selects">
              <div class="select-group">
                <label>{{ t("parcels") }}</label>
                <select v-model="selectedParcel">
                  <option value="">-- {{ t("allParcels") }} --</option>
                  <option v-for="parcel in parcels.filter(p => p != null)" :key="parcel.uuid" :value="parcel.uuid">
                    {{ parcel.parcel_name }}
                  </option>
                </select>
              </div>
              <div class="select-group">
                <label>{{ t("crops") }}</label>
                <select v-model="selectedCrop">
                  <option value="">-- {{ selectedParcel ? t("parcelCrops") : t("allCrops") }} --</option>
                  <option v-for="crop in availableCrops.filter(c => c != null)" :key="crop.id" :value="crop.name">
                    {{ crop.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="modules-grid">
              <label v-for="module in moduleKeys" :key="module" class="module-chip">
                <input type="checkbox" v-model="userModules[module]" />
                <span>{{ t(module) }}</span>
              </label>
            </div>
          </div>
        </transition>

        <div class="input-row">
          <button
            @click="showOptions = !showOptions"
            class="btn-icon"
            :class="{ 'btn-icon--active': showOptions }"
            title="Options de contexte"
          >
            <i class="bx bx-slider-alt"></i>
          </button>

          <input
            v-model="inputMessage"
            @keyup.enter="sendMessage()"
            type="text"
            :placeholder="t('ask')"
            class="chat-input"
            :disabled="isLoading"
          />

          <button
            @click="sendMessage()"
            class="btn-send"
            :disabled="!inputMessage.trim() || isLoading"
          >
            <i class="bx bx-up-arrow-alt"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted, watch } from "vue";
import { useAuthStore } from "~/stores/auth";
import { useApi } from "~/composables/useApi";

const authStore = useAuthStore();
const { apiFetch } = useApi();
const { t: nuxtT, tm, rt } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

const isHistoryOpen = ref(true); // Fermé par défaut sur mobile (géré en CSS)
const sessions = ref<any[]>([]);
const currentSessionId = ref<string | null>(null);
const loadingSessions = ref(false);

const showOptions = ref(false);
const parcelCrops = ref<any[]>([]);
const parcels = ref<any[]>([]);
const crops = ref<any[]>([]);
const cachedParcels = useState<any[]>("cachedParcels", () => []);
const cachedCrops = useState<any[]>("cachedCrops", () => []);
const cachedParcelCrops = useState<Record<string, any[]>>("cachedParcelCrops", () => ({}));
const selectedParcel = ref("");
const selectedCrop = ref("");
const moduleKeys = ["parcel", "crop", "soil", "weather", "tasks", "yield_records"];
const userModules = ref<Record<string, boolean>>({
  parcel: true, crop: true, soil: true,
  weather: true, tasks: true, yield_records: true,
});

const availableCrops = computed(() => {
  if (selectedParcel.value && parcelCrops.value.length > 0) {
    return parcelCrops.value;
  }
  return crops.value;
});

const messages = ref<any[]>([]);
const inputMessage = ref("");
const chatContainer = ref<HTMLElement | null>(null);
const footer = ref<HTMLElement | null>(null);
const isLoading = ref(false);
const showWelcome = ref(true);
const footerHeight = ref(80);
const isMounted = ref(false);

onMounted(async () => {
  isMounted.value = true;
  if (footer.value) footerHeight.value = footer.value.offsetHeight + 10;

  if (!authStore.isAuthenticated) return;

  // Charger les sessions passées
  fetchSessions();

  if (!cachedParcels.value.length) {
    try {
      const res: any = await apiFetch('/api/parcels/');
      const data = res.results || res;
      cachedParcels.value = Array.isArray(data) ? data.filter(p => p != null) : [];
    } catch { cachedParcels.value = []; }
  }
  parcels.value = cachedParcels.value;

  if (!cachedCrops.value.length) {
    try {
      const res: any = await apiFetch('/api/crops/');
      const data = res.results || res;
      cachedCrops.value = Array.isArray(data) ? data.filter(c => c != null) : [];
    } catch { cachedCrops.value = []; }
  }
  crops.value = cachedCrops.value;
});

async function fetchSessions() {
  loadingSessions.value = true;
  try {
    const data: any = await apiFetch('/api/v2/smart-assistant/sessions/');
    sessions.value = data.sessions || [];
  } catch (err) {
    console.error("Failed to load sessions:", err);
  } finally {
    loadingSessions.value = false;
  }
}

async function loadSessionDetail(sessionId: string) {
  if (currentSessionId.value === sessionId) return;
  
  isLoading.value = true;
  currentSessionId.value = sessionId;
  showWelcome.value = false;
  messages.value = [];
  
  try {
    const data: any = await apiFetch(`/api/v2/smart-assistant/sessions/${sessionId}/`);
    if (data.messages) {
      messages.value = data.messages;
      await nextTick();
      scrollToBottom();
    }
  } catch (err) {
    console.error("Failed to load session detail:", err);
  } finally {
    isLoading.value = false;
  }
}

function createNewChat() {
  currentSessionId.value = null;
  messages.value = [];
  showWelcome.value = true;
}

async function fetchParcelCrops(parcelId: string) {
  if (!parcelId) { parcelCrops.value = []; return; }
  if (cachedParcelCrops.value[parcelId]) { parcelCrops.value = cachedParcelCrops.value[parcelId]; return; }
  
  try {
    const data: any = await apiFetch(`/api/parcel-crops/?parcel=${parcelId}`);
    // Le backend renvoie souvent des objets ParcelCrop avec une FK 'crop'
    const list = data.map((pc: any) => ({
      id: pc.crop?.id || pc.id,
      name: pc.crop?.name || pc.crop_name || "Inconnu"
    }));
    cachedParcelCrops.value[parcelId] = list;
    parcelCrops.value = list;
  } catch (err) { 
    console.error("Error fetching parcel crops:", err);
    parcelCrops.value = []; 
  }
}

watch(selectedParcel, (v) => { fetchParcelCrops(v); selectedCrop.value = ""; });

function formatMessage(text: string) {
  if (!text) return "";
  // Nettoyage Markdown de base + gestion des icônes Sesily
  return text
    .replace(/^### (.*$)/gim, '<h3 class="text-lg font-bold mt-2 mb-1">$1</h3>')
    .replace(/^## (.*$)/gim, '<h2 class="text-xl font-bold mt-3 mb-2">$1</h2>')
    .replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold mt-4 mb-2">$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/^\s*[-*+]\s+(.*)$/gim, "<li class='ml-6 list-disc mb-1'>$1</li>")
    .replace(/^\s*\d+\.\s+(.*)$/gim, "<li class='ml-6 list-decimal mb-1'>$1</li>")
    .replace(/\n/g, "<br>")
    .replace(/📋/g, '<span class="icon-section">📋</span>')
    .replace(/📊/g, '<span class="icon-section">📊</span>')
    .replace(/⚠️/g, '<span class="icon-section">⚠️</span>')
    .replace(/💡/g, '<span class="icon-section">💡</span>')
    .replace(/<\/li><br>/g, "</li>")
    .replace(/<br><li/g, "<li");
}

function scrollToBottom() {
  if (chatContainer.value) {
    chatContainer.value.scrollTo({ top: chatContainer.value.scrollHeight, behavior: "smooth" });
  }
}

async function sendMessage() {
  if (!inputMessage.value.trim()) return;
  
  if (showWelcome.value) {
    showWelcome.value = false;
  }
  
  const userMessage = inputMessage.value;
  messages.value.push({ role: "user", content: userMessage });
  inputMessage.value = "";
  await nextTick();
  scrollToBottom();

  try {
    isLoading.value = true;
    const payload = {
      question: userMessage,
      session_id: currentSessionId.value,
      parcel_id: !selectedParcel.value ? null : selectedParcel.value,
      crop_name: !selectedCrop.value ? null : selectedCrop.value,
      user_modules: userModules.value,
    };
    
    const data: any = await apiFetch('/api/v2/smart-assistant/', {
      method: 'POST',
      body: payload,
    });
    
    isLoading.value = false;
    
    if (data.answer) {
      if (!currentSessionId.value) {
        currentSessionId.value = data.session_id;
        fetchSessions(); // Rafraîchir la liste car nouveau titre auto-généré
      }
      
      messages.value.push({ 
        id: data.message_id,
        role: "assistant", 
        content: data.answer,
        metadata: data.meta,
        feedback: null
      });
    } else {
      messages.value.push({ role: "assistant", content: t("noResponseAssistant") });
    }
  } catch (err: any) {
    isLoading.value = false;
    console.error("Assistant Error:", err);
    messages.value.push({ 
      role: "assistant", 
      content: t("errAssistant")
    });
  }
  await nextTick();
  scrollToBottom();
}

async function handleFeedback(messageId: number, rating: number) {
  if (!messageId) return;
  
  try {
    const data: any = await apiFetch('/api/v2/smart-assistant/feedback/', {
      method: 'POST',
      body: {
        message_id: messageId,
        rating: rating
      }
    });
    
    if (data.success) {
      // Mettre à jour localement
      const msg = messages.value.find(m => m.id === messageId);
      if (msg) msg.feedback = { rating };
    }
  } catch (err) {
    console.error("Feedback error:", err);
  }
}

const formatBold = (text: string) => text.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Sora:wght@600;700&display=swap');

.chat-wrapper {
  display: flex;
  height: calc(100vh - 80px - 48px); /* 80px header + 48px padding (p-6) */
  background: #f8fafc;
  overflow: hidden;
  font-family: 'Outfit', sans-serif;
  border-radius: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

/* Sidebar Styling */
.chat-sidebar {
  width: 280px;
  background: #0f172a; /* Plus sombre, bleu nuit premium */
  color: #fff;
  display: flex;
  flex-direction: column;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-right: 1px solid rgba(255,255,255,0.05);
  flex-shrink: 0;
  height: 100%;
}

.chat-wrapper:not(.sidebar-open) .chat-sidebar {
  width: 0;
  transform: translateX(-100%);
  opacity: 0;
  visibility: hidden;
}

.sidebar-header {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-title {
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  color: #94a3b8;
  letter-spacing: 0.05em;
}

.btn-new-chat {
  width: 36px; height: 36px;
  background: #334155;
  border: none;
  border-radius: 10px;
  color: #fff;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.25rem;
  transition: all 0.2s;
}
.btn-new-chat:hover { background: #10b481; transform: scale(1.05); }

.sessions-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.session-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-radius: 12px;
  color: #cbd5e1;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s;
  width: 100%;
}
.session-item:hover { background: rgba(255,255,255,0.05); color: #fff; }
.session-item--active { background: rgba(16, 180, 129, 0.15) !important; color: #10b481 !important; border-left: 3px solid #10b481; border-radius: 0 12px 12px 0; }

.session-label {
  font-size: 0.9rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Main Chat Page Adjustments */
.chat-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  min-width: 0;
}

.chat-header {
  height: 64px;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  z-index: 20;
  flex-shrink: 0; /* Fixer le header */
}

.header-left { display: flex; align-items: center; gap: 1rem; }
.btn-toggle-sidebar { width: 40px; height: 40px; border: none; background: #f1f5f9; border-radius: 10px; cursor: pointer; color: #64748b; font-size: 1.5rem; display: flex; align-items: center; justify-content: center; }
.brand { display: flex; align-items: center; gap: 0.75rem; }
.brand-name { font-weight: 700; color: #0f172a; font-family: 'Sora', sans-serif; }
.ai-avatar-mini { width: 32px; height: 32px; background: linear-gradient(135deg, #10b481, #059669); border-radius: 8px; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 1rem; }

.btn-action-mobile { display: none; width: 40px; height: 40px; border: none; background: #10b481; border-radius: 10px; color: #fff; cursor: pointer; font-size: 1.25rem; }

.orb { position: absolute; border-radius: 50%; filter: blur(100px); pointer-events: none; z-index: 0; opacity: 0.3; }
.orb-1 { width: 500px; height: 500px; background: radial-gradient(circle, #10b481, transparent 70%); top: -200px; right: -150px; }
.orb-2 { width: 400px; height: 400px; background: radial-gradient(circle, #3b82f6, transparent 70%); bottom: -100px; left: -100px; }

.messages-area { flex: 1; min-height: 0; overflow-y: auto; padding: 1.5rem 0; z-index: 1; }
.messages-inner { max-width: 800px; margin: 0 auto; padding: 0 1.5rem; }
.msg-list { display: flex; flex-direction: column; gap: 2rem; }

.msg-row { display: flex; align-items: flex-start; gap: 1rem; }
.msg-row--user { justify-content: flex-end; }
.msg-row--ai { justify-content: flex-start; }

.message-content-wrapper { display: flex; flex-direction: column; gap: 0.5rem; max-width: 80%; }
.msg-row--user .message-content-wrapper { align-items: flex-end; }

.ai-avatar { width: 40px; height: 40px; background: linear-gradient(135deg, #10b481, #059669); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 1.2rem; flex-shrink: 0; box-shadow: 0 10px 15px -3px rgba(16, 180, 129, 0.2); }

.bubble { padding: 1rem 1.25rem; border-radius: 20px; font-size: 0.95rem; line-height: 1.6; transition: all 0.2s; }
.bubble--user { background: #1e293b; color: #f8fafc; border-top-right-radius: 4px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
.bubble--ai { background: #fff; color: #1e293b; border-top-left-radius: 4px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); border: 1px solid #f1f5f9; }

.icon-section { font-size: 1.2rem; margin-right: 0.5rem; display: inline-block; vertical-align: middle; }

/* AI Meta Tools */
.message-tools { display: flex; align-items: center; justify-content: space-between; padding: 0 0.5rem; gap: 1rem; }
.metadata-tags { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.tag { font-size: 0.75rem; padding: 2px 8px; border-radius: 6px; font-weight: 500; }
.tag--intent { background: #f1f5f9; color: #64748b; }
.tag--provider { background: #f0fdf4; color: #10b481; }

.feedback-tools { display: flex; gap: 0.25rem; }
.btn-feedback { width: 28px; height: 28px; border: none; background: transparent; color: #94a3b8; cursor: pointer; border-radius: 6px; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
.btn-feedback:hover { background: #f1f5f9; color: #1e293b; }
.btn-feedback--active { background: #f1f5f9; color: #10b481 !important; transform: scale(1.1); }

.bubble--typing { display: flex; align-items: center; gap: 6px; padding: 1rem 1.5rem; }
.bubble--typing .dot { width: 6px; height: 6px; background: #10b481; border-radius: 50%; animation: bounce 0.6s infinite alternate; }

@keyframes bounce { from { transform: translateY(0); } to { transform: translateY(-4px); } }

.welcome-screen { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 2rem; z-index: 5; background: #f8fafc; }
.welcome-icon { width: 80px; height: 80px; background: linear-gradient(135deg, #10b481, #059669); border-radius: 24px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 2.5rem; margin-bottom: 1.5rem; }
.welcome-title { font-family: 'Sora', sans-serif; font-size: 2.5rem; font-weight: 700; color: #0f172a; margin-bottom: 1rem; }
.welcome-sub { color: #64748b; font-size: 1.1rem; margin-bottom: 2.5rem; }
.input-bar { 
  padding: 1rem 2rem 2rem; 
  background: transparent; 
  z-index: 10; 
  width: 100%; 
  max-width: 850px; 
  margin: 0 auto; 
  position: relative; 
}
.input-row { display: flex; gap: 0.75rem; background: #fff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 0.6rem; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); }
.chat-input { flex: 1; border: none; outline: none; padding: 0.5rem; font-size: 1rem; }
.btn-icon { width: 42px; height: 42px; background: #f1f5f9; border: none; border-radius: 14px; color: #64748b; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.btn-icon--active { background: #10b481; color: #fff; }
.btn-send { width: 42px; height: 42px; background: #10b481; border: none; border-radius: 14px; color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.25rem; }
.btn-send:disabled { background: #e2e8f0; cursor: not-allowed; }

.options-panel { 
  position: absolute;
  bottom: calc(100% + 0.5rem);
  left: 0;
  width: 380px; 
  max-width: calc(100vw - 2rem);
  background: #fff; 
  border: 1px solid #e2e8f0; 
  border-radius: 20px; 
  padding: 1.25rem; 
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); 
  z-index: 50;
}
.options-header { display: flex; justify-content: space-between; margin-bottom: 1.25rem; }
.options-selects { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1.25rem; }
.select-group label { display: block; font-size: 0.8rem; font-weight: 600; color: #64748b; margin-bottom: 0.5rem; }
.select-group select { width: 100%; padding: 0.6rem; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 0.9rem; outline: none; }
.modules-grid { display: flex; flex-wrap: wrap; gap: 0.6rem; }
.module-chip { padding: 0.4rem 0.8rem; background: #f1f5f9; border: 1px solid #e2e8f0; border-radius: 100px; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
.module-chip input { display: none; }
.module-chip:has(input:checked) { background: #10b481; color: #fff; border-color: #10b481; }

/* Transitions */
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(20px); opacity: 0; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 1024px) {
  .chat-sidebar { position: absolute; left: 0; top: 0; bottom: 0; z-index: 50; }
  .chat-wrapper:not(.sidebar-open) .chat-sidebar { width: 0; }
  .chat-wrapper.sidebar-open .chat-sidebar { width: 280px; box-shadow: 10px 0 30px rgba(0,0,0,0.1); }
}

@media (max-width: 640px) {
  .btn-action-mobile { display: flex; }
  .welcome-title { font-size: 1.75rem; }
  .brand-name { display: none; }
  .input-bar { padding: 1rem; }
  .message-content-wrapper { max-width: 90%; }
}
</style>
