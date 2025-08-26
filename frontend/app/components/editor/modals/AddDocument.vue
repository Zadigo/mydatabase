<template>
  <nuxt-modal v-model:open="show">
    <template #title>
      Create new document
    </template>

    <template #body>
      <!-- CSV -->
      <nuxt-file-upload v-model="newDocument.file" class="w-full min-h-48" accept=".csv,.json,.xlsx" />

      <nuxt-separator class="my-5" />

      <!-- Other -->
      <div class="space-y-2">
        <nuxt-input v-model="newDocument.url" class="w-full" placeholder="Via url" />
        <nuxt-input v-model="newDocument.google_sheet_id" class="w-full" placeholder="Google Sheet ID" />
      </div>
    </template>

    <template #footer>
      <div class="ms-auto flex gap-2">
        <nuxt-button @click="() => { show = false }">Cancel</nuxt-button>
        <nuxt-button @click="() => {}">Create</nuxt-button>
      </div>
    </template>
  </nuxt-modal>
</template>

<script setup lang="ts">
import { useCreateDocument } from '~/composables/use/documents'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'udpate:modelValue': [] }>()
const show = useVModel(props, 'modelValue', emit, { defaultValue: true })

const { newDocument } = useCreateDocument()
</script>
