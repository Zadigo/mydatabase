<template>
  <nav class="fixed top-0 left-0 w-full bg-gray-50 px-5 py-2 min-h-(--navbar-min-height) border-b-1 border-gray-100 z-20">
    <div class="flex justify-between">
      <nuxt-breadcrumb :items="dbPageItems" />

      <div id="profile">
        <nuxt-dropdown-menu :items="dropdownItems" :content="{ align: 'start' }">
          <nuxt-avatar />
        </nuxt-dropdown-menu>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import type { BreadcrumbItem, DropdownMenuItem } from '@nuxt/ui'

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

const dropdownItems = ref<DropdownMenuItem[]>([
  {
    label: 'Profile',
    icon: 'i-lucide-user'
  },
  {
    label: 'Billing',
    icon: 'i-lucide-credit-card'
  },
  {
    label: 'Settings',
    icon: 'i-lucide-cog'
  }
])
</script>
