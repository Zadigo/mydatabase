<template>
  <section id="site">
    <base-navbar />
    <base-sidebar :items="items" />

    <main class="not-has-[#base-aside]:ps-[calc(var(--sidebar-width)+1rem)] has-[#base-aside]:ps-[calc(var(--sidebar-width)+255px+1rem)] pe-5 mt-[calc(var(--navbar-min-height)+2rem)] mb-10 relative">
      <!-- Aside -->
      <!-- v-if="hasAside && currentAside === 'editor-aside'" -->
      <base-aside />

      <!-- Content -->
      <slot />
    </main>
  </section>
</template>

<script setup lang="ts">
const dbStore = useDatabasesStore()
const { currentDatabase, currentAside } = storeToRefs(dbStore)

const hasAside = computed(() => currentAside.value !== null)

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
