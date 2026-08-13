type FooterLink = {
  title: string
  to: string
}

type FooterSection = {
  title: string
  links: FooterLink[]
}

type FooterData<S = FooterSection[]> = {
  description: string
  sections: S
}

export const FOOTER_DATA: FooterData = {
  description: 'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Rerum unde quaerat eveniet cumque accusamus atque qui error quo enim fugiat?',
  sections: [
    {
      title: 'Entreprise',
      links: [
        {
          title: 'À propos',
          to: '/'
        },
        {
          title: 'Nous contacter',
          to: '/'
        }
      ]
    }
  ]
}
