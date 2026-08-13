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
                  <p class="text-lg font-semibold mb-2">
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
