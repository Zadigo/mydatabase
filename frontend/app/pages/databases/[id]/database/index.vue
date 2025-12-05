<template>
  <section id="database-schema" class="bg-slate-50">
    <div id="tables-wrapper" ref="containerEl" class="tables-wrapper w-full h-screen z-50 relative">
      <database-tables-draggable v-for="table in availableTables" :key="table.id" :table="table" :container="containerEl" />
    </div>
  </section>
</template>

<script setup lang="ts">
/**
 * TODO: Page is in Bêta mode and needs work
 */

definePageMeta({
  label: 'Database: Schema',
  layout: 'details'
})

const dbStore = useDatabasesStore()
const { availableTables } = storeToRefs(dbStore)

const containerEl = useTemplateRef('containerEl')
</script>
