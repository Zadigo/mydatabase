<template>
  <section class="flex flex-col items-center">
    <!-- Navbar -->
    <lazy-hero-nav hydrate-on-idle />
    
    <a href="https://prebuiltui.com" class="flex items-center gap-2 bg-indigo-100 rounded-full p-1 pr-3 text-sm mt-23">
      <span class="bg-indigo-600 text-white text-xs px-3 py-1 rounded-full">
        NEW
      </span>

      <p class="flex items-center gap-2 text-indigo-600">
        <span class='text-sm'>Try 30 days free trial option</span>
        <svg class="mt-px" width="6" height="9" viewBox="0 0 6 9" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="m1 1 4 3.5L1 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </p>
    </a>
  
    <h1 class="text-center text-slate-800 md:text-5xl/16 font-bold max-w-3xl leading-tight bg-clip-text my-2.5 px-4">
      Reliable automation to boost your team’s efficiency
    </h1>

    <p class="text-center text-base text-gray-600 max-w-md px-4">
      Toutes vos données au même endroit. Gérez vos projets, vos tâches et vos équipes avec une seule plateforme.
    </p>
    
    <div class="flex items-center gap-4 mt-5 justify-center z-1">
      <nuxt-link to="/auth/waitlist" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-md cursor-pointer">
        Get Started
      </nuxt-link>

      <nuxt-link to="/auth/waitlist" class="flex items-center gap-2 text-indigo-600 border border-indigo-600 hover:bg-indigo-50/50 px-6 py-3 rounded-md active:scale-95 transition cursor-pointer">
        En savoir plus
      </nuxt-link>
    </div>
  
    <div class="relative mt-12 w-full max-w-4xl px-4">
      <div class="pointer-events-none absolute -top-20 left-1/2 -translate-x-1/2 w-full h-full bg-[#d7bef4] blur-[100px] opacity-70 z-0"></div>
      <nuxt-img class="relative z-1 w-full object-cover object-top" src="https://assets.prebuiltui.com/components/hero-section/hero-dashImage2.png" alt="dashboard" />
    </div>
    
  </section>
</template>

<script lang="ts" setup>
</script>
