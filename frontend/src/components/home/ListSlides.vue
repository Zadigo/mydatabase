<template>
  <q-list bordered separator>
    <q-item v-for="slide in searchedSlides" :key="slide.id" clickable v-ripple>
      <router-link :to="{ name: 'slide', params: { id: slide.id } }">
        {{ slide.name }}
      </router-link>

      <!-- <v-menu>
        <template v-slot:activator="{ props }">
          <q-btn color="light" v-bind="props" variant="tonal" @click="selectedSlide = slide">
            <font-awesome-icon :icon="['fas', 'ellipsis-vertical']" />
          </q-btn>
        </template>

        <v-list>
          <v-list-item v-for="index in 4" :key="index" :value="index">
            <v-list-item-title>{{ index }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu> -->
    </q-item>
  </q-list>
</template>

<script setup lang="ts">
import { useStorage } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { api } from 'src/boot/axios'
import { useSlides } from 'src/stores/slides'
import { computed } from 'vue'

import type { Slide } from 'src/types'

const props = defineProps({
  search: {
    type: String,
    default: ''
  }
})


const slidesStore = useSlides()
const { slides } = storeToRefs(slidesStore)

const cachedSlides = useStorage<Slide[]>('slides', [])

const searchedSlides = computed(() => {
  if (props.search && props.search !== '') {
    return slides.value.filter((slide) => {
      return (
        slide.name.toLowerCase() === props.search ||
        slide.name.toLowerCase().includes(props.search)
      )
    })
  } else {
    return slides.value
  }
})

/**
 * Get all the user's slides 
 */
async function getSlides() {
  try {
    const response = await api.get<Slide[]>('/api/v1/slides')
    cachedSlides.value = response.data
    slides.value = cachedSlides.value
  } catch (e) {
    console.log(e)
  }
}

await getSlides()
</script>
