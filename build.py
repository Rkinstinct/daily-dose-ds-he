#!/usr/bin/env python3
"""Reads issues.json and writes index.html (static, Hebrew RTL).
Run: python3 build.py"""
import json, html, collections
SRC = "https://blog.dailydoseofds.com"
css = open('base.css').read() + """
.lec{background:var(--card,#111317);border:1px solid #24282f;border-radius:16px;padding:20px;margin:16px 0}
.lec h3{margin:0 0 4px;font-size:1.15rem;direction:ltr;text-align:right}.meta{color:#9aa0a8;font-size:.85rem;margin:0 0 12px}
.tags span{display:inline-block;border:1px solid #3a3f48;border-radius:999px;padding:2px 10px;margin:0 0 6px 6px;font-size:.78rem;color:#c9ced6}
.lec ul{padding-right:20px}.lec li{margin:6px 0}.aud{border-top:1px solid #24282f;margin-top:12px;padding-top:10px;color:#c9ced6}
.src{display:inline-block;margin-top:10px;color:#F7931A;text-decoration:none;font-weight:600}
.daytitle{margin-top:36px}.note{color:#9aa0a8;font-size:.9rem}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0}.toc a{border:1px solid #24282f;border-radius:999px;padding:6px 14px;font-size:.85rem;color:#9aa0a8;text-decoration:none}
"""
L = json.load(open('issues.json'))
L.sort(key=lambda x: x['date'], reverse=True)
HEB = ['ינואר','פברואר','מרץ','אפריל','מאי','יוני','יולי','אוגוסט','ספטמבר','אוקטובר','נובמבר','דצמבר']
def dlabel(d):
    y, m, dd = d.split('-'); return f"{int(dd)} ב{HEB[int(m)-1]} {y}"
groups = collections.OrderedDict()
for x in L: groups.setdefault(x['date'], []).append(x)
body = []; toc = []
for d, items in groups.items():
    toc.append(f'<a href="#d{d}">{dlabel(d)}</a>')
    cards = []
    for x in items:
        s = x['summary_he']
        pts = ''.join(f'<li>{html.escape(p)}</li>' for p in s['points'])
        tags = ''.join(f'<span>{html.escape(t)}</span>' for t in s['tags'])
        notes = []
        if x['access'] != 'full': notes.append('התוכן המלא של הגיליון לא היה נגיש (חסום בתשלום), והסיכום מבוסס על החלק הציבורי בלבד.')
        if s.get('note'): notes.append(s['note'])
        nt = f'<p class="note">{html.escape(" ".join(notes))}</p>' if notes else ''
        cards.append(f'''<article class="lec" id="{x['slug']}"><h3>{html.escape(x['title'])}</h3>
<p class="meta">{dlabel(x['date'])}</p>
<p><strong>בקצרה:</strong> {html.escape(s['tldr'])}</p><ul>{pts}</ul>
<p class="aud"><strong>למי זה מתאים:</strong> {html.escape(s['audience'])}</p>{nt}
<div class="tags">{tags}</div><a class="src" href="{x['url']}" rel="noopener" target="_blank">לגיליון המקורי ←</a></article>''')
    body.append(f'<section class="section" id="d{d}"><div class="wrap"><h2 class="daytitle">{dlabel(d)}</h2>{"".join(cards)}</div></section>')
n = len(L)
page = f'''<!DOCTYPE html>
<html dir="rtl" lang="he"><head><meta charset="utf-8"/><meta content="width=device-width, initial-scale=1" name="viewport"/><meta content="#030304" name="theme-color"/><meta content="הסברים בעברית לגיליונות הניוזלטר Daily Dose of Data Science" name="description"/><title>Daily Dose of Data Science בעברית | DATA&amp;AI</title><link href="https://fonts.googleapis.com" rel="preconnect"/><link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600;700;800&amp;family=Space+Grotesk:wght@500;700&amp;display=swap" rel="stylesheet"/><style>{css}</style></head><body>
<header class="top"><div class="wrap"><a class="brand" href="https://rkinstinct.github.io/data-ai-hub/">DATA<span style="color:#F7931A">&amp;</span>AI <b>/ Daily Dose of DS</b></a></div></header>
<main id="main"><div class="hero"><div class="wrap"><div class="eyebrow">DAILY DOSE OF DATA SCIENCE · מדריך בעברית</div><h1>Daily Dose of Data Science בעברית</h1>
<p class="lead">הסבר בעברית לכל גיליון של הניוזלטר <a href="{SRC}" rel="noopener" target="_blank" style="color:#F7931A">Daily Dose of Data Science</a>. כל כרטיס נכתב מתוכן הגיליון עצמו, מהחדש לישן, עם הנקודות העיקריות וקישור לגיליון המקורי.</p>
<p class="note">{n} גיליונות עד כה, כולם נגישים במלואם בארכיון הציבורי. בכל כרטיס מצוין אם יש בגיליון חסות או אם חלק ממנו לא סוכם. הקוד והמספרים הם כפי שהם מופיעים בגיליון, ולא נבדקו בנפרד. Jev הוא מודל של TypeSafe AI להחלטות מוקלדות, והוא מופיע בגיליונות רבים בסדרה.</p>
<div class="toc">{''.join(toc)}</div></div></div>
{''.join(body)}</main>
<footer><div class="wrap"><span>הסברים עצמאיים, לא פרסום רשמי של Daily Dose of Data Science. התוכן המקורי שייך ליוצריו.</span></div><p class="rights-line" style="text-align:center;margin:18px auto 0;padding:0 16px;font-size:.92em;opacity:.9;width:100%">© כל הזכויות שמורות לראובן קזורר</p></footer></body></html>'''
open('index.html', 'w').write(page)
print('built', n, 'issues,', len(page), 'bytes')
