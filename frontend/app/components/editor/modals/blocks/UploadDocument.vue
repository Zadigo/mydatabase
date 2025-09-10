<template>
  <div id="upload">
    <div class="space-y-2">
      <nuxt-alert v-if="!dbStore.hasTables" class="mb-5" title="Missing tables" description="Your database currently has no tables. You will nened to create one in order to upload a file" />

      <!-- Name -->
      <nuxt-input v-model="value.name" variant="subtle" class="w-full" placeholder="Document Name" />

      <!-- Entry Key -->
      <p class="mb-3 text-sm font-light mt-3">If applicable, for a JSON object specify the entry key to extract the relevant data from</p>
      <nuxt-input v-model="value.entry_key" variant="subtle" class="w-full" placeholder="Entry Key e.g. results, data" />

      <!-- CSV/Json -->
      <nuxt-file-upload v-model="value.file" class="w-full min-h-48" accept=".csv,.json,.xlsx" />
    </div>

    <nuxt-separator class="my-5" />

    <!-- Other -->
    <div class="space-y-2">
      <p class="mb-3 text-sm font-light">You can also provide a URL or a Google Sheet ID to import data from external sources.</p>
      <nuxt-input v-model="value.url" class="w-full" placeholder="Url hosting the CSV or JSON file" />
      <nuxt-input v-model="value.google_sheet_id" :disabled="true" class="w-full" placeholder="Google Sheet ID" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NewDocument } from '~/composables/use/documents'

const dbStore = useDatabasesStore()

const props = defineProps<{ modelValue: NewDocument }>()
const emit = defineEmits<{ 'update:ModelValue': [document: NewDocument] }>()

const value = useVModel(props, 'modelValue', emit, { defaultValue: {} as NewDocument })
</script>
