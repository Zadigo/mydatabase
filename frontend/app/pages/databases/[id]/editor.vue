<template>
  <section id="editor">
    <nuxt-card>
      <template #header>
        <div v-if="selectedTable" class="flex justify-between items-center">
          <h2 class="text-lg font-semibold">
            {{ selectedTable.name }}
          </h2>

          <nuxt-button @click="() => { tableEditionStore.toggleEditTableDrawer() }">
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
      <component :is="displayComponent" v-if="!isLoading" />
      <template v-else>
        <div class="space-y-2">
          <nuxt-skeleton class="w-full h-10" />
          <nuxt-skeleton class="w-6/12 h-10" />
        </div>
      </template>
    </nuxt-card>

    <!-- Modals -->
    <lazy-editor-modals-edit-table hydrate-on-idle />
    <lazy-editor-modals-add-document hydrate-on-idle />
    <lazy-editor-modals-edit-document hydrate-on-idle />
    <lazy-editor-modals-create-table hydrate-on-idle />
  </section>
</template>

<script setup lang="ts">
import { EditorTablesDataTable } from '#components'
import type { TableComponent } from '~/types'

definePageMeta({
  label: 'Editor: Table',
  layout: 'details'
})

/**
 * Edition
 */

const tableEditionStore = useTableEditionStore()
const { selectedTable, tableData, hasDocuments, hasData, selectedTableDocument, editableTableRef } = storeToRefs(tableEditionStore)

const componentMapping: Record<TableComponent, Component> = {
  'data-table': EditorTablesDataTable,
  'graph-table': EditorTablesDataTable
}

const displayComponent = computed(() => isDefined(editableTableRef) ? componentMapping[editableTableRef.value.component] : undefined)

/**
 * Page refreshing
 */

useEditorPageRefresh(selectedTable)

/**
 * Websocket
 */

const { wsObject } = useTableWebocketManager(selectedTable, selectedTableDocument)
wsObject.open()

const [isLoading, toggleIsLoading] = useToggle(true)
const { stringify } = useWebsocketMessage()

watchDebounced(selectedTableDocument, (newValue) => {
  if (isDefined(newValue)) {
    toggleIsLoading(false)
    wsObject.send(
      stringify({
        action: 'load_document_data',
        document_uuid: newValue.document_uuid
      })
    )
  }
}, { debounce: 1000, immediate: true })

/**
 * Provides
 */

provide('hasData', hasData)
provide('tableData', tableData)
provide('hasDocuments', hasDocuments)
provide('editableTableRef', editableTableRef)
provide('selectedTable', selectedTable)
provide('selectedTableDocument', selectedTableDocument)

console.log('editableTableRef', editableTableRef.value)
</script>
