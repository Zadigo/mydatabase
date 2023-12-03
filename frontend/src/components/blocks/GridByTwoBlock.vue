<template>
  <base-card :class="{ 'border border-info': selected }" class="shadow-sm" @click="selected = !selected">
    <template #body>
      <div class="row gx-2 text-center">
        <div class="col-sm-12 col-md-6 bg-light rounded p-2">
          <base-button class="my-4">Add block</base-button>
          <component :is="'table-block'" />
        </div>
        
        <div class="col-sm-12 col-md-6 bg-light rounded p-2">
          <base-button class="my-4">Add block</base-button>
        </div>
      </div>
    </template>
  </base-card>
</template>

<script>
import BaseButton from '../../layouts/bootstrap/buttons/BaseButton.vue'
import BaseCard from '../../layouts/bootstrap/cards/BaseCard.vue'
import TableBlock from './TableBlock'

export default {
  components: {
    BaseCard,
    BaseButton,
    TableBlock
  },
  data () {
    return {
      selected: false,
      blockTypes: [
        {
          name: 'Table',
          component: 'table-block',
          icon: 'table'
        },
        {
          name: 'Calendar',
          component: 'calendar-block',
          icon: 'calendar'
        },
        {
          name: 'Chart',
          component: 'chart-block',
          icon: 'chart-simple'
        },
        {
          name: 'Grid',
          component: 'grid-by-two-block',
          icon: 'grid'
        }
      ]
    }
  }
}
</script>
