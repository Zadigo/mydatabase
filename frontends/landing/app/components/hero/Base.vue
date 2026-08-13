<template>
  <section class="flex flex-col items-center">
    <!-- Navbar -->
    <lazy-hero-nav />
    
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
  
    <h1 class="text-center text-slate-800 text-4xl md:text-5xl/16 font-semibold max-w-3xl leading-tight bg-clip-text my-2.5 px-4">
      Reliable <span class='bg-linear-to-r from-indigo-600 to-pink-400 bg-clip-text text-transparent'>automation</span> to boost your team’s efficiency
    </h1>
    
    <p class="text-center text-base text-gray-600 max-w-md px-4">
      Workflows that never miss. automation that helps your team do more, effortlessly.
    </p>
    
    <div class="flex items-center gap-4 mt-5 justify-center z-1">
      <button class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-md cursor-pointer">Get Started</button>
      <button class="flex items-center gap-2 text-indigo-600 border border-indigo-600 hover:bg-indigo-50/50 px-6 py-3 rounded-md active:scale-95 transition cursor-pointer">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"/><path d="M20 2v4"/><path d="M22 4h-4"/><circle cx="4" cy="20" r="2"/>
        </svg>
        AI Features
      </button>
    </div>
  
    <div class="relative mt-12 w-full max-w-4xl px-4">
      <div class="pointer-events-none absolute -top-20 left-1/2 -translate-x-1/2 w-full h-full bg-[#d7bef4] blur-[100px] opacity-70 z-0"></div>
      <img class="relative z-1 w-full object-cover object-top" src="https://assets.prebuiltui.com/components/hero-section/hero-dashImage2.png" alt="dashboard" />
    </div>
    
  </section>
</template>

<script lang="ts" setup>
</script>
