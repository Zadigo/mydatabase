<template>
  <base-card :class="{ 'border border-info': selected }" class="shadow-sm" @click="handleBlockSelection(details)">
    <template #body>
      <bar-format v-if="pageStore.blockHasData || pageStore.pageHasData" :chart-data="chartData" />
      <no-sheet-alert v-else />
    </template>
  </base-card>
</template>

<script setup lang="ts">
import { useSlides } from 'src/stores/slides'
import { mapState, storeToRefs } from 'pinia'
import { computed, getCurrentInstance } from 'vue'
import { useBlocksComposable } from 'src/composables/blocks'

import BarFormat from '../charts/BarFormat.vue'
import BaseCard from '../../layouts/bootstrap/cards/BaseCard.vue'
import NoSheetAlert from '../NoSheetAlert.vue'

defineProps({
  details: {
    type: Object,
    required: true
  }
})

defineEmits({
  'block-selected' () {
    return true
  }
})

const slidesStore = useSlides()
const { hasActiveSheet } = storeToRefs(slidesStore)

const { selected, handleBlockSelection } = useBlocksComposable()

const chartData = computed(() => {
  const column = 'nom'
  const statistics = {}
  const values = slidesStore.availableData.results.map((item) => {
    return item[column]
  })
  
  values.forEach((value) => {
    statistics[value] = 0
  })
  
  values.forEach((value) => {
    statistics[value] += 1
  })
  
  return {
    labels: Object.keys(statistics),
    datasets: [{
      label: `Count of ${column}`,
      data: Object.values(statistics)
    }]
  }
})
</script>
