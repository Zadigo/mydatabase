<template>
  <footer :class="footerClasses">
    <div class="container p-4">
      <section v-if="items.socials.length > 0" class="mb-4 text-center">
        <a v-for="(social, i) in items.socials" :key="i" :href="social.href" :style="`background-color: #${getColor(social.name)}`" class="btn btn-primary btn-floating m-1" role="button">
          <font-awesome-icon :icon="`fa-brands ${ getIcon(social.name) }`" />
        </a>
      </section>

      <section class="text-left my-4">
        <div class="row">
          <!-- Section -->
          <div v-for="(section, i) in items.sections" :key="i" class="col-lg-3 col-md-6 mb-4 mb-md-0">
            <h5 class="text-uppercase">
              {{ section.title }}
            </h5>

            <!-- Pages -->
            <ul class="list-unstyled mb-0">
              <li v-for="(link, t) in section.links" :key="t">
                <router-link :to="{ name: link.to }" :class="[darkMode ? 'text-light' : 'text-dark']">
                  {{ link.name }}
                </router-link>
              </li>
            </ul>
          </div>

          <slot></slot>
        </div>
      </section>
    </div>

    <!-- Copyright -->
    <div class="copyright text-center p-3">
      © {{ new Date().getFullYear() }} Copyright:
      <router-link to="/" :class="[darkMode ? 'text-light' : 'text-dark']">
        {{ brand }}
      </router-link>
    </div>
  </footer>
</template>

<script>
import { inject } from 'vue'

export default {
  name: 'BaseFooter',
  props: {
    items: {
      type: Object,
      default: () => {}
    },
    brand: {
      type: String
    }
  },
  setup () {
    const darkMode = inject('darkMode', false)
    return {
      darkMode
    }
  },
  computed: {
    footerClasses () {
      return [
        {
          'bg-dark text-light': this.darkMode,
          'bg-light': !this.darkMode
        }
      ]
    }
  },
  methods: {
    getColor (name) {
      // Get social media color
      const colors = {
        'Facebook': '#3b5998',
        'Google': '#dd4b39',
        'Instagram': '#ac2bac',
        'Twitter': '#55acee',
        'Linkedin': '#0082ca'
      }
      return colors[name]
    },
    getIcon (name) {
      // Returns the correct social media icon
      if (name === 'Facebook') {
        return 'fa-facebook-f'
      } else {
        return `fa-${name.toLowerCase() }`
      }
    }
  }
}
</script>

<style scoped>
.copyright {
  background-color: rgba(0, 0, 0, 0.2)
}
</style>
