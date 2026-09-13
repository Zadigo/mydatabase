<template>
  <form class="space-y-3" @submit.prevent>
    <editor-modals-blocks-upload-input-block v-for="(_, idx) in newDocument.documents" :key="idx" :idx="idx" @remove-document="(index) => { emit('remove-document', index) }" />
  </form>
</template>

<script lang="ts" setup>
const emit = defineEmits<{
  'remove-document': [index: number]
}>()

const { newDocument } = useCreateDocument()
</script>
