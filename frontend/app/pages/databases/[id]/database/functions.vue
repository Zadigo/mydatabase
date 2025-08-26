<template>
  <section id="database-functions" class="w-5xl mx-auto">
    <!-- Header -->
    <base-page-card-header v-model="search" placeholder="Search functions" title="Database functions" />

    <nuxt-card class="bg-gray-100">
      <div class="space-y-3">
        <div class="p-5 rounded-md bg-gray-50 text-2xl font-light lowercase">
          {{ selectedColumn }}[tableName].{{ selectedFunction }}("{{ functionArgument }}").{{ selectedReturnType }} >> {{ selectedChain }} || {{ selectedFailureMode }}
        </div>
  
        <div class="flex-col gap-2 space-y-2">
          <p class="text-sm">Column on wich to apply the function</p>
          <nuxt-select v-model="selectedColumn" :items="['firstname', 'lastname']" class="w-90" />
        </div>
  
        <div class="flex-col gap-2 spae-y-2">
          <p class="text-sm">The function to apply</p>
          <nuxt-select-menu v-model="selectedFunction" :items="availableFunctions" class="w-90" />
        </div>
  
        <div>
          <p class="text-sm">Function argument an return type</p>
          <div class="flex gap-2">
            <nuxt-input v-model="functionArgument" class="w-90" />
            <nuxt-select v-model="selectedReturnType" :items="availableReturnTypes" class="w-90" />
          </div>
        </div>
  
        <nuxt-switch label="Chain to" />
        <nuxt-select v-model="selectedChain" :items="['Other function']" class="w-70" />
  
        <nuxt-separator class="my-5" />
  
        <p class="font-semibold">
          What should your function do on fail?
        </p>
  
        <nuxt-select v-model="selectedFailureMode" :items="availableFailures" class="w-50" />
        <nuxt-input placeholder="Default value" class="w-50" />
      </div>
    </nuxt-card>
  </section>
</template>

<script setup lang="ts">
/**
 * TODO: Page is in Bêta mode and needs work
 */

definePageMeta({
  title: 'Database: Functions',
  layout: 'details'
})

const selectedColumn = ref<string>()
const selectedFunction = ref<string>()
const functionArgument = ref<string>()
const selectedReturnType = ref<string>('void')
const selectedFailureMode = ref<string>('Skip')
const selectedChain = ref<string>()

const search = ref<string>()

const availableFunctions = ref<string[]>([
  {
    type: 'label',
    label: 'Aggegrate'
  },
  'Count',
  'Sum',
  'Avg',
  'Min',
  'Max',
  {
    type: 'separator'
  },
  {
    type: 'label',
    label: 'String'
  },
  'Upper',
  'Lower',
  'Length',
  'Trim',
  'Group concat',
  'Coalesce',
  'Extract',
  {
    type: 'separator'
  },
  {
    type: 'label',
    label: 'Date'
  },
  'Now',
  'Date',
  'Time',
  'Datetime',
  'Strftime',
  'Current timestamp',
  'Current date',
  'Current time',
  {
    type: 'separator'
  },
  {
    type: 'label',
    label: 'Miscellanous'
  },
  'Random',
  'MD5',
  'SHA256',
  'SHA512'
])

const availableReturnTypes = ref<string[]>([
  'void',
  'integer',
  'float',
  'bool',
  'time',
  'text',
  'time',
  'timetz',
  'timestamp',
  'timestamptz',
  'uuid'
])

const availableFailures = ref<string[]>([
  'Record',
  'Default',
  'Skip'
])
</script>
