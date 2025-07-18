<template>
  <NuxtCard>
    <div class="text-center">
      <Icon name="i-fa-solid:home" size="150" />

      <p class="my-3">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. 
        Enim cupiditate aliquid vero fuga rem suscipit ducimus in 
        exercitationem architecto, dolorem, sint libero quae hic quidem 
        reiciendis rerum. Natus, voluptas aliquam!
      </p>
      
      <NuxtButton rounded @click="emit('show:add-blocks-modal')">
        Add your first block
      </NuxtButton>
    </div>
  </NuxtCard>
</template>

<script setup lang="ts">
const emit = defineEmits(['show:add-blocks-modal'])
</script> 
