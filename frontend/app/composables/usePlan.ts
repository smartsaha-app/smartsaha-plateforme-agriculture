import { computed } from 'vue'

export type Plan = 'FREE' | 'PRO'

export const usePlan = () => {
  const spaces = useCookie<Record<string, any>>('user_spaces')

  const plan = computed<Plan>(() => spaces.value?.plan ?? 'FREE')
  const isPro  = computed(() => plan.value === 'PRO')
  const isFree = computed(() => plan.value === 'FREE')

  return { plan, isPro, isFree }
}
