<template>
  <q-page padding>
    <div class="row">
      <h1 class="text-h3">Home</h1>
    </div>

    <div class="row">
      <q-card style="width: 100%;">
        <q-card-section class="q-gutter-md q-px-md">
          <div class="row q-flex justify-between">
            <q-input v-model="search" placeholder="Search slides..." standout="bg-grey-1" style="width: 30%;" clearable></q-input>
            <q-btn color="primary" @click="showNewSlideModal = true">
              Create slide
            </q-btn>
          </div>
        </q-card-section>

        <q-separator dark />

        <!-- Slides -->
        <q-card-section>
          <q-list bordered separator>
            <q-item v-for="slide in searchedSlides" :key="slide.slide_id" class="q-pa-md">
              <q-item-section avatar>
                <q-avatar :color="slide.access === 'Public' ? 'green' : 'danger'" text-color="white">
                  <span v-if="slide.access === 'Public'">Pu</span>
                  <span v-else>Pr</span>
                </q-avatar>
              </q-item-section>

              <q-item-section>
                <router-link :to="{ name: 'slide', params: { id: slide.slide_id } }">
                  {{ slide.name }}
                </router-link>
              </q-item-section>

              <q-item-section side>
                <q-btn color="primary" flat>
                  Menu

                  <q-menu>

                  </q-menu>
                </q-btn>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
    </div>

    <q-dialog v-model="showNewSlideModal" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">New slide</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input v-model="requestData.name" :rules="[maxLength]" placeholder="Name" standout="bg-grey-1" clearable></q-input>
          <q-toggle v-model="newSlideAccess" size="xl" label="Private slide" icon="lock" />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn v-close-popup color="primary" flat label="Cancel" />
          <q-btn color="primary" label="Save" @click="handleCreateSlide" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import _ from 'lodash'
import { useSlides } from '../stores/slides'
import { useDataSources } from '../stores/connections'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'
import { useRules } from '../composables/rules'
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'HomePage',
  setup () {
    const { maxLength } = useRules()
    const notifications = useQuasar()
    const slidesStore = useSlides()
    const { slides } = storeToRefs(slidesStore)
    const dataSourcesStore = useDataSources()
    const { dataSources } = storeToRefs(dataSourcesStore)
    const showNewSlideModal = ref(false)
    const newSlideAccess = ref(false)
    const search = ref(null)
    const requestData = ref({
      name: null,
      access: 'Public'
    })
    return {
      search,
      notifications,
      slidesStore,
      dataSources,
      newSlideAccess,
      slides,
      showNewSlideModal,
      requestData,
      maxLength
    }
  },
  computed: {
    searchedSlides () {
      // Returns the slides which names match
      // the string withing the search value
      if (this.search && this.search !== "") {
        return _.filter(this.slides, (item) => {
          return (
            item.name.includes(this.search) ||
            item.name.toLowerCase().includes(this.search)
          )
        })
      } else {
        return this.slides
      }
    }
  },
  watch: {
    newSlideAccess (n) {
      if (n) {
        this.requestData.access = 'Private'
      } else {
        this.requestData.access = 'Public'
      }
    }
  },
  beforeMount () {
    this.requestSlides()
  },
  methods: {
    async requestSlides () {
      // Returns all the slides that were created
      // by the current user
      try {
        const response = await this.$api.get('/slides')
        const responseDataSources = await this.$api.get('/sheets')
        this.dataSources = responseDataSources.data
        this.slidesStore.$patch((state) => {
          state.slides = response.data
        })
      } catch (error) {
        // Pass
      }
    },
    async handleCreateSlide () {
      // Creates a new slide for the current user
      try {
        const response = await this.$api.post('slides/create', this.requestData)
        this.slidesStore.slides.push(response.data)
        this.notifications.notify({
          message: 'New slide created',
          color: 'green'
        })
        this.showNewSlideModal = false
      } catch (error) {
        console.error(error)
        this.notifications.notify({
          message: 'Slide could not be created',
          color: 'warning'
        })
      }
    }
  }
})
</script>
