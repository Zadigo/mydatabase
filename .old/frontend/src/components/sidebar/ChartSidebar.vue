<template>
  <div class="p-4 my-4">
    <!-- Sheets -->
    <sheet-selection is-block />

    <div class="my-4">
      <label for="group-by">Group by</label>
      <v-select id="group-by" v-model="chartDetails.group_by" class="mb-2" :items="pageStore.availableDataColumns" variant="outlined" hide-details></v-select>

      <label for="metric">Metric</label>
      <v-select id="metric" v-model="chartDetails.metric" :items="defaultMetrics" variant="outlined" hide-details></v-select>
    </div>

    <v-btn color="danger" variant="tonal" rounded block @click="handleBlockDeletion">Delete</v-btn>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useSlides } from '@/store/slides'
import { storeToRefs } from 'pinia'
import { useColumnFilters } from '@/composables/page'

import SheetSelection from '../SheetSelection.vue'

export default {
  name: 'ChartSidebar',
  components: {
    SheetSelection
  },
  setup () {
    const pageStore = useSlides()
    const { currentBlock } = storeToRefs(pageStore)

    const { defaultOperators, defaultColumnInputs } = useColumnFilters()
    const showFilterSettings = ref(false)

    const defaultMetrics = [
      'Sum',
      'Average',
      'Count',
      'Percent'
    ]

    const chartDetails = ref({
      group_by: null,
      metric: 'Count'
    })


    return {
      chartDetails,
      defaultMetrics,
      defaultOperators,
      defaultColumnInputs,
      showFilterSettings,
      currentBlock,
      pageStore,
    }
  },
  methods: {
    async handleSelection (data) {
      console.log(data)
    },
    async handleBlockDeletion () {
      // Deletes a block from a given page
      try {
        const path = `sheets/pages/${this.pageStore.currentPage.page_id}/blocks/${this.currentBlock.block_id}/delete`
        const response = await this.$http.post(path)
        this.pageStore.currentPage.blocks = response.data.blocks
        this.$session.create('pages', this.pageStore.pages)
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>
