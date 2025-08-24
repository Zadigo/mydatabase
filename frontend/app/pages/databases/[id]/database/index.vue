<template>
  <section id="database-schema">
    Database schema
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Database schema',
  layout: 'details'
})

const dbStore = useDatabasesStore()
const { currentAside } = storeToRefs(dbStore)

currentAside.value = 'database-aside'

// onUnmounted(() => {
//   currentAside.value = null
// })
</script>
