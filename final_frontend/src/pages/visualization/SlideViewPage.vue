<template>
  <q-page class="q-pa-xl" padding>
    <template v-for="block in slide.blocks" :key="block.block_id">
      <component :is="getComponent(block.component)" :block="block" :slide-data-results="slideDataResults" />
    </template>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue';

import TableViewBlock from 'src/components/visualization/TableViewBlock.vue';
import { Slide } from './slides';

export default defineComponent({
  name: 'SlideViewPage',
  components: {
    TableViewBlock
  },
  setup () {
    const slide = ref<Slide>({})
    const slideDataResults = ref([])
    return {
      slide,
      slideDataResults
    }
  },
  created () {
    this.requestSlide()
  },
  methods: {
    /**
     * 
     */
    async requestSlide () {
      try {
        const response = await this.$api.get(`slides/${this.$route.params.id}`)
        this.slide = response.data

        const response2 = await this.$api.get(`datasources/${response.data.slide_data_source.data_source_id}`)
        this.slideDataResults = response2.data
      } catch (error) {
        // Handle error
      }
    },
    /**
     * 
     */
    getComponent (name) {
      const components = {
        'table-block': 'table-view-block'
      }
      return components[name]
    }
  }
})
</script>
