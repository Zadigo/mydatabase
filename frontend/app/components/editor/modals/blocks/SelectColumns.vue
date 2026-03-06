<template>
  <div id="select-columns">
    {{ newDocument }}
    <base-column-type-option v-for="(_, idx) in newDocument.using_columns" :key="idx" v-model:edited-column="newDocument.using_columns[idx]" />
  </div>
</template>

<script setup lang="ts">
import type { NewDocument } from '~/composables/use/documents'

const newDocument = defineModel<NewDocument>('newDocument', { required: true })
</script>
