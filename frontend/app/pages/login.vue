<template>
  <section id="login">
    <nuxt-container>
      <div class="flex justify-center my-30">
        <nuxt-card class="space-y-2">
          <nuxt-input v-model="email" label="Email" type="text" class="w-full" />
          <nuxt-input v-model="password" label="Password" type="password" class="w-full" />

          <nuxt-button @click="() => { login() }">
            Login
          </nuxt-button>
        </nuxt-card>
      </div>
    </nuxt-container>
  </section>
</template>

<script setup lang="ts">
import type { TokenApiResponse } from '~/types'

const email = ref<string>('')
const password = ref<string>('')

const { data, execute: login } = useFetch<TokenApiResponse>('/v1/auth/token/', {
  immediate: false,
  baseURL: useRuntimeConfig().public.prodDomain,
  method: 'POST',
  body: {
    username: email.value,
    password: password.value
  } as {
    username: string
    password: string
  }
})


if (data.value) {
  useState('authTokens', () => data.value)

  useCookie('access').value = data.value.access
  useCookie('refresh').value = data.value.refresh

  navigateTo('/')
}
</script>
