<template>
  <section id="home">
    <div class="container my-5">
      <div class="row">
        <div class="col-md-10 col-sm-12 offset-md-1">
          <div class="card mb-2">
            <div class="card-body">
              <h1 class="h2 m-0">
                Slides
              </h1>
            </div>
          </div>

          <div class="card shadow-md">
            <div class="card-header">
              <div class="d-flex justify-content-between align-items-center p-2">
                <!-- Search -->
                <input id="search-slides" v-model="search" class="w-50 p-3 form-input" placeholder="Search slides...">

                <button id="cta-new-slide" type="button" class="btn btn-primary" rounded @click="showCreateSlideModal = true">
                  <IconBase name="fa-solid:plus" class="me-2" />
                  Create slide
                </button>
              </div>
            </div>

            <div class="card-body">
              <suspense>
                <template #default>
                  <async-list-slides :search="search" />
                </template>

                <template #fallback>
                  Loading...
                </template>
              </suspense>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <teleport to="body">
      <v-dialog id="create-slide-modal" v-model="showCreateSlideModal" width="300">
        <v-card class="p-2">
          <v-card-text>
            <div class="row">
              <div class="col-12">
                <h2 class="h4 mb-3">
                  New Slide
                </h2>

                <input id="new-slide" v-model="newSlideRequestData.name" type="text" placeholder="Name" class="p-3 form-input" @keypress.enter="handleCreateNewSlide">
                <v-switch v-model="newSlideRequestData.private" class="my-2" label="Private slide" inset />
              </div>
            </div>
          </v-card-text>

          <v-card-actions class="justify-content-end">
            <button type="button" class="btn btn-info" @click="showCreateSlideModal=false">
              Cancel
            </button>
            <button type="button" class="btn btn-info" @click="handleCreateNewSlide">
              Validate
            </button>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>
  </section>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { api } from 'src/plugins'
import { useSlides } from 'src/stores/slides'
import { newSlideSchema, type NewSlide } from 'src/utils/schemas'
import { defineAsyncComponent, ref } from 'vue'

import type { Slide } from 'src/types'

const AsyncListSlides = defineAsyncComponent({
  loader: () => import('@/components/home/ListSlides.vue')
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
