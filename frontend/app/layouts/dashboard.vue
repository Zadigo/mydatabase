<template>
  <section id="site">
    <base-navbar />
    <base-sidebar :items="items" />

    <main class="ps-[calc(var(--sidebar-width)+1rem)] pe-5 mt-[calc(var(--navbar-min-height)+2rem)] mb-10">
      <slot />
    </main>
  </section>
</template>

<script setup lang="ts">
const items = [
  {
    name: 'Projects',
    to: '/databases',
    icon: 'i-fa7-regular:home'
  },
  {
    name: 'Integrations',
    to: '/integrations',
    icon: 'i-fa7-solid:plug'
  },
  {
    name: 'Organization settings',
    to: '/settings',
    icon: 'i-fa7-solid:cog'
  }
]
</script>
