<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- Header -->
    <PageHeader :title="t('messaging.inbox')">
      <template #subtitle>
        <span class="px-2.5 py-1 bg-gray-50 border border-gray-100 rounded-lg text-[9px] font-black uppercase tracking-widest text-gray-500">
          {{ conversations.length }} {{ t('messaging.inbox').toLowerCase() }}
        </span>
      </template>
      <template #breadcrumb>
        <NuxtLink to="/buyer/dashboard" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
          <span>{{ t('dashboard.home') }}</span>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('messaging.inbox') }}</span>
      </template>
    </PageHeader>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="h-20 bg-white rounded-xl border border-gray-100 animate-pulse"></div>
    </div>

    <!-- Empty state -->
    <div v-else-if="conversations.length === 0"
      class="bg-white rounded-2xl border border-gray-100 shadow-sm p-16 flex flex-col items-center text-center gap-4">
      <div class="w-16 h-16 rounded-2xl bg-gray-50 flex items-center justify-center">
        <i class="bx bx-message-dots text-3xl text-gray-300"></i>
      </div>
      <div>
        <p class="text-base font-black text-[#112830]">{{ t('messaging.noConversations') }}</p>
        <p class="text-sm text-gray-400 mt-1">{{ t('messaging.noConversationsDesc') }}</p>
      </div>
      <NuxtLink to="/buyer/products"
        class="mt-2 px-5 py-2.5 bg-[#112830] text-white text-sm font-bold rounded-xl hover:bg-[#10b481] transition-all">
        {{ t('buyer.goToShop') }}
      </NuxtLink>
    </div>

    <!-- Liste conversations -->
    <div v-else class="space-y-2">
      <ConversationItem
        v-for="conv in conversations"
        :key="conv.uuid"
        :conversation="conv"
        :current-user-uuid="authStore.uuid ?? ''"
        @click="router.push(`/buyer/messages/${conv.uuid}`)"
      />
    </div>

  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '~/stores/auth';
import { useMessaging } from '~/composables/useMessaging';
import ConversationItem from '~/components/features/messaging/ConversationItem.vue';

const { t } = useI18n();
definePageMeta({ layout: 'dashboard' });

const router    = useRouter();
const authStore = useAuthStore();
const { conversations, loading, fetchConversations } = useMessaging();

onMounted(fetchConversations);
</script>
