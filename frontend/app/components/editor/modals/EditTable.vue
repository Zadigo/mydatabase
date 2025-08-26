<template>
  <nuxt-drawer v-model:open="show" direction="right" :handle="false" class="w-90">
    <template #header>
      <h2 class="font-bold">Update table</h2>
    </template>

    <template #content>
      <div v-if="editableTableRef" class="space-y-4 p-4 overflow-y-scroll">
        <!-- Name -->
        <nuxt-input v-model="editableTableRef.name" class="w-full" placeholder="Table name" />
        <!-- Description -->
        <nuxt-input v-model="editableTableRef.description" class="w-full" placeholder="Table description" />

        <nuxt-separator class="my-5" />

        <!-- Column Types -->
        <div class="space-y-2">
          <p class="font-bold">
            Column types
          </p>

          <div v-for="(column, index) in columnTypeOptions" :key="index" class="grid grid-cols-7 gap-1 content-center">
            <nuxt-input v-model="column.name" class="col-span-3" />
            <nuxt-select v-model="column.columnType" :items="columnTypesMenuItem" class="col-span-3" />

            <!-- Dropdown -->
            <nuxt-dropdown-menu :items="constrainMenuItem">
              <nuxt-button class="col-span-1" variant="soft">
                <icon name="i-lucide-ellipsis-vertical" />
              </nuxt-button>
            </nuxt-dropdown-menu>
          </div>
        </div>
      </div>

      <div v-else class="space-y-2">
        <nuxt-skeleton class="w-full h-4" />
        <nuxt-skeleton class="w-full h-4" />
        <nuxt-skeleton class="w-full h-4" />
        <nuxt-skeleton class="w-full h-4" />
      </div>
    </template>
  </nuxt-drawer>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { columnTypesMenuItem, useTableColumns } from '~/composables/use/tables'
import type { DocumentData, Table } from '~/types'
import type { DropdownMenuItem } from '@nuxt/ui'

const tableData = inject<Ref<DocumentData>>('tableData')
const editableTableRef = inject<Ref<Table>>('editableTableRef')

const { columnTypeOptions } = useTableColumns(tableData.value)

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [boolean] }>()
const show = useVModel(props, 'modelValue', emit)

const constrainMenuItem: DropdownMenuItem[] = [
  {
    label: 'Unique',
    icon: 'i-lucide-star',
    onClick: () => {
      // Handle constrain action
    }
  },
  {
    label: 'Not nullable',
    icon: 'i-lucide-lock',
    onClick: () => {
      // Handle constrain action
    }
  }
]
</script>
