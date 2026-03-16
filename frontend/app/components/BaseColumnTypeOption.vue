<template>
  <div v-if="editedColumn" class="grid grid-cols-12 gap-1 content-center space-y-2">
    <div class="col-span-1">
      <nuxt-checkbox v-model="editedColumn.visible">
        <template #label>
          <icon name="i-lucide-eye" />
        </template>
      </nuxt-checkbox>
    </div>

    <nuxt-input v-model="editedColumn.name" class="col-span-3" disabled />
    <nuxt-input v-model="editedColumn.newName" class="col-span-3" />
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

  <div v-else>
    <nuxt-skeleton />
  </div>
</template>

<script setup lang="ts">
import type { ColumnTypeOptions, Undefineable } from '~/types'

const props = defineProps<{
  columnType: Undefineable<ColumnTypeOptions>
}>()

const editedColumn = computed({
  get() {
    return props.columnType
  },
  set() {
    // Do nothing, changes are emitted on blur to avoid excessive emissions while editing
  }
})
</script>
