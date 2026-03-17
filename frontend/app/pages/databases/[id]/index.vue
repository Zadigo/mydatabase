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
  label: 'Project overview',
  layout: {
    name: 'details',
    props: {
      asideName: 'none'
    }
  }
})
</script>
