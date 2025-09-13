<template>
  <base-section-wrapper>
    <template #header>
      <!-- Header -->
      <base-page-card-header v-model="search" placeholder="Search connections" title="Connections" />
    </template>

    <!-- Tools -->
    <suspense>
      <database-connections-card @connect="showComponent" />
      
      <template #fallback>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          <nuxt-skeleton-loader v-for="n in 5" :key="n" class="h-32 w-full rounded-lg" />
        </div>
      </template>
    </suspense>

    <!-- Modal -->
    <nuxt-slideover v-model:open="showModal" class="min-w-6xs">
      <template #header>
        <h3 class="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100">
          Connect to
          {{ selectedTool }}
        </h3>
      </template>

      <template #body>
        <component :is="integrationComponent" />
      </template>
    </nuxt-slideover>
  </base-section-wrapper>
</template>

<script setup lang="ts">
import type { Nullable, IntegrationTool } from '~/types'
import GoogleSheets from '~/components/database/connections/GoogleSheets.vue'
import type { Component } from 'vue'

definePageMeta({
  title: 'Database: Connections',
  layout: 'details'
})

const search = ref<string>('')

function useConnections() {
  const [showModal, toggleModal] = useToggle()
  const selectedTool = ref<Nullable<IntegrationTool>>(null)
  const integrationComponent = ref<Nullable<Component>>(null)

  watchTriggerable(selectedTool, (tool) => {
    if (!tool) {
      integrationComponent.value = null
    } else {
      switch (tool) {
        case 'Google Sheets':
          integrationComponent.value = GoogleSheets
          break

        default:
          break
      }
    }
  })

  function showComponent(tool: IntegrationTool) {
    selectedTool.value = tool
    toggleModal()
  }

  return {
    showModal,
    selectedTool,
    integrationComponent,
    toggleModal,
    showComponent
  }
}

const { showComponent, integrationComponent, showModal, selectedTool } = useConnections()
</script>
