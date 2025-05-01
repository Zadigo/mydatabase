<template>
  <header>
    <!-- Sidebar -->
    <nav v-if="$route.name !== 'slide'" id="sidebar" link="sidebar" class="collapse d-lg-block sidebar collapse bg-white">
      <div class="position-sticky">
        <keep-alive>
          <div class="list-group list-group-flush mx-3 mt-4">
            <router-link v-for="(link, i) in adminLinks" :key="i" :to="{ name: link.to }" class="list-group-item list-group-item-action py-2 ripple" aria-current="true">
              <IconBase :name="`fa-solid:${link.icon}`" class="me-3" />
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
          <IconBase class="fa-solid:bars" />
        </button>

        <router-link to="/" class="navbar-brand">
          <div class="fw-bold text-uppercase">
            Templates
          </div>
          <!-- <img src="https://mdbootstrap.com/img/logo/mdb-transaprent-noshadows.png" height="25" loading="lazy" alt="Image 4" /> -->
        </router-link>

        <ul class="navbar-nav ms-auto d-flex flex-row">
          <router-link :to="{ name: 'home' }">
            Some link
          </router-link>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const pageLinks = computed(() => {
  return [
    {
      title: 'Home',
      to: 'home',
      icon: 'fa-solid:home'
    }
  ]
})

const adminLinks = computed(() => {
  return [
    {
      title: 'Home',
      to: 'home',
      icon: 'fa-solid:home'
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
</script>
