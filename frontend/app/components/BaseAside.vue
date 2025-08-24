<template>
  <aside id="base-aside" class="fixed top-(--navbar-min-height) left-(--sidebar-width) h-screen bg-gray-100 w-64 border-r border-gray-200">
    <div class="p-5">
      <h2 class="text-lg font-semibold">
        Table editor
      </h2>

      <nuxt-separator class=" mt-2 mb-5" />

      <editor-aside-links v-if="currentAside==='editor-aside'" />
      <database-aside-links v-else-if="currentAside==='database-aside'" />
    </div>
  </aside>
</template>

<script setup lang="ts">
const dbStore = useDatabasesStore()
const { currentAside } = storeToRefs(dbStore)
</script>
