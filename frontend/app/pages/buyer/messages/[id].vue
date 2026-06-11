<template>
  <!-- Conteneur fixe : occupe exactement l'espace du main (100vh - header - padding) sans scroll de page -->
  <div class="flex flex-col overflow-hidden bg-[#f8fafc]" style="height: calc(100vh - 7rem);">

    <!-- PageHeader — taille fixe, ne scroll pas -->
    <div class="flex-shrink-0 pb-4">
      <PageHeader :title="otherParticipantName">
        <template #subtitle>
          <span v-if="conversation?.related_post_name"
            class="px-2.5 py-1 bg-gray-50 border border-gray-100 rounded-lg text-[9px] font-black uppercase tracking-widest text-gray-500">
            <i class="bx bx-package mr-1"></i>{{ conversation.related_post_name }}
          </span>
        </template>
        <template #breadcrumb>
          <NuxtLink to="/buyer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
            <i class="bx bx-home text-sm"></i>
          </NuxtLink>
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <NuxtLink to="/buyer/inbox" class="hover:text-[#10b481] transition-colors">{{ t('messaging.inbox') }}</NuxtLink>
          <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
          <span class="text-[#10b481] truncate max-w-[120px]">{{ otherParticipantName }}</span>
        </template>
      </PageHeader>
    </div>

    <!-- Carte chat — prend tout l'espace restant, seule la zone messages scroll -->
    <div class="flex-1 min-h-0 bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden flex flex-col">

      <!-- Zone messages — seule partie scrollable -->
      <div class="flex-1 min-h-0 overflow-y-auto p-4" ref="messagesContainer">

        <!-- Loading skeleton -->
        <div v-if="loading && currentMessages.length === 0" class="space-y-4">
          <div v-for="i in 5" :key="i" :class="['flex gap-2', i % 2 === 0 ? 'flex-row-reverse' : 'flex-row']">
            <div class="w-7 h-7 rounded-full bg-gray-100 animate-pulse flex-shrink-0"></div>
            <div :class="['h-10 rounded-2xl bg-gray-100 animate-pulse', i % 2 === 0 ? 'w-48' : 'w-64']"></div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-else-if="currentMessages.length === 0"
          class="h-full flex flex-col items-center justify-center gap-3 text-center">
          <i class="bx bx-message-dots text-5xl text-gray-200"></i>
          <p class="text-sm font-black text-gray-400">{{ t('messaging.noMessages') }}</p>
          <p class="text-xs text-gray-300">{{ t('messaging.startConversation') }}</p>
        </div>

        <!-- Messages -->
        <div v-else>
          <MessageBubble
            v-for="msg in currentMessages"
            :key="msg.uuid"
            :message="msg"
            :current-user-uuid="authStore.uuid ?? ''"
          />
        </div>
      </div>

      <!-- Input — taille fixe en bas de la carte -->
      <ChatInput :disabled="sending" @send="handleSend" />
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '~/stores/auth';
import { useMessaging } from '~/composables/useMessaging';
import MessageBubble from '~/components/features/messaging/MessageBubble.vue';
import ChatInput from '~/components/features/messaging/ChatInput.vue';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const route     = useRoute();
const authStore = useAuthStore();
const {
  conversations, currentMessages, currentConversation,
  loading, sending,
  fetchConversations, fetchMessages, sendMessage, markAsRead,
} = useMessaging();

const messagesContainer = ref<HTMLElement | null>(null);
const convId = computed(() => route.params.id as string);

const conversation = computed(
  () => currentConversation.value ?? conversations.value.find((c: any) => c.uuid === convId.value)
);

const otherParticipantName = computed(() => {
  const participants = conversation.value?.participants ?? [];
  const other = participants.find((p: any) => p.uuid !== authStore.uuid);
  if (!other) return '…';
  return other.first_name
    ? `${other.first_name} ${other.last_name ?? ''}`.trim()
    : other.username;
});

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
}

let pollInterval: ReturnType<typeof setInterval> | null = null;

async function load() {
  if (conversations.value.length === 0) await fetchConversations();
  await fetchMessages(convId.value);
  await markAsRead(convId.value);
  scrollToBottom();
}

async function handleSend(content: string) {
  await sendMessage(convId.value, content);
  scrollToBottom();
}

onMounted(() => {
  load();
  pollInterval = setInterval(async () => {
    await fetchMessages(convId.value);
    scrollToBottom();
  }, 5000);
});

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval);
});
</script>
