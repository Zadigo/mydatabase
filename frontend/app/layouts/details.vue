<template>
  <section id="site">
    <base-navbar />
    <base-sidebar :items="items" />

    <main class="not-has-[#base-aside]:ps-[calc(var(--sidebar-width)+1rem)] has-[#base-aside]:ps-[calc(var(--sidebar-width)+255px+1rem)] pe-5 mt-[calc(var(--navbar-min-height)+2rem)] mb-10 relative">
      <!-- Aside -->
      <base-aside v-if="hasAside" />

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
    icon: 'i-lucide-home'
  },
  {
    name: 'Table editor',
    to: `/databases/${currentDatabase.value?.id}/editor`,
    icon: 'i-lucide-table'
  },
  {
    separator: true
  },
  {
    name:'Integrations',
    to: `/databases/${currentDatabase.value?.id}/integrations`,
    icon: 'i-lucide-plug'
  },
  {
    name: 'Database',
    to: `/databases/${currentDatabase.value?.id}/database`,
    icon: 'i-lucide-database'
  },
  {
    name: 'Project settings',
    to: `/databases/${currentDatabase.value?.id}/settings`,
    icon: 'i-lucide-cog'
  }
]

onUnmounted(() => {
  dbStore.routeId = null
})
</script>
