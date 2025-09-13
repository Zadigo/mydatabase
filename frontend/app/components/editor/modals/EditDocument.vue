<template>
  <nuxt-slideover v-model:open="show" direction="right" class="min-w-150">
    <template #title>
      Edit document
    </template>

    <template #body>
      <div v-if="availableDocuments.length > 0" class="space-y-2">
        <div v-for="tableDocument in availableDocuments" :key="tableDocument.id" class="p-5 rounded-md bg-info-50">
          <div class="flex justify-between items-center">
            <p class="font-bold">
              <icon name="i-solid-csv" /> Document
            </p>

            <nuxt-button-group>
              <nuxt-button color="neutral" variant="subtle" @click="() => { remove(tableDocument) }">
                <icon name="i-lucide-trash" />
              </nuxt-button>

              <nuxt-dropdown-menu :items="dropdownItems">
                <nuxt-button color="neutral" variant="outline" icon="i-lucide-chevron-down" />
              </nuxt-dropdown-menu>
            </nuxt-button-group>
          </div>

          <!-- Table Name -->
          <p class="font-light text-sm">
            {{ tableDocument.name || tableDocument.document_uuid }}
          </p>

          <nuxt-separator class="my-5" />

          <!-- Column Types -->
          <div class="space-y-2">
            <p class="font-bold">
              Column types
            </p>

            <div v-for="(column, index) in tableDocument.column_types" :key="index" class="grid grid-cols-7 gap-1 content-center">
              <nuxt-input v-model="column.name" class="col-span-3" />
              <nuxt-select v-model="column.columnType" :items="columnTypesMenuItem" item-label="label" value-key="label" class="col-span-3" />

              <!-- Dropdown -->
              <nuxt-dropdown-menu :items="constrainMenuItem">
                <nuxt-button icon="i-lucide-ellipsis-vertical" class="col-auto" variant="soft" />
              </nuxt-dropdown-menu>
            </div>
          </div>

          <!-- Relationship -->
          <div class="p-1 bg-gray-100 my-5">
            <div class="flex justify-center gap-3 items-center cursor-pointer rounded-md border border-gray-200 hover:bg-gray-100 p-2">
              <icon name="i-lucide-key" />
              <nuxt-select v-model="primaryKey" :items="primaryKeyColumns" placeholder="Primary key" />

              <icon name="i-lucide-arrow-right" />
              <div class="flex gap-1">
                <nuxt-select v-model="foreignTableId" :items="availableDocuments" label-key="name" value-key="document_uuid" placeholder="Document" />
                <nuxt-select v-model="foreignTableForeignKey" :items="foreignTableColumns" placeholder="Foreign key" />
              </div>

              <nuxt-button icon="i-lucide-save" variant="soft" color="success" @click="() => { create() }" />
            </div>
          </div>
        </div>
      </div>

      <div v-else class="space-y-2">
        <nuxt-skeleton class="h-20 w-full" />
        <nuxt-skeleton class="h-20 w-full" />
        <nuxt-skeleton class="h-20 w-full" />
      </div>
    </template>
  </nuxt-slideover>
</template>

<script setup lang="ts">
import { useEditDocument, useEditDocumentRelationship } from '~/composables/use/documents'
import type { DropdownMenuItem } from '@nuxt/ui'

const props = defineProps<{ modelValue: boolean }>()
const emit = defineEmits<{ 'update:modelValue': [] }>()
const show = useVModel(props, 'modelValue', emit, { defaultValue: true })

const dropdownItems: DropdownMenuItem[] = [
  {
    label: 'Merge versions',
    icon: 'i-lucide-git-merge',
    onSelect (e) {
      // Handle merge versions
      console.log(e)
    }
  },
  {
    label: 'Versions',
    icon: 'i-lucide-user-plus',
    children: [
      {
        label: 'New version',
        icon: 'i-lucide-git-pull-request-create'
      },
      {
        label: 'Compare version',
        icon: 'i-lucide-git-compare-arrows'
      },
      {
        label: 'Delete version',
        icon: 'i-lucide-git-pull-request-closed'
      }
    ]
  },
  {
    label: 'Transfer ownership',
    icon: 'i-lucide-hard-drive-upload'
  },
  {
    label: 'Lock file',
    icon: 'i-lucide-file-lock'
  }
]

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

/**
 * Edit document
 */

const { remove } = useEditDocument()

/**
 * Relationships
 */

const { primaryKeyColumns, foreignTableColumns, availableDocuments, primaryKey, foreignTableId, foreignTableForeignKey, create } = useEditDocumentRelationship()
</script>
