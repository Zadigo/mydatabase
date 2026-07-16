import tailwind from '@tailwindcss/vite'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({

  modules: [
    '@vueuse/nuxt',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/ui',
    '@pinia/nuxt',
    '@nuxt/test-utils/module',
    'pinia-plugin-persistedstate/nuxt',
    'nuxt-authentication',
    '@nuxt/eslint'
  ],
  ssr: true,
  devtools: { enabled: true },

  css: [
    '~/assets/css/tailwind.css'
  ],

  ui: {
    prefix: 'Nuxt'
  },

  runtimeConfig: {
    public: {
      prodDomain: process.env.NUXT_PUBLIC_PROD_DOMAIN,
      wsProdDomain: process.env.NUXT_PUBLIC_WS_PROD_DOMAIN
    }
  },

  routeRules: {
    '/': { prerender: true },
    '/databases/**': { ssr: false },
    '/presentations': { prerender: true },
    '/settings/**': { ssr: false },
    '/integrations': { ssr: false },
    '/login': { prerender: true }
  },
  compatibilityDate: '2025-07-15',

  vite: {
    plugins: [
      tailwind()
    ]
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  },

  nuxtAuthentication: {
    domain: process.env.NUXT_PUBLIC_PROD_DOMAIN
  }
})
