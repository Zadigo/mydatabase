<template>
  <section class="dashboard">
    <div class="sidebar-overlay"></div>

    <!-- Header -->
    <header>
      <!-- Sidebar -->
      <nav id="sidebar" link="sidebar" class="collapse d-lg-block sidebar collapse bg-white">
        <div v-if="(blockSelected && $route.name === 'slide_view') || $route.name === 'slide_view'" class="position-sticky">
          <component :is="activeSidebarComponent" />
        </div>
        
        <div v-else class="position-sticky">
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
            <i class="fas fa-bars"></i>
          </button>

          <router-link to="/" class="navbar-brand">
            <div class="fw-bold text-uppercase">Templates</div>
            <!-- <img src="https://mdbootstrap.com/img/logo/mdb-transaprent-noshadows.png" height="25" loading="lazy" alt="Image 4" /> -->
          </router-link>

          <ul class="navbar-nav ms-auto d-flex flex-row">
            <nav-item :to="{ name: 'home_view' }" link-name="Some link" />
          </ul>
        </div>
      </nav>
    </header>

    <!-- Main -->
    <main>
      <div :class="bodyClasses" class="container pt-4">
        <router-view></router-view>
      </div>
    </main>

    <transition name="pop">
      <button v-if="!arrivedState.top" id="back-to-top" class="btn btn-primary btn-floating" type="button" @click="scrollToTop">
        <font-awesome-icon icon="fa-solid fa-arrow-up" />
      </button>
    </transition>
  </section>
</template>

<script>
import { ref } from 'vue'
import { scrollToTop } from '../composables/utils'
import { useScroll } from '@vueuse/core'
import { useSlides } from '@/store/slides'
import { mapState } from 'pinia'

import ChartSidebar from '@/components/sidebar/ChartSidebar.vue'
import DefaultSlideSidebar from '@/components/sidebar/DefaultSlideSidebar.vue'
import NavItem from './bootstrap/nav/NavItem.vue'
import TableSidebar from '../components/sidebar/TableSidebar.vue'

export default {
  name: 'DashboardLayout',
  components: {
    ChartSidebar,
    DefaultSlideSidebar,
    NavItem,
    TableSidebar
  },
  props: {
    bodyClasses: {
      type: String,
      required: false
    }
  },
  setup () {
    const slidesStore = useSlides()
    const target = ref(null)
    const { y, arrivedState } = useScroll(target)

    return {
      target,
      scrollToTop,
      scrollY: y,
      arrivedState,
      slidesStore
    }
  },
  computed: {
    ...mapState(useSlides, ['blockSelected', 'activeSidebarComponent']),
    pageLinks () {
      return [
        {
          title: 'Home',
          to: 'home_view',
          icon: 'house'
        }
      ]
    },
    adminLinks () {
      return [
        {
          title: 'Home',
          to: 'home_view',
          icon: 'house'
        },
        {
          title: 'Connections',
          to: 'connections_view',
          icon: 'link'
        },
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
    }
  },
  mounted () {
    this.target = window.document
    document.querySelector('.dashboard').classList.add('bg-light')
  }
}
</script>

<style scoped>
@import url('@/layouts/bootstrap/css/dashboard1.css');
.dashboard {
  height: 100%;
}
</style>
