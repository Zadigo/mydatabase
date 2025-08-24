<template>
  <nav class="fixed top-0 left-0 w-full bg-gray-50 px-5 py-2 border-b-1 border-gray-100 z-20">
    <div class="flex">
      <nuxt-breadcrumb :items="dbPageItems" />
    </div>
  </nav>
</template>

<script setup lang="ts">
import type { BreadcrumbItem } from '@nuxt/ui'

const dbStore = useDatabasesStore()

const baseItems = computed(() => {
  return [
    {
      icon: 'i-lucide-house',
      to: '/databases'
    },
    {
      label: 'My project',
      icon: 'i-lucide-box',
      to: '/databases'
    }
  ] as BreadcrumbItem[]
})

const dbPageItems = computed(() => {
  if (dbStore.currentDatabase) {
    return [
      ...baseItems.value,
      {
        label: dbStore.currentDatabase.name,
        icon: 'i-lucide-database',
        to: `/databases/${dbStore.currentDatabase.id}`
      }
    ] as BreadcrumbItem[]
  } else {
    return baseItems.value
  }
})
</script>
