<template>
  <base-section-wrapper>
    <template #header>
      <!-- Header -->
      <base-page-card-header v-model="search" placeholder="Search connections" title="Connections" @create="() => { }" />
    </template>

    <div class="grid grid-cols-12 gap-2">
      <div v-for="connection in connections" :key="connection.name" class="col-span-4">
        <nuxt-card class="text-center cursor-pointer hover:shadow-lg transition">
          <nuxt-avatar :src="connection.logo" />
          
          <p class="font-bold">
            {{ connection.name }}
          </p>

          <p class="font-light my-1 text-sm">
            {{ connection.short_description }}
          </p>
        </nuxt-card>
      </div>
    </div>
  </base-section-wrapper>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Database: Connections',
  layout: 'details'
})

const search = ref<string>('')

interface ConnectionOptions {
  name: 'Zapier' | 'Make' | 'Google Sheets' | 'Airtable' | 'Supabase' | 'Excel' | 'N8N' | 'Notion'
  short_description: string
  logo: string
}

const connections: ConnectionOptions[] = [
  {
    name: 'Zapier',
    short_description: 'Connect your database to 5,000+ apps',
    logo: '/logos/zapier.jpeg'
  },
  {
    name: 'Make',
    short_description: 'Connect your database to 1,000+ apps',
    logo: '/logos/make.jpeg'
  },
  {
    name: 'Google Sheets',
    short_description: 'Connect your database to Google Sheets',
    logo: '/logos/sheets.png'
  },
  {
    name: 'Airtable',
    short_description: 'Connect your database to Airtable',
    logo: '/logos/airtable.png'
  },
  {
    name: 'Supabase',
    short_description: 'Connect your database to Supabase',
    logo: '/logos/supabase.jpeg'
  },
  {
    name: 'Excel',
    short_description: 'Connect your database to Excel',
    logo: '/logos/excel.png'
  },
  {
    name: 'N8N',
    short_description: 'Connect your database to N8N',
    logo: '/logos/n8n.png'
  },
  {
    name: 'Notion',
    short_description: 'Connect your database to Notion',
    logo: '/logos/notion.png'
  }
]
</script>
