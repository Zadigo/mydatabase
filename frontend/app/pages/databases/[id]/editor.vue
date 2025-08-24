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

        <nuxt-skeleton v-else class="h-10 w-10" />
      </template>

      <!-- Component -->
      <component :is="displayComponent" />
    </nuxt-card>

    <!-- Modals -->
    <editor-modals-edit-table v-model="showEditTableDrawer" />
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Editor: Table',
  layout: 'details'
})

const tableEditorStore = useTableEditionStore()
const { selectedTable, tableData, hasData } = storeToRefs(tableEditorStore)

const { displayComponent, editableTableRef, showEditTableDrawer, toggleEditTableDrawer } = useTable(selectedTable)

provide('tableData', tableData)
provide('hasData', hasData)
provide('editableTableRef', editableTableRef)
</script>
