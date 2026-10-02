<script setup>
import { withBase, useData } from 'vitepress'

const { site } = useData()

function getUrl(slug) {
  const ext = site.value.cleanUrls ? '' : '.html'
  return withBase(`/dict/${slug}${ext}`)
}

function formatCount(count) {
  if (count === 1) return '1 entrée'
  return `${count.toLocaleString('fr-FR')} entrées`
}

const groups = [
  {
    title: 'Voyelles (स्वर, Svara)',
    subtitle: '13 sections phonétiques',
    cards: [
      { slug: 'a', deva: 'अ', iast: 'a', count: 2677 },
      { slug: 'aa', deva: 'आ', iast: 'ā', count: 796 },
      { slug: 'i', deva: 'इ', iast: 'i', count: 147 },
      { slug: 'ii', deva: 'ई', iast: 'ī', count: 53 },
      { slug: 'u', deva: 'उ', iast: 'u', count: 873 },
      { slug: 'uu', deva: 'ऊ', iast: 'ū', count: 55 },
      { slug: 'r', deva: 'ऋ', iast: 'ṛ', count: 61 },
      { slug: 'rr', deva: 'ॠ', iast: 'ṝ', count: 1 },
      { slug: 'l_vowel', deva: 'ऌ', iast: 'ḷ', count: 1 },
      { slug: 'e', deva: 'ए', iast: 'e', count: 153 },
      { slug: 'ai', deva: 'ऐ', iast: 'ai', count: 22 },
      { slug: 'o', deva: 'ओ', iast: 'o', count: 26 },
      { slug: 'au', deva: 'औ', iast: 'au', count: 36 }
    ]
  },
  {
    title: 'Gutturales (कण्ठ्य, Kaṇṭhya)',
    subtitle: '5 consonnes vélaires',
    cards: [
      { slug: 'ka', deva: 'क', iast: 'ka', count: 1514 },
      { slug: 'kha', deva: 'ख', iast: 'kha', count: 116 },
      { slug: 'ga', deva: 'ग', iast: 'ga', count: 601 },
      { slug: 'gha', deva: 'घ', iast: 'gha', count: 77 },
      { slug: 'nga', deva: 'ङ', iast: 'ṅa', count: 1 }
    ]
  },
  {
    title: 'Palatales (तालव्य, Tālavya)',
    subtitle: '5 consonnes palatales',
    cards: [
      { slug: 'ca', deva: 'च', iast: 'ca', count: 443 },
      { slug: 'cha', deva: 'छ', iast: 'cha', count: 71 },
      { slug: 'ja', deva: 'ज', iast: 'ja', count: 446 },
      { slug: 'jha', deva: 'झ', iast: 'jha', count: 13 },
      { slug: 'nya', deva: 'ञ', iast: 'ña', count: 1 }
    ]
  },
  {
    title: 'Cérébrales / Rétroflexes (मूर्धन्य, Mūrdhanya)',
    subtitle: '5 consonnes rétroflexes',
    cards: [
      { slug: 'tta', deva: 'ट', iast: 'ṭa', count: 15 },
      { slug: 'ttha', deva: 'ठ', iast: 'ṭha', count: 4 },
      { slug: 'dda', deva: 'ड', iast: 'ḍa', count: 12 },
      { slug: 'ddha', deva: 'ढ', iast: 'ḍha', count: 1 },
      { slug: 'nna', deva: 'ण', iast: 'ṇa', count: 9 }
    ]
  },
  {
    title: 'Dentales (दन्त्य, Dantya)',
    subtitle: '5 consonnes dentales',
    cards: [
      { slug: 'ta', deva: 'त', iast: 'ta', count: 751 },
      { slug: 'tha', deva: 'थ', iast: 'tha', count: 6 },
      { slug: 'da', deva: 'द', iast: 'da', count: 819 },
      { slug: 'dha', deva: 'ध', iast: 'dha', count: 281 },
      { slug: 'na', deva: 'न', iast: 'na', count: 1037 }
    ]
  },
  {
    title: 'Labiales (ओष्ठ्य, Oṣṭhya)',
    subtitle: '5 consonnes labiales',
    cards: [
      { slug: 'pa', deva: 'प', iast: 'pa', count: 2601 },
      { slug: 'pha', deva: 'फ', iast: 'pha', count: 44 },
      { slug: 'ba', deva: 'ब', iast: 'ba', count: 411 },
      { slug: 'bha', deva: 'भ', iast: 'bha', count: 508 },
      { slug: 'ma', deva: 'म', iast: 'ma', count: 1244 }
    ]
  },
  {
    title: 'Semi-voyelles (अन्तस्थ, Antastha)',
    subtitle: '4 semi-voyelles / spirantes',
    cards: [
      { slug: 'ya', deva: 'य', iast: 'ya', count: 372 },
      { slug: 'ra', deva: 'र', iast: 'ra', count: 537 },
      { slug: 'la', deva: 'ल', iast: 'la', count: 320 },
      { slug: 'va', deva: 'व', iast: 'va', count: 2219 }
    ]
  },
  {
    title: 'Sibilantes & Aspirée (ऊष्मन्, Ūṣman)',
    subtitle: '3 sibilantes et la consonne glottale',
    cards: [
      { slug: 'sha', deva: 'श', iast: 'śa', count: 975 },
      { slug: 'ssa', deva: 'ष', iast: 'ṣa', count: 55 },
      { slug: 'sa', deva: 'स', iast: 'sa', count: 2488 },
      { slug: 'ha', deva: 'ह', iast: 'ha', count: 368 }
    ]
  }
]
</script>

<template>
  <div class="alphabet-index-container">
    <section v-for="grp in groups" :key="grp.title" class="alphabet-group">
      <div class="group-header">
        <h3 class="group-title">{{ grp.title }}</h3>
        <span class="group-subtitle">{{ grp.subtitle }}</span>
      </div>
      <div class="alphabet-grid">
        <a
          v-for="card in grp.cards"
          :key="card.slug"
          :href="getUrl(card.slug)"
          class="alphabet-card"
        >
          <span class="grid-deva">{{ card.deva }}</span>
          <span class="grid-iast">{{ card.iast }}</span>
          <span class="grid-count">{{ formatCount(card.count) }}</span>
        </a>
      </div>
    </section>
  </div>
</template>

<style scoped>
.alphabet-index-container {
  margin: 1.5rem 0 3rem 0;
}

.alphabet-group {
  margin-bottom: 2.2rem;
}

.group-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  border-bottom: 1px solid var(--vp-c-divider);
  padding-bottom: 0.4rem;
  margin-bottom: 1rem;
}

.group-title {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  font-size: 1.25rem !important;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.group-subtitle {
  font-size: 0.85rem;
  color: var(--vp-c-text-3);
  font-style: italic;
}

@media (max-width: 640px) {
  .group-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
  }
}
</style>
