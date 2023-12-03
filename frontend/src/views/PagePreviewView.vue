<template>
  <section class="container my-5">
    <div class="row">
      <div class="col-12">
        <component :is="block.component" v-for="(block, i) in currentPage.blocks" :key="block.block_id" :class="{ 'mb-2': i >= 0 }" :details="block" />
      </div>
    </div>
  </section>
</template>

<script>
import { usePublishedPages } from '@/store/published_pages'
import { mapState } from 'pinia'

import BaseCard from '@/layouts/bootstrap/cards/BaseCard.vue'
import TableBlock from '@/components/preview_blocks/TableBlock.vue'

export default {
  name: 'PagePreviewView',
  components: {
    BaseCard,
    TableBlock
  },
  setup() {
    const pageStore = usePublishedPages()

    return {
      pageStore
    }
  },
  computed: {
    ...mapState(usePublishedPages, ['currentPage'])
  },
  beforeMount() {
    this.getPage()
  },
  methods: {
    async getPage () {
      try {
        const response = await this.$http.get(`sheets/pages/${this.$route.params.id}`)
        this.pageStore.$patch({
          currentPage: response.data
        })
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>
