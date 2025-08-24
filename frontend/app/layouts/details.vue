<template>
  <section id="site">
    <base-navbar />
    <base-sidebar :items="items" />

    <main class="ps-[calc(240px+1rem)] pe-5 mt-[calc(42px+2rem)] mb-10">
      <slot />
    </main>
  </section>
</template>

<script setup lang="ts">
const items = [
  {
    name: 'Overview',
    to: '/databases',
    icon: 'i-fa7-regular:home'
  },
  {
    name: 'Table editor',
    to: '/integrations',
    icon: 'i-fa7-solid:table'
  },
  {
    separator: true
  },
  {
    name: 'Database',
    to: '/integrations',
    icon: 'i-fa7-solid:database'
  },
  {
    name: 'Project settings',
    to: '/settings',
    icon: 'i-fa7-solid:cog'
  }
]
</script>
