<template>
  <section id="home">
    Home Page
    
    <nuxt-link to="/databases">Go to Databases</nuxt-link>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Home page',
  layout: 'default'
})
</script>
