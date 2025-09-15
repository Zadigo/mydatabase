<template>
  <div id="select-columns">
    {{ newDocument }}
    <base-column-type-option v-for="(column, idx) in newDocument.using_columns" :key="idx" v-model="newDocument.using_columns[idx]" />
  </div>
</template>

<script setup lang="ts">
import type { NewDocument } from '~/composables/use/documents'

const props = defineProps<{ modelValue: NewDocument }>()
const emit = defineEmits<{ 'update:ModelValue': [document: NewDocument] }>()
const newDocument = useVModel(props, 'modelValue', emit, { defaultValue: {} as NewDocument })
</script>
