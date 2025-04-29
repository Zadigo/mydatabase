<template>
  <section class="container my-5">
    <div class="row">
      <div class="col-12">
        <h1>{{ currentSlide.name || Slide }}</h1>
        <!-- <component :is="block.component" v-for="(block, i) in currentPage.blocks" :key="block.block_id" :class="{ 'mb-2': i >= 0 }" :details="block" /> -->
      </div>
    </div>
  </section>
</template>

<script>
// import { mapState } from 'pinia'
import { useConnections } from '@/store/connections'
import { usePublishedSlides } from '@/store/published_slides'
import { storeToRefs } from 'pinia'

// import BaseCard from '@/layouts/bootstrap/cards/BaseCard.vue'
// import TableBlock from '@/components/preview_blocks/TableBlock.vue'

export default {
  name: 'SlidePreviewView',
  components: {
    // BaseCard,
    // TableBlock
  },
  setup() {
    const slidesStore = usePublishedSlides()
    const { currentSlide } = storeToRefs(slidesStore)
    const connectionsStore = useConnections()
    const { currentConnection } = storeToRefs(connectionsStore)

    return {
      currentSlide,
      connectionsStore,
      currentConnection,
      slidesStore
    }
  },
  computed: {
  },
  beforeMount() {
    this.getCurrentSlide()
  },
  methods: {
    async getCurrentSlide () {
      try {
        const response = await this.$http.get(`slides/${this.$route.params.id}`)
        this.slidesStore.$patch((state) => {
          state.currentSlide = response.data
        })
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>
