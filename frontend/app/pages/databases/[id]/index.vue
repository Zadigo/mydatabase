<template>
  <section id="tables">
    Project overview

    <nuxt-button :to="`/presentations/1`">
      Go to Presentation
    </nuxt-button>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Project overview',
  layout: 'details'
})
</script>
