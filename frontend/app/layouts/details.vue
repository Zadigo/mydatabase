<template>
  <section id="site">
    <base-navbar />
    <base-sidebar :items="items" />

    <main class="ps-[calc(240px+1rem)] pe-5 mt-[calc(42px+2rem)] mb-10">
      <slot />
    </main>
  </section>
</template>

<script setup lang="ts">
const dbStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(dbStore)

const { id } = useRoute().params as { id: string }
dbStore.routeId = Number(id)

const items = [
  {
    name: 'Overview',
    to: `/databases/${currentDatabase.value?.id}`,
    icon: 'i-fa7-regular:home'
  },
  {
    name: 'Table editor',
    to: `/databases/${currentDatabase.value?.id}/editor`,
    icon: 'i-fa7-solid:table'
  },
  {
    separator: true
  },
  {
    name: 'Database',
    to: `/databases/${currentDatabase.value?.id}/database`,
    icon: 'i-fa7-solid:database'
  },
  {
    name: 'Project settings',
    to: `/databases/${currentDatabase.value?.id}/settings`,
    icon: 'i-fa7-solid:cog'
  }
]

onUnmounted(() => {
  dbStore.routeId = null
})
</script>
