"""One-off: turn the Davies index.html into the gerrodkottman.com page (run once on a fresh copy)."""
import sys, html
path = sys.argv[1]
L = open(path).read().split("\n")
head, hero, work, feature = L[:122], L[122:181], L[181:363], L[363:477]
cta_foot = L[1538:]
P = [  # name, tag, license/status, image, url
 ("Mortiflix", "Motion design studio", "AGPL", "mortiflix", "https://mortiflix.com"),
 ("MoBlend", "Blender MoGraph", "GPL", "moblend", "https://github.com/GTKottman/moblend"),
 ("Nova FX", "Blender FX engine", "GPL", "nova", "https://github.com/GTKottman/nova-fx"),
 ("Strata", "Mastering plugin", "GPL", "strata", "https://gtkottman.github.io/strata/"),
 ("Mortiflix Music", "Music studio", "AGPL", "music", "https://github.com/GTKottman/mortiflix-music-oss"),
 ("Mortiflix Singer", "Singing synth", "OSS", "singer", "https://github.com/GTKottman/mortiflix-singer"),
 ("Remotion Transitions", "Transition library", "MIT", "transitions", "https://github.com/GTKottman/remotion-transitions"),
 ("Blender Multiplayer", "Live co-editing", "OSS", "multiplayer", "https://github.com/GTKottman/blender-multiplayer"),
 ("Hollowell", "Godot tycoon game", "SOON", "hollowell", None),
 ("Kottman Consulting", "Business site", "LIVE", "kottman", "https://kottmanconsulting.com"),
]
T = "\n".join
s_head = T(head).replace("""<li class="menu-item"><a href="#serviceScroll" class="item-link link text-caption"><span>02
                                                /</span>SERVICES</a>
                                    </li>
                                    <li class="menu-item"><a href="#aboutScroll" class="item-link link text-caption"><span>03
                                                /</span>ABOUT</a></li>
                                    <li class="menu-item"><a href="#contactScroll" class="item-link link text-caption"><span>04""",
 """<li class="menu-item"><a href="#projectsScroll" class="item-link link text-caption"><span>02
                                                /</span>PROJECTS</a>
                                    </li>
                                    <li class="menu-item"><a href="#contactScroll" class="item-link link text-caption"><span>03""")
s_head = s_head.replace('content="Gerrod Kottman - Personal Portfolio"', 'content="Gerrod Kottman builds open-source studios, Blender tools, audio plugins and games."')
s_hero = T(hero)
for a, b in [('<source src="assets/images/video/corridor.webm" type="video/mp4">',
              '<source src="assets/images/video/hero-wave.webm" type="video/webm">\n                    <source src="assets/images/video/hero-wave.mp4" type="video/mp4">'),
             ('>WEB-DESIGNER<', '>OPEN SOURCE<'), ('>BLOGER<', '>BLENDER<'), ('>TREND ANALYST<', '>AUDIO<'),
             ("""I craft bold brands and modern websites with purpose. Each detail balances design and usability for
                                        impact. My
                                        work
                                        adapts as your vision grows.""",
              """I build open-source creative studios, Blender tools, audio plugins and games, then make the work with them."""),
             ('href="#contactScroll" class="tf-btn ">\n                                            START A PROJECT',
              'href="#workScroll" class="tf-btn ">\n                                            SEE THE WORK')]:
    assert a in s_hero, a[:40]; s_hero = s_hero.replace(a, b)
# selected works: 3 slides
s_work = T(work)
names = ["Future", "NexoPay", "Seeson"]; new = ["Mortiflix", "MoBlend", "Nova FX"]
for a, b in zip(names, new): s_work = s_work.replace(f'fw-semibold">{a}</p>', f'fw-semibold">{b}</p>')
for i, img in enumerate(["mortiflix", "moblend", "nova"], 1):
    s_work = s_work.replace(f'src="assets/images/section/work-{i}.jpg"', f'src="assets/images/projects/{img}.jpg"')
s_work = s_work.replace('alt="Image">', 'alt="">')
import re
s_work = re.sub(r'\s*<div class="image-award">.*?</div>', '', s_work, flags=re.S)
tags = [["VIDEO", "OPEN SOURCE"], ["BLENDER", "MOGRAPH", "MCP"], ["BLENDER", "FX"]] * 2
lis = re.findall(r'<li>\s*<div class="group-btn">.*?</div>\s*</li>', s_work, flags=re.S)
assert len(lis) == 6
for li, tg in zip(lis, tags):
    btns = "".join(f'\n                                        <span class="tf-btn style-2">\n                                            {t}\n                                        </span>' for t in tg)
    s_work = s_work.replace(li, f'<li>\n                                    <div class="group-btn">{btns}\n                                    </div>\n                                </li>', 1)
s_work = s_work.replace('20<span class="text-primary">25</span>', '20<span class="text-primary">26</span>')
# all projects
cards = []
for name, tag, lic, img, url in P:
    href = url or "#projectsScroll"
    ext = ' target="_blank" rel="noopener"' if url else ''
    cards.append(f'''                            <div class="swiper-slide">
                                <div class="wg-feature-v01 hover-img main-mouse-hover">
                                    <a href="{href}"{ext} class="feature-image img-style">
                                        <img loading="lazy" width="628" height="471" src="assets/images/projects/{img}.jpg" alt="{html.escape(name)}">
                                    </a>
                                    <div class="feature-content">
                                        <div class="info">
                                            <p class="tag text-white-64 letter-space--1">{tag}</p>
                                            <h5 class="name letter-space--2">
                                                <a href="{href}"{ext} class="link">{html.escape(name)}</a>
                                            </h5>
                                        </div>
                                        <h5 class="price letter-space--2 text-primary">
                                            {lic}
                                        </h5>
                                    </div>
                                    <div class="tf-mouse">
                                        <a href="{href}"{ext} class="action tf-btn-2">
                                            <i class="icon icon-arrow-long-right"></i>
                                        </a>
                                    </div>
                                </div>
                            </div>''')
s_feat = T(feature)
s_feat = s_feat.replace('<section class="section-feature flat-spacing tf-btn-swiper-main">', '<section class="section-feature flat-spacing tf-btn-swiper-main" id="projectsScroll">')
s_feat = s_feat.replace("Featured Templates", "All projects")
s_feat = s_feat.replace('<a href="#" class="tf-btn">\n                        BROWSE ALL', '<a href="https://github.com/GTKottman" target="_blank" rel="noopener" class="tf-btn">\n                        GITHUB')
s_feat = re.sub(r'<div class="swiper-wrapper">.*?</div>\s*<div class="group-btn-slider">',
                '<div class="swiper-wrapper">\n' + "\n".join(cards) + '\n                        </div>\n                        <div class="group-btn-slider">', s_feat, count=1, flags=re.S)
# CTA + footer + mobile menu
s_end = T(cta_foot)
s_end = re.sub(r'<form class="form-cta">.*?</form>', '''<div class="form-cta">
                            <div class="form-action">
                                <a href="mailto:hello@kottmanconsulting.com" class="tf-btn">
                                    <span class="text-caption">EMAIL ME</span>
                                </a>
                                <p class="text-body-1">
                                    say hello - <a href="mailto:hello@kottmanconsulting.com" class="text-primary">hello@kottmanconsulting.com</a>
                                </p>
                            </div>
                        </div>''', s_end, count=1, flags=re.S)
s_end = s_end.replace('''<li><a href="#aboutScroll" class="link letter-space--2 h5">About</a></li>
                                <li><a href="#workScroll" class="link letter-space--2 h5">Works</a></li>
                                <li><a href="#serviceScroll" class="link letter-space--2 h5">Services</a></li>''',
 '''<li><a href="#workScroll" class="link letter-space--2 h5">Works</a></li>
                                <li><a href="#projectsScroll" class="link letter-space--2 h5">Projects</a></li>''')
s_end = s_end.replace('''<li><a href="#" class="link letter-space--2 h5">Twitter (X)</a></li>
                                <li><a href="#" class="link letter-space--2 h5">Dribbble</a></li>
                                <li><a href="#" class="link letter-space--2 h5">LinkedIn</a></li>''',
 '''<li><a href="https://github.com/GTKottman" target="_blank" rel="noopener" class="link letter-space--2 h5">GitHub</a></li>
                                <li><a href="https://mortiflix.com" target="_blank" rel="noopener" class="link letter-space--2 h5">Mortiflix</a></li>''')
s_end = s_end.replace("WORKING GLOBALLY", "TEXAS, USA")
s_end = s_end.replace('<a href="#aboutScroll" class="mb-menu-link text-display-1">\n                                        <span class="text">About</span>',
                      '<a href="#projectsScroll" class="mb-menu-link text-display-1">\n                                        <span class="text">Projects</span>').replace("View About", "View Projects")
s_end = re.sub(r'\s*<li>\s*<div class="item close-mb-menu">\s*<a href="#serviceScroll".*?</li>', '', s_end, count=1, flags=re.S)
s_end = re.sub(r'<div class="right">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*<!-- /Mobile Menu -->',
  '''<div class="right">
                            <a href="https://github.com/GTKottman" target="_blank" rel="noopener" class="tf-link-icon text-caption link">
                                <i class="icon icon-arrow-top-right"></i>
                                GITHUB
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- /Mobile Menu -->''', s_end, count=1, flags=re.S)
open(path, "w").write(T([s_head, s_hero, s_work, s_feat, "        <!-- CTA -->"]) + "\n" + s_end.split("<!-- CTA -->", 1)[1] if "<!-- CTA -->" in s_end else T([s_head, s_hero, s_work, s_feat, s_end]))
print("ok")
