<template>
  <header id="block-selection" class="col-12">
    <div class="card shadow-sm mb-5">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
          <div class="d-flex justify-content-start gap-2">
            <button v-for="blockType in blockTypes" :key="blockType.name" type="button" class="btn btn-info shadow-none btn-rounded" rounded @click="handleAddBlock(blockType)">
              <IconBase :icon="`${blockType.icon}`" />
            </button>
          </div>

          <div class="d-flex justify-content-end gap-1">
            <button type="button" class="btn btn-rounded btn-dark d-flex inline-flex shadow-none align-items-center" rounded>
              <IconBase icon="fa-solid:eye" class="me-2" />
              Publish
            </button>

            <div v-if="currentSlide">
              <router-link :to="{ name: 'page_preview', params: { id: currentSlide.slide_id } }" class="btn btn-rounded btn-success d-flex inline-flex shadow-none align-items-center">
                <IconBase icon="fa-solid:eye" class="me-2" />
                Preview
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useSlides } from 'src/stores/slides'
import { storeToRefs } from 'pinia'
import { PropType } from 'vue'

import type { BlockType } from 'src/types'

defineProps({
  blockTypes: {
    type: Array as PropType<BlockType[]>,
    required: true
  }
})

const slidesStore = useSlides()
const { currentSlide } = storeToRefs(slidesStore)

/**
 * TODO:
 */
async function handleAddBlock(blockType: BlockType) {
  // Creates a new block for the slide
  try {
    const path = `/api/v1/sheets/pages/${pageStore.currentPage.page_id}/blocks/create`
    const response = await api.post(path, {
      name: null,
      component: blockType.component,
      conditions: { filters: [] }
    })

    currentPage.blocks.push(response.data)
    this.$session.create('pages', this.pageStore.pages)
    this.showBlocksModal = false
  } catch (e) {
    console.error(e)
  }
}
</script>
