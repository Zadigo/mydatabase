<template>
  <q-list>
    <q-item v-for="slide in slides" :key="slide.id">
      <router-link :to="{ name: 'slide_view', params: { id: slide.id } }">
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
import { useStorage } from '@vueuse/core';
import { api } from 'src/boot/axios';
import type { Slide } from 'src/types'
import { PropType, computed } from 'vue';

const props = defineProps({
  search: {
    type: String,
    default: ''
  },
  slides: {
    type: Array as PropType<Slide[]>
  }
})

const cachedSlides = useStorage<Slide[]>('slides', [])

const searchedSlides = computed(() => {
  // R
  // criteria in the search parameter
  if (props.search) {
    return props.slides.filter((slide) => {
      return (
        slide.name.toLowerCase() === props.search.value ||
        slide.name.toLowerCase().includes(props.search.value)
      )
    })
  } else {
    return props.slides
  }
})

/**
 *  Get all the user's slides 
 */
async function getSlides () {
  try {
    const response = await api.get<Slide[]>('slides')
    cachedSlides.value = response.data
  } catch (e) {
    console.log(e)
  }
}

await getSlides()
</script>
