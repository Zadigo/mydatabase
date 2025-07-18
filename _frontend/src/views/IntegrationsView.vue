<template>
  <page-section page-title="Integrations" section-id="integrations">
    <base-card class="shadow-sm">
      <template #body>
        <div class="p-2">
          <label for="webhooks" class="h5">Webook</label>
          <p>
            Receive real-time updates in one of your tables by creating a webhook here. 
            Specify the event table and start getting instant notifications
          </p>
          <v-select :items="pageStore.connections" variant="solo" item-title="name" item-value="sheet_id" placeholder="Select a sheet"></v-select>
          <v-text-field type="url" elevation="0" variant="solo-filled" placeholder="Webhook url" disabled hide-details />
          <div class="d-flex justify-content-end">
            <v-btn class="mt-3" elevation="0" variant="tonal" color="primary" rounded>
              Generate webhook
            </v-btn>
          </div>
        </div>

        <div class="p-2 mt-4">
          <label for="make" class="h5">API Key</label>
          <base-input id="make" disabled class="p-3" />
          <base-input id="make" disabled class="p-3 mt-1" />
          
          <div class="d-flex justify-content-end">
            <v-btn class="mt-3" elevation="0" variant="tonal" color="primary" rounded>
              Generate API key
            </v-btn>
          </div>
        </div>
      </template>
    </base-card>
  </page-section>
</template>

<script>
import { useSlides } from '@/store/slides'
import PageSection from '../layouts/PageSection.vue'
import BaseInput from '../layouts/bootstrap/BaseInput.vue'
import BaseCard from '../layouts/bootstrap/cards/BaseCard.vue'

export default {
  name: 'IntegrationsView',
  components: {
    BaseInput,
    BaseCard,
    PageSection
  },
  setup () {
    const pageStore = useSlides()
    return {
      pageStore
    }
  },
  beforeMount () {
    this.pageStore.loadFromCache()
  }
}
</script>
