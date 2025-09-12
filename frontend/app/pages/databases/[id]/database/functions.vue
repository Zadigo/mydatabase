<template>
  <section id="database-functions" class="w-5xl mx-auto">
    <!-- Header -->
    <base-page-card-header v-model="search" placeholder="Search functions" title="Database functions" @create="create" />

    <div class="space-y-2">
      <database-functions-card v-for="(item, idx) in searched" :key="idx" :database-function="item" />
    </div>
  </section>
</template>

<script setup lang="ts">
import type { SelectItem } from '@nuxt/ui'
import { useDatabaseFunctions } from '~/composables/use/databases/functions'

/**
 * TODO: Page is in Bêta mode and needs work
 */

definePageMeta({
  title: 'Database: Functions',
  layout: 'details'

})

/**
 * Creation
 */

const { dbFunctions, search, searched, create } = useDatabaseFunctions()
</script>
