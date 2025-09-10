<template>
  <nuxt-modal v-model:open="show">
    <template #title>
      Create new document
    </template>

    <template #body>
      <!-- Stepper -->
      <nuxt-stepper ref="stepper" :items="items">
        <template #content="{ item }">
          {{ item }}
          <editor-modals-blocks-upload-document v-if="item.title === 'Upload file'" v-model="newDocument" />
          <editor-modals-blocks-select-columns v-else-if="item.title === 'Select columns'" v-model="newDocument" />
        </template>
      </nuxt-stepper>
    </template>

    <template #footer>
      <div class="ms-auto flex gap-2">
        <nuxt-button @click="() => { show = false }">Cancel</nuxt-button>
        <nuxt-button :disabled="!dbStore.hasTables" @click="() => { create() }">Create</nuxt-button>
      </div>
    </template>
  </nuxt-modal>
</template>

<script setup lang="ts">
import { useCreateDocument } from '~/composables/use/documents'
import type { StepperItem } from '@nuxt/ui'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [boolean] }>()
const show = useVModel(props, 'modelValue', emit, { defaultValue: true })

/**
 * Document creation
 */

const { newDocument, create } = useCreateDocument()

/**
 * Checks
 */

const dbStore = useDatabasesStore()

const items: StepperItem[] = [
  {
    title: 'Upload file',
    icon: 'i-lucide-file'
  }, 
  {
    title: 'Select columns',
    icon: 'i-lucide-table'
  }
]
</script>
