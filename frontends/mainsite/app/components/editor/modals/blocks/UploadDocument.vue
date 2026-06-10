<template>
  <div id="upload">
    <div class="space-y-2">
      {{ newDocument }}
      <!-- Alert -->
      <nuxt-alert v-if="!dbStore.hasTables" class="mb-5" title="Missing tables" description="Your database currently has no tables. You will nened to create one in order to upload a file" />

      <!-- Name -->
      <nuxt-input v-model="newDocument.name" variant="subtle" class="w-full" placeholder="Document Name" />

      <!-- Tabs -->
      <nuxt-tabs :items="items">
        <template #content="{ item }">
          <!-- File -->
          <div v-if="item.label === 'File'" id="fileupload" class="py-3 space-y-2">
            <!-- Entry Key -->
            <p class="mb-3 text-sm font-light mt-3">If applicable, for a JSON object specify the entry key to extract the relevant data from</p>
            <nuxt-input v-model="newDocument.entry_key" variant="subtle" class="w-full" placeholder="Entry Key e.g. results, data" />
            
            {{ fileCheckoutResponse }}

            <!-- CSV/Json -->
            <nuxt-file-upload v-model="newDocument.file" label="CSV, JSON" description="Select a CSV or JSON file to upload" class="w-full min-h-48" accept=".csv,.json,.xlsx" />
          </div>

          <!-- Url -->
          <div v-else-if="item.label === 'Url'" id="url" class="py-3">
            <p class="mb-3 text-sm font-light">You can also provide a URL or a Google Sheet ID to import data from external sources.</p>
            <nuxt-input v-model="newDocument.url" :loading="true" class="w-full" placeholder="Url hosting the CSV or JSON file" />

            <nuxt-button @click="testSend">Test prefetch</nuxt-button>
          </div>
      
          <!-- Other -->
          <div v-else-if="item.label === 'Google sheet'" id="googlesheet" class="space-y-2 py-3">
            <nuxt-input v-model="newDocument.google_sheet_id" class="w-full" placeholder="Google Sheet ID" />
          </div>
        </template>
      </nuxt-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TabsItem } from '@nuxt/ui'

/**
 * Store
 */

const dbStore = useDatabasesStore()

/**
 * Creation
 */

const { newDocument } = useCreateDocument()

/**
 * File reading
 */

const { fileCheckoutResponse } = useFileCheckoutStore()

/**
 * Url prefetching
 */

const { stringify } = useWebsocketMessage()
watch(() => newDocument.value, (newDoc) => {
  console.log(newDoc)
  if (isDefined(wsObject) && newDoc.url !== '') {
    wsObject.send(stringify({ action: 'load_via_url', url: newDoc.url, entry_key: newDoc.entry_key || undefined }))
    
    if(isDefined(wsObject.data)) {
      const data = parse(wsObject.data)
      if (data?.action === 'checkedout_url') {
        newDocument.value.using_columns = data.columns.type_options
        console.log('AddDocument.vue - newDocument', wsObject.data.value)
      }
    }
  }
})


// TESTING
const tableEditionStore = useTableEditionStore()
const { selectedTable, selectedTableDocument } = storeToRefs(tableEditionStore)
const { wsObject } = useTableWebocketManager(selectedTable, selectedTableDocument)
const { parse } = useWebsocketMessage()

function testSend() {
  wsObject.send(JSON.stringify({ action: 'checkout_url', url: 'https://jsonplaceholder.typicode.com/todos' }))
  if (isDefined(wsObject.data)) {
    const data = parse(wsObject.data)
    if (data?.action === 'checkedout_url') {
      newDocument.value.using_columns = data.columns.type_options
      console.log('AddDocument.vue - newDocument', wsObject.data.value)
    }
  }
}

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
</script>
