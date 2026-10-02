import DefaultTheme from 'vitepress/theme'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    if (typeof window !== 'undefined') {
      localStorage.setItem('vitepress:local-search-detailed-list', 'true')
    }
  }
}
