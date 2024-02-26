<template>
  <q-card :id="`block_${block.block_id}`" class="q-mb-sm">
    <q-card-section>
      <q-table :columns="tableColumns" :rows="dataResults" :loading="loading" flat />
    </q-card-section>
  </q-card>
</template>

<script>
import _ from 'lodash'
import { ref } from 'vue'
import { defineComponent, getCurrentInstance } from 'vue'
import { useBlocksComposable } from '../composables/blocks'

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
    const loading = ref(true)
    return {
      loading,
      tableColumns,
      dataResults,
      cachedDataSource,
      dataSourceId,
      setDataSource,
      requestDataSource
    }
  },
  created () {
    const self = this
    if (this.$session.dictExists('sources', this.dataSourceId)) {
      this.setDataSource(this.$session.dictGet('sources', this.dataSourceId))
    } else {
      this.requestDataSource(() => {
        self.loading = false
      })
    }
  },
  mounted () {
    setTimeout(() => {
      this.tableColumns = _.map(this.cachedDataSource.column_names || [], (column) => {
        return {
          name: column,
          label: column,
          field: row => row[column],
          sortable: true
        }
      }) 
    }, 1000)
  }
})
</script>
