<template>
  <section id="home">
    <div class="container">
      <div class="row">
        <div class="col-md-10 col-sm-12 offset-md-1">
          <h1 class="h2 mb-4">Slides</h1>

          <base-card class="shadow-sm">
            <template #header>
              <div class="d-flex justify-content-between align-items-center p-2">
                <!-- Search -->
                <base-input id="search-slides" v-model="search" class="w-50 p-3" placeholder="Search slides..." />

                <base-button id="cta-new-slide" rounded @click="showCreateSlideModal = true">
                  <font-awesome-icon :icon="['fas', 'plus']" class="me-2" />
                  Create slide
                </base-button>
              </div>
            </template>

            <template #body>
              <div class="list-group">
                <a v-for="slide in searchedSlides" :key="slide.id" href class="list-group-item p-3 d-flex justify-content-between align-items-center" @click.prevent>
                  <router-link :to="{ name: 'slide_view', params: { id: slide.id } }">
                    {{ slide.name }}
                  </router-link>

                  <v-menu>
                    <template v-slot:activator="{ props }">
                      <v-btn color="light" v-bind="props" variant="tonal" @click="selectedSlide = slide">
                        <font-awesome-icon :icon="['fas', 'ellipsis-vertical']" />
                      </v-btn>
                    </template>

                    <v-list>
                      <v-list-item v-for="index in 4" :key="index" :value="index">
                        <v-list-item-title>{{ index }}</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </a>
              </div>
            </template>
          </base-card>
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
                <h2 class="h4 mb-3">New Slide</h2>
                <base-input id="new-slide" v-model="newSlideRequestData.name" type="text" placeholder="Name" class="p-3" @keypress.enter="handleCreateNewSlide" />
                <v-switch v-model="newSlideRequestData.private" class="my-2" label="Private slide" inset></v-switch>
              </div>
            </div>
          </v-card-text>
  
          <v-card-actions class="justify-content-end">
            <v-btn @click="showCreateSlideModal = false">Cancel</v-btn>
            <v-btn variant="tonal" @click="handleCreateNewSlide">Validate</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </teleport>
  </section>
</template>

<script>
import _ from 'lodash'

import { useSlides } from '../store/slides'
import { ref } from 'vue'
import { storeToRefs } from 'pinia'

import BaseCard from '../layouts/bootstrap/cards/BaseCard.vue'
import BaseInput from '../layouts/bootstrap/BaseInput.vue'
import BaseButton from '../layouts/bootstrap/buttons/BaseButton.vue'

export default {
  name: 'HomeView',
  components: {
    BaseCard,
    BaseInput,
    BaseButton
  },
  setup () {
    const store = useSlides()
    const { slides } = storeToRefs(store)

    const search = ref(null)
    const selectedSlide = ref(null)
    const showCreateSlideModal = ref(false)
    const newSlideRequestData = ref({
      name: null,
      private: false
    })

    return {
      search,
      selectedSlide,
      showCreateSlideModal,
      newSlideRequestData,
      slides
    }
  },
  computed: {
    searchedSlides () {
      // Returns the list of slides based on the
      // criteria in the search parameter
      if (this.search) {
        return _.filter(this.slides, (slide) => {
          return (
            slide.name.toLowerCase() === this.search ||
            slide.name.toLowerCase().includes(this.search) ||
            slide.name === this.search ||
            slide.name.includes(this.search)
          )
        })
      } else {
        return this.slides
      }
    }
  },
  created () {
    this.getSlides()
  },
  methods: {
    async getSlides () {
      // Get all the user's slides
      try {
        const response = await this.$http.get('slides')
        this.slides = response.data
        this.$session.create('slides', response.data)
      } catch (e) {
        console.log(e)
      }
    },
    async handleCreateNewSlide () {
      // Creates a new slide
      try {
        const response = await this.$http.post('slides/create', this.newSlideRequestData)
        this.$session.listPush('slides', response.data)
        this.slides.push(response.data)

        this.showCreateSlideModal = false
        this.requestDetails = { name: null, private: false }
      } catch (e) {
        console.log(e)
      }
    }
  }
}
</script>
