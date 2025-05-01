<template>
  <div class="text-center text-body-tertiary">
    <div class="row">
      <div class="col-md-12">
        <div class="card shadow-sm">
          <div class="card-body">
            <IconBase icon="fa-solid:home" class="fa-6x" />
            <p class="my-3">
              Lorem ipsum dolor sit amet consectetur adipisicing elit.
              Enim cupiditate aliquid vero fuga rem suscipit ducimus in
              exercitationem architecto, dolorem, sint libero quae hic quidem
              reiciendis rerum. Natus, voluptas aliquam!
            </p>

            <button type="button" class="btn btn-info btn-lg btn-rounded shadow-none" @click="emit('block-modal')">
              Add your first block
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits({
  'block-modal'() {
    return true
  }
})
</script>
