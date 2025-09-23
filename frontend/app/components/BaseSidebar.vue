<template>
  <nav class="fixed top-9 left-0 px-5 py-10 bg-gray-50 border-r-1 border-gray-100 h-screen w-(--sidebar-width) z-10">
    <ul class="space-y-1">
      <li v-for="item in noneAlphaLinks" :key="item.name">
        <nuxt-separator v-if="item.separator" class="my-5" />
        <nuxt-link v-else :to="item.to" class="flex items-center justify-start gap-2 space-x-3 py-2 px-3 rounded-md hover:bg-gray-200">
          <nuxt-icon v-if="item.icon" :name="item.icon" />
          <span class="font-light text-sm">{{ item.name }}</span>
          <!-- <nuxt-badge size="xs" color="info" variant="subtle">Bêta</nuxt-badge> -->
        </nuxt-link>
      </li>
    </ul>
  </nav>
</template>

<script setup lang="ts">
interface LinkItems {
  name: string
  to: string
  icon: string,
  separator: boolean,
  isAlpha: boolean
}

const props = defineProps<{ items: Partial<LinkItems>[] }>()

const noneAlphaLinks = computed(() => props.items.filter(item => !item.isAlpha))
</script>

<style scoped>
li>.router-link-exact-active {
  background-color: var(--color-gray-200);
}
</style>
