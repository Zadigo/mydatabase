<template>
  <nuxt-card class="bg-gray-100 dark:bg-slate-800">
    <div class="space-y-3">
      <!-- Table -->
      <nuxt-select v-if="currentDatabase" v-model.number="editedFunction.function.table" :items="currentDatabase.tables" placeholder="Select a table" value-key="id" label-key="name" class="w-3/6" />

      <div class="flex-col gap-2 space-y-2">
        <p class="text-sm font-semibold">Column on which to apply the function</p>
        <nuxt-select v-model="editedFunction.function.columns" :multiple="true" :items="columnNames" class="w-90" />
      </div>

      <div class="flex-col gap-2 space-y-2">
        <p class="text-sm font-semibold">The function to apply</p>
        <nuxt-select-menu v-model="editedFunction.function.name" :items="selectFunctionMenuItems" class="w-90" />
      </div>

      <div>
        <p class="text-sm font-semibold">Function return type</p>
        <div class="flex gap-2">
          <nuxt-input v-model.trim="editedFunction.function.returns.value" class="w-90" placeholder="Default return value" />
          <nuxt-select v-model="editedFunction.function.returns.type" :items="Array.from(functionReturnTypes)" class="w-90" />
        </div>
      </div>

      <nuxt-switch v-model="chainTo" label="Chain to" />
      <nuxt-select v-if="chainTo" v-model="editedFunction.function.chain_to" :multiple="true" :items="otherFunctions" class="w-70" />

      <nuxt-separator class="my-5" />

      <p class="font-semibold">
        What should your function do on fail?
      </p>

      <nuxt-select v-model="editedFunction.function.signals.failure.do" :items="Array.from(functionFailures)" class="w-50" />
      <nuxt-input v-model="editedFunction.function.signals.failure.default_value" :disabled="!shouldReturnDefault" placeholder="Default value" class="w-50" />

      <pre>
        {{ editedFunction }}
      </pre>
    </div>

    <div>
      <nuxt-skeleton class="h-5 w-full" />
    </div>
  </nuxt-card>
</template>

<script setup lang="ts">
import type { DatabaseFunction } from '~/types'

const { databaseFunction } = defineProps<{ databaseFunction: DatabaseFunction }>()

const databaseStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(databaseStore)

/**
 * Function
 */

const { dbFunctions } = useDatabaseFunctions()
const { editedFunction, chainTo, columnNames, otherFunctions, shouldReturnDefault } = useEditDatabaseFunction(dbFunctions, currentDatabase, databaseFunction)
</script>
