import { computed } from 'vue'

export type Plan = 'FREE' | 'PRO'

export const usePlan = () => {
  const spaces = useCookie<Record<string, any>>('user_spaces')

  const plan    = computed<Plan>(() => spaces.value?.plan ?? 'FREE')
  const isPro   = computed(() => plan.value === 'PRO')
  const isFree  = computed(() => plan.value === 'FREE')

  const planExpiresAt = computed<Date | null>(() => {
    const val = spaces.value?.plan_expires_at
    return val ? new Date(val) : null
  })

  const isPlanExpired = computed(() => {
    if (!planExpiresAt.value) return false
    return planExpiresAt.value < new Date()
  })

  const planDaysLeft = computed<number | null>(() => {
    if (!planExpiresAt.value) return null
    const diff = planExpiresAt.value.getTime() - Date.now()
    return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)))
  })

  return { plan, isPro, isFree, planExpiresAt, isPlanExpired, planDaysLeft }
}
