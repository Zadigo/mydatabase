<template>
  <div class="grid grid-cols-12 gap-2">
    <div v-for="connection in connections" :key="connection.name" class="col-span-4">
      <nuxt-card class="cursor-pointer hover:shadow-lg transition" @click="emit('connect', connection.name)">
        <template #header>
          <div class="flex justify-end">
            <icon name="i-lucide-circle-check" class="text-green-500" />
          </div>
        </template>
        
        <div class="text-center">
          <nuxt-avatar :src="connection.logo" />
  
          <p class="font-bold mt-3 flex justify-center  gap-2 py-2">
            {{ connection.name }} 
            <nuxt-badge v-if="connection.beta" size="sm" variant="soft" color="warning">Bêta</nuxt-badge>
            <nuxt-badge v-if="connection.coming_soon" size="sm" variant="soft" color="info">Coming soon</nuxt-badge>
          </p>
  
          <p class="font-light my-1 text-sm">
            {{ connection.short_description }}
          </p>
        </div>
      </nuxt-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ConnectionOptions } from '~/types/databases/connections';

const connections: ConnectionOptions[] = [
  {
    name: 'Zapier',
    short_description: 'Connect your database to 5,000+ apps',
    logo: '/logos/zapier.jpeg',
    coming_soon: true,
    beta: false
  },
  {
    name: 'Make',
    short_description: 'Connect your database to 1,000+ apps',
    logo: '/logos/make.jpeg',
    coming_soon: true,
    beta: false
  },
  {
    name: 'Google Sheets',
    short_description: 'Connect your database to Google Sheets',
    logo: '/logos/sheets.png',
    coming_soon: false,
    beta: false
  },
  {
    name: 'Airtable',
    short_description: 'Connect your database to Airtable',
    logo: '/logos/airtable.png',
    coming_soon: true,
    beta: false
  },
  {
    name: 'Supabase',
    short_description: 'Connect your database to Supabase',
    logo: '/logos/supabase.jpeg',
    coming_soon: true,
    beta: false
  },
  {
    name: 'Excel',
    short_description: 'Connect your database to Excel',
    logo: '/logos/excel.png',
    coming_soon: true,
    beta: false
  },
  {
    name: 'N8N',
    short_description: 'Connect your database to N8N',
    logo: '/logos/n8n.png',
    coming_soon: true,
    beta: false
  },
  {
    name: 'Notion',
    short_description: 'Connect your database to Notion',
    logo: '/logos/notion.png',
    coming_soon: true,
    beta: false
  }
]

const emit = defineEmits<{ connect: [tool: ConnectionOptions['name']] }>()

/**
 * Active connections
 */

const { execute, data: activeConnections } = useFetch('/api/integrations', {
  method: 'GET',
  lazy: true
})

await execute()
</script>
