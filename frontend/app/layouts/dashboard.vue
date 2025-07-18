<template>
  <section id="site">
    <!-- Header -->
    <header>
      <Navbar/>
      <Sidebar/>
    </header>
    
    <main class="px-5 ms-[calc(256px+1rem)] my-20">
      <slot />
    </main>
  </section>
</template>

<script setup lang="ts">
onMounted(() => {
  document.body.classList.add('bg-slate-100')
})
</script>
