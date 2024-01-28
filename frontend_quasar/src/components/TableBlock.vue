<template>
  <q-card :id="`block_${block.block_id}`">
    <q-card-section>
      <q-table :columns="tableColumns" :rows="dataResults" flat />
    </q-card-section>
  </q-card>
</template>

<script>
import { defineComponent, getCurrentInstance } from 'vue'
import { ref } from 'vue'
import { useBlocksComposable } from '../composables/blocks'
import _ from 'lodash'

export default defineComponent({
  name: 'TableBlock',
  props: {
    block: {
      type: Object,
      required: true
    }
  },
  setup () {
    const app = getCurrentInstance()
    const { dataSourceId, cachedDataSource, dataResults, setDataSource, requestDataSource } = useBlocksComposable(app)
    const tableColumns = ref([])
    return {
      tableColumns,
      dataResults,
      cachedDataSource,
      dataSourceId,
      setDataSource,
      requestDataSource
    }
  },
  created () {
    if (this.$session.dictExists('sources', this.dataSourceId)) {
      this.setDataSource(this.$session.dictGet('sources', this.dataSourceId))
    } else {
      this.requestDataSource()
    }
  },
  mounted () {
    this.tableColumns = _.map(this.cachedDataSource.columns || [], (column) => {
      return {
        name: column,
        label: column,
        field: column,
        sortable: true
      }
    })
  }
})
</script>
