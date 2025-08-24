<template>
  <section id="editor">
    Editor
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Project overview',
  layout: 'details'
})

const dbStore = useDatabasesStore()
const { currentAside } = storeToRefs(dbStore)

currentAside.value = 'editor-aside'

onUnmounted(() => {
  currentAside.value = null
})
</script>
