<template>
  <nuxt-card class="bg-gray-100">
    <div v-if="editedFunction" class="space-y-3">
      <!-- <div class="p-5 rounded-md bg-gray-50 text-2xl font-light lowercase">
        {{ selectedColumn }}[tableName].{{ selectedFunction }}("{{ functionArgument }}").{{ selectedReturnType }} >> {{ selectedChain }} || {{ selectedFailureMode }}
      </div> -->

      <div class="flex-col gap-2 space-y-2">
        <p class="text-sm">Column on wich to apply the function</p>
        <nuxt-select v-model="editedFunction.function.columns" :multiple="true" :items="['firstname', 'lastname']" class="w-90" />
      </div>

      <div class="flex-col gap-2 space-y-2">
        <p class="text-sm">The function to apply</p>
        <nuxt-select-menu v-model="editedFunction.function.name" :items="selectFunctionMenuItems" class="w-90" />
      </div>

      <div>
        <p class="text-sm">Function argument an return type</p>
        <div class="flex gap-2">
          <nuxt-input v-model="editedFunction.function.returns.value" class="w-90" />
          <nuxt-select v-model="editedFunction.function.returns.type" :items="Array.from(functionReturnTypes)" class="w-90" />
        </div>
      </div>

      <nuxt-switch label="Chain to" />
      <nuxt-select v-model="editedFunction.function.chain_to" :multiple="true" :items="['Other function']" class="w-70" />

      <nuxt-separator class="my-5" />

      <p class="font-semibold">
        What should your function do on fail?
      </p>

      <nuxt-select v-model="editedFunction.function.failure.on" :items="Array.from(functionFailures)" class="w-50" />
      <nuxt-input v-model="editedFunction.function.failure.default_value" placeholder="Default value" class="w-50" />
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
const { editedFunction } = useEditDatabaseFunction(props.databaseFunction)
</script>
