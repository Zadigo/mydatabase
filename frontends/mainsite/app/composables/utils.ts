export function useComputedQuery<T extends Record<string, string>>() {
  return computed(() => useRoute().query as T)
}
