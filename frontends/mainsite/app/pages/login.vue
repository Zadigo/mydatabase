<template>
  <section id="login">
    <nuxt-container>
      <div class="flex justify-center my-30">
        <nuxt-card class="space-y-2">
          <form id="form-login" @submit.prevent>
            <nuxt-input v-model="usernameField" label="Email" type="text" name="email" class="w-full" />
            <nuxt-input v-model="password" label="Password" type="password" name="password" class="w-full" />
  
            <nuxt-button id="action-login" @click="() => { login(async () => { await navigateTo('/') }) }">
              Login
            </nuxt-button>
          </form>
        </nuxt-card>
      </div>
    </nuxt-container>
  </section>
</template>

<script setup lang="ts">
/**
 * Login
 */

preloadRouteComponents('/') // Preload home page for faster navigation after login

const { login, usernameField, password } = useLogin('email')
</script>
