import tailwindcss from '@tailwindcss/vite'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,

  css: [
    '~/assets/css/main.css'
  ],
  ui: {
    prefix: 'Nuxt'
  },

  vite: {
    plugins: [
      tailwindcss()
    ]
  },

  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@nuxt/ui',
    '@pinia/nuxt',
    'pinia-plugin-persistedstate',
    '@vueuse/nuxt'
  ]
})