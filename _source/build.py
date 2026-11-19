#!/usr/bin/env python3
"""Builds the static multilingual site for santorinimesotopossuites.com into ../site"""
import json, os, html
from texts import T, LANGS, SLIDES, SLIDE_TEXT

SITE = "https://santorinimesotopossuites.com"
OUT = os.path.join(os.path.dirname(__file__), "..")
BOOKING_URL = "https://www.booking.com/hotel/gr/mesotopos.html"
EMAIL = "info@mesotopos.gr"
PHONE_DISPLAY = "+30 22860 24013"
PHONE_TEL = "+302286024013"
MAP_EMBED = "https://maps.google.com/maps?q=Santorini%20Mesotopos%2C%20Fira%2C%20Santorini&z=14&output=embed"
MAP_LINK = "https://www.google.com/maps/search/?api=1&query=Santorini+Mesotopos+Fira+Santorini"
FB = "https://www.facebook.com/Santorini.Mesotopos"
IG = "https://www.instagram.com/explore/locations/118027471/santorini-mesotopos/"

ICONS = {
 "pool": '<path d="M2 18c2 0 2-1.5 4-1.5S8 18 10 18s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5M2 22c2 0 2-1.5 4-1.5S8 22 10 22s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5M8 14V5a2 2 0 0 1 4 0M16 14V5a2 2 0 0 0-4 0M8 9h8"/>',
 "wifi": '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19.5" r="1"/>',
 "parking": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/>',
 "car": '<path d="M5 16V11l2-5h10l2 5v5M3 16h18v3H3zM7 19v2M17 19v2M5 11h14"/>',
 "plane": '<path d="M2 16l20-6-2-2-6 2-5-6-2 1 3 6-5 2-2-2-1 1 3 4z"/>',
 "map": '<path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2-6-2zM9 4v14M15 6v14"/>',
 "bag": '<rect x="4" y="7" width="16" height="13" rx="2"/><path d="M9 7V5a3 3 0 0 1 6 0v2"/>',
 "book": '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
 "clean": '<path d="M12 3l1.8 4.2L18 9l-4.2 1.8L12 15l-1.8-4.2L6 9l4.2-1.8zM19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/>',
 "heart": '<path d="M12 20s-7-4.5-9-9a5 5 0 0 1 9-3 5 5 0 0 1 9 3c-2 4.5-9 9-9 9z"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "jacuzzi": '<path d="M3 12h18v3a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5zM7 8c0-1 1-1 1-2s-1-1-1-2M12 8c0-1 1-1 1-2s-1-1-1-2M17 8c0-1 1-1 1-2s-1-1-1-2"/>',
}
def icon(name):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

FACILITIES = [("pool","f_pool"),("jacuzzi","f_jacuzzi"),("wifi","f_wifi"),("parking","f_parking"),
              ("plane","f_transfer"),("car","f_rental"),("map","f_tours"),("bag","f_luggage"),
              ("clean","f_maid"),("book","f_library"),("heart","f_bridal"),("sun","f_views")]

GALLERY = [("pool.jpg","g_pool","wide"),("sunset-terrace.jpg","g_sunset","tall"),("pergola.jpg","g_pergola",""),
           ("balcony-view.jpg","g_balcony",""),("suites-exterior.jpg","g_exterior","wide"),("jacuzzi.jpg","g_jacuzzi",""),
           ("village-view.jpg","g_village",""),("terrace-chairs.jpg","g_chairs","tall"),("living-detail.jpg","g_living","wide"),
           ("bathroom.jpg","g_bath",""),("pool-panorama.jpg","g_panorama","")]

ROOMS = [
  ("junior", ["junior-suite.jpg","junior-suite-2.jpg","pool.jpg"]),
  ("honeymoon", ["honeymoon-suite.jpg","honeymoon-suite-2.jpg","pergola.jpg"]),
  ("dome", ["dome-suite.jpg","dome-suite-loft.jpg","dome-suite-view.jpg"]),
]

def path_for(lang):
    return "/" if lang == "en" else f"/{lang}/"

def e(s):  # escape text
    return html.escape(s, quote=True)

def page(lang):
    t = T[lang]
    pre = "" if lang == "en" else "../"   # relative path to site root
    img = lambda f: f"{pre}images/{f}"
    book = f'{BOOKING_URL}?lang={t["booking_lang"]}'
    mail = f"mailto:{EMAIL}?subject={e(t['mail_subject'])}"

    alts = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{path_for(l)}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    options = "".join(f'<option value="{pre}{("" if l=="en" else l+"/")}index.html"{" selected" if l==lang else ""} lang="{l}">{LANGS[l]}</option>' for l in LANGS)

    ld = {"@context":"https://schema.org","@type":"Hotel","name":"Santorini Mesotopos Suites",
          "url":SITE+path_for(lang),"email":EMAIL,"telephone":PHONE_TEL,
          "image":SITE+"/images/slides/slide-1.jpg",
          "address":{"@type":"PostalAddress","addressLocality":"Fira","postalCode":"84700","addressRegion":"Santorini","addressCountry":"GR"},
          "checkinTime":"15:00","checkoutTime":"11:00","petsAllowed":False,
          "amenityFeature":[{"@type":"LocationFeatureSpecification","name":n,"value":True} for n in ["Outdoor pool","Jacuzzi","Free Wi-Fi","Free parking"]],
          "sameAs":[FB]}

    st = SLIDE_TEXT[lang]
    slides_html = "".join(
        f'<img class="slide{" is-active" if i==0 else ""}" src="{img("slides/"+f)}" alt="{e(st["alts"][i])}" width="1224" height="600"'
        + (' fetchpriority="high"' if i==0 else ' decoding="async"') + (' aria-hidden="true"' if i else '') + '>'
        for i,f in enumerate(SLIDES))
    dots_html = "".join(
        f'<button type="button" class="sc-dot{" is-active" if i==0 else ""}" data-i="{i}" aria-label="{e(st["slide"])} {i+1} / {len(SLIDES)}"{" aria-current=\"true\"" if i==0 else ""}></button>'
        for i in range(len(SLIDES)))
    rooms_html = ""
    for key, photos in ROOMS:
        r = t["rooms"][key]
        badge = f'<span class="badge">{e(r["badge"])}</span>' if r.get("badge") else ""
        meta = "".join(f"<li>{e(m)}</li>" for m in r["meta"])
        pics = "".join(f'<img src="{img(p)}" alt="{e(r["alts"][i])}" loading="lazy" width="1000" height="665">' for i,p in enumerate(photos))
        rooms_html += f'''
      <article class="room" id="room-{key}">
        <div class="room-photos">{pics}</div>
        <div class="room-body">
          {badge}
          <h3>{e(r["name"])}</h3>
          <ul class="room-meta">{meta}</ul>
          <p>{e(r["desc"])}</p>
          <a class="btn btn-ghost" href="{book}" target="_blank" rel="noopener">{e(t["check_avail"])}</a>
        </div>
      </article>'''

    inroom = "".join(f"<li>{e(x)}</li>" for x in t["in_room"])
    facs = "".join(f'<div class="fac">{icon(ic)}<h3>{e(t[k][0])}</h3><p>{e(t[k][1])}</p></div>' for ic,k in FACILITIES)
    gal = "".join(f'<a class="{cls}" href="{img(f)}" data-caption="{e(t[k])}"><img src="{img(f)}" alt="{e(t[k])}" loading="lazy"></a>' for f,k,cls in GALLERY)
    dist = "".join(f"<li><span>{e(a)}</span><span>{e(b)}</span></li>" for a,b in t["distances"])
    rules = "".join(f"<li>{e(x)}</li>" for x in t["rules"])
    nav = "".join(f'<a href="#{a}">{e(b)}</a>' for a,b in t["nav"])

    return f'''<!doctype html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["meta_desc"])}">
<link rel="canonical" href="{SITE}{path_for(lang)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["meta_desc"])}">
<meta property="og:image" content="{SITE}/images/slides/slide-1.jpg">
<meta property="og:url" content="{SITE}{path_for(lang)}">
<meta name="theme-color" content="#153a5a">
<link rel="icon" href="{pre}images/favicon.png">
<link rel="stylesheet" href="{pre}assets/style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{e(t["skip"])}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{pre}index.html" aria-label="Santorini Mesotopos Suites"><img src="{img('logo.png')}" alt="Santorini Mesotopos" width="168" height="80"></a>
    <nav class="nav" aria-label="{e(t["nav_label"])}">{nav}</nav>
    <div class="header-actions">
      <label class="lang"><span class="sr-only">{e(t["lang_label"])}</span>
        <select id="lang-switch" aria-label="{e(t["lang_label"])}">{options}</select>
      </label>
      <a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{e(t["book"])}</a>
    </div>
  </div>
</header>

<main id="main">
  <section class="hero" aria-labelledby="hero-title">
    <div class="slides" role="region" aria-roledescription="carousel" aria-label="{e(st["label"])}">{slides_html}</div>
    <div class="wrap">
      <p class="eyebrow">{e(t["hero_eyebrow"])}</p>
      <h1 id="hero-title">{e(t["hero_title"])}</h1>
      <p>{e(t["hero_text"])}</p>
      <div class="cta">
        <a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{e(t["book_booking"])}</a>
        <a class="btn btn-light" href="{mail}">{e(t["email_us"])}</a>
      </div>
      <ul class="facts">{"".join(f"<li>{e(x)}</li>" for x in t["hero_facts"])}</ul>
    </div>
    <div class="slide-ctrl">
      <button type="button" class="sc-btn" id="sc-prev" aria-label="{e(st["prev"])}">‹</button>
      <div class="sc-dots">{dots_html}</div>
      <button type="button" class="sc-btn" id="sc-pause" aria-label="{e(st["pause"])}" data-pause="{e(st["pause"])}" data-play="{e(st["play"])}"><span aria-hidden="true">❚❚</span></button>
      <button type="button" class="sc-btn" id="sc-next" aria-label="{e(st["next"])}">›</button>
    </div>
  </section>

  <section id="about" aria-labelledby="about-title">
    <div class="wrap about">
      <div>
        <p class="eyebrow">{e(t["about_eyebrow"])}</p>
        <h2 id="about-title">{e(t["about_title"])}</h2>
        {"".join(f'<p class="lede">{e(p)}</p>' if i==0 else f"<p>{e(p)}</p>" for i,p in enumerate(t["about_text"]))}
      </div>
      <img src="{img('suites-exterior.jpg')}" alt="{e(t["about_alt"])}" loading="lazy" width="1224" height="600">
    </div>
  </section>

  <section id="rooms" class="rooms" aria-labelledby="rooms-title">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">{e(t["rooms_eyebrow"])}</p>
        <h2 id="rooms-title">{e(t["rooms_title"])}</h2>
        <p class="lede">{e(t["rooms_text"])}</p>
      </div>
      <div class="room-list">{rooms_html}
      </div>
      <div class="in-room">
        <h3>{e(t["in_room_title"])}</h3>
        <ul class="chips">{inroom}</ul>
      </div>
    </div>
  </section>

  <section id="facilities" aria-labelledby="fac-title">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">{e(t["fac_eyebrow"])}</p>
        <h2 id="fac-title">{e(t["fac_title"])}</h2>
      </div>
      <div class="fac-grid">{facs}</div>
    </div>
  </section>

  <section id="gallery" class="gallery" aria-labelledby="gal-title">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">{e(t["gal_eyebrow"])}</p>
        <h2 id="gal-title">{e(t["gal_title"])}</h2>
        <p class="lede">{e(t["gal_text"])}</p>
      </div>
      <div class="gal">{gal}</div>
    </div>
  </section>

  <section id="location" aria-labelledby="loc-title">
    <div class="wrap loc">
      <div>
        <p class="eyebrow">{e(t["loc_eyebrow"])}</p>
        <h2 id="loc-title">{e(t["loc_title"])}</h2>
        <p class="lede">{e(t["loc_text"])}</p>
        <ul class="dist">{dist}</ul>
        <p style="margin-top:22px"><a class="btn btn-ghost" href="{MAP_LINK}" target="_blank" rel="noopener">{e(t["open_maps"])}</a></p>
      </div>
      <div class="map"><iframe title="{e(t["map_title"])}" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
    </div>
  </section>

  <section id="info" class="stay" aria-labelledby="info-title">
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">{e(t["info_eyebrow"])}</p>
        <h2 id="info-title">{e(t["info_title"])}</h2>
      </div>
      <div class="info-grid">
        <div class="info">
          <h3>{e(t["times_title"])}</h3>
          <dl><dt>{e(t["checkin"])}</dt><dd>15:00 – 22:00</dd><dt>{e(t["checkout"])}</dt><dd>{e(t["until"])} 11:00</dd></dl>
        </div>
        <div class="info">
          <h3>{e(t["rules_title"])}</h3>
          <ul>{rules}</ul>
        </div>
        <div class="info">
          <h3>{e(t["cancel_title"])}</h3>
          <p style="color:var(--muted);margin:0">{e(t["cancel_text"])}</p>
        </div>
      </div>
    </div>
  </section>

  <section id="contact" class="contact" aria-labelledby="contact-title">
    <div class="wrap">
      <p class="eyebrow" style="color:#ffd9c4">{e(t["contact_eyebrow"])}</p>
      <h2 id="contact-title">{e(t["contact_title"])}</h2>
      <p>{e(t["contact_text"])}</p>
      <div class="cta">
        <a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{e(t["book_booking"])}</a>
        <a class="btn btn-light" href="{mail}">{e(t["email_us"])}</a>
      </div>
      <ul class="contact-lines">
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
        <li>{e(t["address"])}</li>
      </ul>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div>
        <h3>Santorini Mesotopos Suites</h3>
        <p>{e(t["address"])}<br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></p>
        <p>{e(t["mhte"])}: 1015219</p>
      </div>
      <div>
        <h3>{e(t["follow"])}</h3>
        <ul>
          <li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
          <li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
          <li><a href="{book}" target="_blank" rel="noopener">{e(t["reviews_link"])}</a></li>
        </ul>
      </div>
      <div>
        <h3>{e(t["espa_title"])}</h3>
        <a class="espa" href="{pre}images/espa-plaque.pdf" target="_blank" rel="noopener"><img src="{img('espa-banner.jpg')}" alt="{e(t["espa_alt"])}" width="200" height="161" loading="lazy"></a>
      </div>
    </div>
    <div class="copy"><span>© <span id="yr">2026</span> Santorini Mesotopos Suites</span><span>{e(t["footer_note"])}</span></div>
  </div>
</footer>

<div class="mbar">
  <a class="btn btn-primary" href="{book}" target="_blank" rel="noopener">{e(t["book"])}</a>
  <a class="btn btn-ghost" href="{mail}">{e(t["email_short"])}</a>
</div>

<dialog class="lightbox" id="lb" aria-label="{e(t["gal_title"])}">
  <figure style="margin:0"><img id="lb-img" alt=""><figcaption id="lb-cap"></figcaption></figure>
  <button class="lb-close" id="lb-close" aria-label="{e(t["close"])}">×</button>
  <button class="lb-nav lb-prev" id="lb-prev" aria-label="{e(t["prev"])}">‹</button>
  <button class="lb-nav lb-next" id="lb-next" aria-label="{e(t["next"])}">›</button>
</dialog>

<script>
document.getElementById('yr').textContent=new Date().getFullYear();
document.getElementById('lang-switch').addEventListener('change',function(){{location.href=this.value||'./';}});
(function(){{
  var sl=[].slice.call(document.querySelectorAll('.slide')),dots=[].slice.call(document.querySelectorAll('.sc-dot')),pb=document.getElementById('sc-pause'),cur=0,timer=null;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches,playing=!reduce;
  function go(n){{sl[cur].classList.remove('is-active');sl[cur].setAttribute('aria-hidden','true');dots[cur].classList.remove('is-active');dots[cur].removeAttribute('aria-current');
    cur=(n+sl.length)%sl.length;sl[cur].classList.add('is-active');sl[cur].removeAttribute('aria-hidden');dots[cur].classList.add('is-active');dots[cur].setAttribute('aria-current','true');}}
  function start(){{stop();if(playing)timer=setInterval(function(){{go(cur+1);}},6000);}}
  function stop(){{if(timer)clearInterval(timer);timer=null;}}
  function setBtn(){{pb.setAttribute('aria-label',playing?pb.dataset.pause:pb.dataset.play);pb.firstElementChild.textContent=playing?'❚❚':'▶';}}
  document.getElementById('sc-prev').onclick=function(){{go(cur-1);start();}};
  document.getElementById('sc-next').onclick=function(){{go(cur+1);start();}};
  dots.forEach(function(d){{d.onclick=function(){{go(+d.dataset.i);start();}};}});
  pb.onclick=function(){{playing=!playing;setBtn();start();}};
  var hero=document.querySelector('.hero');
  hero.addEventListener('mouseenter',stop);hero.addEventListener('mouseleave',start);
  hero.addEventListener('focusin',stop);hero.addEventListener('focusout',start);
  document.addEventListener('visibilitychange',function(){{document.hidden?stop():start();}});
  setBtn();start();
}})();
(function(){{
  var links=[].slice.call(document.querySelectorAll('.gal a')),lb=document.getElementById('lb'),im=document.getElementById('lb-img'),cap=document.getElementById('lb-cap'),i=0;
  if(!lb.showModal)return;
  function show(n){{i=(n+links.length)%links.length;im.src=links[i].href;im.alt=links[i].dataset.caption;cap.textContent=links[i].dataset.caption;}}
  links.forEach(function(a,n){{a.addEventListener('click',function(ev){{ev.preventDefault();show(n);lb.showModal();}});}});
  document.getElementById('lb-close').onclick=function(){{lb.close();}};
  document.getElementById('lb-prev').onclick=function(){{show(i-1);}};
  document.getElementById('lb-next').onclick=function(){{show(i+1);}};
  lb.addEventListener('click',function(ev){{if(ev.target===lb)lb.close();}});
  lb.addEventListener('keydown',function(ev){{if(ev.key==='ArrowLeft')show(i-1);if(ev.key==='ArrowRight')show(i+1);}});
}})();
</script>
</body>
</html>
'''

def main():
    for lang in LANGS:
        d = OUT if lang == "en" else os.path.join(OUT, lang)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(lang))
    # sitemap + robots
    urls = "".join(f"<url><loc>{SITE}{path_for(l)}</loc></url>" for l in LANGS)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("built", list(LANGS))

if __name__ == "__main__":
    main()
