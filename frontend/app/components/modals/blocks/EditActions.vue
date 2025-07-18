<template>
  <v-dialog id="column-update-modal" v-model="showColumnActionsModal" width="500">
    <v-card>
      <v-card-text>
        <v-text-field v-model="currentUpdatedColumn.name" label="Column name" variant="outlined"></v-text-field>
        <v-select v-model="currentUpdatedColumn.column_type" :items="columnTypeChoices" label="Column type" variant="outlined"></v-select>
        <v-select v-model="currentUpdatedColumn.column_sort" :items="columnSortingChoices" label="Sort" variant="outlined" clearable hide-details></v-select>
        <v-switch v-model="currentUpdatedColumn.allow_column_creation" label="Allow column creation" inset hide-details></v-switch>
        <v-switch v-model="currentUpdatedColumn.allow_column_update" label="Allow column update" inset hide-details></v-switch>
        <v-switch v-model="currentUpdatedColumn.allow_column_search" label="Allow column search" inset hide-details></v-switch>
        <v-switch v-model="currentUpdatedColumn.column_visibility" label="Visibility" inset hide-details></v-switch>
      </v-card-text>

      <v-card-actions>
        <v-btn @click="showColumnActionsModal = false">Cancel</v-btn>
        <v-btn variant="tonal" @click="handleUpdateColumn">Validate</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
