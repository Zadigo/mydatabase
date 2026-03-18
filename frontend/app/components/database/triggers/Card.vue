<template>
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
    <nuxt-select v-model="dbTriggers.on.event" :items="Array.from(databaseTriggerEvent)" class="w-60" placeholder="After or before the event" />


    <p class="font-semibold text-sm mb-2">Orientation</p>
    <nuxt-select v-if="isDefined(editingTrigger)" v-model="editingTrigger.orientation" :items="Array.from(databaseTriggerOrientation)" class="w-60" placeholder="Select orientation" />

    <nuxt-separator class="my-5" />

    <p class="font-semibold text-sm mb-2">Function to trigger</p>
    <div class="p-8 border bg-gray-200 dark:bg-slate-700 hover:bg-gray-300 dark:hover:bg-slate-600 border-gray-300 dark:border-slate-600 transition-all duration-1000 ease-in-out rounded-md text-center cursor-pointer" @click="() => { toggerFunctionsModal() }">
      <icon name="i-lucide-square-function" class="text-xl" />
      Choose a function to trigger
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DatabaseTrigger } from '~/types'

const props = defineProps<{
  dbTrigger: DatabaseTrigger['trigger'][number]
}>()

const { dbTriggers, toggerFunctionsModal, editableTrigger } = useDatabaseTriggers()
const editingTrigger = editableTrigger(props.dbTrigger)
</script>
