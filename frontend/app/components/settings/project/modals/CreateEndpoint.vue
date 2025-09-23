<template>
  <nuxt-modal v-model:open="showModal">
    <template #header>
      Create an endpoint
    </template>

    <template #body>
      <nuxt-input v-model="newEndpointName" placeholder="Endpoint name" class="w-full" variant="subtle" />
    </template>

    <template #footer>
      <nuxt-button class="ms-auto" color="neutral" variant="soft" @click="() => { toggleShowModal()  }">
        Cancel
      </nuxt-button>

      <nuxt-button color="primary" @click="() => { create() }">
        Create
      </nuxt-button>
    </template>
  </nuxt-modal>
</template>

<script setup lang="ts">
import { useDatabaseEndpoints } from '~/composables/use/databases'

const { create, toggleShowModal, newEndpointName, showModal } = useDatabaseEndpoints()
</script>
