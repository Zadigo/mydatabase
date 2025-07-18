<template>
  <NuxtCard>
    <template #header>
      <div class="flex justify-between items-center">
        <NuxtButton v-if="blockDetails.allow_record_search" @click="openSearchPermissionsModal">
          <Icon name="i-fa-solid:search" />
          Columns for search
        </NuxtButton>

        <div class="right-actions space-x-2">
          <NuxtButton @click.prevent>
            <Icon name="i-fa-solid:filter" />
            User filters
          </NuxtButton>
  
          <NuxtButton v-if="blockDetails.allow_record_creation" @click="toggleCreatePermissionsModal">
            <Icon name="i-fa-solid:plus" />
            Columns for creation
          </NuxtButton>
        </div>
      </div>
    </template>

    <NuxtTable :data="activeData.results" :columns="activeData.columns" />
  </NuxtCard>
</template>

<script setup lang="ts">
import { useBlockPermissions, useTableBlock } from '~/composables/blocks'
import type { Block } from '~/types'

const props = defineProps<{  blockDetails: Block, isSelected: boolean }>()
const emit = defineEmits<{ 'show:permissions-modal': [modal: 'create' | 'search', block: Block]}>()

const { activeData, currentBlockPermissions } = useTableBlock(props.blockDetails)
const { showCreatePermissionsModal, showSearchPermissionsModal, toggleCreatePermissionsModal, toggleSearchPermissionsModal } = useBlockPermissions(currentBlockPermissions)

// function openSearchPermissionsModal() {
//   toggleSearchPermissionsModal()
//   emit('show:permissions-modal', 'search', props.blockDetails)
// }

// function toggleCreatePermissionsModal() {
//   toggleCreatePermissionsModal()
//   emit('show:permissions-modal', 'create', props.blockDetails)
// }
</script>
