import type { Nullable } from '~/types'
import type { BusinessDetails, BusinessDetailsKeys, BusinessDetailsKeyValue, Social, SocialPlatform } from '.'

export const businessDetails: BusinessDetails = {
  name: 'Lorélie',
  legalName: 'Lorélie',
  alternateName: [
    'Lorélie',
    'Lorelie'
],
  siren: '',
  siret: '',
  numberoTVA: '',
  creationDate: '2024-12-14',
  description: 'Lorélie',
  logo: '/logos/lorelie-dark-small.png',
  sameAs: [
    'https://fr.pinterest.com/labeautedineiah',
    'https://facebook.com/labeautedineiah',
    'https://www.instagram.com/ineiah'
],
  image: [
    '/logos/lorelie-dark-small.png',
    '/logos/lorelie-light-small.png'
],
  rcs: '',
  address: {
    street: '13 Place Nouvelle Aventure',
    postalCode: '59000',
    city: 'Lille',
    lat: 50.626999404132064,
    lng: 3.0499777837365993
  },
  priceRange: '$$',
  foundingDate: '2024-12-14',
  foundingLocation: 'Lille, France',
  founderImage: '/images/natachamorel/natacha-morel-coiffure.jpg',
  shareCapital: null,
  founder: 'Natacha Morel',
  founderDescription: 'John Pendenque est un développeur web passionné par la création d\'applications performantes et intuitives. Avec une expertise en JavaScript, Vue.js et Nuxt.js, il se spécialise dans le développement de solutions web modernes et réactives. Son approche centrée sur l\'utilisateur et son souci du détail lui permettent de concevoir des interfaces élégantes et fonctionnelles. En dehors du codage, John aime explorer les nouvelles technologies et contribuer à des projets open source.',
  founderKnowsAbout: [
    'JavaScript',
    'Vue.js',
    'Nuxt.js',
    'Web Development',
    'UI/UX Design',
    'Golang',
    'Python',
    'Node.js',
],
  webContentManager: 'John Pendenque',
  publishingDirector: 'John Pendenque',
  editorInChief: 'John Pendenque',
  websiteProvider: {
    legalName: 'Gency313',
    url: 'https://johnpm-consulting.fr/'
  },
  cloudProvider: {
    legalName: 'SAS OVH',
    url: 'http://www.ovhcloud.com/fr/',
    description: 'OVH SAS est une filiale de la société OVH Groupe SA, société immatriculée au RCS de Lille',
    address: '2 rue Kellermann - 59100 Roubaix - France',
    rcs: '424 761 419 00045'
  },
  contact: {
    telephone: '+33 07 86 20 94 59',
    email: 'labeautedineiah@gmail.com',
    address: '13 Place Nouvelle Aventure, 59000 Lille'
  },
  socials: {
    // instagram: {
    //   url: 'https://www.instagram.com/ineiah',
    //   handle: '@ineiah'
    // },
    // facebook: {
    //   url: 'https://www.facebook.com/labeautedineiah',
    //   handle: 'labeautedineiah'
    // },
    // pinterest: {
    //   url: 'https://fr.pinterest.com/labeautedineiah',
    //   handle: 'labeautedineiah'
    // }
  }
}

/**
 * A composable to access business details throughout the application. It provides a `get` function
 * to retrieve specific details by key, ensuring type safety and consistency across the app.
 */
export function useBusinessDetails() {
  function get<K extends BusinessDetailsKeys>(key: K): BusinessDetailsKeyValue[K] {
    return businessDetails[key]
  }

  const reactiveGet = reactify(get)
  const activeSocials = computed(() => Object.keys(get('socials')) as SocialPlatform[])

  function getSocial(platform: SocialPlatform): Social | null {
    const socials = get('socials')
    return socials[platform] || null
  }

  function getSocialIcon(platform: SocialPlatform): string {
    const icons: Record<SocialPlatform, string> = {
      instagram: 'lucide:instagram',
      facebook: 'lucide:facebook',
      pinterest: 'fa7-brands:pinterest',
      twitter: 'lucide:twitter',
      linkedin: 'lucide:linkedin',
      tiktok: 'lucide:tiktok',
      youtube: 'lucide:youtube'
    }
    return icons[platform]
  }

  const address = computed(() => {
    const address = get('address')
    return `${address.street}, ${address.postalCode} ${address.city}`
  })

  const geoLocation = computed(() => {
    const address = get('address')
    if (isDefined(address.lat) && isDefined(address.lng)) {
      return `${address.lat.toString()},${address.lng.toString()}`
    } else {
      return '0,0'
    }
  })

  function suffixLegalName(name: Nullable<string>, separator: string = ' - '): string {
    const legalName = get('legalName')
    return `${name ?? ''}${separator}${legalName}`
  }

  function _buildPath(path: Nullable<string>): Nullable<string> {
    if (!isDefined(path)) {
      return null
    } else {
      try {
        const rootUrl = useRuntimeConfig().public.siteUrl
        return new URL(path, rootUrl).toString()
      } catch {
        return path
      }
    }
  }

  const founderImage = computed(() => {
    return _buildPath(get('founderImage'))
  })

  const organizationLogo = computed(() => {
    return _buildPath(get('logo'))
  })

  const organizationImages = computed(() => {
    return get('image').map((image: string) => _buildPath(image))
  })

  return {
    /**
     * The business details object containing all relevant information about the business,
     * including contact details, social media links, and more.
     */
    businessDetails,
    /**
     * A computed property that returns an array of active social media
     * platforms based on the provided socials in the business details.
     */
    activeSocials,
    /**
     * A computed property that returns the full address of the business
     * as a formatted string, combining the street, postal code, and city.
     */
    address,
    /**
     * A computed property that returns the geographical location of the business
     * in the format "latitude,longitude". If latitude or longitude is not defined.
     * @default
     * "0,0"
     */
    geoLocation,
    /**
     * A computed property that returns the full URL of the founder's 
     * image, constructed from the base site URL and the relative path provided in the business details.
     */
    founderImage,
    /**
     * A computed property that returns the full URL of the organization's logo,
     * constructed from the base site URL and the relative path provided in the business details.
     */
    organizationLogo,
    /**
     * A computed property that returns an array of full URLs for the organization's images,
     * constructed from the base site URL and the relative paths provided in the business details.
     */
    organizationImages,
    /**
     * A function that appends the legal name of the business to a given name,
     * separated by a specified separator (default is ' - ').
     */
    suffixLegalName,
    /**
     * A function to retrieve specific business details by key, ensuring type safety.
     * @param key - The key of the business detail to retrieve.
     */
    get,
    /**
     * A reactive version of the `get` function, useful for reactive contexts.
     * @param key - The key of the business detail to retrieve reactively.
     */
    reactiveGet,
    /**
     * A function to retrieve social media details for a specific platform.
     * @param platform - The social media platform to retrieve details for (e.g., 'instagram', 'facebook').
     */
    getSocial,
    /**
     * A function to retrieve the icon name for a specific social media platform.
     * @param platform - The social media platform to retrieve the icon for (e.g., 'instagram', 'facebook').
     */
    getSocialIcon
  }
}
