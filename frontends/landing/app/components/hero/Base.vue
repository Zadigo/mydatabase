<template>
  <section class="flex flex-col items-center relative">
    <!-- Navbar -->
    <lazy-hero-nav hydrate-on-idle />
    
    <a href="https://prebuiltui.com" class="flex items-center gap-2 bg-blue-100 rounded-full p-1 pr-3 text-sm mt-23">
      <span class="bg-blue-600 text-white text-xs px-3 py-1 rounded-full">
        NEW
      </span>

      <p class="flex items-center gap-2 text-blue-600">
        <span class='text-sm'>Try 30 days free trial option</span>
        <svg class="mt-px" width="6" height="9" viewBox="0 0 6 9" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="m1 1 4 3.5L1 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </p>
    </a>
    
    <h1 class="text-center text-blue-950 md:text-5xl/16 font-bold max-w-3xl leading-tight bg-clip-text my-2.5 px-4">
      Reliable automation to boost your team’s efficiency
    </h1>

    <p class="text-center text-base text-blue-900 max-w-md px-4">
      Toutes vos données au même endroit. Gérez vos projets, vos tâches et vos équipes avec une seule plateforme.
    </p>
    
    <div class="flex items-center gap-4 mt-5 justify-center z-1">
      <u-button to="/auth/waitlist" size="xl">
        Get Started
      </u-button>

      <u-button to="/auth/waitlist" variant="outline" size="xl">
        En savoir plus
      </u-button>
    </div>
  
    <div class="relative mt-12 w-full max-w-4xl px-4">
      <div class="pointer-events-none absolute -top-20 left-1/2 -translate-x-1/2 w-full h-full bg-blue-50 blur-[100px] opacity-70 z-0"></div>
      <motion :preset="VueUseMotions.Pop" :delay="0">
        <nuxt-img class="relative z-1 w-full object-cover object-top" src="https://assets.prebuiltui.com/components/hero-section/hero-dashImage2.png" alt="dashboard" />
      </motion>
    </div>
  </section>
</template>

<script lang="ts" setup>
</script>
