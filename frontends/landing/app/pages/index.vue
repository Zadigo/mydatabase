<template>
  <section id="home">
    <!-- Hero -->
    <hero-base />

    <!-- Intermediate -->
    <lazy-hero-intermediate hydrate-on-visible />

    <!-- Product Grid -->
    <lazy-hero-product-grid hydrate-on-visible />
  </section>
</template>

<script lang="ts" setup>
onMounted(() => {
  document.querySelector('body')?.classList.add('bg-blue-50')
})

onUnmounted(() => {
  document.querySelector('body')?.classList.remove('bg-blue-50')
})
</script>
