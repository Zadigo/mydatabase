<template>
  <section id="database-endpoints" class="max-w-5xl mx-auto space-y-2">
    <header>
      <h3 class="font-bold">Endpoints</h3>
      <nuxt-button @click="() => { toggleShowModal() }">
        Add Endpoint
      </nuxt-button>

      
      <nuxt-card v-for="endpoint in endpoints" :key="endpoint.id">
        {{ endpoint }}

        <nuxt-button variant="subtle" color="error" icon="i-lucide-trash" />

        <div class="space-y-2">
          <nuxt-input v-model="endpoint.endpoint" class="w-full" />
  
          <nuxt-button-group class="w-full">
            <nuxt-input v-model="endpoint.endpoint_uuid" class="w-full" variant="subtle" :disabled="true" />
  
            <nuxt-tooltip text="Copy to clipboard">
              <nuxt-button color="neutral" variant="subtle" icon="i-lucide-clipboard" @click="proxyCopy(endpoint)" />
            </nuxt-tooltip>
          </nuxt-button-group>

          <div v-for="method in endpoint.methods" :key="method" class="p-3 rounded-lg bg-slate-50 border border-slate-100">
            <span class="font-bold">{{ method }}</span>
            <span class="font-light">/v1/{{ endpoint.endpoint }}</span>
            <nuxt-switch />
          </div>
  
          <!-- <nuxt-input v-model="endpoint.database_schema.name" icon="i-lucide-link" variant="subtle" class="w-full" :disabled="true" /> -->
        </div>
      </nuxt-card>
    </header>

    <!-- Modals -->
    <settings-project-modals-create-endpoint />
  </section>
</template>

<script setup lang="ts">
import { useDatabaseEndpoints } from '~/composables/use/databases'
import type { DatabaseEndpoint } from '~/types/databases/endpoints'

definePageMeta({
  title: 'Settings: Home',
  layout: 'details'
})

/**
 * Endpoints
 */

const { endpoints, toggleShowModal } = useDatabaseEndpoints()

function proxyCopy(endpoint: DatabaseEndpoint) {
  const { copy } = useClipboard({ source: endpoint.endpoint_uuid })
  copy()
}
</script>
