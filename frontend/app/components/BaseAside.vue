<template>
  <aside id="base-aside" class="fixed top-(--navbar-min-height) left-(--sidebar-width) h-screen bg-gray-100 w-64 border-r border-gray-200">
    <div class="p-5">
      <h2 class="text-lg font-semibold">
        Table editor
      </h2>

      <nuxt-separator class=" mt-2 mb-5" />

      <editor-aside-links v-if="route.meta.title && route.meta.title.startsWith('Editor:')" />
      <database-aside-links v-else-if="route.meta.title && route.meta.title.startsWith('Database:')" />
      <settings-project-aside-links v-else-if="route.meta.title && route.meta.title.startsWith('Settings:')" />
    </div>
  </aside>
</template>

<script setup lang="ts">
const route = useRoute()
</script>
