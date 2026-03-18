<template>
  <section id="database-triggers" class="mx-auto">
    <!-- Header -->
    <base-page-card-header v-model="search" placeholder="Search triggers" title="Database triggers" @create="() => { create() }" />

    <!-- Triggers -->
    <nuxt-card v-for="(item, idx) in dbTriggers.trigger" :key="idx" class="bg-gray-100 dark:bg-slate-800 mt-5">
      <template #header>
        <nuxt-button size="sm" variant="outline" color="error" class="ms-2" @click="() => { deleteTrigger(item) }">
          <icon name="i-lucide-trash" />
        </nuxt-button>
      </template>

      <nuxt-form-field class="font-semibold" label="Name" required>
        <nuxt-input v-model="item.name" class="w-60" />
      </nuxt-form-field>

      <nuxt-separator class="my-5" />

      <div class="ms-5 my-3">
        <p class="font-semibold text-sm mb-2">Events</p>
        <div class="py-2">
          <nuxt-checkbox v-model="item.when.before" label="Before" />
          <p class="text-sm font-light ms-6">Before an event occurs on the table</p>
        </div>

        <div class="py-2">
          <nuxt-checkbox v-model="item.when.after" label="After" />
          <p class="text-sm font-light ms-6">After an event occurs on the table</p>
        </div>

        <p class="text-gray-400 mt-5 w-5/6">
          These are the events that are watched by the trigger, only the events
          selected above will fire the trigger on the table you've selected.
        </p>

        <nuxt-separator class="my-5" />

        <nuxt-form-field class="font-semibold mb-5" label="When" help="After or before the event">
          <nuxt-select v-model="item.event" :items="Array.from(databaseTriggerEvent)" class="w-60" />
        </nuxt-form-field>

        <nuxt-form-field class="font-semibold" label="Orientation" help="Row or column level">
          <nuxt-select v-model="item.orientation" :items="Array.from(databaseTriggerOrientation)" class="w-60" />
        </nuxt-form-field>

        <nuxt-separator class="my-5" />

        <p class="font-semibold text-sm mb-2">Function to trigger</p>
        <div class="p-8 border bg-slate-200 dark:bg-slate-700 hover:bg-gray-300 dark:hover:bg-slate-600 border-gray-300 dark:border-slate-600 transition-all duration-1000 ease-in-out rounded-md text-center cursor-pointer" @click="() => { toggerFunctionsModal() }">
          <icon name="i-lucide-square-function" class="text-xl" />
          Choose a function to trigger
        </div>
      </div>

      <div class="flex justify-end mb-5">
        <nuxt-button>
          Save
        </nuxt-button>
      </div>
    </nuxt-card>

    <!-- Modals -->
    <lazy-nuxt-drawer v-model:open="showFunctionsModal" :handle="false" direction="right" handle-only>
      <template #title>
        Pick a Function
      </template>

      <template #body>
        <div class="space-y-3">
          No functions
          <div v-for="(dbFunction, idx) in dbFunctions" :key="idx" class="p-5 bg-slate-50 dark:bg-slate-800 w-150 rounded-md cursor-pointer hover:bg-slate-100 dark:hover:bg-slate-700 text-semibold leading-8" @click="() => { selectFunction(item, dbFunction) }">
            <div class="flex items-center gap-2">
              <icon name="i-lucide-square-function" class="text-xl" />
              <span>{{ dbFunction.function.name }}</span>
            </div>
          </div>
        </div>
      </template>
    </lazy-nuxt-drawer>
  </section>
</template>

<script setup lang="ts">
import { useAsyncValidator } from '@vueuse/integrations/useAsyncValidator'

definePageMeta({
  label: 'Database: Triggers',
  layout: {
    name: 'details',
    props: {
      asideName: 'database'
    }
  }
})

/**
 * Triggers
 */

const { dbTriggers, search, showFunctionsModal, deleteTrigger, toggerFunctionsModal, create, selectFunction } = useDatabaseTriggers()

/**
 * Functions
 */

const { dbFunctions } = useDatabaseFunctions()
</script>
