<template>
  <section id="database-tables">
    Database tables
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Database tables',
  layout: 'details'
})

const dbStore = useDatabasesStore()
const { currentAside } = storeToRefs(dbStore)

currentAside.value = 'database-aside'

onUnmounted(() => {
  currentAside.value = null
})
</script>
