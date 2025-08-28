<template>
  <nuxt-modal v-model:open="show">
    <template #title>
      Create new document
    </template>

    <template #body>
      <!-- Stepper -->
      <nuxt-stepper ref="stepper" :items="items">
        <template #content="{ item }">
          {{ item.title }}
        </template>
      </nuxt-stepper>

      <div class="space-y-2">
        <nuxt-alert v-if="!dbStore.hasTables" class="mb-5" title="Missing tables" description="Your database currently has no tables. You will nened to create one in order to upload a file" />

        <!-- Name -->
        <nuxt-input v-model="newDocument.name" variant="subtle" class="w-full" placeholder="Document Name" />

        <!-- Entry Key -->
        <p class="mb-3 text-sm font-light mt-3">If applicable, for a JSON object specify the entry key to extract the relevant data from</p>
        <nuxt-input v-model="newDocument.entry_key" variant="subtle" class="w-full" placeholder="Entry Key e.g. results, data" />

        <!-- CSV/Json -->
        <nuxt-file-upload v-model="newDocument.file" class="w-full min-h-48" accept=".csv,.json,.xlsx" />
      </div>

      <nuxt-separator class="my-5" />

      <!-- Other -->
      <div class="space-y-2">
        <p class="mb-3 text-sm font-light">You can also provide a URL or a Google Sheet ID to import data from external sources.</p>
        <nuxt-input v-model="newDocument.url" class="w-full" placeholder="Url hosting the CSV or JSON file" />
        <nuxt-input v-model="newDocument.google_sheet_id" :disabled="true" class="w-full" placeholder="Google Sheet ID" />
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
import type { StepperItem } from '@nuxt/ui'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'udpate:modelValue': [] }>()
const show = useVModel(props, 'modelValue', emit, { defaultValue: true })

const { newDocument, create } = useCreateDocument()

/**
 * Checks
 */

const dbStore = useDatabasesStore()

const items: StepperItem[] = [
  {
    title: 'Uplaod file',
    icon: 'i-lucide-file'
  }, 
  {
    title: 'Select columns',
    icon: 'i-lucide-table'
  }
]
</script>
