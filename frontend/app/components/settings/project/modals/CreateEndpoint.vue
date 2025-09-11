<template>
  <nuxt-modal v-model:open="showModal">
    <template #content>
      <nuxt-input v-model="newEndpoint.endpoint" />
    </template>

    <template #footer>
      <nuxt-button color="neutral" variant="outline" @click="() => { toggleShowModal()  }">
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

const { create, toggleShowModal, newEndpoint, showModal } = useDatabaseEndpoints()
</script>
