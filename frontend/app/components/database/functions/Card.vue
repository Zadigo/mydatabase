<template>
  <nuxt-card class="bg-gray-100">
    <div v-if="editedFunction" class="space-y-3">
      <!-- <div class="p-5 rounded-md bg-gray-50 text-2xl font-light lowercase">
        {{ selectedColumn }}[tableName].{{ selectedFunction }}("{{ functionArgument }}").{{ selectedReturnType }} >> {{ selectedChain }} || {{ selectedFailureMode }}
      </div> -->
      {{ editedFunction }}
      <nuxt-select v-if="currentDatabase" v-model.number="editedFunction.table" :items="currentDatabase.tables" placeholder="Select a table" label-value="id" label-key="name" class="w-3/6" />

      {{ selectedTable }}

      <div class="flex-col gap-2 space-y-2">
        <p class="text-sm font-semibold">Column on wich to apply the function</p>
        <nuxt-select v-model="editedFunction.columns" :multiple="true" :items="['firstname', 'lastname']" class="w-90" />
      </div>

      <div class="flex-col gap-2 space-y-2">
        <p class="text-sm font-semibold">The function to apply</p>
        <nuxt-select-menu v-model="editedFunction.name" :items="selectFunctionMenuItems" class="w-90" />
      </div>

      <!-- <div>
        <p class="text-sm font-semibold">Function argument an return type</p>
        <div class="flex gap-2">
          <nuxt-input v-model="editedFunction.returns.value" class="w-90" />
          <nuxt-select v-model="editedFunction.returns.type" :items="Array.from(functionReturnTypes)" class="w-90" />
        </div>
      </div> -->

      <nuxt-switch v-model="chainTo" label="Chain to" />
      <nuxt-select v-if="chainTo" v-model="editedFunction.chain_to" :multiple="true" :items="['Other function']" class="w-70" />

      <nuxt-separator class="my-5" />

      <p class="font-semibold">
        What should your function do on fail?
      </p>

      <!-- <nuxt-select v-model="editedFunction.on_fail.do" :items="Array.from(functionFailures)" class="w-50" /> -->
      <!-- <nuxt-input v-model="editedFunction.on_fail.default_value" placeholder="Default value" class="w-50" /> -->
      {{ editedFunction }}
    </div>
    <div v-else>
      <nuxt-skeleton class="h-5 w-full" />
    </div>
  </nuxt-card>
</template>

<script setup lang="ts">
import { selectFunctionMenuItems, useEditDatabaseFunction } from '~/composables/use/databases/functions'
import type { DatabaseFunction } from '~/types/functions'
import { functionFailures, functionReturnTypes } from '~/types/functions'

const props = defineProps<{ databaseFunction: DatabaseFunction }>()
console.log('props.databaseFunction', props.databaseFunction)

/**
 * Function
 */

const databaseStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(databaseStore)

const { editedFunction, selectedTable, chainTo } = useEditDatabaseFunction(currentDatabase, props.databaseFunction)
</script>
