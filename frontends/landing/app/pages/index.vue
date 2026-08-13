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
import { useBusinessDetails } from '~/composables/business'
import type { PageTitleOrDescription } from '~/types'

onMounted(() => {
  document.querySelector('body')?.classList.add('bg-blue-50')
})

onUnmounted(() => {
  document.querySelector('body')?.classList.remove('bg-blue-50')
})

/**
 * SEO
 */

const { get } = useBusinessDetails()

const i18n = useI18n()

const titles: PageTitleOrDescription<typeof i18n.locale.value> = {
  fr: "Plateforme de gestion de données",
  en: 'Data management platform'
}

const descriptions: PageTitleOrDescription<typeof i18n.locale.value> = {
  fr: "Connectez tous vos outils, unifiez vos données, et donnez-y accès à votre LLM préféré — sans écrire une ligne de code",
  en: "Connect all your tools, unify your data, and give access to your favorite LLM — without writing a single line of code"
}

const url = useRequestURL()

useSeoMeta({
  title: titles[i18n.locale.value],
  description: descriptions[i18n.locale.value],
  author: get('legalName'),
  twitterDescription: descriptions[i18n.locale.value],
  twitterCard: 'summary_large_image',
  ogTitle: titles[i18n.locale.value],
  ogDescription: descriptions[i18n.locale.value],
  ogUrl: url.href
})

if (import.meta.env.NODE_ENV !== 'test') {
  defineOgImage('NuxtSeoTakumi', {
    title: titles[i18n.locale.value],
    description: descriptions[i18n.locale.value]
  })
}
</script>
