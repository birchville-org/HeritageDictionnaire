#!/usr/bin/env python3
"""
index_pdf.py - Injects a complete, hierarchical Table of Contents (Document Outlines / Bookmarks)
into HeritageDictionnaire.pdf.
"""

import sys
import os
import re
import unicodedata
import pymupdf

def to_clean_prefix(text):
    t = text.replace('´', '').replace('\u0301', '')
    t = t.replace('¯r.', 'ṝ').replace('t.h', 'ṭh').replace('d.h', 'ḍh')
    t = t.replace('¯a', 'ā').replace('¯ı', 'ī').replace('¯u', 'ū')
    t = t.replace('r.', 'ṛ').replace('l.', 'ḷ').replace('˙n', 'ṅ').replace('˜n', 'ñ')
    t = t.replace('t.', 'ṭ').replace('d.', 'ḍ').replace('n.', 'ṇ')
    t = t.replace('´s', 'ś').replace('s.', 'ṣ')
    t = t.replace('m.', 'ṃ').replace('h.', 'ḥ')
    t = re.sub(r'[^a-zA-Zāīūṛṝḷṅñṭṭhḍḍhṇśṣṃḥ]', '', t)
    return t

# 43 Classical Sanskrit Letters with exact starting pages in HeritageDictionnaire.pdf (v3.75)
LETTERS = [
    ('अ', 'a', 12),
    ('आ', 'ā', 141),
    ('इ', 'i', 179),
    ('ई', 'ī', 187),
    ('उ', 'u', 190),
    ('ऊ', 'ū', 233),
    ('ऋ', 'ṛ', 235),
    ('ॠ', 'ṝ', 238),
    ('ऌ', 'ḷ', 238),
    ('ए', 'e', 238),
    ('ऐ', 'ai', 245),
    ('ओ', 'o', 246),
    ('औ', 'au', 247),
    ('क', 'ka', 249),
    ('ख', 'kha', 333),
    ('ग', 'ga', 339),
    ('घ', 'gha', 371),
    ('ङ', 'ṅa', 375),
    ('च', 'ca', 375),
    ('छ', 'cha', 400),
    ('ज', 'ja', 403),
    ('झ', 'jha', 425),
    ('ञ', 'ña', 426),
    ('ट', 'ṭa', 426),
    ('ठ', 'ṭha', 426),
    ('ड', 'ḍa', 426),
    ('ढ', 'ḍha', 427),
    ('ण', 'ṇa', 427),
    ('त', 'ta', 428),
    ('थ', 'tha', 463),
    ('द', 'da', 463),
    ('ध', 'dha', 506),
    ('न', 'na', 520),
    ('प', 'pa', 572),
    ('फ', 'pha', 704),
    ('ब', 'ba', 706),
    ('भ', 'bha', 729),
    ('म', 'ma', 759),
    ('य', 'ya', 824),
    ('र', 'ra', 843),
    ('ल', 'la', 873),
    ('व', 'va', 889),
    ('श', 'śa', 1004),
    ('ष', 'ṣa', 1058),
    ('स', 'sa', 1061),
    ('ह', 'ha', 1198)
]

def get_page_headwords(page):
    """
    Extract genuine Sanskrit headwords from page using font signature:
    Velthuis-dvng10 followed by CMSL10 (Computer Modern Slanted).
    """
    d = page.get_text('dict')
    hws = []
    for b in d['blocks']:
        if 'lines' in b:
            for l in b['lines']:
                spans = l['spans']
                for i in range(len(spans)-1):
                    if 'Velthuis' in spans[i]['font']:
                        for j in range(i+1, min(i+4, len(spans))):
                            if 'CMSL' in spans[j]['font']:
                                txt = spans[j]['text'].strip()
                                clean = to_clean_prefix(txt)
                                if len(clean) >= 2:
                                    hws.append(clean)
                                break
    return hws

def find_subclusters_for_letter(doc, start_p, end_p, letter_iast):
    """
    Scans pages from start_p to end_p and finds sub-clusters based on verified headwords.
    """
    subclusters = []
    seen_prefixes = set()
    base_prefix = letter_iast.rstrip('a').lower()
    
    last_p = start_p - 10
    
    for p in range(start_p, end_p + 1):
        hws = get_page_headwords(doc[p - 1])
        for w in hws:
            if not w.lower().startswith(base_prefix):
                continue
            
            # Form clean prefix
            if w.startswith(('kṣ', 'jñ', 'sth', 'sph', 'str')):
                pref = w[:3] + '-'
            elif w.startswith(('sk', 'st', 'sp', 'sm', 'sn', 'sy', 'sv', 'sr', 'pr', 'pl', 'br', 'bh', 'dr', 'dv', 'dh', 'tr', 'tv', 'gr', 'gh', 'kr', 'kl', 'kv', 'kh')):
                pref = w[:2] + '-'
            elif len(w) >= 2:
                pref = w[:2] + '-'
            else:
                pref = w + '-'
                
            # Keep if prefix not yet seen in this letter section and spaced reasonably
            if pref not in seen_prefixes:
                if (p - last_p >= 3) or (pref.startswith(('kā', 'sā', 'pā', 'mā', 'dā', 'tā', 'bā', 'vā', 'hā', 'ki', 'ku', 'kṛ', 'si', 'su', 'pi', 'pu', 'pṛ', 'vi', 'vṛ')) and p - last_p >= 2):
                    seen_prefixes.add(pref)
                    subclusters.append((p, pref, w))
                    last_p = p
                    break
                    
    return subclusters

def build_toc(doc):
    toc = []
    
    # 1. Frontmatter
    toc.append([1, "Héritage du Sanskrit (Titre)", 1])
    toc.append([1, "Notice & Droits d'auteur", 2])
    toc.append([1, "Avant-propos", 3])
    toc.append([1, "Préface à la première édition (1998)", 3])
    toc.append([1, "L'alphabet devanāgarī & phonétique", 3])
    toc.append([2, "Voyelles & Diphtongues", 3])
    toc.append([2, "Consonnes (Gutturales, Palatales...)", 4])
    toc.append([2, "Sibilantes, Aspirée & Syllabes", 5])
    toc.append([2, "Alternances vocaliques (guṇa, vṛddhi)", 6])
    toc.append([2, "Ligatures devanāgarī", 6])
    toc.append([2, "Méthode de transcription", 6])
    toc.append([1, "Présentation du lexique", 6])
    toc.append([1, "Abréviations utilisées", 9])
    
    # 2. Dictionnaire sanskrit-français
    toc.append([1, "Dictionnaire sanskrit-français", 12])
    
    for i, (dev, iast, start_p) in enumerate(LETTERS):
        end_p = LETTERS[i+1][2] - 1 if i+1 < len(LETTERS) else 1217
        toc.append([2, f"{dev} ({iast})", start_p])
        
        # If section is long (>= 7 pages), generate verified subclusters
        page_span = end_p - start_p + 1
        if page_span >= 7:
            sub = find_subclusters_for_letter(doc, start_p, end_p, iast)
            for p, pref, w in sub:
                if p > start_p:
                    toc.append([3, f"{pref} ({w})", p])
                    
    return toc

def main():
    input_pdf = "input/HeritageDictionnaire.pdf"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_pdf = os.path.join(output_dir, "HeritageDictionnaire_indexed.pdf")
    
    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} not found!", file=sys.stderr)
        sys.exit(1)
        
    print(f"Opening {input_pdf}...")
    doc = pymupdf.open(input_pdf)
    print(f"Total pages: {len(doc)}")
    
    print("Building hierarchical Table of Contents (Outlines)...")
    toc = build_toc(doc)
    print(f"Generated {len(toc)} bookmark entries.")
    
    # Print sample TOC
    print("\n--- TOC Sample (First 20 entries) ---")
    for level, title, page in toc[:20]:
        indent = "  " * (level - 1)
        print(f"{indent}• {title} -> Page {page}")
        
    print("\n--- TOC Sample (Last 15 entries) ---")
    for level, title, page in toc[-15:]:
        indent = "  " * (level - 1)
        print(f"{indent}• {title} -> Page {page}")
        
    print(f"\nInjecting outlines into PDF...")
    doc.set_toc(toc)
    
    print(f"Saving to {output_pdf}...")
    doc.save(output_pdf, garbage=3, deflate=True)
    doc.close()
    
    print("Validating generated PDF...")
    check_doc = pymupdf.open(output_pdf)
    check_toc = check_doc.get_toc()
    print(f"Verification successful: {len(check_toc)} bookmarks saved in {output_pdf}.")
    check_doc.close()

if __name__ == "__main__":
    main()
