<template>
  <section id="signup">
    <u-card class="rounded-lg max-w-sm mx-auto bg-gray-50 border border-gray-200">
      <div class="py-4 flex justify-center">
        <nuxt-link to="/">
          <nuxt-img src="https://raw.githubusercontent.com/prebuiltui/prebuiltui/main/assets/dummyLogo/dummyFavicon.svg" alt="icon" width="45" height="45" loading="lazy" />
        </nuxt-link>
      </div>

      <h1 class="mb-4 text-center text-2xl font-semibold">
        Rejoindre la liste d'attente
      </h1>

      <form @submit.prevent>
        <div class="mb-4">
          <label for="email" class="mb-1 block text-sm text-gray-400">Nom</label>
          <input type="email" id="email" placeholder="name@example.com" autocomplete="email" class="py-2 w-full rounded border border-gray-300 bg-slate-100 px-2 text-center text-gray-400 placeholder-[#7f8c8d] focus:ring-2 focus:ring-indigo-500 focus:outline-none" />
        </div>
        
        <div class="mb-4">
          <label for="email" class="mb-1 block text-sm text-gray-400">Prénom</label>
          <input type="email" id="email" placeholder="name@example.com" autocomplete="email" class="py-2 w-full rounded border border-gray-300 bg-slate-100 px-2 text-center text-gray-400 placeholder-[#7f8c8d] focus:ring-2 focus:ring-indigo-500 focus:outline-none" />
        </div>

        <div class="mb-4">
          <label for="email" class="mb-1 block text-sm text-gray-400">Entreprise</label>
          <input type="email" id="email" placeholder="name@example.com" autocomplete="email" class="py-2 w-full rounded border border-gray-300 bg-slate-100 px-2 text-center text-gray-400 placeholder-[#7f8c8d] focus:ring-2 focus:ring-indigo-500 focus:outline-none" />
        </div>
        
        <div class="mb-4">
          <label for="email" class="mb-1 block text-sm text-gray-400">Email</label>
          <input type="email" id="email" placeholder="name@example.com" autocomplete="email" class="py-2 w-full rounded border border-gray-300 bg-slate-100 px-2 text-center text-gray-400 placeholder-[#7f8c8d] focus:ring-2 focus:ring-indigo-500 focus:outline-none" />
        </div>
        
        <u-button size="xl" block>
          Rejoindre
        </u-button>
      </form>

      <p class="mt-8 text-center text-sm text-gray-400">
        By clicking on sign in, you agree to our
        <a href="#" class="underline">Terms of Service</a> and <a href="#" class="underline">Privacy Policy</a>.
      </p>
    </u-card>
  </section>
</template>

<script lang="ts" setup>
definePageMeta({
  layout: 'authentication',
})
</script>
