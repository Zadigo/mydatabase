<template>
  <q-page padding>
    <div class="row">
      <h1 class="text-h3">Connections</h1>
    </div>

    <div class="row">
      <q-banner class="bg-warning text-white q-mb-md" rounded>
        Lorem, ipsum dolor sit amet consectetur adipisicing elit. Praesentium nulla vitae laborum nam inventore architecto rem sunt cupiditate dolore, aperiam facilis commodi nesciunt expedita vero consequatur voluptates velit exercitationem amet.
        <template v-slot:action>
          <q-btn flat color="white" label="Dismiss" />
          <q-btn flat color="white" label="Update Credit Card" />
        </template>
      </q-banner>

      <q-card style="width: 100%;">
        <q-card-section>
          <div class="flex justify-end">
            <q-btn class="q-mr-md" color="primary" @click="showApiModal = true">
              Call API
            </q-btn>

            <q-btn color="primary" @click="() => { }">
              Upload file
            </q-btn>
          </div>
        </q-card-section>

        <q-card-section>
          <q-list bordered separator>
            <q-item v-for="dataSource in dataSources" :key="dataSource.sheet_id" class="q-pa-md">
              <q-item-section avatar>
                <q-icon color="teal" text-color="white" name="link" />
              </q-item-section>

              <q-item-section>
                <q-item-label>{{ dataSource.name }}</q-item-label>
                <q-item-label caption lines="1">Label</q-item-label>
              </q-item-section>

              <q-item-section side>
                <q-btn flat>
                  <q-icon name="link"></q-icon>

                  <q-menu>
                    <q-list style="min-width: 100px">
                      <q-item v-for="item in connectionMenuItems" :key="item" clickable v-close-popup @click="handleMenuActions(item, dataSource)">
                        <q-item-section>{{ item }}</q-item-section>
                      </q-item>
                    </q-list>
                  </q-menu>
                </q-btn>
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card>
    </div>

    <q-dialog v-model="showApiModal" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">New data source</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input v-model="requestData.name" class="q-mb-md" placeholder="Name" standout="bg-grey-1" clearable></q-input>
          <q-input v-model="requestData.endpoint_url" class="q-mb-md" type="url" placeholder="Url" standout="bg-grey-1" clearable></q-input>
          <q-input v-model="requestData.endpoint_data_key" class="q-mb-md" placeholder="Column name" standout="bg-grey-1" clearable></q-input>
          <q-select v-model="requestData.columns" placeholder="Columns" standout="bg-grey-1" use-input new-value-mode="add" multiple use-chips clearable></q-select>

        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn color="primary" flat label="Cancel" v-close-popup />
          <q-btn color="primary" label="Save" @click="handleDataUpload" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { useQuasar } from 'quasar'
import { storeToRefs } from 'pinia'
import { useDataSources } from '../stores/connections'
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'ConnectionPage',
  setup () {
    const notifications = useQuasar()
    const showApiModal = ref(false)
    const dataSourcesStore = useDataSources()
    const { dataSources, currentSlideDataSource } = storeToRefs(dataSourcesStore)
    const requestData = ref({
      name: null,
      columns_to_clean: [],
      endpoint_url: null,
      endpoint_data_key: null,
      columns: []
    })
    return {
      notifications,
      showApiModal,
      requestData,
      dataSources,
      currentSlideDataSource,
      dataSourcesStore,
      connectionMenuItems: [
        'Update',
        'Remove'
      ]
    }
  },
  created () {
    this.requestConnections()
  },
  methods: {
    async requestConnections () {
      try {
        const response = await this.$api.get('/sheets')
        this.dataSourcesStore.$patch((state) => {
          state.dataSources = response.data
        })
      } catch (error) {
        // Pass
      }
    },
    async handleDataUpload () {
      // Use this function to upload a new connection
      // or data source to the backend
      try {
        const response = await this.$api.post('/sheets/upload', this.requestData)
        this.requestData.columns = columns
        this.dataSources.push(response.data)
        this.showApiModal = false
        this.requestData = {
            name: null,
            columns_to_clean: [],
            endpoint_url: null,
            endpoint_data_key: null,
            columns: []
        }
        this.notifications.notify({
          message: 'Data created',
          color: 'success'
        })
      } catch (error) {
        this.notifications.notify({
          message: error,
          caption: 'Error',
          color: 'secondary'
        })
        this.showApiModal = false
      }
    },
    async handleRemoveConnection (id) {
      try {
        const response = await this.$api.post(`sheets/${id}/remove`)
        this.dataSourcesStore.dataSources = response.data
        this.notifications.notify({
          message: 'Connection removed'
        })
      } catch (error) {
        this.notifications.notify({
          message: 'Could not remove data source',
          color: 'danger'
        })
      }
    },
    handleMenuActions (action, dataSource) {
      console.log(action, dataSource)
      switch (action) {
        case 'Remove':
          this.handleRemoveConnection(dataSource.sheet_id)
          break
      
        default:
          break
      }
    }
  }
})
</script>
