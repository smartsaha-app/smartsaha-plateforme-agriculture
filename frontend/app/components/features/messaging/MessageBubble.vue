<template>
  <div :class="['flex gap-2 mb-3', isMe ? 'flex-row-reverse' : 'flex-row']">
    <!-- Avatar -->
    <div
      v-if="!isMe"
      class="w-7 h-7 rounded-full bg-[#112830] text-white flex items-center justify-center text-[10px] font-black flex-shrink-0 mt-1"
    >
      {{ senderInitials }}
    </div>

    <!-- Bulle -->
    <div :class="['max-w-[72%] space-y-0.5', isMe ? 'items-end' : 'items-start', 'flex flex-col']">
      <p v-if="!isMe" class="text-[10px] font-black text-gray-400 px-1">{{ senderName }}</p>
      <div
        :class="[
          'px-4 py-2.5 rounded-2xl text-sm leading-relaxed',
          isMe
            ? 'bg-[#112830] text-white rounded-br-sm'
            : 'bg-white border border-gray-100 text-[#112830] rounded-bl-sm shadow-sm'
        ]"
      >
        {{ message.content }}
      </div>
      <p :class="['text-[10px] px-1', isMe ? 'text-right text-gray-400' : 'text-gray-400']">
        {{ formattedTime }}
        <span v-if="isMe && message.is_read" class="ml-1 text-[#10b481]">
          <i class="bx bx-check-double"></i>
        </span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  message: any;
  currentUserUuid: string;
}>();

const isMe = computed(() => props.message.is_me ?? props.message.sender?.uuid === props.currentUserUuid);

const senderName = computed(() => props.message.sender_name ?? 'Utilisateur');

const senderInitials = computed(() => {
  const name = senderName.value;
  const parts = name.trim().split(' ').filter(Boolean);
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
  return name.slice(0, 2).toUpperCase();
});

const formattedTime = computed(() => {
  if (!props.message.created_at) return '';
  return new Date(props.message.created_at).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
});
</script>
