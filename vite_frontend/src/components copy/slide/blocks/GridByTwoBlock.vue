<template>
  <base-card :class="{ 'border border-info': selected }" class="shadow-sm" @click="selected = !selected">
    <template #body>
      <div class="row gx-2 text-center">
        <div class="col-sm-12 col-md-6 bg-light rounded p-2">
          <base-button class="my-4">
            {{ $t('Add block') }}
          </base-button>

          <component :is="'table-block'" />
        </div>

        <div class="col-sm-12 col-md-6 bg-light rounded p-2">
          <base-button class="my-4">
            {{ $t('Add block') }}
          </base-button>
        </div>
      </div>
    </template>
  </base-card>
</template>

<script setup lang="ts">
import { useBlocksComposable } from 'src/composables/blocks'

const { selected } = useBlocksComposable()
</script>
