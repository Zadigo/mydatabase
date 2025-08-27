<template>
  <nuxt-modal v-model:open="show">
    <template #title>
      Create new document
    </template>

    <template #body>
      <div class="space-y-2">
        <nuxt-alert v-if="!dbStore.hasTables" class="mb-5" title="Missing tables" description="Your database currently has no tables. You will nened to create one in order to upload a file" />

        <!-- Name -->
        <nuxt-input v-model="newDocument.name" class="w-full" placeholder="Document Name" />

        <!-- CSV -->
        <nuxt-file-upload v-model="newDocument.file" class="w-full min-h-48" accept=".csv,.json,.xlsx" />
      </div>

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
        <nuxt-button :disabled="!dbStore.hasTables" @click="() => { create() }">Create</nuxt-button>
      </div>
    </template>
  </nuxt-modal>
</template>

<script setup lang="ts">
import { useCreateDocument } from '~/composables/use/documents'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'udpate:modelValue': [] }>()
const show = useVModel(props, 'modelValue', emit, { defaultValue: true })

const { newDocument, create } = useCreateDocument()

/**
 * Checks
 */

const dbStore = useDatabasesStore()
// const tableEditionStore = useTableEditionStore()
// const {  } = storeToRefs(tableEditionStore)
</script>
