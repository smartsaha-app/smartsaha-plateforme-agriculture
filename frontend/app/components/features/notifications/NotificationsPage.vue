<template>
  <div class="min-h-screen bg-[#f8fafc] p-6 md:p-8 space-y-6">

    <!-- Header -->
    <PageHeader :title="t('notifications.title')">
      <template #subtitle>
        <span class="px-2.5 py-1 bg-gray-50 border border-gray-100 rounded-lg text-[9px] font-black uppercase tracking-widest text-gray-500">
          {{ unreadNotifCount }} {{ t('notifications.unread') }}
        </span>
      </template>
      <template #breadcrumb>
        <NuxtLink :to="homePath" class="flex items-center gap-1 hover:text-[#10b481] transition-colors">
          <i class="bx bx-home text-sm"></i>
        </NuxtLink>
        <i class="bx bx-chevron-right text-gray-300 text-xs"></i>
        <span class="text-[#10b481]">{{ t('notifications.title') }}</span>
      </template>
    </PageHeader>

    <!-- Marquer tout lu -->
    <div v-if="notifications.length > 0 && unreadNotifCount > 0" class="flex justify-end">
      <button
        @click="markAllAsRead"
        class="text-sm font-semibold text-[#10b481] hover:underline transition"
      >
        {{ t('notifications.markAllRead') }}
      </button>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loadingNotifs && notifications.length === 0" class="space-y-3">
      <div v-for="i in 5" :key="i" class="h-[72px] bg-white rounded-xl border border-gray-100 animate-pulse"></div>
    </div>

    <!-- Empty state -->
    <div
      v-else-if="notifications.length === 0"
      class="bg-white rounded-2xl border border-gray-100 shadow-sm p-16 flex flex-col items-center text-center gap-4"
    >
      <div class="w-16 h-16 rounded-2xl bg-gray-50 flex items-center justify-center">
        <i class="bx bx-bell text-3xl text-gray-300"></i>
      </div>
      <div>
        <p class="text-base font-black text-[#112830]">{{ t('notifications.empty') }}</p>
        <p class="text-sm text-gray-400 mt-1">{{ t('notifications.emptyDesc') }}</p>
      </div>
    </div>

    <!-- Liste -->
    <div v-else class="space-y-2">
      <div
        v-for="notif in notifications"
        :key="notif.uuid"
        @click="handleClick(notif)"
        :class="[
          'bg-white rounded-xl border border-gray-100 p-4 flex items-start gap-4 cursor-pointer',
          'hover:border-[#10b481]/40 hover:shadow-sm transition-all duration-200',
          !notif.is_read ? 'border-l-4 border-l-[#10b481]' : ''
        ]"
      >
        <!-- Icône -->
        <div :class="['w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0', iconBg(notif.notification_type)]">
          <i :class="['text-xl', notifIcon(notif.notification_type)]"></i>
        </div>

        <!-- Contenu -->
        <div class="flex-1 min-w-0">
          <p :class="['text-sm text-[#112830] truncate', !notif.is_read ? 'font-bold' : 'font-semibold']">
            {{ notif.title }}
          </p>
          <p class="text-sm text-gray-500 mt-0.5 line-clamp-2">{{ notif.body }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ formatDate(notif.created_at) }}</p>
        </div>

        <!-- Indicateur non lu -->
        <div v-if="!notif.is_read" class="w-2.5 h-2.5 rounded-full bg-[#10b481] mt-1.5 flex-shrink-0"></div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotifications } from '~/composables/useNotifications'
import type { Notification } from '~/composables/useNotifications'

const props = defineProps<{ space: string }>()

const { t } = useI18n()
const router = useRouter()
const {
  notifications, unreadNotifCount, loadingNotifs,
  fetchNotifications, markAsRead, markAllAsRead,
} = useNotifications()

// Lien dashboard propre à chaque espace
const homePath = computed(() =>
  props.space === 'admin' ? '/admin' : `/${props.space}/dashboard`
)

// Redirection selon le type de notification + espace
function resolveTarget(notif: Notification): string | null {
  const s = props.space
  if (notif.notification_type === 'new_message' && notif.data?.conversation_id) {
    // Seuls buyer et seller ont une page messages
    if (s === 'buyer' || s === 'seller') {
      return `/${s}/messages/${notif.data.conversation_id}`
    }
    return null
  }
  if (['new_order', 'order_status', 'payment_received'].includes(notif.notification_type)) {
    if (s === 'farmer') return '/farmer/marketplace/orders'
    if (s === 'buyer' || s === 'seller') return `/${s}/orders`
    return null
  }
  return null
}

async function handleClick(notif: Notification) {
  if (!notif.is_read) await markAsRead(notif.uuid)
  const target = resolveTarget(notif)
  if (target) router.push(target)
}

function notifIcon(type: string) {
  const map: Record<string, string> = {
    new_message:      'bx bx-message-dots text-blue-500',
    new_order:        'bx bx-shopping-bag text-[#10b481]',
    order_status:     'bx bx-package text-orange-500',
    payment_received: 'bx bx-wallet text-purple-500',
    weather_alert:    'bx bx-cloud-lightning text-yellow-500',
    system:           'bx bx-bell text-gray-500',
  }
  return map[type] ?? 'bx bx-bell text-gray-500'
}

function iconBg(type: string) {
  const map: Record<string, string> = {
    new_message:      'bg-blue-50',
    new_order:        'bg-[#10b481]/10',
    order_status:     'bg-orange-50',
    payment_received: 'bg-purple-50',
    weather_alert:    'bg-yellow-50',
    system:           'bg-gray-50',
  }
  return map[type] ?? 'bg-gray-50'
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit',
  })
}

onMounted(fetchNotifications)
</script>
