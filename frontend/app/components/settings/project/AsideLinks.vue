<template>
  <div class="space-y-4">
    <ul v-if="currentDatabase" class="space-y-1">
      <p class="font-semibold mb-3">Management</p>

      <li v-for="item in endpoints" :key="item.name" class="w-full">
        <nuxt-link id="database-aside-link" :to="`/databases/${currentDatabase.id}/settings/${item.endpoint}`" class="block py-1 ps-3 text-sm rounded-md">
          {{ item.name }}
        </nuxt-link>
      </li>
    </ul>
    <div v-else class="space-y-2">
      <nuxt-skeleton v-for="i in 5" :key="i" class="w-full h-3" />
    </div>
  </div>
</template>

<script setup lang="ts">
const dbStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(dbStore)

const endpoints = [
  {
    name: 'General',
    endpoint: ''
  },
  {
    name: 'Endpoints',
    endpoint: 'endpoints'
  },
  {
    name: 'Api Keys',
    endpoint: 'api-keys'
  }
]
</script>

<style scoped>
[id$="aside-link"].router-link-exact-active {
  background-color: var(--color-gray-200);
}
</style>
