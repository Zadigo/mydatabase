<template>
  <NuxtModal v-model:open="show">
    <template #title>
      Create a new block
    </template>

    <template #body>
      <div class="grid grid-cols-4 grid-rows-1 gap-2">
        <div v-for="blockType in blockTypes" :key="blockType.name" class="p-10 border-1 border-primary-50 rounded-md cursor-pointer bg-primary-200/50 hover:bg-primary-200/70" @click="create(blockType)">
          <Icon :name="blockType.icon" size="30" />
        </div>
      </div>
    </template>
  </NuxtModal>
</template>

<script setup lang="ts">
import { useBlock } from '~/composables/blocks'
import { blockTypes } from '~/data/constants'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [boolean] }>()
const show = useVModel(props, 'modelValue', emit)

const { create } = useBlock()
</script>
