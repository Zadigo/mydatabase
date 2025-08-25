<template>
  <section id="databases">
    <div class="grid grid-cols-12 my-10 gap-2">
      <div class="col-span-12">
        <nuxt-card class="mb-2">
          <nuxt-input v-model="search" placeholder="Search databases" />
        </nuxt-card>
      </div>

      <nuxt-link v-for="database in searched" :key="database.id" :to="`/databases/${database.id}`" class="col-span-3">
        <nuxt-card>
          <template #header>
            <h2>{{ database.name }}</h2>
          </template>

          Lorem ipsum, dolor sit amet consectetur
          adipisicing elit. Sit doloremque sint molestias
        </nuxt-card>
      </nuxt-link>
    </div>
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
</script>
