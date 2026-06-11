<template>
  <button
    @click="$emit('click')"
    :class="[
      'w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all text-left',
      active
        ? 'bg-[#112830] text-white'
        : 'bg-white hover:bg-gray-50 border border-gray-100'
    ]"
  >
    <!-- Avatar -->
    <div
      :class="[
        'w-10 h-10 rounded-full flex items-center justify-center text-sm font-black flex-shrink-0',
        active ? 'bg-[#10b481] text-white' : 'bg-[#112830] text-white'
      ]"
    >
      {{ initials }}
    </div>

    <!-- Contenu -->
    <div class="flex-1 min-w-0">
      <div class="flex items-center justify-between gap-2">
        <p :class="['text-sm font-black truncate', active ? 'text-white' : 'text-[#112830]']">
          {{ otherParticipant }}
        </p>
        <span :class="['text-[10px] flex-shrink-0', active ? 'text-white/60' : 'text-gray-400']">
          {{ formattedDate }}
        </span>
      </div>
      <div class="flex items-center justify-between gap-2 mt-0.5">
        <p :class="['text-xs truncate', active ? 'text-white/70' : 'text-gray-500']">
          {{ lastMessagePreview }}
        </p>
        <span
          v-if="conversation.unread_count > 0"
          class="flex-shrink-0 min-w-[18px] h-[18px] px-1 bg-[#10b481] text-white text-[10px] font-black rounded-full flex items-center justify-center"
        >
          {{ conversation.unread_count }}
        </span>
      </div>
      <p v-if="conversation.related_post_name" :class="['text-[10px] mt-0.5 truncate', active ? 'text-white/50' : 'text-gray-400']">
        <i class="bx bx-package mr-0.5"></i>{{ conversation.related_post_name }}
      </p>
    </div>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  conversation: any;
  currentUserUuid: string;
  active?: boolean;
}>();

defineEmits<{ click: [] }>();

const otherParticipant = computed(() => {
  const other = props.conversation.participants?.find(
    (p: any) => p.uuid !== props.currentUserUuid
  );
  if (!other) return '—';
  return other.first_name
    ? `${other.first_name} ${other.last_name ?? ''}`.trim()
    : other.username;
});

const initials = computed(() => {
  const name = otherParticipant.value;
  const parts = name.trim().split(' ').filter(Boolean);
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
  return name.slice(0, 2).toUpperCase();
});

const lastMessagePreview = computed(() => {
  const msg = props.conversation.last_message;
  if (!msg) return '—';
  return msg.content?.length > 50 ? msg.content.slice(0, 50) + '…' : msg.content;
});

const formattedDate = computed(() => {
  const raw = props.conversation.updated_at;
  if (!raw) return '';
  const d = new Date(raw);
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - d.getTime()) / 86400000);
  if (diffDays === 0) return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  if (diffDays === 1) return 'Hier';
  if (diffDays < 7) return d.toLocaleDateString([], { weekday: 'short' });
  return d.toLocaleDateString([], { day: '2-digit', month: '2-digit' });
});
</script>
