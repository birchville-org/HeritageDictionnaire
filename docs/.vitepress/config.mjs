import { defineConfig } from 'vitepress'

export default defineConfig({
  base: process.env.GITHUB_ACTIONS ? '/HeritageDictionnaire/' : '/',
  title: "Héritage du Sanskrit",
  description: "Dictionnaire sanskrit-français de Gérard Huet (INRIA) - Édition numérique interactive",
  lang: 'fr-FR',
  head: [
    ['meta', { name: 'google', content: 'notranslate' }],
    ['link', { rel: 'icon', href: '/birchville_logo.png' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.googleapis.com' }],
    ['link', { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }],
    ['link', { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+Devanagari:wght@400;600;700&display=swap' }]
  ],
  transformHtml(code) {
    code = code.replace('<html', '<html translate="no" class="notranslate"')
    const base = process.env.GITHUB_ACTIONS ? '/HeritageDictionnaire/' : '/'
    if (base !== '/') {
      code = code.replaceAll('href="/HeritageDictionnaire_indexed.pdf"', f'href="{base}HeritageDictionnaire_indexed.pdf"')
      code = code.replaceAll('href="/birchville_logo.png"', f'href="{base}birchville_logo.png"')
    }
    return code
  },
  themeConfig: {
    logo: '/birchville_logo.png',
    siteTitle: 'Héritage du Sanskrit',
    search: {
      provider: 'local',
      options: {
        detailedView: true,
        locales: {
          root: {
            translations: {
              button: {
                buttonText: 'Rechercher',
                buttonAriaLabel: 'Rechercher dans la documentation'
              },
              modal: {
                displayDetails: 'Afficher les détails',
                resetButtonTitle: 'Effacer la recherche',
                backButtonTitle: 'Fermer la recherche',
                noResultsText: 'Aucun résultat trouvé pour',
                footer: {
                  selectText: 'pour sélectionner',
                  selectKeyAriaLabel: 'Entrée',
                  navigateText: 'pour naviguer',
                  navigateUpKeyAriaLabel: 'Flèche vers le haut',
                  navigateDownKeyAriaLabel: 'Flèche vers le bas',
                  closeText: 'pour fermer',
                  closeKeyAriaLabel: 'Échap'
                }
              }
            }
          }
        }
      }
    },
    outline: {
      label: 'Sur cette page'
    },
    docFooter: {
      prev: 'Page précédente',
      next: 'Page suivante'
    },
    darkModeSwitchLabel: 'Apparence',
    lightModeSwitchTitle: 'Passer au thème clair',
    darkModeSwitchTitle: 'Passer au thème sombre',
    sidebarMenuLabel: 'Menu',
    returnToTopLabel: 'Retour en haut',
    notFound: {
      title: 'PAGE NON TROUVÉE',
      quote: 'Mais si vous ne changez pas de direction et continuez à chercher, vous pourriez vous retrouver là où vous vous dirigez.',
      linkLabel: 'Aller à l\'accueil',
      linkText: 'Retour à l\'accueil'
    },
    nav: [
      { text: 'Accueil', link: '/' },
      {
        text: 'Introduction',
        items: [
          { text: 'Avant-propos & Préface', link: '/intro/avant-propos' },
          { text: 'L\'alphabet devanāgarī', link: '/intro/alphabet' },
          { text: 'Abréviations', link: '/intro/abreviations' }
        ]
      },
      {
        text: 'Dictionnaire',
        items: [
          { text: 'Voyelles (अ à औ)', link: '/dict/a' },
          { text: 'Gutturales (क à ङ)', link: '/dict/ka' },
          { text: 'Palatales (च à ञ)', link: '/dict/ca' },
          { text: 'Cérébrales (ट à ण)', link: '/dict/tta' },
          { text: 'Dentales (त à न)', link: '/dict/ta' },
          { text: 'Labiales (प à म)', link: '/dict/pa' },
          { text: 'Semi-voyelles (य à व)', link: '/dict/ya' },
          { text: 'Sibilantes & H (श à ह)', link: '/dict/sha' }
        ]
      },
      { text: '📥 PDF Indexé (1217 p.)', link: '/HeritageDictionnaire_indexed.pdf', target: '_blank' }
    ],
    sidebar: {
      '/intro/': [
        {
          text: 'Introduction',
          items: [
            { text: 'Avant-propos & Préface', link: '/intro/avant-propos' },
            { text: 'L\'alphabet devanāgarī', link: '/intro/alphabet' },
            { text: 'Abréviations utilisées', link: '/intro/abreviations' }
          ]
        },
        {
          text: 'Dictionnaire (Accès rapide)',
          items: [
            { text: 'Index général des lettres', link: '/' }
          ]
        }
      ],
      '/dict/': [
        {
          text: 'Voyelles (Svara)',
          collapsed: false,
          items: [
            { text: 'अ (a)', link: '/dict/a' },
            { text: 'आ (ā)', link: '/dict/aa' },
            { text: 'इ (i)', link: '/dict/i' },
            { text: 'ई (ī)', link: '/dict/ii' },
            { text: 'उ (u)', link: '/dict/u' },
            { text: 'ऊ (ū)', link: '/dict/uu' },
            { text: 'ऋ (ṛ)', link: '/dict/r' },
            { text: 'ॠ (ṝ)', link: '/dict/rr' },
            { text: 'ऌ (ḷ)', link: '/dict/l_vowel' },
            { text: 'ए (e)', link: '/dict/e' },
            { text: 'ऐ (ai)', link: '/dict/ai' },
            { text: 'ओ (o)', link: '/dict/o' },
            { text: 'औ (au)', link: '/dict/au' }
          ]
        },
        {
          text: 'Consonnes (Gutturales & Palatales)',
          collapsed: true,
          items: [
            { text: 'क (ka)', link: '/dict/ka' },
            { text: 'ख (kha)', link: '/dict/kha' },
            { text: 'ग (ga)', link: '/dict/ga' },
            { text: 'घ (gha)', link: '/dict/gha' },
            { text: 'ङ (ṅa)', link: '/dict/nga' },
            { text: 'च (ca)', link: '/dict/ca' },
            { text: 'छ (cha)', link: '/dict/cha' },
            { text: 'ज (ja)', link: '/dict/ja' },
            { text: 'झ (jha)', link: '/dict/jha' },
            { text: 'ञ (ña)', link: '/dict/nya' }
          ]
        },
        {
          text: 'Consonnes (Cérébrales & Dentales)',
          collapsed: true,
          items: [
            { text: 'ट (ṭa)', link: '/dict/tta' },
            { text: 'ठ (ṭha)', link: '/dict/ttha' },
            { text: 'ड (ḍa)', link: '/dict/dda' },
            { text: 'ढ (ḍha)', link: '/dict/ddha' },
            { text: 'ण (ṇa)', link: '/dict/nna' },
            { text: 'त (ta)', link: '/dict/ta' },
            { text: 'थ (tha)', link: '/dict/tha' },
            { text: 'द (da)', link: '/dict/da' },
            { text: 'ध (dha)', link: '/dict/dha' },
            { text: 'न (na)', link: '/dict/na' }
          ]
        },
        {
          text: 'Consonnes (Labiales & Semi-voyelles)',
          collapsed: true,
          items: [
            { text: 'प (pa)', link: '/dict/pa' },
            { text: 'फ (pha)', link: '/dict/pha' },
            { text: 'ब (ba)', link: '/dict/ba' },
            { text: 'भ (bha)', link: '/dict/bha' },
            { text: 'म (ma)', link: '/dict/ma' },
            { text: 'य (ya)', link: '/dict/ya' },
            { text: 'र (ra)', link: '/dict/ra' },
            { text: 'ल (la)', link: '/dict/la' },
            { text: 'व (va)', link: '/dict/va' }
          ]
        },
        {
          text: 'Sibilantes & Aspirée',
          collapsed: true,
          items: [
            { text: 'श (śa)', link: '/dict/sha' },
            { text: 'ष (ṣa)', link: '/dict/ssa' },
            { text: 'स (sa)', link: '/dict/sa' },
            { text: 'ह (ha)', link: '/dict/ha' }
          ]
        }
      ]
    },
    footer: {
      message: 'Basé sur les travaux de Gérard Huet (INRIA Paris) - Version 3.75/3.84 sous licence CC BY-NC 4.0',
      copyright: '© Gérard Huet 1994–2026. Édition numérique interactive VitePress.'
    }
  }
})
