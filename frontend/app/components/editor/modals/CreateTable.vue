<template>
  <nuxt-modal v-model:open="show">
    <template #title>
      Create new table
    </template>

    <template #body>
      <div class="space-y-2">
        <!-- Name -->
        <nuxt-input v-model="newTable.name" class="w-full" placeholder="Document Name" />
      </div>
    </template>

    <template #footer>
      <div class="ms-auto flex gap-2">
        <nuxt-button @click="() => { show = false }">
          Cancel
        </nuxt-button>

        <nuxt-button @click="() => { create() }">
          Create
        </nuxt-button>
      </div>
    </template>
  </nuxt-modal>
</template>

<script setup lang="ts">
import { useCreateTable } from '~/composables/use/tables';

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'udpate:modelValue': [] }>()
const show = useVModel(props, 'modelValue', emit, { defaultValue: false })

/**
 * Create table
 */

const { create, newTable } = useCreateTable(show)
</script>
