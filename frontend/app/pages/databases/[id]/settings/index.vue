<template>
  <section id="project-settings" class="max-w-5xl mx-auto space-y-2">
    <header>
      <h3 class="font-bold">Project settings</h3>
    </header>

    Updating: {{ isUpdating }} {{ newDatabaseName  }}

    <nuxt-card>
      <p class="font-bold">Project name</p>
      <nuxt-input v-if="currentDatabase" v-model="newDatabaseName" />
      <nuxt-skeleton v-else />

      <p class="font-bold">Project ID</p>
      <nuxt-input v-if="currentDatabase" v-model="currentDatabase.id" :disabled="true" variant="subtle" />
      <nuxt-skeleton v-else />
    </nuxt-card>

    <nuxt-card>
      <div class="flex-col gap-2 space-y-2">
        <p>Lorem ipsum, dolor sit amet consectetur adipisicing elit. Atque nemo rerum eum quae! Deleniti aspernatur velit ex at optio hic, totam inventore culpa officiis debitis. Ad provident quis consectetur fugiat.</p>
        <div class="flex gap-2">
          <nuxt-button @click="restartProject">
            Restart your project
          </nuxt-button>

          <nuxt-button @click="pauseProject">
            Pause your project
          </nuxt-button>
        </div>
      </div>
    </nuxt-card>

    <nuxt-card>
      <p class="font-bold">Deleting this project will also remove your database.</p>
      <p>Make sure you have made a backup if you want to keep your data.</p>
      <nuxt-button @click="() => { execute() }">Delete project</nuxt-button>
    </nuxt-card>
  </section>
</template>

<script setup lang="ts">
import { useEditDatabase } from '~/composables/use/databases'

definePageMeta({
  label: 'Settings: Home',
  layout: {
    name: 'details',
    props: {
      asideName: 'settings'
    }
  }
})

const { id } = useRoute().params as { id: string }
const config = useRuntimeConfig()

const { execute } = useFetch(`/v1/databases/${id}/delete`, {
  method: 'DELETE',
  baseURL: config.public.prodDomain,
  immediate: false,
  onResponse(response) {
    console.log(response)
    if (response.response.status === 204) {
      navigateTo('/databases')
    }
  }
})

function restartProject() {
  $fetch(`/v1/databases/${id}/restart`, {
    method: 'POST',
    baseURL: config.public.prodDomain,
    onResponse(response) {
      if (response.response.status === 204) {
        navigateTo('/databases')
      }
    }
  })
}

function pauseProject() {}

const dbStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(dbStore)

const { newDatabaseName, isUpdating } = useEditDatabase(currentDatabase)
</script>
