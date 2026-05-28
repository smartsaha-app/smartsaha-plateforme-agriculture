<template>
  <div class="chat-wrapper" :class="{ 'sidebar-open': isHistoryOpen }">

    <!-- ===== SIDEBAR ===== -->
    <aside class="chat-sidebar">
      <div class="sidebar-top">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-[#10b481] to-[#059669] flex items-center justify-center shadow-lg shadow-emerald-900/30">
            <i class="bx bx-leaf text-white text-lg"></i>
          </div>
          <div>
            <p class="text-sm font-black text-white leading-none">Sesily</p>
            <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Assistant IA</p>
          </div>
        </div>
        <button @click="createNewChat" class="sidebar-new-btn" :title="t('newChat')">
          <i class="bx bx-edit text-base"></i>
        </button>
      </div>

      <div class="sidebar-section-label">{{ t('chatHistory') }}</div>

      <div class="sessions-list">
        <div v-if="loadingSessions" class="flex flex-col gap-2 px-2">
          <div v-for="i in 5" :key="i" class="h-10 rounded-xl bg-white/5 animate-pulse"></div>
        </div>

        <template v-else>
          <button
            v-for="session in sessions"
            :key="session.id"
            @click="loadSessionDetail(session.id)"
            class="session-item"
            :class="{ 'session-active': currentSessionId === session.id }"
          >
            <i class="bx bx-message-rounded text-sm flex-shrink-0"></i>
            <span class="session-label">{{ session.title || 'Sans titre' }}</span>
          </button>

          <div v-if="sessions.length === 0" class="flex flex-col items-center justify-center py-10 gap-2 text-center">
            <i class="bx bx-chat text-3xl text-slate-600"></i>
            <p class="text-xs text-slate-500 font-medium">{{ t('noHistoryFound') }}</p>
          </div>
        </template>
      </div>
    </aside>

    <!-- ===== MAIN CHAT AREA ===== -->
    <div class="chat-main">

      <!-- Internal header -->
      <header class="chat-header">
        <div class="flex items-center gap-3">
          <button @click="isHistoryOpen = !isHistoryOpen" class="toggle-btn">
            <i class="bx text-xl text-slate-500"
               :class="isHistoryOpen ? 'bx-sidebar' : 'bx-menu'"></i>
          </button>
          <div class="flex items-center gap-3">
            <div class="relative">
              <div class="w-10 h-10 rounded-2xl bg-gradient-to-br from-[#10b481] to-[#059669] flex items-center justify-center shadow-md shadow-emerald-200">
                <i class="bx bx-leaf text-white text-lg"></i>
              </div>
              <span class="absolute -bottom-0.5 -right-0.5 w-3 h-3 bg-[#10b481] border-2 border-white rounded-full"></span>
            </div>
            <div>
              <p class="text-sm font-black text-[#112830] leading-none">Sesily AI</p>
              <p class="text-[10px] font-bold text-[#10b481] uppercase tracking-widest">En ligne · Agriculture</p>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button @click="createNewChat"
            class="flex items-center gap-2 px-3 py-2 rounded-xl bg-gray-50 hover:bg-[#112830] hover:text-white text-gray-500 transition-all text-xs font-bold border border-gray-100"
            :title="t('newChat')"
          >
            <i class="bx bx-plus text-base"></i>
            <span class="hidden sm:block">Nouveau</span>
          </button>
        </div>
      </header>

      <!-- Ambient orbs -->
      <div class="orb orb-1"></div>
      <div class="orb orb-2"></div>

      <!-- Messages -->
      <div ref="chatContainer" class="messages-area" v-if="isMounted">
        <div class="messages-inner">

          <!-- Welcome screen -->
          <transition name="fade">
            <div v-if="showWelcome && messages.length === 0" class="welcome-screen">
              <div class="welcome-glow"></div>
              <div class="welcome-icon">
                <i class="bx bx-leaf text-white text-4xl"></i>
              </div>
              <h1 class="welcome-title" v-html="formatBold(t('heroTitle'))"></h1>
              <p class="welcome-sub">{{ t('ask') }}</p>

              <!-- Quick suggestions -->
              <div class="suggestions-grid">
                <button
                  v-for="s in suggestions"
                  :key="s.text"
                  @click="fillSuggestion(s.text)"
                  class="suggestion-chip"
                >
                  <div class="suggestion-icon">
                    <i :class="s.icon"></i>
                  </div>
                  <span>{{ s.text }}</span>
                </button>
              </div>
            </div>
          </transition>

          <!-- Messages list -->
          <transition-group name="msg" tag="div" class="msg-list">
            <div
              v-for="(msg, index) in messages"
              :key="index"
              class="msg-row"
              :class="msg.role === 'user' ? 'msg-user' : 'msg-ai'"
            >
              <div v-if="msg.role === 'assistant'" class="ai-avatar">
                <i class="bx bx-leaf text-white"></i>
              </div>

              <div class="bubble-wrap" :class="msg.role === 'user' ? 'items-end' : 'items-start'">
                <div class="bubble" :class="msg.role === 'user' ? 'bubble-user' : 'bubble-ai'">
                  <span v-html="formatMessage(msg.content)"></span>
                </div>

                <!-- AI actions row -->
                <div v-if="msg.role === 'assistant'" class="msg-actions">
                  <div class="flex items-center gap-1.5 flex-wrap">
                    <span v-if="msg.metadata?.intent" class="meta-chip">
                      <i class="bx bx-target-lock text-xs"></i>
                      {{ msg.metadata.intent }}
                    </span>
                    <span class="meta-chip meta-chip--green">
                      <i class="bx bx-leaf text-xs"></i>
                      Sesily IA
                    </span>
                  </div>
                  <div class="flex items-center gap-1">
                    <button @click="handleFeedback(msg.id, 2)" class="fb-btn" :class="{ 'fb-active': msg.feedback?.rating === 2 }">
                      <i class="bx bx-like text-sm"></i>
                    </button>
                    <button @click="handleFeedback(msg.id, 1)" class="fb-btn" :class="{ 'fb-active-bad': msg.feedback?.rating === 1 }">
                      <i class="bx bx-dislike text-sm"></i>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </transition-group>

          <!-- Typing indicator -->
          <div v-if="isLoading" class="msg-row msg-ai">
            <div class="ai-avatar">
              <i class="bx bx-leaf text-white"></i>
            </div>
            <div class="bubble bubble-ai bubble-typing">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </div>
          </div>

        </div>
      </div>

      <!-- Input zone -->
      <div class="input-zone">

        <!-- Context options panel -->
        <transition name="slide-up">
          <div v-if="showOptions" class="options-panel">
            <div class="flex items-center justify-between mb-4">
              <span class="text-sm font-black text-[#112830] flex items-center gap-2">
                <i class="bx bx-slider-alt text-[#10b481]"></i>
                {{ t('optionsTitle') }}
              </span>
              <button @click="showOptions = false"
                class="w-7 h-7 rounded-lg hover:bg-gray-100 flex items-center justify-center text-gray-400 transition-colors">
                <i class="bx bx-x"></i>
              </button>
            </div>

            <div class="flex flex-col gap-3 mb-4">
              <div class="select-group">
                <label>{{ t('parcels') }}</label>
                <select v-model="selectedParcel">
                  <option value="">-- {{ t('allParcels') }} --</option>
                  <option v-for="p in parcels.filter(p => p != null)" :key="p.uuid" :value="p.uuid">
                    {{ p.parcel_name }}
                  </option>
                </select>
              </div>
              <div class="select-group">
                <label>{{ t('crops') }}</label>
                <select v-model="selectedCrop">
                  <option value="">-- {{ selectedParcel ? t('parcelCrops') : t('allCrops') }} --</option>
                  <option v-for="c in availableCrops.filter(c => c != null)" :key="c.id" :value="c.name">
                    {{ c.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="flex flex-wrap gap-2">
              <label v-for="module in moduleKeys" :key="module" class="module-chip">
                <input type="checkbox" v-model="userModules[module]" />
                <span>{{ t(module) }}</span>
              </label>
            </div>
          </div>
        </transition>

        <!-- Input bar -->
        <div class="input-bar" :class="{ 'input-bar--focused': isInputFocused }">
          <button
            @click="showOptions = !showOptions"
            class="input-action-btn"
            :class="showOptions ? 'input-action-btn--on' : ''"
            title="Contexte"
          >
            <i class="bx bx-slider-alt"></i>
          </button>

          <textarea
            ref="inputRef"
            v-model="inputMessage"
            @keydown.enter.exact.prevent="sendMessage()"
            @keydown.shift.enter="() => {}"
            @focus="isInputFocused = true"
            @blur="isInputFocused = false"
            @input="autoResize"
            rows="1"
            :placeholder="t('ask')"
            class="chat-input"
            :disabled="isLoading"
          ></textarea>

          <button
            @click="sendMessage()"
            class="send-btn"
            :disabled="!inputMessage.trim() || isLoading"
          >
            <i v-if="!isLoading" class="bx bx-up-arrow-alt text-xl"></i>
            <div v-else class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          </button>
        </div>

        <p class="input-hint">
          <i class="bx bx-keyboard text-xs"></i>
          Entrée pour envoyer &nbsp;·&nbsp; Maj+Entrée pour nouvelle ligne
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, onMounted, watch } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useApi } from '~/composables/useApi';

const authStore = useAuthStore();
const { apiFetch } = useApi();
const { t: nuxtT } = useI18n();
const t = (key: string) => nuxtT(`dashboard.${key}`);

// ─── History sidebar ───────────────────────────────────────────────
const isHistoryOpen  = ref(true);
const sessions       = ref<any[]>([]);
const currentSessionId = ref<string | null>(null);
const loadingSessions  = ref(false);

// ─── Context options ───────────────────────────────────────────────
const showOptions   = ref(false);
const parcels       = ref<any[]>([]);
const crops         = ref<any[]>([]);
const parcelCrops   = ref<any[]>([]);
const cachedParcels = useState<any[]>('cachedParcels', () => []);
const cachedCrops   = useState<any[]>('cachedCrops', () => []);
const cachedParcelCrops = useState<Record<string, any[]>>('cachedParcelCrops', () => ({}));
const selectedParcel = ref('');
const selectedCrop   = ref('');
const moduleKeys = ['parcel', 'crop', 'soil', 'weather', 'tasks', 'yield_records'];
const userModules = ref<Record<string, boolean>>({
  parcel: true, crop: true, soil: true, weather: true, tasks: true, yield_records: true,
});

const availableCrops = computed(() =>
  selectedParcel.value && parcelCrops.value.length > 0 ? parcelCrops.value : crops.value
);

// ─── Chat state ────────────────────────────────────────────────────
const messages     = ref<any[]>([]);
const inputMessage = ref('');
const chatContainer = ref<HTMLElement | null>(null);
const inputRef     = ref<HTMLTextAreaElement | null>(null);
const isLoading    = ref(false);
const showWelcome  = ref(true);
const isMounted    = ref(false);
const isInputFocused = ref(false);

// ─── Quick suggestions ─────────────────────────────────────────────
const suggestions = [
  { icon: 'bx bx-droplet',    text: "Quand arroser mes cultures de riz ?" },
  { icon: 'bx bx-bug',        text: "Comment traiter les maladies fongiques ?" },
  { icon: 'bx bx-sun',        text: "Météo et conseils pour cette semaine" },
  { icon: 'bx bx-leaf',       text: "Meilleures cultures pour la saison sèche" },
];

function fillSuggestion(text: string) {
  inputMessage.value = text;
  inputRef.value?.focus();
}

function autoResize() {
  const el = inputRef.value;
  if (!el) return;
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 160) + 'px';
}

// ─── Lifecycle ─────────────────────────────────────────────────────
onMounted(async () => {
  isMounted.value = true;
  if (!authStore.isAuthenticated) return;

  fetchSessions();

  if (!cachedParcels.value.length) {
    try {
      const res: any = await apiFetch('/api/parcels/');
      cachedParcels.value = (res.results || res || []).filter(Boolean);
    } catch { cachedParcels.value = []; }
  }
  parcels.value = cachedParcels.value;

  if (!cachedCrops.value.length) {
    try {
      const res: any = await apiFetch('/api/crops/');
      cachedCrops.value = (res.results || res || []).filter(Boolean);
    } catch { cachedCrops.value = []; }
  }
  crops.value = cachedCrops.value;
});

// ─── Session management ────────────────────────────────────────────
async function fetchSessions() {
  loadingSessions.value = true;
  try {
    const data: any = await apiFetch('/api/v2/smart-assistant/sessions/');
    sessions.value = data.sessions || [];
  } catch (err) {
    console.error('Failed to load sessions:', err);
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
    console.error('Failed to load session detail:', err);
  } finally {
    isLoading.value = false;
  }
}

function createNewChat() {
  currentSessionId.value = null;
  messages.value = [];
  showWelcome.value = true;
  if (inputRef.value) {
    inputRef.value.style.height = 'auto';
  }
}

// ─── Parcel crops ──────────────────────────────────────────────────
async function fetchParcelCrops(parcelId: string) {
  if (!parcelId) { parcelCrops.value = []; return; }
  if (cachedParcelCrops.value[parcelId]) { parcelCrops.value = cachedParcelCrops.value[parcelId]; return; }
  try {
    const data: any = await apiFetch(`/api/parcel-crops/?parcel=${parcelId}`);
    const list = data.map((pc: any) => ({
      id: pc.crop?.id || pc.id,
      name: pc.crop?.name || pc.crop_name || 'Inconnu',
    }));
    cachedParcelCrops.value[parcelId] = list;
    parcelCrops.value = list;
  } catch { parcelCrops.value = []; }
}

watch(selectedParcel, (v) => { fetchParcelCrops(v); selectedCrop.value = ''; });

// ─── Message formatting ────────────────────────────────────────────
function formatMessage(text: string) {
  if (!text) return '';
  return text
    .replace(/^### (.*$)/gim, '<h3 class="text-base font-bold mt-3 mb-1 text-[#112830]">$1</h3>')
    .replace(/^## (.*$)/gim,  '<h2 class="text-lg font-bold mt-4 mb-2 text-[#112830]">$1</h2>')
    .replace(/^# (.*$)/gim,   '<h1 class="text-xl font-bold mt-4 mb-2 text-[#112830]">$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g,     '<em>$1</em>')
    .replace(/^\s*[-*+]\s+(.*)$/gim, '<li class="ml-5 list-disc mb-1 leading-relaxed">$1</li>')
    .replace(/^\s*\d+\.\s+(.*)$/gim, '<li class="ml-5 list-decimal mb-1 leading-relaxed">$1</li>')
    .replace(/\n/g, '<br>')
    .replace(/<\/li><br>/g, '</li>')
    .replace(/<br><li/g, '<li');
}

function scrollToBottom() {
  if (chatContainer.value) {
    chatContainer.value.scrollTo({ top: chatContainer.value.scrollHeight, behavior: 'smooth' });
  }
}

// ─── Send message ──────────────────────────────────────────────────
async function sendMessage() {
  if (!inputMessage.value.trim() || isLoading.value) return;
  showWelcome.value = false;

  const userMessage = inputMessage.value;
  messages.value.push({ role: 'user', content: userMessage });
  inputMessage.value = '';
  if (inputRef.value) inputRef.value.style.height = 'auto';
  await nextTick();
  scrollToBottom();

  try {
    isLoading.value = true;
    const data: any = await apiFetch('/api/v2/smart-assistant/', {
      method: 'POST',
      body: {
        question: userMessage,
        session_id: currentSessionId.value,
        parcel_id: selectedParcel.value || null,
        crop_name: selectedCrop.value || null,
        user_modules: userModules.value,
      },
    });
    isLoading.value = false;

    if (data.answer) {
      if (!currentSessionId.value) {
        currentSessionId.value = data.session_id;
        fetchSessions();
      }
      messages.value.push({
        id: data.message_id,
        role: 'assistant',
        content: data.answer,
        metadata: data.meta,
        feedback: null,
      });
    } else {
      messages.value.push({ role: 'assistant', content: t('noResponseAssistant') });
    }
  } catch (err: any) {
    isLoading.value = false;
    messages.value.push({ role: 'assistant', content: t('errAssistant') });
  }
  await nextTick();
  scrollToBottom();
}

// ─── Feedback ──────────────────────────────────────────────────────
async function handleFeedback(messageId: number, rating: number) {
  if (!messageId) return;
  try {
    const data: any = await apiFetch('/api/v2/smart-assistant/feedback/', {
      method: 'POST',
      body: { message_id: messageId, rating },
    });
    if (data.success) {
      const msg = messages.value.find(m => m.id === messageId);
      if (msg) msg.feedback = { rating };
    }
  } catch (err) {
    console.error('Feedback error:', err);
  }
}

const formatBold = (text: string) => text.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
</script>

<style scoped>
/* ─── Layout ──────────────────────────────────────────────────── */
.chat-wrapper {
  display: flex;
  height: calc(100vh - 64px - 48px);
  background: #f8fafc;
  overflow: hidden;
  border-radius: 1.5rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  font-family: 'Readex Pro', sans-serif;
}

/* ─── Sidebar ─────────────────────────────────────────────────── */
.chat-sidebar {
  width: 260px;
  background: #0c1825;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1),
              opacity 0.3s ease,
              visibility 0.3s;
  border-right: 1px solid rgba(255,255,255,0.04);
  overflow: hidden;
}
.chat-wrapper:not(.sidebar-open) .chat-sidebar {
  width: 0;
  opacity: 0;
  visibility: hidden;
}

.sidebar-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
}
.sidebar-new-btn {
  width: 34px; height: 34px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 10px;
  color: #94a3b8;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}
.sidebar-new-btn:hover { background: #10b481; color: #fff; border-color: #10b481; }

.sidebar-section-label {
  padding: 1rem 1rem 0.5rem;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #475569;
}

.sessions-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.25rem 0.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}
.sessions-list::-webkit-scrollbar { width: 3px; }
.sessions-list::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }

.session-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.875rem;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #64748b;
  cursor: pointer;
  text-align: left;
  width: 100%;
  transition: all 0.15s;
}
.session-item:hover { background: rgba(255,255,255,0.04); color: #cbd5e1; }
.session-active {
  background: rgba(16,180,129,0.12) !important;
  color: #10b481 !important;
}
.session-label {
  font-size: 0.82rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ─── Main ────────────────────────────────────────────────────── */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  position: relative;
  background: #f8fafc;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.25rem;
  height: 60px;
  background: #fff;
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
  z-index: 10;
}
.toggle-btn {
  width: 38px; height: 38px;
  border: none; background: transparent;
  border-radius: 10px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.15s;
}
.toggle-btn:hover { background: #f1f5f9; }

/* ─── Orbs ────────────────────────────────────────────────────── */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
  opacity: 0.25;
}
.orb-1 { width: 400px; height: 400px; background: radial-gradient(circle, #10b481, transparent 70%); top: -150px; right: -100px; }
.orb-2 { width: 300px; height: 300px; background: radial-gradient(circle, #6366f1, transparent 70%); bottom: 60px; left: -80px; }

/* ─── Messages ────────────────────────────────────────────────── */
.messages-area {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 1.5rem 0 0.5rem;
  z-index: 1;
  scroll-behavior: smooth;
}
.messages-area::-webkit-scrollbar { width: 4px; }
.messages-area::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 4px; }

.messages-inner {
  max-width: 780px;
  margin: 0 auto;
  padding: 0 1.5rem;
}
.msg-list { display: flex; flex-direction: column; gap: 1.75rem; }

.msg-row { display: flex; align-items: flex-start; gap: 0.875rem; }
.msg-user { justify-content: flex-end; }
.msg-ai   { justify-content: flex-start; }

.ai-avatar {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, #10b481, #059669);
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 1rem;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(16,180,129,0.25);
}

.bubble-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 78%;
}
.msg-user .bubble-wrap { align-items: flex-end; }

.bubble {
  padding: 0.875rem 1.125rem;
  border-radius: 18px;
  font-size: 0.9rem;
  line-height: 1.65;
  word-break: break-word;
}
.bubble-user {
  background: #112830;
  color: #f8fafc;
  border-top-right-radius: 4px;
  box-shadow: 0 4px 16px rgba(17,40,48,0.15);
}
.bubble-ai {
  background: #fff;
  color: #1e293b;
  border-top-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  border: 1px solid #f1f5f9;
}
.bubble-typing {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 0.875rem 1.25rem;
}
.dot {
  width: 7px; height: 7px;
  background: #10b481;
  border-radius: 50%;
  animation: bounce 0.6s infinite alternate;
}
.dot:nth-child(2) { animation-delay: 0.15s; }
.dot:nth-child(3) { animation-delay: 0.3s; }
@keyframes bounce { from { transform: translateY(0); opacity: 0.6; } to { transform: translateY(-5px); opacity: 1; } }

/* ─── Message actions ─────────────────────────────────────────── */
.msg-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0 0.25rem;
}
.meta-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  background: #f8fafc;
  color: #94a3b8;
  border: 1px solid #f1f5f9;
}
.meta-chip--green { background: #f0fdf4; color: #10b481; border-color: #d1fae5; }

.fb-btn {
  width: 28px; height: 28px;
  border: none;
  background: transparent;
  color: #cbd5e1;
  cursor: pointer;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.fb-btn:hover { background: #f1f5f9; color: #64748b; }
.fb-active { background: #f0fdf4 !important; color: #10b481 !important; }
.fb-active-bad { background: #fff1f2 !important; color: #f43f5e !important; }

/* ─── Welcome screen ──────────────────────────────────────────── */
.welcome-screen {
  position: absolute;
  inset: 60px 0 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
  z-index: 5;
  background: #f8fafc;
}
.welcome-glow {
  position: absolute;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(16,180,129,0.08), transparent 65%);
  border-radius: 50%;
  pointer-events: none;
}
.welcome-icon {
  width: 72px; height: 72px;
  background: linear-gradient(135deg, #10b481, #059669);
  border-radius: 22px;
  display: flex; align-items: center; justify-content: center;
  margin-bottom: 1.5rem;
  box-shadow: 0 16px 40px rgba(16,180,129,0.25);
  position: relative;
}
.welcome-title {
  font-size: 2rem;
  font-weight: 900;
  color: #112830;
  margin-bottom: 0.75rem;
  line-height: 1.2;
}
.welcome-sub {
  color: #94a3b8;
  font-size: 1rem;
  margin-bottom: 2rem;
}

.suggestions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
  max-width: 560px;
  width: 100%;
}
.suggestion-chip {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  cursor: pointer;
  text-align: left;
  font-size: 0.83rem;
  color: #475569;
  font-weight: 500;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.suggestion-chip:hover {
  border-color: #10b481;
  background: #f0fdf4;
  color: #112830;
  box-shadow: 0 4px 12px rgba(16,180,129,0.1);
  transform: translateY(-1px);
}
.suggestion-icon {
  width: 34px; height: 34px;
  background: #f0fdf4;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #10b481;
  font-size: 1rem;
  flex-shrink: 0;
}
.suggestion-chip:hover .suggestion-icon { background: #10b481; color: #fff; }

/* ─── Input zone ──────────────────────────────────────────────── */
.input-zone {
  padding: 0.75rem 1.5rem 1.25rem;
  background: transparent;
  z-index: 10;
  position: relative;
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
}

.input-bar {
  display: flex;
  align-items: flex-end;
  gap: 0.625rem;
  background: #fff;
  border: 1.5px solid #e2e8f0;
  border-radius: 18px;
  padding: 0.5rem 0.5rem 0.5rem 0.75rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.05);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.input-bar--focused {
  border-color: #10b481;
  box-shadow: 0 4px 16px rgba(16,180,129,0.12);
}

.chat-input {
  flex: 1;
  border: none;
  outline: none;
  resize: none;
  font-size: 0.9rem;
  line-height: 1.5;
  color: #1e293b;
  background: transparent;
  font-family: inherit;
  max-height: 160px;
  padding: 0.35rem 0;
  overflow-y: auto;
}
.chat-input::placeholder { color: #94a3b8; }
.chat-input::-webkit-scrollbar { width: 3px; }
.chat-input::-webkit-scrollbar-thumb { background: #e2e8f0; border-radius: 4px; }

.input-action-btn {
  width: 36px; height: 36px;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 12px;
  color: #94a3b8;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  transition: all 0.15s;
  flex-shrink: 0;
}
.input-action-btn:hover { background: #f1f5f9; color: #64748b; }
.input-action-btn--on { background: #10b481 !important; color: #fff !important; border-color: #10b481 !important; }

.send-btn {
  width: 38px; height: 38px;
  background: #112830;
  border: none;
  border-radius: 13px;
  color: #fff;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}
.send-btn:not(:disabled):hover { background: #10b481; transform: scale(1.05); }
.send-btn:disabled { background: #e2e8f0; cursor: not-allowed; }

.input-hint {
  text-align: center;
  font-size: 0.68rem;
  color: #cbd5e1;
  font-weight: 500;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
}

/* ─── Options panel ───────────────────────────────────────────── */
.options-panel {
  position: absolute;
  bottom: calc(100% + 0.5rem);
  left: 1.5rem;
  width: 360px;
  max-width: calc(100vw - 3rem);
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 18px;
  padding: 1.25rem;
  box-shadow: 0 16px 40px -8px rgba(0,0,0,0.12);
  z-index: 50;
}
.select-group label {
  display: block;
  font-size: 0.72rem;
  font-weight: 800;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.4rem;
}
.select-group select {
  width: 100%;
  padding: 0.55rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 0.85rem;
  color: #1e293b;
  outline: none;
  background: #f8fafc;
  cursor: pointer;
}
.select-group select:focus { border-color: #10b481; }

.module-chip {
  padding: 0.35rem 0.75rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 100px;
  font-size: 0.78rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s;
}
.module-chip input { display: none; }
.module-chip:has(input:checked) { background: #10b481; color: #fff; border-color: #10b481; }

/* ─── Transitions ─────────────────────────────────────────────── */
.msg-enter-active { transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.msg-enter-from   { opacity: 0; transform: translateY(12px) scale(0.97); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-up-enter-from, .slide-up-leave-to       { transform: translateY(12px); opacity: 0; }

/* ─── Responsive ──────────────────────────────────────────────── */
@media (max-width: 1024px) {
  .chat-sidebar {
    position: absolute;
    top: 0; left: 0; bottom: 0;
    z-index: 50;
    height: 100%;
  }
  .chat-wrapper.sidebar-open .chat-sidebar {
    width: 260px;
    opacity: 1;
    visibility: visible;
    box-shadow: 8px 0 24px rgba(0,0,0,0.15);
  }
}

@media (max-width: 640px) {
  .welcome-title { font-size: 1.5rem; }
  .suggestions-grid { grid-template-columns: 1fr; }
  .input-zone { padding: 0.75rem 1rem 1rem; }
  .message-inner { padding: 0 1rem; }
  .bubble-wrap { max-width: 90%; }
}
</style>