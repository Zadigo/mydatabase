<template>
  <div class="list-group">
    <a v-for="slide in searchedSlides" :key="slide.id" href="#" class="list-group-item p-3 d-flex justify-content-between align-items-center" @click.prevent>
      <router-link :to="{ name: 'slide', params: { id: slide.id } }">
        {{ slide.name }}
      </router-link>

      {{ searchedSlides }}

      <!-- <v-menu>
        <template #activator="{ props }">
          <button type="button" class="btn btn-primary" v-bind="props" variant="tonal" @click="selectedSlide = slide">
            <IconBase icon="fas-solid:ellipsis-vertical" />
          </button>
        </template>

        <v-list>
          <v-list-item v-for="index in 4" :key="index" :value="index">
            <v-list-item-title>{{ index }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu> -->
    </a>
  </div>
</template>

<script setup lang="ts">
import { useStorage } from '@vueuse/core'
import { storeToRefs } from 'pinia'
import { useSlides } from 'src/stores/slides'
import { computed } from 'vue'
import { api } from 'src/plugins'

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
        slide.name.toLowerCase() === props.search
        || slide.name.toLowerCase().includes(props.search)
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
