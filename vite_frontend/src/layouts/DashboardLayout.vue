<template>
  <section :class="{ 'no-sidebar': $route.name === 'slide_view' }" class="dashboard">
    <div class="sidebar-overlay" />

    <!-- Header -->
    <header>
      <!-- Sidebar -->
      <nav v-if="$route.name !== 'slide_view'" id="sidebar" link="sidebar" class="collapse d-lg-block sidebar collapse bg-white">
        <div class="position-sticky">
          <keep-alive>
            <div class="list-group list-group-flush mx-3 mt-4">
              <router-link v-for="(link, i) in adminLinks" :key="i" :to="{ name: link.to }" class="list-group-item list-group-item-action py-2 ripple" aria-current="true">
                <font-awesome-icon :icon="['fas', `${link.icon}`]" class="me-3" />
                <span>{{ link.title }}</span>
              </router-link>
            </div>
          </keep-alive>
        </div>
      </nav>

      <!-- Navbar -->
      <nav id="main-navbar" class="navbar navbar-expand-lg navbar-light bg-white fixed-top">
        <div class="container-fluid">
          <button class="navbar-toggler" type="button" aria-controls="sidebarMenu" aria-expanded="false" aria-label="Toggle navigation">
            <i class="fas fa-bars" />
          </button>

          <router-link to="/" class="navbar-brand">
            <div class="fw-bold text-uppercase">
              Templates
            </div>
            <!-- <img src="https://mdbootstrap.com/img/logo/mdb-transaprent-noshadows.png" height="25" loading="lazy" alt="Image 4" /> -->
          </router-link>

          <ul class="navbar-nav ms-auto d-flex flex-row">
            <nav-item :to="{ name: 'home' }" link-name="Some link" />
          </ul>
        </div>
      </nav>
    </header>

    <!-- Main -->
    <main>
      <div :class="bodyClasses" class="pt-4">
        <router-view />
      </div>
    </main>

    <transition name="pop">
      <button v-if="!arrivedState.top" id="back-to-top" class="btn btn-primary btn-floating" type="button" @click="scrollToTop">
        <font-awesome-icon icon="fa-solid fa-arrow-up" />
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

const pageLinks = computed(() => {
  return [
    {
      title: 'Home',
      to: 'home',
      icon: 'house'
    }
  ]
})

const adminLinks = computed(() => {
  return [
    {
      title: 'Home',
      to: 'home',
      icon: 'house'
    },
    // {
    //   title: 'Connections',
    //   to: 'connections',
    //   icon: 'link'
    // }
    // {
    //   title: 'Integrations',
    //   to: 'integrations_view',
    //   icon: 'bolt-lightning'
    // },
    // {
    //   title: 'Settings',
    //   to: 'settings_view',
    //   icon: 'cog'
    // }
  ]
})

onMounted(() => {
  target.value = window.document
  document.querySelector('.dashboard').classList.add('bg-light')
})
</script>

<style scoped>
/* @import url('@/layouts/bootstrap/css/dashboard1.css');
.dashboard {
  height: 100%;
} */
</style>
