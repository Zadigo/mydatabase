<template>
  <section id="editor">
    <nuxt-card>
      <template #header>
        selectedTable {{ selectedTable }}

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
      <component :is="displayComponent" v-if="hasData" />
      <template v-else>
        No data, no table
      </template>
    </nuxt-card>

    <!-- Modals -->
    <editor-modals-edit-table v-model="showModal" />
  </section>
</template>

<script setup lang="ts">
// import { useWebsocketMessage } from '~/composables/use'
import { EditorTablesDataTable } from '#components'
import { useEditorPageRefresh, useTableWebocketManager } from '~/composables/use/tables'
import type { TableComponent } from '~/types'

definePageMeta({
  title: 'Editor: Table',
  layout: 'details'
})

/**
 * Edition
 */

const tableEditionStore = useTableEditionStore()
const { selectedTable, tableData, hasDocuments, hasData, selectedTableDocument, editableTableRef, showModal } = storeToRefs(tableEditionStore)

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

/**
 * Provides
 */

provide('hasData', hasData)
provide('tableData', tableData)
provide('hasDocuments', hasDocuments)
provide('editableTableRef', editableTableRef)
provide('wsObject', wsObject)

console.log('editableTableRef', editableTableRef.value)
</script>
