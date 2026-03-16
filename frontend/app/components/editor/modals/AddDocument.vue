<template>
  <nuxt-modal v-model:open="showAddDocumentModal">
    <template #title>
      Create new document
    </template>

    <template #body>
      <!-- Stepper -->
      <nuxt-stepper ref="stepper" :items="items" @next="updateStep" @prev="updateStep">
        <template #content="{ item }">
          <keep-alive>
            <editor-modals-blocks-upload-document v-if="item.title === 'Upload file'" />
            <editor-modals-blocks-select-columns v-else-if="item.title === 'Select columns'" />
          </keep-alive>
        </template>
      </nuxt-stepper>
    </template>

    <template #footer>
      <div class="ms-auto flex gap-2">
        <nuxt-button variant="soft" color="neutral" @click="() => { toggleShowAddDocumentModal() }">Cancel</nuxt-button>
        <nuxt-button v-if="canSend" :disabled="!dbStore.hasTables" @click="() => { create() }">Create</nuxt-button>
        <nuxt-button v-else @click="() => { stepperEl?.next() }">Next</nuxt-button>
      </div>
    </template>
  </nuxt-modal>
</template>

<script setup lang="ts">
import { useColumnTypeOptions, useCreateDocument } from '~/composables/use/documents'
import type { StepperItem } from '@nuxt/ui'
import { useTableWebocketManager } from '~/composables/use/tables'

const stepperEl = useTemplateRef('stepper')

/**
 * Document creation
 */

const tableEditionStore = useTableEditionStore()
const { selectedTable, selectedTableDocument } = storeToRefs(tableEditionStore)

const { wsObject } = useTableWebocketManager(selectedTable, selectedTableDocument)
const { newDocument, create, showAddDocumentModal, toggleShowAddDocumentModal, canSend, updateStep } = useCreateDocument(wsObject)

useFileCheckout(selectedTable, newDocument)

/**
 * Checks
 */

const dbStore = useDatabasesStore()

/**
 * Stepper
 */

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

/**
 * Document headers
 */

const { getTypeOptions } = useColumnTypeOptions()

function getDocumentHeaders(headers: string[]) {
  console.log('getDocumentHeaders', headers)
  const columns = getTypeOptions(headers)
  console.log('getDocumentHeaders', columns)
  newDocument.value.using_columns = columns
}
</script>
