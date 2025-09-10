<template>
  <div id="select-columns">
    <div v-for="(column, idx) in tempColumnsTypes" :key="idx" class="flex justify-around">
      <nuxt-input v-model="column.name" />
      <nuxt-select v-model="column.columnType" :items="columnTypesMenuItem" value-key="label" item-label="label" />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NewDocument } from '~/composables/use/documents'

const props = defineProps<{ modelValue: NewDocument }>()
const emit = defineEmits<{ 'update:ModelValue': [document: NewDocument] }>()
const value = useVModel(props, 'modelValue', emit, { defaultValue: {} as NewDocument })

const { tempColumnsTypes } = useTempDocument(value)
</script>
