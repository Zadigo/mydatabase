<template>
  <section id="login">
    <nuxt-container>
      <div class="flex justify-center my-30">
        <nuxt-card class="space-y-2">
          <nuxt-input v-model="usernameField" label="Email" type="text" class="w-full" />
          <nuxt-input v-model="password" label="Password" type="password" class="w-full" />

          <nuxt-button @click="() => { login(() => { navigateTo('/') }) }">
            Login
          </nuxt-button>
        </nuxt-card>
      </div>
    </nuxt-container>
  </section>
</template>

<script setup lang="ts">
/**
 * Login
 */

const { login, usernameField, password } = useLogin('email')
</script>
