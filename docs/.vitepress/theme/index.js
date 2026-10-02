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
    }
  }
}

