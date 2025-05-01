import { computed, ref } from 'vue'
import { type DefaultColumnTypes, defaultColumnTypes, type DefaultSortingChoices, defaultSortingChoices } from '../data'
import type { DataSourceDataApiResponse } from '../types'

export function useBlocksComposable() {
  const cachedData = ref<DataSourceDataApiResponse>()

  const results = computed(() => {
    if (cachedData.value) {
      return cachedData.value.results
    } else {
      return []
    }
  })

  const columnSortingChoices = computed((): DefaultSortingChoices[] => {
    return [...defaultSortingChoices]
  })

  const columnTypeChoices = computed((): DefaultColumnTypes[] => {
    return [...defaultColumnTypes]
  })

  const hasData = computed(() => {
    return results.value.length > 0
  })

  return {
    hasData,
    results,
    cachedData,
    columnTypeChoices,
    columnSortingChoices,
  }
}
