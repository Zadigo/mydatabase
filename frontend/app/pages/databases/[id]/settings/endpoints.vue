<template>
  <section id="database-endpoints" class="max-w-5xl mx-auto space-y-2">
    <header>
      <h3 class="font-bold">Endpoints</h3>
      <nuxt-button @click="() => { toggleShowModal() }">
        Add Endpoint
      </nuxt-button>

      <!-- Endpoints -->
      <div class="space-y-2">
        <settings-project-endpoint-block v-for="endpoint in endpoints" :key="endpoint.id" :endpoint="endpoint" />
      </div>
    </header>

    <!-- Modals -->
    <settings-project-modals-create-endpoint />
  </section>
</template>

<script setup lang="ts">
import { useDatabaseEndpoints } from '~/composables/use/databases'

definePageMeta({
  title: 'Settings: Home',
  layout: 'details'
})

/**
 * Endpoints
 */

const { endpoints, toggleShowModal } = useDatabaseEndpoints()
</script>
