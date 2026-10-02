#!/usr/bin/env python3
"""
convert_stardict_to_vitepress.py
Parses StarDict data (23,261 entries) into VitePress Markdown pages and a client search index.
"""

import os
import sys
import struct
import html
import re
import json
import unicodedata
from collections import defaultdict

# Mapping of Sanskrit letters to file slugs and titles
LETTERS_MAP = [
    ('a', 'अ', 'a', 'a'),
    ('aa', 'आ', 'ā', 'aa'),
    ('i', 'इ', 'i', 'i'),
    ('ii', 'ई', 'ī', 'ii'),
    ('u', 'उ', 'u', 'u'),
    ('uu', 'ऊ', 'ū', 'uu'),
    ('r', 'ऋ', 'ṛ', 'r'),
    ('rr', 'ॠ', 'ṝ', 'rr'),
    ('l', 'ऌ', 'ḷ', 'l_vowel'),
    ('e', 'ए', 'e', 'e'),
    ('ai', 'ऐ', 'ai', 'ai'),
    ('o', 'ओ', 'o', 'o'),
    ('au', 'औ', 'au', 'au'),
    ('k', 'क', 'ka', 'ka'),
    ('kh', 'ख', 'kha', 'kha'),
    ('g', 'ग', 'ga', 'ga'),
    ('gh', 'घ', 'gha', 'gha'),
    ('ng', 'ङ', 'ṅa', 'nga'),
    ('c', 'च', 'ca', 'ca'),
    ('ch', 'छ', 'cha', 'cha'),
    ('j', 'ज', 'ja', 'ja'),
    ('jh', 'झ', 'jha', 'jha'),
    ('ny', 'ञ', 'ña', 'nya'),
    ('tt', 'ट', 'ṭa', 'tta'),
    ('tth', 'ठ', 'ṭha', 'ttha'),
    ('dd', 'ड', 'ḍa', 'dda'),
    ('ddh', 'ढ', 'ḍha', 'ddha'),
    ('nn', 'ण', 'ṇa', 'nna'),
    ('t', 'त', 'ta', 'ta'),
    ('th', 'थ', 'tha', 'tha'),
    ('d', 'द', 'da', 'da'),
    ('dh', 'ध', 'dha', 'dha'),
    ('n', 'न', 'na', 'na'),
    ('p', 'प', 'pa', 'pa'),
    ('ph', 'फ', 'pha', 'pha'),
    ('b', 'ब', 'ba', 'ba'),
    ('bh', 'भ', 'bha', 'bha'),
    ('m', 'म', 'ma', 'ma'),
    ('y', 'य', 'ya', 'ya'),
    ('ra', 'र', 'ra', 'ra'),
    ('la', 'ल', 'la', 'la'),
    ('v', 'व', 'va', 'va'),
    ('sh', 'श', 'śa', 'sha'),
    ('ss', 'ष', 'ṣa', 'ssa'),
    ('s', 'स', 'sa', 'sa'),
    ('h', 'ह', 'ha', 'ha')
]

def clean_iast(text):
    t = unicodedata.normalize('NFD', text)
    t = re.sub(r'[\u0300-\u036f]', '', t)
    return t.lower()

def clean_html_definition(raw_html):
    """
    Cleans up the definition HTML from StarDict for VitePress display:
    - Protects all valid HTML tags with placeholders
    - Restores authentic mathematical angle brackets ⟨ ⟩ used in Huet's TeX original
    - Replaces bword:// links with valid internal anchor links
    - Replaces font tags with semantic spans
    """
    t = raw_html.strip()
    # Remove trailing bullet symbols
    t = re.sub(r'<br\s*/?>\s*••\s*$', '', t)
    t = re.sub(r'••\s*$', '', t)
    
    # 1. Clean invalid </br> tags
    t = re.sub(r'</br\s*>', '<br>', t)
    t = re.sub(r'<br\s*/>', '<br>', t)
    
    # 2. Replace bword:// links first
    def link_repl(m):
        target = re.sub(r'[^a-zA-Z0-9_\-]', '_', m.group(1))
        inner = m.group(2)
        clean_lbl = re.sub(r'<[^>]+>', '', inner).strip()
        return f'<a href="#entry-{target}" class="skt-link">{clean_lbl}</a>'
        
    t = re.sub(r'<a\s+href="bword://([^"]+)">([\s\S]*?)</a>', link_repl, t)
    
    # 3. Replace font color tags with semantic spans
    t = re.sub(r'<font color="red">([\s\S]*?)</font>', r'<span class="skt-grammar">\1</span>', t)
    t = re.sub(r'<font color="blue">([\s\S]*?)</font>', r'<span class="skt-root">\1</span>', t)
    t = re.sub(r'<font color="#00008B">([\s\S]*?)</font>', r'<span class="skt-proper">\1</span>', t)
    t = re.sub(r'<font color="#FFA500">\|</font>', r'<span class="skt-pipe">|</span>', t)
    t = re.sub(r'</?font[^>]*>', '', t)
    
    # 4. Protect valid HTML tags with placeholders (tag must be followed by space, / or >)
    placeholders = []
    def tag_saver(m):
        placeholders.append(m.group(0))
        return f'___HTML_TAG_{len(placeholders)-1}___'

    t = re.sub(r'</?(?:span|div|a|i|b|br|em|strong|code)(?=[\s/>])[^>]*>', tag_saver, t)
    
    # 5. Convert remaining <...> (e.g. <i.>, <abl.>, <loc.>) to authentic mathematical brackets ⟨ ⟩
    t = re.sub(r'<([^>]+)>', r'⟨\1⟩', t)
    t = t.replace('<', '&lt;').replace('>', '&gt;')
    
    # 6. Restore valid HTML tags
    for idx, tag in enumerate(placeholders):
        t = t.replace(f'___HTML_TAG_{idx}___', tag)
        
    return t.strip()

def determine_letter_slug(raw_key, iast, deva):
    """
    Determines which letter section a word belongs to.
    """
    # Clean key
    k = raw_key.lstrip('-').lstrip('.').lstrip('√').strip()
    
    # Check IAST starting character
    clean_i = iast.lstrip('-').lstrip('.').lstrip('√').strip()
    if clean_i.startswith('ā'):
        return 'aa'
    if clean_i.startswith('ī'):
        return 'ii'
    if clean_i.startswith('ū'):
        return 'uu'
    if clean_i.startswith(('ṝ', 'r̥̄')):
        return 'rr'
    if clean_i.startswith(('ṛ', 'r̥')):
        return 'r'
    if clean_i.startswith(('ḷ', 'l̥')):
        return 'l_vowel'
    if clean_i.startswith('ai'):
        return 'ai'
    if clean_i.startswith('au'):
        return 'au'
    if clean_i.startswith('e'):
        return 'e'
    if clean_i.startswith('o'):
        return 'o'
    if clean_i.startswith('a'):
        return 'a'
    if clean_i.startswith('i'):
        return 'i'
    if clean_i.startswith('u'):
        return 'u'
        
    # Consonants
    if clean_i.startswith('kh'):
        return 'kha'
    if clean_i.startswith('k'):
        return 'ka'
    if clean_i.startswith('gh'):
        return 'gha'
    if clean_i.startswith('g'):
        return 'ga'
    if clean_i.startswith('ṅ'):
        return 'nga'
    if clean_i.startswith('ch'):
        return 'cha'
    if clean_i.startswith('c'):
        return 'ca'
    if clean_i.startswith('jh'):
        return 'jha'
    if clean_i.startswith('j'):
        return 'ja'
    if clean_i.startswith('ñ'):
        return 'nya'
    if clean_i.startswith('ṭh'):
        return 'ttha'
    if clean_i.startswith('ṭ'):
        return 'tta'
    if clean_i.startswith('ḍh'):
        return 'ddha'
    if clean_i.startswith('ḍ'):
        return 'dda'
    if clean_i.startswith('ṇ'):
        return 'nna'
    if clean_i.startswith('th'):
        return 'tha'
    if clean_i.startswith('t'):
        return 'ta'
    if clean_i.startswith('dh'):
        return 'dha'
    if clean_i.startswith('d'):
        return 'da'
    if clean_i.startswith('n'):
        return 'na'
    if clean_i.startswith('ph'):
        return 'pha'
    if clean_i.startswith('p'):
        return 'pa'
    if clean_i.startswith('bh'):
        return 'bha'
    if clean_i.startswith('b'):
        return 'ba'
    if clean_i.startswith('m'):
        return 'ma'
    if clean_i.startswith('y'):
        return 'ya'
    if clean_i.startswith('r'):
        return 'ra'
    if clean_i.startswith('l'):
        return 'la'
    if clean_i.startswith('v'):
        return 'va'
    if clean_i.startswith('ś') or k.startswith('z'):
        return 'sha'
    if clean_i.startswith('ṣ'):
        return 'ssa'
    if clean_i.startswith('s'):
        return 'sa'
    if clean_i.startswith('h'):
        return 'ha'
        
    return 'a'

def parse_entries():
    idx_file = 'input/goldendict/Heritage_du_sanskrit_san-fra/dictionnaire-heritage_du_sanskrit_san-fra.idx'
    dict_file = 'input/goldendict/Heritage_du_sanskrit_san-fra/dictionnaire-heritage_du_sanskrit_san-fra.dict'
    
    if not os.path.exists(idx_file) or not os.path.exists(dict_file):
        print(f"Error: StarDict files not found at {idx_file}", file=sys.stderr)
        sys.exit(1)
        
    p_root = re.compile(r'^\s*√\s*<span class=\"deva\" lang=\"sa\">([^<]+)</span>\s*<i>([^<]+)</i>')
    p_main = re.compile(r'^\s*<span class=\"deva\" lang=\"sa\">([^<]+)</span>\s*<i>([^<]+)</i>')
    p_sub = re.compile(r'^\s*<i>([^<]+)</i>')
    
    entries = []
    
    with open(idx_file, 'rb') as f_idx, open(dict_file, 'rb') as f_dict:
        idx_data = f_idx.read()
        pos = 0
        while pos < len(idx_data):
            null_pos = idx_data.find(b'\x00', pos)
            raw_key = idx_data[pos:null_pos].decode('utf-8')
            offset, size = struct.unpack('>II', idx_data[null_pos+1:null_pos+9])
            pos = null_pos + 9
            
            f_dict.seek(offset)
            raw_html = html.unescape(f_dict.read(size).decode('utf-8'))
            
            is_root = False
            deva = ""
            iast = ""
            
            m_r = p_root.match(raw_html)
            if m_r:
                is_root = True
                deva = m_r.group(1).strip()
                iast = m_r.group(2).strip()
            else:
                m_m = p_main.match(raw_html)
                if m_m:
                    deva = m_m.group(1).strip()
                    iast = m_m.group(2).strip()
                else:
                    m_s = p_sub.match(raw_html)
                    if m_s:
                        iast = m_s.group(1).strip()
                    else:
                        iast = raw_key
                        
            # Clean definition
            clean_def = clean_html_definition(raw_html)
            
            # Plain text definition for search index
            plain_def = re.sub(r'<[^>]+>', ' ', clean_def)
            plain_def = ' '.join(plain_def.split())[:200]
            
            slug = determine_letter_slug(raw_key, iast, deva)
            
            entries.append({
                'key': raw_key,
                'slug': slug,
                'iast': iast,
                'deva': deva,
                'is_root': is_root,
                'html': clean_def,
                'plain_def': plain_def,
                'clean_iast': clean_iast(iast)
            })
            
    return entries

def main():
    print("Reading and parsing StarDict database...")
    entries = parse_entries()
    print(f"Total entries loaded: {len(entries)}")
    
    docs_dir = "docs"
    dict_dir = os.path.join(docs_dir, "dict")
    public_dir = os.path.join(docs_dir, "public")
    os.makedirs(dict_dir, exist_ok=True)
    os.makedirs(public_dir, exist_ok=True)
    
    # Group entries by letter slug and write markdown pages
    by_letter = defaultdict(list)
    for e in entries:
        by_letter[e['slug']].append(e)
        
    slug_to_info = {item[3]: item for item in LETTERS_MAP}
    
    print("\nWriting dictionary markdown pages...")
    for slug, letter_entries in sorted(by_letter.items()):
        info = slug_to_info.get(slug, (slug, '', slug, slug))
        deva_letter = info[1]
        iast_letter = info[2]
        
        md_file = os.path.join(dict_dir, f"{slug}.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"title: \"{deva_letter} ({iast_letter}) - Héritage du Sanskrit\"\n")
            f.write(f"description: \"Section {deva_letter} ({iast_letter}) du Dictionnaire sanskrit-français\"\n")
            f.write(f"outline: false\n")
            f.write(f"---\n\n")
            
            f.write(f"# <span class=\"deva-large\">{deva_letter}</span> <span class=\"iast-large\">{iast_letter}</span>\n\n")
            f.write(f"<div class=\"dict-page-header\">\n")
            f.write(f"  <span class=\"badge-count\">{len(letter_entries)} entrées</span>\n")
            f.write(f"  <a href=\"../\" class=\"back-link\">← Index du dictionnaire</a>\n")
            f.write(f"</div>\n\n")
            f.write(f"---\n\n")
            
            for item in letter_entries:
                clean_k = re.sub(r'[^a-zA-Z0-9_\-]', '_', item['key'])
                anchor_id = f"entry-{clean_k}"
                f.write(f"<div class=\"skt-entry\" id=\"{anchor_id}\">\n")
                f.write(f"  <div class=\"skt-entry-content\">\n")
                f.write(f"    {item['html']}\n")
                f.write(f"  </div>\n")
                f.write(f"</div>\n\n")
                
        print(f"  • {md_file}: {len(letter_entries)} entries.")
        
    print("\nDictionary generation complete!")

if __name__ == "__main__":
    main()
