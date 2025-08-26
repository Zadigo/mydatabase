<template>
  <section id="project-settings" class="max-w-5xl mx-auto space-y-2">
    <header>
      <h3 class="font-bold">Project settings</h3>
    </header>

    <nuxt-card>
      <p class="font-bold">Project name</p>
      <nuxt-input />

      <p class="font-bold">Project ID</p>
      <nuxt-input />
    </nuxt-card>

    <nuxt-card>
      <nuxt-button>Restart your project</nuxt-button>
      <nuxt-button>Pause your project</nuxt-button>
    </nuxt-card>

    <nuxt-card>
      <p class="font-bold">Deleting this project will also remove your database.</p>
      <p>Make sure you have made a backup if you want to keep your data.</p>
      <nuxt-button>Delete project</nuxt-button>
    </nuxt-card>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Settings: Home',
  layout: 'details'
})
</script>
