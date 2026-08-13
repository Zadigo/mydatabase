<template>
  <nuxt-layout>
    <u-app>
      <nuxt-page />
    </u-app>
  </nuxt-layout>
</template>

<script lang="ts" setup>
import { provideSSRWidth } from '@vueuse/core'
import { useBusinessDetails, useWorkingDaysComposable } from '~/composables/business'

const nuxtApp = useNuxtApp()
provideSSRWidth(1024, nuxtApp.vueApp)

const isMobile = useMediaQuery('(min-width: 320px)')
const isLargeScreen = useMediaQuery('(min-width: 1024px)')

useState('isMobile', () => isMobile)
useState('isLargeScreen', () => isLargeScreen)

const { locales, locale } = useI18n()
useState('ogLocaleAlternate', () => locales.value.filter(l => l.code !== locale.value).map(l => l.code))

/**
 * General SEO Tags
 */

const { geoLocation, founderImage, organizationLogo, organizationImages, get } = useBusinessDetails()

const { workingDays, days } = useWorkingDaysComposable({
  only: 'Weekdays',
  startTime: '09:00',
  endTime: '17:00'
})

useHead({
  meta: [
    {
      name: 'geo.region',
      content: 'FR-HDF'
    },
    {
      name: 'geo.placename',
      content: get('address').city
    },
    {
      name: 'geo.position',
      content: geoLocation.value
    },
    {
      name: 'ICBM',
      content: geoLocation.value
    }
  ]
})

useHead({
  htmlAttrs: {
    lang: locale.value
  },
  link: [
    {
      rel: 'icon',
      type: 'image/png',
      href: '/favicon.png'
    }
  ]
})

useSchemaOrg(
  [
    defineOrganization({
      '@type': 'HairSalon',
      'name': get('legalName'),
      'legalName': get('legalName'),
      'alternateName': 'Inéïah Beauté',
      'description': get('description'),
      'logo': organizationLogo.value,
      'email': get('contact').email,
      'telephone': get('contact').telephone,
      'sameAs': get('sameAs'),
      'image': organizationImages.value,
      'priceRange': '$$',
      'foundingDate': get('foundingDate'),
      'foundingLocation': {
        '@type': 'Place',
        'name': get('foundingLocation')
      },
      'founder': {
        '@type': 'Person',
        'name': get('founder'),
        'jobTitle': 'Founder & CEO',
        'description': get('founderDescription'),
        'image': founderImage.value,
        'url': null,
        'sameAs': get('sameAs'),
        'worksFor': {
          '@type': 'Organization',
          'name': get('legalName')
        }
      },
      'numberOfEmployees': {
        '@type': 'QuantitativeValue',
        'value': 1
      },
      'taxId': null,
      'vatId': null,
      'address': {
        streetAddress: get('address').street,
        addressLocality: get('address').city,
        postalCode: get('address').postalCode,
        addressCountry: 'FR'
      },
      'currenciesAccepted': 'EUR',
      'areaServed': {
        '@type': 'Place',
        'name': get('address').city,
        'sameAs': `https://fr.wikipedia.org/wiki/${get('address').city}`
      },
      'paymentAccepted': [
        'Credit Card',
        'Apple Pay',
        'Google Pay'
      ],
      'openingHoursSpecification': workingDays.value.map(item => ({
        '@type': 'OpeningHoursSpecification',
        'dayOfWeek': item.day,
        'opens': item.startTime,
        'closes': item.endTime
      })),
      'contactPoint': [
        {
          '@type': 'ContactPoint',
          'contactType': 'customer service',
          'telephone': get('contact').telephone,
          'email': get('contact').email,
          'availableLanguage': ['English', 'French'],
          'hoursAvailable': {
            '@type': 'OpeningHoursSpecification',
            'dayOfWeek': days.value,
            'opens': '09:00:00',
            'closes': '15:00:00'
          }
        }
      ]
    })
  ]
)

/**
 * Href Lang
 */

const head = useLocaleHead({
  dir: true,
  lang: true,
  seo: true,
})

useHead({
  htmlAttrs: { lang: head.value.htmlAttrs?.lang },
  link: [...(head.value.link || [])],
  meta: [...(head.value.meta || [])]
})
</script>
