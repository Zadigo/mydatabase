<template>
  <section id="integrations">
    <div class="w-full border-b border-gray-200 pb-8 font-bold text-2xl">
      Integrations
    </div>

    <div class="grid grid-cols-6 gap-2 mt-10">
      <div class="col-span-6 space-x-2 py-5">
        <nuxt-button variant="subtle" rounded>All</nuxt-button>
        <nuxt-button variant="subtle" rounded>Automation</nuxt-button>
        <nuxt-button variant="subtle" rounded>Wrapper</nuxt-button>
        <nuxt-input class="w-45" icon="i-lucide-search" placeholder="Search" />
      </div>

      <nuxt-card v-for="integration in baseIntegrations" :key="integration.name" class="cursor-pointer transition-all ease-in-out hover:bg-gray-100">
        <p class="font-semibold text-md">{{ integration.name }}</p>
        <p class="font-light text-sm">Small description</p>
      </nuxt-card>
    </div>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  label: 'Integrations',
  layout: 'details'
})

const baseIntegrations = [
  {
    name: 'Airtable',
    icon: ''
  },
  {
    name: 'Redis',
    icon: ''
  },
  {
    name: 'Zapier',
    icon: ''
  },
  {
    name: 'Make',
    icon: ''
  },
  {
    name: 'Notion',
    icon: ''
  },
  {
    name: 'Supabase',
    icon: ''
  },
  {
    name: 'Slack',
    icon: ''
  },
  {
    name: 'Firebase',
    icon: ''
  },
  {
    name: 'Cal.com',
    icon: ''
  }
]
</script>
