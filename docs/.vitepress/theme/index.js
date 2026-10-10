import DefaultTheme from 'vitepress/theme'
import AlphabetIndex from './components/AlphabetIndex.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('AlphabetIndex', AlphabetIndex)
    if (typeof window !== 'undefined') {
      localStorage.setItem('vitepress:local-search-detailed-list', 'true')
      document.documentElement.setAttribute('translate', 'no')
      document.documentElement.classList.add('notranslate')

      // Fallback-Handler für PDF-Assets auf Unterpfad-Deployments (z. B. GitHub Pages)
      document.addEventListener('click', (e) => {
        const a = e.target.closest('a')
        if (!a) return
        const href = a.getAttribute('href')
        if (href && href.startsWith('/') && !href.startsWith(import.meta.env.BASE_URL) && href.endsWith('.pdf')) {
          e.preventDefault()
          const resolved = `${import.meta.env.BASE_URL}${href.slice(1)}`
          if (a.target === '_blank') {
            window.open(resolved, '_blank')
          } else {
            window.location.href = resolved
          }
        }
      }, true)
    }
  }
}

