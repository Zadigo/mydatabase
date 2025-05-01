<template>
  <section id="settings">
    <div class="container">
      <div class="row">
        <div class="col-md-8 col-sm-12 offset-md-2">
          <base-card>
            <template #body>
              <div class="p-1">
                <label for="default-page-name" class="fw-bold mb-2">Default page name</label>
                <base-input id="default-page-name" v-model="newValues.pageName" class="p-2" max="200" />
              </div>
            </template>

            <template v-if="canValidate" #footer>
              <div class="d-flex justify-content-end">
                <base-button color="primary" rounded>
                  <font-awesome-icon :icon="['fas', 'circle-check']" class="me-2" />
                  Validate
                </base-button>
              </div>
            </template>
          </base-card>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import BaseCard from '../layouts/bootstrap/cards/BaseCard.vue'
import BaseInput from '../layouts/bootstrap/BaseInput.vue'
import BaseButton from '../layouts/bootstrap/buttons/BaseButton.vue'
export default {
  components: {
    BaseCard,
    BaseInput,
    BaseButton
  },
  data() {
    return {
      newValues: {
        pageName: null
      }
    }
  },
  computed: {
    canValidate() {
      return Object.keys(this.newValues).map((key) => {
        return this.newValues[key] !== null || this.newValues[key] !== ''
      }).some(x => x === true)
    }
  }
}
</script>
