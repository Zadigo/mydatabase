<template>
  <section :class="{ 'no-sidebar': $route.name === 'slide' }" class="dashboard">
    <div class="sidebar-overlay" />

    <!-- Header -->
    <BaseHeader />

    <!-- Main -->
    <main>
      <div :class="bodyClasses" class="pt-4">
        <router-view />
      </div>
    </main>

    <transition name="pop">
      <button v-if="!arrivedState.top" id="back-to-top" class="btn btn-primary btn-floating" type="button" @click="scrollToTop">
        <IconBase name="fa-solid:arrow-up" />
      </button>
    </transition>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
// import { scrollToTop } from '../composables/utils'
import { useScroll } from '@vueuse/core'
import { useSlides } from 'src/stores/slides'
import { storeToRefs } from 'pinia'
import { useRoute } from 'vue-router'

import BaseHeader from '@/components/dashboard/BaseHeader.vue'

// import NavItem from './bootstrap/nav/NavItem.vue'

const slidesStore = useSlides()

const route = useRoute()
const { blockSelected, activeSidebarComponent } = storeToRefs(slidesStore)

const target = ref<HTMLElement>()
const { y, arrivedState } = useScroll(target)

const bodyClasses = computed(() => {
  return [
    {
      'container-fluid': route.name === 'slide_view',
      'container': route.name !== 'slide_view'
    }
  ]
})

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  target.value = window.document
  document.querySelector('.dashboard').classList.add('bg-light')
})
</script>
