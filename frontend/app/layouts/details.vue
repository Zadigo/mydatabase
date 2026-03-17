<template>
  <section id="site" class="relative">
    <!-- Navbar -->
    <base-navbar />

    <!-- Sidebar -->
    <base-sidebar :items="items" />

    <!-- Websocket Alerts -->
    <div v-if="!isConnected" class="bg-info-500/30 shadow-2xl space-y-2 flex-col w-auto h-auto rounded-2xl backdrop-blur-3xl fixed bottom-5 right-5 p-5 text-slate-50 z-50">
      <p>Disconnected from server</p>

      <nuxt-button class="self-end" variant="subtle" color="warning" @click="() => { wsObject.open() }">
        Reconnect
      </nuxt-button>
    </div>

    <main class="not-has-[#base-aside]:ps-[calc(var(--sidebar-width)+1rem)] has-[#base-aside]:ps-[calc(var(--sidebar-width)+255px+1rem)] pe-5 mt-[calc(var(--navbar-min-height)+2rem)] mb-10 relative">
      <!-- Aside -->
      <base-aside v-if="hasAside" :aside-name="asideName" />

      <!-- Content -->
      <slot />
    </main>

    <dev-only>
      <dev-container />
    </dev-only>
  </section>
</template>

<script setup lang="ts">
const dbStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(dbStore)

type AsideLinks = {
  name: string
  to: string
  icon: string
  isAlpha: boolean
}

type AsideSeparator = {
  separator: true
}

const props = defineProps<{
  asideName: 'editor' | 'database' | 'settings' | 'none'
}>()

/**
 * Aside logic
 */

const hasAside = computed(() => props.asideName !== 'none')

const { id } = useRoute().params as { id: string }
dbStore.routeId = Number(id)

const items: (AsideLinks | AsideSeparator)[] = [
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
