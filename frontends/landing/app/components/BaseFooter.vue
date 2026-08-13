<template>
  <footer class="px-6 py-20 bg-primary-950 md:px-16 lg:px-24 xl:px-32">
    <div class="flex flex-col md:flex-row items-start justify-between gap-10 py-10 border-b border-blue-500/30 text-blue-100">
      <div>
        <nuxt-link to="/">
          <nuxt-img class="w-34 md:w-32" src="https://raw.githubusercontent.com/prebuiltui/prebuiltui/main/assets/dummyLogo/dummyLogoColored.svg" alt="dummyLogoColored" />
        </nuxt-link>

        <p class="max-w-102.5 mt-6">
          {{ FOOTER_DATA.description }}
        </p>
      </div>

      <div class="flex flex-wrap justify-between w-full md:w-[45%] gap-5">
        <div v-for="(section, index) in FOOTER_DATA.sections" :key="index">
          <h3 class="font-semibold text-base text-white md:mb-5 mb-2">
            {{ section.title }}
          </h3>

          <ul class="text-sm space-y-1">
            <li v-for="(link, idx) in section.links">
              <nuxt-link :to="link.to" class="hover:underline transition">
                {{ link.title }}
              </nuxt-link>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <p class="py-4 text-center text-sm md:text-base text-blue-100">
      Copyright <nuxt-time :datetime="new Date()" year="numeric" /> © PrebuiltUI All Right Reserved.
    </p>
  </footer>
</template>

<script lang="ts" setup>
</script>
