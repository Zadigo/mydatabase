<template>
  <q-page>
    <div class="">
      <h1 class="">Slides</h1>

      <q-card>
        <q-card-section>
          <div class="flex justify-between items-center q-p-5">
            <!-- Search -->
            <q-input id="search-slides" v-model="search" class="w-50 p-3" placeholder="Search slides..." />

            <q-btn id="cta-new-slide" rounded @click="showCreateSlideModal = true">
              <IconBase icon="fa-solid:plus" class="me-2" />
              Create slide
            </q-btn>
          </div>
        </q-card-section>

        <q-card-section>
          <suspense>
            <template #default>
              <AsyncListSlides :search="search" />
            </template>

            <template #fallback>
              Loading...
            </template>
          </suspense>
        </q-card-section>
      </q-card>
    </div>

    <!-- Modals -->
    <q-dialog id="create-slide-modal" v-model="showCreateSlideModal" width="300">
      <q-card class="p-2">
        <q-card-section>
          <div class="row">
            <div class="col-12">
              <h2 class="h4 mb-3">New Slide</h2>
              <q-input id="new-slide" v-model="newSlideRequestData.name" type="text" placeholder="Name" class="p-3" @keypress.enter="handleCreateNewSlide" />
              <q-switch v-model="newSlideRequestData.private" class="my-2" label="Private slide" inset />
            </div>
          </div>
        </q-card-section>

        <q-card-actions class="justify-content-end">
          <q-btn @click="showCreateSlideModal = false">Cancel</q-btn>
          <q-btn variant="tonal" @click="handleCreateNewSlide">Validate</q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { api } from 'src/boot/axios'
import { useSlides } from 'src/stores/slides'
import { newSlideSchema, type NewSlide } from 'src/utils/schemas/slides'
import { defineAsyncComponent, ref } from 'vue'

import type { Slide } from 'src/types'

const AsyncListSlides = defineAsyncComponent({
  loader: () => import('src/components/home/ListSlides.vue')
})

const store = useSlides()
const { slides } = storeToRefs(store)

const search = ref<string>('')
// const selectedSlide = ref<Slide>(null)
const showCreateSlideModal = ref<boolean>(false)
const newSlideRequestData = ref<NewSlide>({
  name: '',
  private: false
})

/**
 * 
 */
async function handleCreateNewSlide() {
  try {
    newSlideSchema.parse(newSlideRequestData.value)

    const response = await api.post<Slide>('slides/create', newSlideRequestData.value)
    
    slides.value.push(response.data)
    
    showCreateSlideModal.value = false
    newSlideRequestData.value = { name: '', private: false }
  } catch (e) {
    console.log(e)
  }
}
</script>
