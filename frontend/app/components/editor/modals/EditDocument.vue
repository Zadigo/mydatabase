<template>
  <nuxt-slideover v-model:open="show" direction="right" class="min-w-150">
    <template #title>
      Edit document
    </template>

    <template #body>
      <div class="space-y-2">
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
          
          <!-- Relationship -->
          {{ availableDocuments }}
          <div class="p-1 bg-gray-100 my-5">
            <div class="flex justify-center gap-3 items-center cursor-pointer rounded-md border border-gray-200 hover:bg-gray-100 p-2">
              <icon name="i-lucide-key" />
              <nuxt-select v-model="primaryKey" placeholder="Primary key" />
              
              <icon name="i-lucide-arrow-right" />
              <div class="flex gap-1">
                <nuxt-select v-model="foreignTableId" :items="availableDocuments" label-key="name" value-key="document_uuid" placeholder="Document" />
                <nuxt-select v-model="foreignTableForeignKey" placeholder="Foreign key" />
              </div>
            </div>
          </div>
        </div>
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

/**
 * Edit document
 */

const { remove } = useEditDocument()

/**
 * Relationships
 */

const { availableDocuments, primaryKey, foreignTableId, foreignTableForeignKey, create } = useEditDocumentRelationship()
</script>
