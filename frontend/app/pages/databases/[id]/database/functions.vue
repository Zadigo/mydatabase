<template>
  <section id="database-functions">
    Database functions
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Database functions',
  layout: 'details'
})

const dbStore = useDatabasesStore()
const { currentAside } = storeToRefs(dbStore)

currentAside.value = 'database-aside'

onUnmounted(() => {
  currentAside.value = null
})
</script>
