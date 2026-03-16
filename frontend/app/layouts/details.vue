<template>
  <section id="site" class="relative">
    <!-- Navbar -->
    <base-navbar />

    <!-- Sidebar -->
    <base-sidebar :items="items" />

    <!-- Websocket Alerts -->
    <!-- ms-[calc(var(--sidebar-width)+20rem)] -->
    <div v-if="!isConnected" class="bg-error-500 w-full p-5 mt-(--navbar-min-height) text-slate-50 text-light">
      Disconnected from server
      <nuxt-button @click="() => { wsObject.open() }">
        Reconnect
      </nuxt-button>
    </div>

    <main class="not-has-[#base-aside]:ps-[calc(var(--sidebar-width)+1rem)] has-[#base-aside]:ps-[calc(var(--sidebar-width)+255px+1rem)] pe-5 mt-[calc(var(--navbar-min-height)+2rem)] mb-10 relative">
      <!-- Aside -->
      <base-aside v-if="hasAside" />

      <!-- Content -->
      <slot />
    </main>

    <dev-only>
      <dev-container />
    </dev-only>
  </section>
</template>

<script setup lang="ts">
import { useTableWebocketManager } from '~/composables/use/tables'

const dbStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(dbStore)

/**
 * Aside logic
 */

const route = useRoute()

const hasAside = computed(() => {
  return route.meta.label && (
    route.meta.label.startsWith('Database:') || 
    route.meta.label.startsWith('Editor:') || 
    route.meta.label.startsWith('Settings:')
  )
})

const { id } = useRoute().params as { id: string }
dbStore.routeId = Number(id)

const items = [
  {
    name: 'Overview',
    to: `/databases/${currentDatabase.value?.id}`,
    icon: 'i-lucide-home',
    isAlpha: false
  },
  {
    name: 'Table editor',
    to: `/databases/${currentDatabase.value?.id}/editor`,
    icon: 'i-lucide-table',
    isAlpha: false
  },
  {
    separator: true
  },
  {
    name:'Integrations',
    to: `/databases/${currentDatabase.value?.id}/integrations`,
    icon: 'i-lucide-plug',
    isAlpha: true
  },
  {
    name: 'Database',
    to: `/databases/${currentDatabase.value?.id}/database`,
    icon: 'i-lucide-database',
    isAlpha: false
  },
  {
    name: 'Project settings',
    to: `/databases/${currentDatabase.value?.id}/settings`,
    icon: 'i-lucide-cog',
    isAlpha: false
  }
]

onUnmounted(() => {
  dbStore.routeId = null
})

/**
 * Websocket
 */

const tableEditionStore = useTableEditionStore()
const { selectedTable, selectedTableDocument } = storeToRefs(tableEditionStore)

const { wsObject, isConnected } = useTableWebocketManager(selectedTable, selectedTableDocument)
</script>
