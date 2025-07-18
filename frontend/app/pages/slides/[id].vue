<template>
  <section id="slide">
    <header>
      <NuxtCard class="shadow-sm ring-0">
        <template #body>
          <div class="flex justify-between items-center">
            <div class="flex justify-start gap-2">
              <NuxtButton v-for="blockType in blockTypes" :key="blockType.name" @click="handleAddBlock(blockType)">
                <Icon :name="blockType.icon" />
              </NuxtButton>
            </div>
            
            <div class="flex justify-end gap-2">
              <NuxtButton>
                <font-awesome-icon :icon="['fas', 'eye']" class="me-2" />
                Publish
              </NuxtButton>

              <NuxtButton :to="{ name: 'page_preview_view', params: { id: currentSlide.slide_id } }">
                <font-awesome-icon :icon="['fas', 'eye']" class="me-2" />
                Preview
              </NuxtButton>
            </div>
          </div>
        </template>
      </NuxtCard>
    </header>

    <section id="blocks" class="mt-5">
      <div v-if="hasBlocks">
        Blocks here
        <!-- <component :is="block.component" v-for="(block, i) in currentSlide.blocks" :key="block.block_id" :class="{ 'mb-2': i >= 0 }" :block-details="block" :is-selected="checkIsSelected(block)" @block-selected="handleBlockSelection" /> -->
      </div>

      <BlocksEmpty v-else />
    </section>
  </section>
</template>

<script setup lang="ts">
import { useBlock } from '~/composables/blocks'
import { blockTypes } from '~/data/constants'

const { blocks, getBlocks, hasBlocks } = useBlock()
</script>
