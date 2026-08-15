<template>
  <nuxt-modal v-model:open="showAddDocumentModal">
    <template #title>
      Create new document
    </template>

    <template #body>
      <!-- Stepper -->
      <nuxt-stepper ref="stepper" :items="items" @next="updateStep" @prev="updateStep">
        <template #content="{ item }">
          <div class="mt-10">
            <div id="upload-documents" v-if="item.title === 'Documents'" >
              <div class="flex justify-between mb-3">
                <!-- Merging -->
                <nuxt-switch v-model="newDocument.merge" label="Merge files" />
  
                <!-- Add Document -->
                <nuxt-dropdown-menu :filter="{ icon: 'i-lucide-search', loading: false }" :items="addDocumentMenuItems" ignore-filter>
                  <nuxt-button>
                    <icon name="i-lucide-plus" />
                  </nuxt-button>
                </nuxt-dropdown-menu>
              </div>
              
              <!-- Global document name -->
              <nuxt-input v-if="newDocument.merge" v-model="newDocument.name" class="my-5 w-full" variant="subtle" placeholder="Merged document name" />
              
              <!-- Inputs -->
              <div class="space-y-2">
                <editor-modals-blocks-upload-inputs />
              </div>
            </div>
  
            <editor-modals-blocks-select-columns v-else-if="item.title === 'Select columns'" />
          </div>
        </template>
      </nuxt-stepper>
    </template>

    <template #footer>
      <div class="ms-auto flex gap-2">
        <nuxt-button variant="soft" color="neutral" @click="() => { toggleShowAddDocumentModal() }">
          Cancel
        </nuxt-button>

        <nuxt-button :disabled="!hasTables" @click="() => { create() }">
          Create
        </nuxt-button>
        
        <nuxt-button @click="() => { stepperEl?.next() }">
          Next
        </nuxt-button>
      </div>
    </template>
  </nuxt-modal>
</template>

<script setup lang="ts">
import type { DropdownMenuItem, StepperItem } from '@nuxt/ui'

const stepperEl = useTemplateRef('stepper')

/**
 * Document creation
 */

const { selectedTable, selectedTableDocument } = useTableEditionComposable()

const { wsObject } = useTableWebocketManager(selectedTable, selectedTableDocument)
const { newDocument, create, showAddDocumentModal, toggleShowAddDocumentModal, updateStep, addDocument } = useCreateDocument(wsObject)

/**
 * File checkout
 */

const { fileCheckoutResponse } = usePrefetchProvider(selectedTable, newDocument)

/**
 * Checks
 */

const { hasTables } = _useDatabases() 

/**
 * Stepper
 */

const items: StepperItem[] = [
  {
    title: 'Documents',
    icon: 'i-lucide-file'
  }, 
  {
    title: 'Select columns',
    icon: 'i-lucide-table'
  }
]

/**
 * Menu
 */

const addDocumentMenuItems: DropdownMenuItem[] = [
  { 
    label: 'CSV', 
    icon: 'i-lucide-case-sensitive',
    onSelect(event) {
      event.preventDefault()
      addDocument('csv')
    }
  }, 
  {
    label: 'Google sheet', 
    icon: 'i-lucide-table-2',
    onSelect(event) {
      event.preventDefault()
      addDocument('google_sheet')
    }
  }, 
  { 
    label: 'Json', 
    icon: 'i-lucide-file-json-2',
    onSelect(event) {
      event.preventDefault()
      addDocument('json')
    }
  }
]
</script>
