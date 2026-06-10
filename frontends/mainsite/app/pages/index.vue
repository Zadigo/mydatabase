<template>
  <section id="home">
    Home Page
    
    <nuxt-link to="/databases">Go to Databases</nuxt-link>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  label: 'Home page',
  layout: 'default'
})

console.log(useState('authTokens').value)
</script>
