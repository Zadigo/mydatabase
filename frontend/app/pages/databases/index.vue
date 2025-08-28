<template>
  <section id="databases">
    <div class="grid grid-cols-12 my-10 gap-2">
      <!-- Header -->
      <header class="col-span-12">
        <nuxt-card class="mb-2">
          <nuxt-input v-model="search" placeholder="Search databases" />

          <nuxt-button @click="() => { toggleCreationModal() }">
            Create Database
          </nuxt-button>
        </nuxt-card>
      </header>

      <!-- Databases -->
      <template v-if="searched.length > 0">
        <nuxt-link v-for="database in searched" :key="database.id" :to="`/databases/${database.id}`" class="col-span-3">
          <nuxt-card>
            <template #header>
              <h2>{{ database.name }}</h2>
            </template>
  
            <nuxt-badge label="Active" class="me-2" />
            <nuxt-badge :label="`${database.tables.length} tables`" />
          </nuxt-card>
        </nuxt-link>
      </template>

      <template v-else>
        <div v-for="i in 6" :key="i" class="col-span-3">
          <nuxt-skeleton class="h-20 w-full" />
          <nuxt-skeleton class="h-5 w-30 mt-2" />
        </div>
      </template>
    </div>

    <!-- Modals -->
    <nuxt-modal v-model:open="showModal">
      <template #title>
        <h2>Create Database</h2>
      </template>

      <template #body>
        <div class="space-y-2">
          <p class="text-light mb-3 w-full">
            Your project will have its own dedicated instance and full Postgres database.
            An API will be set up so you can easily interact with your new database.
          </p>

          <!-- Name -->
          <nuxt-input v-model="newDatabase.name" class="w-full" placeholder="Name" />
          <!-- Description -->
          <nuxt-input v-model="newDatabase.description" :disabled="true" class="w-full" placeholder="Description" />

          <nuxt-separator class="my-5" />

          <!-- Password -->
          <nuxt-input :disabled="true" class="w-full" placeholder="Password" />
        </div>
      </template>

      <template #footer>
        <div class="flex justify-end w-full gap-2">
          <nuxt-button @click="() => { toggleCreationModal() }">
            Cancel
          </nuxt-button>

          <nuxt-button @click="() => { create() }">
            Create new database
          </nuxt-button>
        </div>
      </template>
    </nuxt-modal>
  </section>
</template> 

<script setup lang="ts">
definePageMeta({
  title: 'Databases',
  layout: 'dashboard'
})

const databasesStore = useDatabasesStore()
  const { search, searched } = storeToRefs(databasesStore)

databasesStore.fetch()

const { showModal, newDatabase, create, toggleCreationModal } = useDatabaseCreation()

// Since the data are persisted, we should reset
// them to undefined when the user makes it back
// on this page. Other solution, persist some of
// the metadata in firebase
const tableEditionStore = useTableEditionStore()
tableEditionStore.selectedTableName = undefined
tableEditionStore.selectedTableDocumentName = undefined

const tableColumnsStore = useTableColumnsStore()
tableColumnsStore.columnNames = []
tableColumnsStore.columnOptions = []
tableColumnsStore.columnTypeOptions = []
</script>
