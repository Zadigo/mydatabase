<template>
  <section id="login">
    <nuxt-container>
      <div class="flex justify-center my-30">
        <nuxt-card class="space-y-2">
          <nuxt-input v-model="email" label="Email" type="text" class="w-full" />
          <nuxt-input v-model="password" label="Password" type="password" class="w-full" />

          {{ isSuccess }}

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


/**
 * Login
 */

const email = ref<string>('')
const password = ref<string>('')

const { login, isSuccess } = await useLogin(email, password)

whenever(isSuccess, () => { navigateTo('/') })

const { userId, payload } = useProfile()
console.log('userId', userId.value, payload)
</script>
