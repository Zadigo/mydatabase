<template>
  <div class="grid grid-cols-12 gap-1 content-center space-y-2">
    <div class="col-span-1">
      <nuxt-checkbox v-model="editedColumn.visible">
        <template #label>
          <icon name="i-lucide-eye" />
        </template>
      </nuxt-checkbox>
    </div>
    <nuxt-input v-model="editedColumn.name" class="col-span-3" />
    <nuxt-select v-model="editedColumn.columnType" :items="columnTypesMenuItem" item-label="label" value-key="label" class="col-span-3" />

    <div class="col-span-1">
      <nuxt-checkbox v-model="editedColumn.unique">
        <template #label>
          <icon name="i-lucide-star" />
        </template>
      </nuxt-checkbox>
    </div>

    <div class="col-span-1">
      <nuxt-checkbox v-model="editedColumn.nullable">
        <template #label>
          <icon name="i-lucide-unlock" />
        </template>
      </nuxt-checkbox>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ColumnTypeOptions } from '~/types'

const props = defineProps<{ modelValue: ColumnTypeOptions }>()
const emit = defineEmits<{ 'update:ModelValue': [ColumnTypeOptions] }>()
const editedColumn = useVModel(props, 'modelValue', emit, { defaultValue: {} as ColumnTypeOptions })
</script>
