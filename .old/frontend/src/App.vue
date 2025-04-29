<template>
  <v-app>
    <router-view :key="$route.name" />
  </v-app>
</template>

<script>
export default {
  name: 'App'
}
</script>
