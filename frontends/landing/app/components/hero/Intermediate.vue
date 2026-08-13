<template>
  <section id="intermediate" class="p-20 bg-blue-100">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-4xl font-bold text-center mb-10">
        Gérez des centaines de comptes en toute sécurité <br/> <span class="text-blue-300">sur un seul ordinateur</span>
      </h2>
  
      <div class="grid grid-cols-2 gap-4">
        <motion :preset="VueUseMotions.PopVisibleOnce" :delay="100">
          <div class="overflow-hidden rounded-xl">
            <nuxt-img :src="faker.image.url({ height: 800 })" class="w-full" alt="Avatar" />
          </div>
        </motion>
          
        <div tag="div" class="p-10 flex flex-col justify-center">
          <div v-for="(item, idx) in items" :key="idx" class="mb-10">
            <motion :preset="VueUseMotions.SlideVisibleOnceLeft">
              <div class="flex items-start gap-4">
                <div class="rounded-full bg-white h-8 w-8 flex items-center justify-center">
                  <icon name="i-lucide-link" />
                </div>
                
                <div>
                  <p class="text-lg font-bold mb-2">
                    {{ item.title }}
                  </p>
    
                  <p>
                    {{ item.description }}
                  </p>
                </div>
              </div>
            </motion>
          </div>
        </div>
      </div>

      <div class="w-full flex justify-center">
        <u-button to="/auth/waitlist" size="xl" class="mt-10">
          S'inscrire à la liste d'attente
          <icon name="i-lucide-arrow-right" />
        </u-button>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { faker } from '@faker-js/faker'

const items = [
  {
    title: "Connectez Lemlist, Airtable, votre CRM et bien d'autres.",
    description: 'Lorélie se branche directement sur vos outils existants via OAuth ou clé API — aucune configuration technique nécessaire.'
  },
  {
    title: 'Unifiez toutes vos données en une seule base.',
    description: "Vos données sont fusionnées et structurées automatiquement, avec une synchronisation continue à mesure qu'elles évoluent dans vos outils sources."
  },
  {
    title: 'Exposez-les à votre LLM en un clic.',
    description: "Lorélie génère un serveur MCP prêt à l'emploi, connectable directement à Claude, ChatGPT ou tout autre client compatible — sans avoir à coder de connecteur."
  }
]
</script>
