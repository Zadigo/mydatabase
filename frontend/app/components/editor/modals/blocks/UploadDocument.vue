<template>
  <div id="upload">
    <div class="space-y-2">
      {{ newFile }}
      <!-- Alert -->
      <nuxt-alert v-if="!dbStore.hasTables" class="mb-5" title="Missing tables" description="Your database currently has no tables. You will nened to create one in order to upload a file" />

      <!-- Name -->
      <nuxt-input v-model="newFile.name" variant="subtle" class="w-full" placeholder="Document Name" />

      <!-- Tabs -->
      <nuxt-tabs :items="items">
        <template #content="{ item }">
          <div v-if="item.label === 'File'" id="fileupload" class="py-3 space-y-2">
            <!-- Entry Key -->
            <p class="mb-3 text-sm font-light mt-3">If applicable, for a JSON object specify the entry key to extract the relevant data from</p>
            <nuxt-input v-model="newFile.entry_key" variant="subtle" class="w-full" placeholder="Entry Key e.g. results, data" />
            
            {{ processedData }}

            <!-- CSV/Json -->
            <nuxt-file-upload v-model="newFile.file" label="CSV, JSON" description="Select a CSV or JSON file to upload" class="w-full min-h-48" accept=".csv,.json,.xlsx" />

            <nuxt-button :loading="isProcessing" @click="process(newFile.file)">Test process</nuxt-button>
          </div>

          <!-- Url -->
          <div v-else-if="item.label === 'Url'" id="url" class="py-3">
            <p class="mb-3 text-sm font-light">You can also provide a URL or a Google Sheet ID to import data from external sources.</p>
            <nuxt-input v-model="newFile.url" class="w-full" placeholder="Url hosting the CSV or JSON file" />
          </div>
      
          <!-- Other -->
          <div v-else-if="item.label === 'Google sheet'" id="googlesheet" class="space-y-2 py-3">
            <nuxt-input v-model="newFile.google_sheet_id" class="w-full" placeholder="Google Sheet ID" />
          </div>
        </template>
      </nuxt-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TabsItem } from '@nuxt/ui'
import { useFileReader } from '~/composables/use/documents'
import type { NewDocument } from '~/composables/use/documents'

const dbStore = useDatabasesStore()

const props = defineProps<{ modelValue: NewDocument }>()
const emit = defineEmits<{ 'update:ModelValue': [document: NewDocument], headers: [headers: string[]] }>()

const newFile = useVModel(props, 'modelValue', emit, { defaultValue: {} as NewDocument })

/**
 * Tabs
 */

const items: TabsItem[] = [
  {
    label: 'File',
    icon: 'i-lucide-file-up'
  },
  {
    label: 'Url',
    icon: 'i-lucide-link'
  },
  {
    label: 'Google sheet',
    icon: 'i-lucide-table'
  }
]

/**
 * File analysis
 */

const { isValid, process, dataSummary, processedData, isProcessing } = useFileReader()

watchDebounced(processedData, (value) => {
  if (isDefined(value)) {
    console.log('processedData', value)
    emit('headers', value.headers)
  }
}, {
  immediate: false,
  debounce: 800
})
</script>
