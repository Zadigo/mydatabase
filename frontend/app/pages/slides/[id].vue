<template>
  <section id="slide">
    <header>
      <NuxtCard class="shadow-sm ring-0">
        <template #body>
          <div class="flex justify-between items-center">
            <div class="flex justify-start gap-2">
              <NuxtButton v-for="blockType in blockTypes" :key="blockType.name" @click="create(blockType)">
                <Icon :name="blockType.icon" />
              </NuxtButton>
            </div>
            
            <div class="flex justify-end gap-2">
              <NuxtButton>
                <Icon name="i-fa-solid:eye" />
                Publish
              </NuxtButton>

              <NuxtButton v-if="activeSlide" :to="`/preview/${activeSlide.slide_id}`">
                <Icon name="i-fa-solid:eye" />
                Preview
              </NuxtButton>
            </div>
          </div>
        </template>
      </NuxtCard>
    </header>

    <section id="blocks" class="mt-5">
      <div v-if="hasBlocks">
        <Suspense>
          <component :is="dynamicComponents[block.component]" v-for="block in blocks" :key="block.block_id" :block-details="block" @select="(block) => { currentSelection=block }" />
        </Suspense>
      </div>

      <BlocksEmpty v-else @show:add-blocks-modal="showCreateModal=true" />
    </section>

    <!-- Modals -->
    <ModalsBlocksCreate v-model="showCreateModal" />
  </section>
</template>

<script setup lang="ts">
import { useBlocks } from '~/composables/blocks'
import { useGetSlideData } from '~/composables/slides'
import { blockTypes } from '~/data/constants'

definePageMeta({
  layout: 'dashboard',
  title: 'Slide Editor',
})


const slidesStore = useSlideStore()
const { slides, activeSlide } = storeToRefs(slidesStore)

const sheetsStore = useSheetsStore()
const { activeSlideSheets, hasSheets, searched } = storeToRefs(sheetsStore)

const { id } = useRoute().params as { id: string }

if (id) {
  activeSlide.value = slides.value.find(slide => slide.slide_id.toString() === id) || null
}

const { blocks, hasBlocks, showCreateModal, create, dynamicComponents, currentSelection } = useBlocks()

const { activeData } = useGetSlideData()
</script>
