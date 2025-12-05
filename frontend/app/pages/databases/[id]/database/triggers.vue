<template>
  <section id="database-triggers" class="w-5xl mx-auto">
    <!-- Header -->
    <base-page-card-header v-model="search" placeholder="Search triggers" title="Database triggers" />

    <nuxt-card class="bg-gray-100 mt-5">
      <p class="font-semibold text-sm mb-2">Name of trigger</p>
      <nuxt-input v-model="triggerName" class="w-60" placeholder="Trigger name" />

      <nuxt-separator class="my-5" />

      <div class="ms-5 my-3">
        <p class="font-semibold text-sm mb-2">Events</p>
        <div class="py-2">
          <nuxt-checkbox label="Before" />
          <p class="text-sm ms-6">Before an event occurs on the table</p>
        </div>

        <div class="py-2">
          <nuxt-checkbox label="After" />
          <p class="text-sm ms-6">After an event occurs on the table</p>
        </div>

        <p class="text-gray-400 mt-5 w-5/6">
          These are the events that are watched by the trigger, only the events
          selected above will fire the trigger on the table you've selected.
        </p>

        <nuxt-separator class="my-5" />

        <p class="font-semibold text-sm mb-2">Trigger types</p>
        <nuxt-select v-model="selectedEvent" :items="availableEvents" class="w-60" placeholder="After or before the event" />


        <p class="font-semibold text-sm mb-2">Orientation</p>
        <nuxt-select v-model="selectedEvent" :items="availableEvents" class="w-60" placeholder="After or before the event" />

        <nuxt-separator class="my-5" />

        <p class="font-semibold text-sm mb-2">Function to trigger</p>
        <div class="p-8 border bg-gray-200 hover:bg-gray-300 border-gray-300 transition-all duration-1000 ease-in-out rounded-md text-center cursor-pointer" @click="() => { toggerFunctionsModal() }">
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
    <nuxt-drawer v-model:open="showFunctionsModal" :handle="false" direction="right" handle-only>
      <template #title>
        Pick a Function
      </template>

      <template #body>
        <div class="space-y-3">
          <div v-for="i in 5" :key="i" class="p-5 bg-info-50 w-150 rounded-md cursor-pointer hover:bg-info-100 text-semibold leading-8">
            <icon name="i-lucide-square-function" class="text-xl" />
            Function_name_to_use
          </div>
        </div>
      </template>
    </nuxt-drawer>
  </section>
</template>

<script setup lang="ts">
/**
 * TODO: Page is in Bêta mode and needs work
 */

definePageMeta({
  label: 'Database: Triggers',
  layout: 'details'
})

const triggerName = ref<string>('')
const search = ref<string>('')

const availableEvents = ref<string[]>([
  'Insert',
  'Update',
  'Before'
])

const selectedEvent = ref<string>()

const [showFunctionsModal , toggerFunctionsModal] = useToggle()
</script>
