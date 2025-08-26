<template>
  <section id="project-settings" class="max-w-5xl mx-auto space-y-2">
    <header>
      <h3 class="font-bold">Api Keys</h3>
    </header>

    <nuxt-card>
      <h3 class="text-bold text-2xl">
        Publishable key
      </h3>

      <nuxt-input v-model="publishableKey" :disabled="true" />
      <nuxt-button @click="() => { copyPublishableKey() }">
        <icon name="i-lucide-copy" />
      </nuxt-button>
    </nuxt-card>
    
    <nuxt-card>
      <h3 class="text-bold text-2xl">
        Secret key
      </h3>

      <nuxt-input v-model="secretKey" :disabled="true" />
      <nuxt-button @click="() => { copySecretKey() }">
        <icon name="i-lucide-copy" />
      </nuxt-button>
    </nuxt-card>
  </section>
</template>

<script setup lang="ts">
definePageMeta({
  title: 'Settings: Api Keys',
  layout: 'details'
})

const publishableKey = ref('cs_1234')
const secretKey = ref('cs_1234')

const { copy: copyPublishableKey } = useClipboard({ source: publishableKey })
const { copy: copySecretKey } = useClipboard({ source: secretKey })
</script>
