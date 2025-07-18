<template>
  <base-card :class="{ 'border border-info': selected }" class="shadow-sm" @click="handleBlockSelection(details)">
    <template #body>
      <bar-format v-if="pageStore.blockHasData || pageStore.pageHasData" :chart-data="chartData" />
      <no-sheet-alert v-else />
    </template>
  </base-card>
</template>

<script>
import _ from 'lodash'
import { useSlides } from '@/store/slides'
import { mapState } from 'pinia'
import { getCurrentInstance } from 'vue'
import { useBlocks } from '@/composables/blocks'

import BarFormat from '../charts/BarFormat.vue'
import BaseCard from '../../layouts/bootstrap/cards/BaseCard.vue'
import NoSheetAlert from '../NoSheetAlert.vue'

export default {
  name: 'ChartBlock',
  components: {
    BarFormat,
    BaseCard,
    NoSheetAlert
  },
  props: {
    details: {
      type: Object,
      required: true
    }
  },
  emits: {
    'block-selected' () {
      return true
    }
  },
  setup () {
    const instance = getCurrentInstance()
    const { selected, handleBlockSelection } = useBlocks(instance)
    const pageStore = useSlides()

    return {
      selected,
      handleBlockSelection,
      pageStore
    }
  },
  computed: {
    ...mapState(useSlides, ['hasActiveSheet']),

    chartData () {
      const column = 'nom'
      const statistics = {}
      const values = _.map(this.pageStore.availableData.results, (item) => {
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
    }
  }
}
</script>
