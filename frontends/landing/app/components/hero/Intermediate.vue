<template>
  <section id="intermediate" class="p-20">
    <div class="max-w-7xl mx-auto">
      <h2 class="text-4xl font-bold text-center mb-10">
        Gérez des centaines de comptes en toute sécurité <br/> <span>sur un seul ordinateur</span>
      </h2>
  
      <div class="grid grid-cols-2 gap-4">
        <div class="overflow-hidden rounded-xl">
          <nuxt-img :src="faker.image.url({ height: 300, width: 300 })" height="300" width="300" class="w-full h-auto" alt="Avatar" />
        </div>
          
        <div class="p-10 flex flex-col justify-center">
          <div v-for="(item, idx) in items" :key="idx" class="mb-10">
            <p class="text-lg font-semibold mb-2">
              {{ item.title }}
            </p>
            <p>
              {{ item.description }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts" setup>
import { faker } from '@faker-js/faker'

const items = [
  {
    title: 'Des comptes plus sûrs, avec moins de risques de suspension soudaine.',
    description: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Autem laborum omnis nihil officiis culpa. Molestias, provident sunt tempore in autem sint eum exercitationem, quo quasi rerum officiis excepturi incidunt expedita?'
  },
  {
    title: 'Gérez vos comptes efficacement',
    description: 'Avec notre solution, vous pouvez gérer des centaines de comptes en toute sécurité, réduisant ainsi les risques de suspension soudaine.'
  },
  {
    title: 'Optimisez votre temps',
    description: 'Notre plateforme vous permet de gérer vos comptes de manière efficace, vous faisant gagner un temps précieux.'
  }
]
</script>
