<template>
  <form @submit.prevent="handleSubmit" class="flex items-end gap-3 p-4 bg-white border-t border-gray-100">
    <textarea
      ref="inputRef"
      v-model="text"
      :placeholder="t('messaging.typeMessage')"
      :disabled="disabled"
      rows="1"
      @keydown.enter.exact.prevent="handleSubmit"
      @input="autoResize"
      class="flex-1 resize-none overflow-hidden rounded-xl border border-gray-200 px-4 py-3 text-sm text-[#112830] placeholder-gray-400 focus:outline-none focus:border-[#10b481] transition-colors disabled:opacity-50 max-h-32"
    ></textarea>
    <button
      type="submit"
      :disabled="!text.trim() || disabled"
      class="w-11 h-11 flex-shrink-0 flex items-center justify-center bg-[#112830] text-white rounded-xl hover:bg-[#10b481] transition-all disabled:opacity-40 disabled:cursor-not-allowed"
    >
      <div v-if="disabled" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
      <i v-else class="bx bx-send text-lg"></i>
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue';

defineProps<{ disabled?: boolean }>();
const emit = defineEmits<{ send: [content: string] }>();

const { t } = useI18n();
const text     = ref('');
const inputRef = ref<HTMLTextAreaElement | null>(null);

function handleSubmit() {
  const content = text.value.trim();
  if (!content) return;
  emit('send', content);
  text.value = '';
  nextTick(() => {
    if (inputRef.value) {
      inputRef.value.style.height = 'auto';
    }
  });
}

function autoResize() {
  if (!inputRef.value) return;
  inputRef.value.style.height = 'auto';
  inputRef.value.style.height = inputRef.value.scrollHeight + 'px';
}
</script>
