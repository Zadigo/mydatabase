<template>
  <v-select id="sheet-selection" v-model="currentSelection" :items="pageStore.connections" item-title="name" item-value="sheet_id" placeholder="Select spreadsheet" variant="outlined" hide-details class="mb-3" @update:model-value="handleSelection"></v-select>
</template>

<script>
import { useSlides } from '@/store/slides'
import { ref } from 'vue'

export default {
  name: 'SheetSelection',
  props: {
    isBlock: {
      type: Boolean
    }
  },
  setup () {
    const currentSelection = ref(null)
    const pageStore = useSlides()
    return {
      currentSelection,
      pageStore
    }
  },
  created () {
    if (this.isBlock) {
      this.currentSelection = this.pageStore.currentBlock.block_url_source
    } else {
      this.currentSelection = this.pageStore.currentPage.page_url_source
    }

    if (!this.pageStore.hasLoadedConnections) {
      this.pageStore.connections = this.$session.retrieve('connections')
    }
  },
  methods: {
    async handleSelection (data) {
      // Sets the data either at the page level or at the
      // block level depending on where are calling the select
      try {
        const response = await this.$http.get(`sheets/${data}`)
        if (this.isBlock) {
          this.pageStore.currentBlock.block_url_source = data
          this.pageStore.currentBlockData = response.data
        } else {
          this.pageStore.currentPage.page_url_source = data
          this.pageStore.currentPageData = response.data
        }
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>
