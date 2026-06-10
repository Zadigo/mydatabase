<template>
  <div id="google-sheets">
    <!-- File -->
    <nuxt-file-upload v-model="file" accept=".json" description="JSON file containing your Google Sheets API credentials" label="Google Sheets Credentials" />

    <!-- Actions -->
    <div class="mt-4 flex justify-end">
      <nuxt-button :loading="isLoading" @click="uploadFile">
        Upload Credentials
      </nuxt-button>
    </div>
  </div>
</template>

<script setup lang="ts">
const file = ref<File | null>(null)
const isLoading = ref<boolean>(false)

const databaseStore = useDatabasesStore()
const { currentDatabase } = storeToRefs(databaseStore)

/**
 * Uploads the selected file to the server.
 */
async function uploadFile() {
  const formData = new FormData()
  
  if (file.value) {
    formData.append('google_sheets', file.value)
  }

  if (isDefined(currentDatabase)) {
    isLoading.value = true

    const { data } = await useFetch<{ id: number, has_google_sheet_connection: boolean }>(`/v1/databases/${currentDatabase.value.id}/integrations`, {
      immediate: true,
      baseURL: useRuntimeConfig().public.prodDomain,
      method: 'POST',
      body: formData
    })
    
    isLoading.value = false
  
    if (data.value) {
      if (data.value.has_google_sheet_connection) {
        file.value = null
      }
    }
  }
}
</script>
