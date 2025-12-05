<template>
  <nuxt-slideover v-model:open="showModal" direction="right" :handle="false" class="w-90">
    <template #header>
      <h2 class="font-bold">
        Update table
      </h2>
    </template>

    <template #body>
      {{ editableTableRef }}
      <div v-if="editableTableRef" class="space-y-4 p-5">
        <!-- Name -->
        <nuxt-input v-model="editableTableRef.name" class="w-full" placeholder="Table name" />
        <!-- Description -->
        <nuxt-input v-model="editableTableRef.description" class="w-full" placeholder="Table description" />
      </div>

      <div v-else class="space-y-2">
        <nuxt-skeleton class="w-full h-10" />
        <nuxt-skeleton class="w-full h-10" />
        <nuxt-skeleton class="w-full h-10" />
        <nuxt-skeleton class="w-full h-10" />
      </div>
    </template>

    <template #footer>
      <div class="flex justify-end">
        <nuxt-button variant="subtle" class="ml-2" @click="() => { tableEditionStore.toggleEditTableDrawer() }">
          Cancel
        </nuxt-button>

        <nuxt-button class="ml-2" @click="tableEditionStore.update()">
          Save
        </nuxt-button>
      </div>
    </template>
  </nuxt-slideover>
</template>

<script setup lang="ts">
const tableEditionStore = useTableEditionStore()
const { editableTableRef, showModal } = storeToRefs(tableEditionStore)
</script>
