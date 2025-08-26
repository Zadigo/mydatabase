<template>
  <section id="editor">
    <nuxt-card>
      <template #header>
        <div v-if="selectedTable" class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">
            {{ selectedTable.name }}
          </h2>

          <nuxt-button @click="() => { toggleEditTableDrawer() }">
            <icon name="i-lucide-pen" class="mr-2" />
            Edit table
          </nuxt-button>
        </div>

        <template v-else>
          <div class="flex gap-2">
            <nuxt-skeleton class="h-5 w-40" />
            <nuxt-skeleton class="h-5 w-20" />
          </div>
        </template>
      </template>

      <!-- Component -->  
      <component :is="displayComponent" v-if="hasData" />
      <template v-else>
        <div v-if="selectedTable" class="w-full text-center">
          <p>Your table has no data. Select a datasource or create a new one</p>

          <nuxt-button class="mt-5">
            <icon name="i-lucide-file-plus-2" />
            Create New Document
          </nuxt-button>
        </div>

        <div v-else class="w-full text-center">
          <p>Select a table</p>
          
          <nuxt-button class="mt-5">
            <icon name="i-lucide-table" />
            Select a table
          </nuxt-button>
        </div>
      </template>
    </nuxt-card>

    <!-- Modals -->
    <editor-modals-edit-table v-model="showEditTableDrawer" />
  </section>
</template>

<script setup lang="ts">
import { useTableWebocketManager } from '~/composables/use/tables'

definePageMeta({
  title: 'Editor: Table',
  layout: 'details'
})

const tableEditorStore = useTableEditionStore()
const { selectedTable, tableData, hasDocuments, hasData, selectedTableDocument } = storeToRefs(tableEditorStore)

const { displayComponent, editableTableRef, showEditTableDrawer, toggleEditTableDrawer } = useTable(selectedTable)

provide('hasData', hasData)
provide('tableData', tableData)
provide('hasDocuments', hasDocuments)
provide('editableTableRef', editableTableRef)

console.log('editableTableRef', editableTableRef.value)

const { wsobject } = useTableWebocketManager(editableTableRef, selectedTableDocument)
</script>
