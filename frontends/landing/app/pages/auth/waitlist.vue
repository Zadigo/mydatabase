<template>
  <section id="signup">
    <u-card class="rounded-lg max-w-sm mx-auto bg-blue-50 border border-blue-200">
      <div class="py-4 flex justify-center">
        <nuxt-link to="/">
          <nuxt-img src="https://raw.githubusercontent.com/prebuiltui/prebuiltui/main/assets/dummyLogo/dummyFavicon.svg" alt="icon" width="45" height="45" loading="lazy" />
        </nuxt-link>
      </div>

      <h1 class="mb-4 text-center text-2xl font-semibold">
        Rejoindre la liste d'attente
      </h1>

      <form @submit.prevent>
        <div class="space-y-2 mb-10">
          <u-input v-model="data.email" type="email" size="xl" variant="subtle" class="w-full" placeholder="Email" />
          <u-input v-model="data.telephone" type="text" size="xl" variant="subtle" class="w-full" placeholder="Téléphone" />
          <u-input v-model="data.firstname" type="text" size="xl" variant="subtle" class="w-full" placeholder="Nom" />
          <u-input v-model="data.lastname" type="text" size="xl" variant="subtle" class="w-full" placeholder="Prénom" />
          <u-input v-model="data.company" type="text" size="xl" variant="subtle" class="w-full" placeholder="Entreprise" />
        </div>
        
        <u-button size="xl" block @click="create">
          Rejoindre
        </u-button>
      </form>

      <p class="mt-8 text-center text-sm text-blue-400">
        By clicking on sign in, you agree to our
        <nuxt-link to="#" class="underline">Terms of Service</nuxt-link> and <nuxt-link to="#" class="underline">Privacy Policy</nuxt-link>.
      </p>
    </u-card>
  </section>
</template>

<script lang="ts" setup>
definePageMeta({
  layout: 'authentication',
})

const data = ref<WaitllistData>({
  firstname: '',
  telephone: '',
  lastname: '',
  company: '',
  email: ''
})

function create() {
  $fetch('/api/waitlist', {
    method: 'POST',
    body: {}
  })
}
</script>
