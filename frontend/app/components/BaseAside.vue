<template>
  <aside id="base-aside" class="fixed top-(--navbar-min-height) left-(--sidebar-width) h-screen bg-gray-100 border-gray-200 dark:bg-slate-900 dark:border-slate-800 dark:text-slate-50 w-64 border-r">
    <div class="p-5">
      <h2 class="text-lg font-semibold">
        Table editor {{ asideName }}
      </h2>

      <nuxt-separator class=" mt-2 mb-5" />

      <editor-aside-links v-if="route.meta.label && route.meta.label.startsWith('Editor:')" />
      <database-aside-links v-else-if="route.meta.label && route.meta.label.startsWith('Database:')" />
      <settings-project-aside-links v-else-if="route.meta.label && route.meta.label.startsWith('Settings:')" />
    </div>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  asideName: 'editor' | 'database' | 'settings' | 'none'
}>()
const route = useRoute()
</script>
