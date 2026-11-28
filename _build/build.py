"""Writes the NSMG public static site into ~/nsmg-public-site (plain HTML/CSS, no build step in the repo).
Content comes verbatim from the portal LWCs in ~/nsmg-community (certData.js / fellowshipData.js via data.json).
The public contact email is read from the NSMG_CONTACT_EMAIL environment variable (set it yourself)."""
import json, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.expanduser('~/nsmg-public-site')
D = json.load(open(os.path.join(HERE, 'data.json')))
E = html.escape
SITE = 'https://www.nationalspinemanagement.com'
PORTAL = 'https://nsmg.my.site.com/nsmg/s/'
LOGIN = 'https://nsmg.my.site.com/nsmg/s/login'
SCHED = 'https://nsmg.my.site.com/schedule/s/flow/CreateAppointment'
AIC_PORTAL = 'https://nsmg.my.site.com/nsmg/s/advanced-imaging-certification'
FS_PORTAL = 'https://nsmg.my.site.com/nsmg/s/fellowship-in-spine-management'
# 2027 National Conference links, copied from the portal homepage components (nsmgConferenceCard buttonUrl / hotelUrl).
# The portal stores the registration link as a site path; the portal base is prefixed here.
CONF_REGISTER = 'https://nsmg.my.site.com/nsmg/s/learning-activity-detail-standard?ltui__urlRecordId=a1jRc000006eNwvIAE&ltui__urlRedirect=learning-activity-detail-standard'
CONF_HOTEL = 'https://www.marriott.com/event-reservations/reservation-link.mi?id=1794501919101&key=GRP&app=resvlink&_branch_match_id=1652725825054783307&_branch_referrer=H4sIAAAAAAAAA8soKSkottLXTywo0MtNLCrKzC8p0UvOz9UvSi0uy0wtN7LPTLE1NLc0MTUwtDS0NDQwVMtOrbR1DwpQSywosAWpysnMy1arK0pNSy0qysxLj08qyi8vTi2ydc4oys9NBQB9I7QtYQAAAA%3D%3D'
LINKEDIN = 'https://www.linkedin.com/in/william-owens-dc-fsbt-58a85719/'
ADDR = {'street': '1275 Main Street, Suite 110', 'city': 'Buffalo', 'region': 'NY', 'zip': '14209'}
PHONE, PHONE_TEL = '716-228-3847', '+17162283847'
EMAIL = os.environ.get('NSMG_CONTACT_EMAIL') or 'EMAIL-NOT-SET'
ORG = 'National Spine Management Group'
ROMAN = ['I', 'II', 'III']

MODS = D['MODULES']; COURSES = D['COURSES']; BIB = D['BIBLIOGRAPHY']; ROTS = D['ROTATIONS']; ICONS = D['ICONS']
TOTAL_H = sum(m['h'] for m in MODS)
C_H = [sum(m['h'] for m in MODS[i * 6:i * 6 + 6]) for i in range(3)]

STAR = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 15.6 6.6 18.5l1.2-6L3.3 8.3l6.1-.7z" fill="#D4A017"/></svg>'


def ld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + '\n</script>'


def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


def faq_ld(faq):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}


def faq_html(faq, title):
    items = ''.join(f'<div class="qa"><h3>{E(q)}</h3><p>{E(a)}</p></div>' for q, a in faq)
    return f'''
<section class="band" id="faq">
 <div class="wrap">
  <p class="eyebrow">Questions</p>
  <h2>{E(title)}</h2>
  <div class="faq">{items}</div>
 </div>
</section>'''


SHARE_MAP = {
    'index.html': 'share-home.png',
    'advanced-imaging-certification/index.html': 'share-advanced-imaging-certification.png',
    'fellowship-in-spine-management/index.html': 'share-fellowship.png',
    'national-conference/index.html': 'share-national-conference.png',
    'about/index.html': 'share-about.png',
    'contact/index.html': 'share-contact.png',
}

def page(path, title, desc, body, lds, active='', not_found=False):
    depth = path.count('/')
    root = '../' * depth
    canon = SITE + '/' + (path.rsplit('index.html', 1)[0])
    cur = lambda key: ' aria-current="page"' if key == active else ''
    if not_found:
        # GitHub Pages serves 404.html at whatever path was requested, so links resolve against a fixed base:
        # "/" on the custom domain, "/nsmg-public-site/" on the temporary github.io address.
        head_extra = ('<base href="/">\n<script>if(/\\.github\\.io$/.test(location.hostname))'
                      'document.querySelector("base").href="/nsmg-public-site/";</script>\n'
                      '<meta name="robots" content="noindex">')
    else:
        head_extra = f'<link rel="canonical" href="{canon}">\n<meta name="robots" content="index, follow">'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{head_extra}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{ORG}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/images/share/{SHARE_MAP.get(path, 'share-home.png')}">
<meta property="og:image:alt" content="{E(title)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{root}images/nsmg-icon.png">
<link rel="apple-touch-icon" href="{root}images/nsmg-icon.png">
<link rel="stylesheet" href="{root}styles.css">
<script>document.documentElement.classList.add('js');</script>
{chr(10).join(ld(x) for x in lds)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
 <div class="wrap bar">
  <a class="brand" href="{root or './'}"><img src="{root}images/nsmg-logo.png" alt="" width="40" height="48"><span><b>National Spine Management Group</b><small>Leaders in Academic Spinal Care</small></span></a>
  <nav aria-label="Main" class="main-nav">
   <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="nav-links"><span class="nav-toggle-bars" aria-hidden="true"></span><span class="nav-toggle-label">Menu</span></button>
   <div class="nav-links" id="nav-links">
   <a href="{root or './'}"{cur('home')}>Home</a>
   <details class="menu">
    <summary>Certifications</summary>
    <div class="menu-list">
     <a href="{root}advanced-imaging-certification/"{cur('aic')}>Advanced Imaging Certification</a>
     <a href="{root}fellowship-in-spine-management/"{cur('fs')}>Fellowship in Spine Management</a>
    </div>
   </details>
   <a href="{root}national-conference/"{cur('conf')}>Conference</a>
   <a href="{root}about/"{cur('about')}>About</a>
   <a href="{root}contact/"{cur('contact')}>Contact</a>
   <a href="{PORTAL}">Member Portal</a>
   </div>
   <a class="btn gold sm" href="{LOGIN}">Member Login</a>
  </nav>
 </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
 <div class="wrap foot">
  <div>
   <p class="fname">National Spine Management Group</p>
   <p class="ftag">Leaders in Academic Spinal Care</p>
  </div>
  <div>
   <address>{ADDR['street']}, {ADDR['city']}, {ADDR['region']} {ADDR['zip']}<br>
   <a href="tel:{PHONE_TEL}">{PHONE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></address>
  </div>
  <nav aria-label="Footer">
   <a href="{root}advanced-imaging-certification/">Advanced Imaging Certification</a>
   <a href="{root}fellowship-in-spine-management/">Fellowship in Spine Management</a>
   <a href="{root}national-conference/">2027 National Conference</a>
   <a href="{root}about/">About Dr. Owens</a>
   <a href="{root}contact/">Contact</a>
   <a href="{PORTAL}">Member Portal</a>
   <a href="{LOGIN}">Member Login</a>
   <a href="{SCHED}">Schedule a Consultation</a>
  </nav>
 </div>
 <div class="wrap copy">© National Spine Management Group</div>
</footer>
<script>
// Close the Certifications menu when clicking elsewhere or pressing Escape (the menu works without this).
document.addEventListener('click',function(e){{document.querySelectorAll('details.menu[open]').forEach(function(d){{if(!d.contains(e.target))d.removeAttribute('open');}});}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')document.querySelectorAll('details.menu[open]').forEach(function(d){{d.removeAttribute('open');}});}});
// Small screens: the Menu button shows and hides the nav links. The links are always in the HTML;
// without JavaScript they are simply shown, and on wide screens the button is hidden.
(function(){{
  var nav=document.querySelector('.main-nav'), btn=nav&&nav.querySelector('.nav-toggle');
  if(!btn)return;
  function setOpen(open){{nav.classList.toggle('is-open',open);btn.setAttribute('aria-expanded',open?'true':'false');}}
  btn.addEventListener('click',function(){{setOpen(btn.getAttribute('aria-expanded')!=='true');}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&nav.classList.contains('is-open')){{setOpen(false);btn.focus();}}}});
  document.addEventListener('click',function(e){{if(nav.classList.contains('is-open')&&!nav.contains(e.target))setOpen(false);}});
}})();
</script>
</body>
</html>
'''


ORG_LD = {'@context': 'https://schema.org', '@type': 'EducationalOrganization', '@id': SITE + '/#organization',
          'name': ORG, 'alternateName': 'NSMG', 'slogan': 'Leaders in Academic Spinal Care', 'url': SITE + '/',
          'logo': SITE + '/images/nsmg-logo.png', 'image': SITE + '/images/nsmg-share.png',
          'description': 'Clinical training, documentation that holds up to scrutiny, and referral relationships with attorneys and physicians — taught as one system by National Spine Management Group.',
          'email': EMAIL, 'telephone': PHONE_TEL,
          'address': {'@type': 'PostalAddress', 'streetAddress': ADDR['street'], 'addressLocality': ADDR['city'], 'addressRegion': ADDR['region'], 'postalCode': ADDR['zip'], 'addressCountry': 'US'},
          'founder': {'@type': 'Person', 'name': 'William J. Owens Jr., DC, FSBT'}}
PROVIDER = {'@type': 'EducationalOrganization', '@id': SITE + '/#organization', 'name': ORG, 'url': SITE + '/'}

# ---------------------------------------------------------------- HOME
PILLARS = [('Educate', 'Train at the academic level', 'Graduate-level spine education, from on-demand courses to a structured fellowship.'),
           ('Document', 'Build records that stand up', 'Diagnosis, imaging and impairment documentation aligned to the standards reviewers use.'),
           ('Connect', 'Earn the referrals', 'Speak the language of attorneys and physicians, and become their first call.'),
           ('Grow', 'Run a practice that scales', 'Practice development for doctors and their teams, with systems your staff can run.')]
home_body = f'''
<section class="hero band">
 <div class="wrap herohome">
  <div>
   <p class="kicker">Leaders in Academic Spinal Care</p>
   <h1>National Spine Management Group</h1>
   <p class="lede big">The complete system for spine-focused chiropractic practice.</p>
   <p class="lede">Clinical training, documentation that holds up to scrutiny, and referral relationships with attorneys and physicians — taught as one system by National Spine Management Group.</p>
   <div class="btns">
    <a class="btn gold" href="{LOGIN}">Member Login</a>
    <a class="btn ghost" href="{PORTAL}">Visit the Member Portal</a>
    <a class="btn ghost" href="{SCHED}">Schedule a Consultation</a>
   </div>
  </div>
  <div class="logocard"><img src="images/nsmg-logo.png" alt="National Spine Management Group logo" width="160" height="190"><p>National Spine Management Group</p><small>Leaders in Academic Spinal Care</small></div>
 </div>
</section>

<section class="band tintband">
 <div class="wrap">
  <p class="eyebrow">The NSMG system</p>
  <h2>Four parts. One way of practicing.</h2>
  <p class="sub">Each program stands on its own, and they are built to work together.</p>
  <div class="pillars">
   {''.join(f'<div><span class="tag">{E(a)}</span><h3>{E(b)}</h3><p>{E(c)}</p></div>' for a, b, c in PILLARS)}
  </div>
 </div>
</section>

<section class="band">
 <div class="wrap">
  <p class="eyebrow">Certifications</p>
  <h2>Post-doctoral training for doctors of chiropractic</h2>
  <div class="certs">
   <article class="cert">
    <div class="pace">{STAR} Approved through the FCLB PACE program</div>
    <h3><a href="advanced-imaging-certification/">Advanced Imaging Certification</a></h3>
    <p>The Spine Management Pathway: an 18-module MRI curriculum for doctors of chiropractic, built on case-based DICOM review and developed by the National Spine Management Group in collaboration with Medality™.</p>
    <ul class="facts"><li><b>18</b> modules</li><li><b>3</b> six-module courses</li><li><b>{TOTAL_H}</b> CE hours</li><li><b>90</b> MRI cases submitted</li></ul>
    <a class="btn navy" href="advanced-imaging-certification/">About the Advanced Imaging Certification</a>
   </article>
   <article class="cert">
    <div class="pace">{STAR} Two-year post-doctoral fellowship for doctors of chiropractic</div>
    <h3><a href="fellowship-in-spine-management/">Fellowship in Spine Management</a></h3>
    <p>Imaging mastery in Year One, then a year of clinical rotations. Interprofessional rotations, coordinated within your own community with the help of NSMG, train chiropractors to work as spine-care navigators alongside radiology, orthopedics, neurosurgery and pain management.</p>
    <ul class="facts"><li><b>2</b> years, post-doctoral</li><li><b>18</b> imaging modules in Year One</li><li><b>6</b> clinical rotations in Year Two</li><li><b>30+</b> peer-reviewed articles per rotation</li></ul>
    <a class="btn navy" href="fellowship-in-spine-management/">About the Fellowship in Spine Management</a>
   </article>
  </div>
 </div>
</section>

<section class="band tintband cta">
 <div class="wrap">
  <h2>Ready to build your system?</h2>
  <p>Book a call with our team, or sign in to the NSMG Member Portal.</p>
  <div class="btns center">
   <a class="btn gold" href="{SCHED}">Schedule a Consultation</a>
   <a class="btn navy" href="{PORTAL}">Visit the Member Portal</a>
   <a class="btn navy" href="{LOGIN}">Member Login</a>
  </div>
 </div>
</section>'''

home = page('index.html', 'National Spine Management Group | Leaders in Academic Spinal Care',
            'National Spine Management Group: clinical training, documentation and referral relationships for spine-focused chiropractic practice, with the Advanced Imaging Certification and the Fellowship in Spine Management.',
            home_body, [ORG_LD, {'@context': 'https://schema.org', '@type': 'WebSite', 'name': ORG, 'url': SITE + '/', 'publisher': {'@id': SITE + '/#organization'}},
                        crumbs_ld([('Home', SITE + '/')])], 'home')

# ---------------------------------------------------------------- IMAGING
def linkify(ref):
    parts = re.split(r'(https?://[^\s]+[^\s.,;)])', ref)
    return ''.join(f'<a href="{E(p)}" rel="noopener">{E(p)}</a>' if p.startswith('http') else E(p) for p in parts)

tiles = ''
for ci in range(3):
    row = ''.join(f'<a class="tile" href="#m{i + 1}" title="Module {i + 1}: {E(MODS[i]["t"])}"><img src="../images/modules/AIC_Module_{i + 1:02d}.jpg" alt="Module {i + 1}: {E(MODS[i]["t"])}" width="320" height="180" loading="lazy"></a>' for i in range(ci * 6, ci * 6 + 6))
    row_label = COURSES[ci]['range'].replace('Modules ', 'Mod. ')
    tiles += f'<div class="row"><em><b>Course {ROMAN[ci]}</b>{row_label}</em>{row}</div>'

paths = ''.join(f'''<div class="path"><div class="tag">Course {ROMAN[i]} · {E(c["range"])}</div><h3>{E(c["name"])}</h3><p>{E(c["blurb"])}</p><div class="hrs">6 modules · {C_H[i]} CE hours</div><a class="btn navy" href="{AIC_PORTAL}">Buy Course {ROMAN[i]}</a></div>''' for i, c in enumerate(COURSES))

syllabus = ''
for ci, c in enumerate(COURSES):
    mods = ''
    for i in range(ci * 6, ci * 6 + 6):
        m = MODS[i]
        chips = ('<ul class="chips">' + ''.join(f'<li>{E(t)}</li>' for t in m['topics']) + '</ul>') if m.get('topics') else ''
        mods += f'''<article class="mod" id="m{i + 1}"><div class="top"><span class="mn">Module {i + 1}</span><span class="mh">{m["h"]} hours</span></div><h4>{E(m["t"])}</h4><p class="meta">{E(m["i"])} · {E(m["len"])}</p><p>{E(m["d"])}</p>{chips}<div class="req"><span>Research review + 350-word summary</span><span>5 MRI case submissions</span></div></article>'''
    syllabus += f'''<div class="course"><div class="chead"><span class="num">Course {ROMAN[ci]}</span><h3>{E(c["name"])}</h3><span class="tot">{E(c["range"])} · {C_H[ci]} hours</span></div><p class="cblurb">{E(c["blurb"])}</p><div class="mods">{mods}</div></div>'''

bib = ''
for i, refs in enumerate(BIB):
    title = 'Module ' + str(i + 1) + ' · ' + re.sub(r'^(MRI|Imaging) Mastery Series: ', '', MODS[i]['t'])
    cnt = f'{len(refs)} reference' + ('' if len(refs) == 1 else 's')
    bib += f'<details class="bib"><summary><b>{E(title)}</b><span>{cnt}</span></summary><ol>' + ''.join(f'<li>{linkify(r)}</li>' for r in refs) + '</ol></details>'
NREF = sum(len(r) for r in BIB)

AIC_FAQ = [
    ('Who is the Advanced Imaging Certification for?',
     'Doctors of chiropractic. It is an 18-module MRI curriculum built on case-based DICOM review, developed by the National Spine Management Group in collaboration with Medality™.'),
    ('Can I take the imaging certification in parts?',
     'Yes. You can complete all 18 modules in one enrollment, or work toward certification one six-module course at a time. Finishing Courses I, II and III completes the Advanced Imaging Certification.'),
    ('How many CE hours is the certification?',
     f'{TOTAL_H} CE hours across 18 modules: Course I is {C_H[0]} hours, Course II is {C_H[1]} hours and Course III is {C_H[2]} hours.'),
    ('Is it approved for continuing education?',
     "Yes. The Advanced Imaging Certification is approved for continuing education through the Federation of Chiropractic Licensing Boards' PACE program, and National Spine Management Group is an FCLB PACE provider. Check with your state board for how PACE hours apply to your license renewal."),
    ('What does each module involve?',
     "Each module has three parts: expert-led video lectures and case vignettes reviewed alongside the actual DICOM images; a research review of the module's assigned literature with a 350-word summary (about 5 hours); and 5 MRI case submissions related to the module's subject (about 5 hours). Lectures are broken into short 5–7 minute clips that fit around a clinic schedule."),
    ('How do I enroll?',
     'Enrollment and purchases are completed through the NSMG learning portal, on the Advanced Imaging Certification page.'),
]

aic_body = f'''
<section class="hero band">
 <div class="wrap herogrid">
  <div class="herotext"><div>
   <nav class="crumb" aria-label="Breadcrumb"><a href="../">Home</a> › Certifications › Advanced Imaging Certification</nav>
   <div class="pace">{STAR} Approved through the FCLB PACE program</div>
   <h1>Advanced Imaging Certification</h1>
   <p class="lede">The Spine Management Pathway: an 18-module MRI curriculum for doctors of chiropractic, built on case-based DICOM review and developed by the National Spine Management Group in collaboration with Medality™.</p>
   <div class="btns"><a class="btn gold" href="{AIC_PORTAL}">Enroll in the full certification</a><a class="btn ghost" href="#paths">Take it in three courses</a></div>
  </div>
  <div class="stats"><div><b>18</b><span>modules</span></div><div><b>3</b><span>six-module courses</span></div><div><b>{TOTAL_H}</b><span>CE hours</span></div><div><b>90</b><span>MRI cases submitted</span></div></div>
  </div>
  <div class="viewer" aria-label="The 18 modules arranged as three courses"><div class="vbar"><span>Spine Management Pathway</span><span>18 series · 3 courses</span></div>{tiles}</div>
 </div>
</section>

<section class="band tintband">
 <div class="wrap">
  <p class="eyebrow">How every module works</p>
  <h2>Lecture, literature, then your own cases</h2>
  <p class="sub">Each module starts at the fundamentals and builds in difficulty. Lectures and case vignettes are paired with DICOM images and broken into short 5–7 minute clips that fit around a clinic schedule.</p>
  <div class="how">
   <div><b>1</b><h3>Didactic lecture</h3><p>Expert-led video lectures and case vignettes reviewed alongside the actual DICOM images.</p></div>
   <div><b>2</b><h3>Research review</h3><p>Review the module's assigned literature and submit a 350-word summary. About 5 hours per module.</p></div>
   <div><b>3</b><h3>Case submission</h3><p>Analyze and submit 5 MRI studies related to the module's subject. About 5 hours per module.</p></div>
  </div>
  <ul class="obj">
   <li>Apply appropriate search patterns to ensure high-quality case assessment</li>
   <li>Identify key anatomical landmarks, variations and abnormalities on imaging</li>
   <li>Accurately interpret advanced imaging cases</li>
   <li>Formulate definitive diagnoses and limited differentials</li>
  </ul>
  <p class="note">Course content is peer-reviewed for content validity by reviewers without conflicts of interest, to verify the material is evidence-based, fair, balanced and free from commercial bias.</p>
 </div>
</section>

<section class="band" id="paths">
 <div class="wrap">
  <p class="eyebrow">Choose your path</p>
  <h2>One certification, or three courses at your own pace</h2>
  <p class="sub">Complete all 18 modules at once, or work toward certification one six-module course at a time. Finishing Courses I, II and III completes the Advanced Imaging Certification.</p>
  <div class="paths">
   <div class="path full"><div class="tag">Complete certification</div><h3>Advanced Imaging Certification</h3><p>All 18 modules and three courses in one enrollment. The most direct route to certification.</p><div class="hrs">18 modules · {TOTAL_H} CE hours</div><a class="btn gold" href="{AIC_PORTAL}">Enroll in the full certification</a></div>
   {paths}
  </div>
  <p class="note">Purchases are completed through the NSMG learning portal.</p>
 </div>
</section>

<section class="band tintband">
 <div class="wrap">
  <p class="eyebrow">Curriculum</p>
  <h2>The 18-module syllabus</h2>
  {syllabus}
 </div>
</section>

<section class="paceband band">
 <div class="wrap pacegrid">
  <svg class="seal" viewBox="0 0 132 132" aria-hidden="true"><defs><linearGradient id="seal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1cd5a"/><stop offset=".55" stop-color="#D4A017"/><stop offset="1" stop-color="#a87d0e"/></linearGradient></defs><circle cx="66" cy="66" r="62" fill="url(#seal)"/><circle cx="66" cy="66" r="52" fill="none" stroke="#0C2340" stroke-width="2" stroke-dasharray="3 4"/><text x="66" y="62" text-anchor="middle" font-family="Cambria,Georgia,serif" font-weight="700" font-size="28" fill="#0C2340">PACE</text><text x="66" y="84" text-anchor="middle" font-family="Calibri,sans-serif" font-weight="700" font-size="13" fill="#0C2340">APPROVED CE</text></svg>
  <div>
   <h2>Accredited through the FCLB PACE program</h2>
   <p>The Advanced Imaging Certification is approved for continuing education through the Federation of Chiropractic Licensing Boards' PACE program (Providers of Approved Continuing Education). National Spine Management Group is an FCLB PACE provider. Check with your state board for how PACE hours apply to your license renewal.</p>
  </div>
  <a class="btn gold" href="{AIC_PORTAL}">Enroll now</a>
 </div>
</section>

<section class="band" id="bibliography">
 <div class="wrap">
  <p class="eyebrow">Curriculum bibliography</p>
  <h2>Research reading, by module</h2>
  <p class="sub">The literature that supports each module's research review and 350-word summary. {NREF} references across 18 modules.</p>
  <div class="biblist">{bib}</div>
 </div>
</section>
{faq_html(AIC_FAQ, 'Advanced Imaging Certification: frequently asked questions')}
<section class="band tintband cta">
 <div class="wrap">
  <h2>Start reading MRI with confidence</h2>
  <p>Enroll in the full Advanced Imaging Certification, or begin with Course I and continue when you're ready.</p>
  <div class="btns center"><a class="btn gold" href="{AIC_PORTAL}">Enroll in the full certification</a><a class="btn navy" href="{AIC_PORTAL}">Start with Course I</a></div>
 </div>
</section>'''

AIC_URL = SITE + '/advanced-imaging-certification/'
aic_ld = {'@context': 'https://schema.org', '@type': 'Course', '@id': AIC_URL + '#course', 'name': 'Advanced Imaging Certification',
          'alternateName': 'Spine Management Pathway', 'url': AIC_URL,
          'description': 'An 18-module MRI curriculum for doctors of chiropractic, built on case-based DICOM review and developed by the National Spine Management Group in collaboration with Medality™. Approved for continuing education through the FCLB PACE program.',
          'provider': PROVIDER, 'audience': {'@type': 'EducationalAudience', 'educationalRole': 'Doctors of chiropractic'},
          'educationalLevel': 'Post-doctoral', 'inLanguage': 'en', 'numberOfCredits': TOTAL_H,
          'educationalCredentialAwarded': {'@type': 'EducationalOccupationalCredential', 'name': 'Advanced Imaging Certification', 'credentialCategory': 'Certificate',
                                           'recognizedBy': {'@type': 'Organization', 'name': 'Federation of Chiropractic Licensing Boards (FCLB) PACE program — Providers of Approved Continuing Education'}},
          'teaches': ['Apply appropriate search patterns to ensure high-quality case assessment', 'Identify key anatomical landmarks, variations and abnormalities on imaging', 'Accurately interpret advanced imaging cases', 'Formulate definitive diagnoses and limited differentials'],
          'hasCourseInstance': {'@type': 'CourseInstance', 'courseMode': 'Online', 'courseWorkload': f'{TOTAL_H} CE hours across 18 modules'},
          'hasPart': [{'@type': 'Course', 'name': f'Course {ROMAN[i]}: {c["name"]} ({c["range"]})', 'description': c['blurb'], 'numberOfCredits': C_H[i], 'provider': PROVIDER} for i, c in enumerate(COURSES)]}
aic = page('advanced-imaging-certification/index.html', 'Advanced Imaging Certification for Chiropractors | MRI Spine Management Pathway | NSMG',
           'An 18-module, FCLB PACE-approved MRI certification for doctors of chiropractic. Spine, neuro and MSK imaging with DICOM case review. Take it all at once or as three 6-module courses.',
           aic_body, [aic_ld, faq_ld(AIC_FAQ), crumbs_ld([('Home', SITE + '/'), ('Advanced Imaging Certification', AIC_URL)])], 'aic')

# ---------------------------------------------------------------- FELLOWSHIP
def icon(name):
    return '<svg viewBox="0 0 24 24" aria-hidden="true">' + ''.join(f'<path d="{E(d)}"/>' for d in ICONS[name]) + '</svg>'

thumbs = ''.join(f'<a class="tile" href="../advanced-imaging-certification/#m{i + 1}" title="Module {i + 1}: {E(n)}"><img src="../images/modules/AIC_Module_{i + 1:02d}.jpg" alt="Module {i + 1}: {E(n)}" width="320" height="180" loading="lazy"></a>' for i, n in enumerate(D['MODULE_NAMES']))
rtiles = ''.join(f'<a class="rtile" href="#r{i + 1}">{icon(r["ic"])}<strong>{E(r["short"])}</strong><small>Rotation {i + 1} · 6 wks</small></a>' for i, r in enumerate(ROTS))
weeks = ''.join(f'<div class="wk"><b>Week {w}</b><div class="days" aria-hidden="true"><i class="on"></i><i></i><i></i><i></i><i></i></div><span>1 on-site day</span></div>' for w in range(1, 7))
rotlist = ''.join(f'''<article class="rot{' cap' if r.get('cap') else ''}" id="r{i + 1}"><div class="ic">{icon(r["ic"])}</div><div><div class="top"><span class="mn">Rotation {i + 1}{' · Capstone' if r.get('cap') else ''}</span><span class="mh">6 weeks · 1 day/week</span></div><h4>{E(r["title"])}</h4><p>{E(r["desc"])}</p><ul class="chips">{''.join(f'<li>{E(c)}</li>' for c in r["chips"])}</ul><div class="req"><span>On-site observation</span><span>30+ peer-reviewed articles</span><span>Evidence summaries</span></div></div></article>''' for i, r in enumerate(ROTS))

FS_FAQ = [
    ('How long is the Fellowship in Spine Management?',
     'Two years, post-doctoral. Year One is the Advanced Imaging Certification (18 imaging modules). Year Two is six interprofessional clinical rotations.'),
    ('Who is the fellowship for?',
     'Doctors of chiropractic: established community-based practitioners who want advanced imaging credentials, medicolegal standing and working relationships with health systems; recent graduates who want structured post-doctoral training; and chiropractors pursuing teaching roles, expert-witness work, or spine-care leadership in health systems and academic institutions.'),
    ('How do the clinical rotations work?',
     'There are six rotations. Each runs one day a week for six weeks with a clinical host in your own community, coordinated with the help of NSMG. Fellows observe live procedures, consults and clinical decision-making on site, work through 30+ peer-reviewed articles per rotation with evidence summaries, and apply what they learn to their own patients the same week.'),
    ('Can I keep my practice running during the fellowship?',
     'Yes. Fellows keep their own practice going between on-site days, which is the point: what they see on clinical rotations goes straight into how they manage their patients.'),
    ('Where do the rotations take place?',
     'Rotations are coordinated within your own community with the help of NSMG. NSMG works with you to arrange host sites near your practice, so rotation order and host sites depend on the clinical services available in your area.'),
    ('What credentials do fellows earn?',
     'A Fellowship Completion Certificate from NSMG; the Advanced Imaging Certification, with its continuing-education hours; documented completion of six interprofessional clinical rotations; CV entry documentation for every completed module and rotation; and a qualification pathway toward FSBT Fellowship designation.'),
]

fs_body = f'''
<section class="hero band">
 <div class="wrap">
  <div class="herotext">
   <div>
    <nav class="crumb" aria-label="Breadcrumb"><a href="../">Home</a> › Certifications › Fellowship in Spine Management</nav>
    <div class="pace">{STAR} Two-year post-doctoral fellowship for doctors of chiropractic</div>
    <h1>Fellowship in Spine Management</h1>
    <p class="lede">Imaging mastery in Year One, then a year of clinical rotations. Interprofessional rotations, coordinated within your own community with the help of NSMG, train chiropractors to work as spine-care navigators alongside radiology, orthopedics, neurosurgery and pain management.</p>
    <div class="btns"><a class="btn gold" href="{SCHED}">Schedule a consultation</a><a class="btn ghost" href="#rotations">See the clinical rotations</a></div>
   </div>
   <div class="stats"><div><b>2</b><span>years, post-doctoral</span></div><div><b>18</b><span>imaging modules in Year One</span></div><div><b>6</b><span>clinical rotations in Year Two</span></div><div><b>30+</b><span>peer-reviewed articles per rotation</span></div></div>
  </div>
  <div class="viewer" aria-label="The two-year program: 18 imaging modules, then six clinical rotations">
   <div class="vbar"><span>Fellowship schedule</span><span>18 series · 6 rotations</span></div>
   <div class="yr"><em><b>Year One</b>Advanced Imaging Certification</em><div class="thumbs">{thumbs}</div></div>
   <div class="yr"><em><b>Year Two</b>Clinical rotations</em><div class="rots">{rtiles}</div></div>
  </div>
 </div>
</section>

<section class="band">
 <div class="wrap">
  <p class="eyebrow">Curriculum structure</p>
  <h2>Read the images first, then begin clinical rotations</h2>
  <p class="sub">The program is sequenced on purpose. Fellows finish the imaging year before rotations begin, so they arrive with the diagnostic vocabulary and imaging literacy that radiology, orthopedic, neurosurgical and pain management teams expect from a colleague.</p>
  <div class="phases">
   <div class="phasecard y1"><div class="tag">Year One · Phase I</div><h3>Advanced Imaging Certification</h3><p>The complete 18-module Spine Management Pathway, developed with Medality™ and delivered on MRI Online.</p>
    <ul><li>Spine, neurologic and musculoskeletal MRI, taught by fellowship-trained radiologists</li><li>Didactic lecture and DICOM case review in every module</li><li>A research review and 350-word evidence summary per module</li><li>5 MRI case submissions per module, building a 90-case portfolio</li></ul>
    <a class="arrowlink" href="../advanced-imaging-certification/">View the full imaging curriculum →</a></div>
   <div class="phasecard"><div class="tag">Year Two · Phase II</div><h3>Interprofessional Clinical Rotations</h3><p>Six rotations coordinated within your own community with the help of NSMG, in the settings where spine patients are actually managed.</p>
    <ul><li>One on-site day per week for six weeks per rotation</li><li>Live procedures observed, then applied to your own patients that same week</li><li>30+ peer-reviewed articles per rotation, with evidence summaries</li><li>Ends with the fellow working as a spine-care navigator on the team</li></ul>
    <a class="arrowlink dark" href="#rotations">See the six rotations →</a></div>
  </div>
 </div>
</section>

<section class="band tintband" id="rotations">
 <div class="wrap">
  <p class="eyebrow">Year Two · Clinical rotations</p>
  <h2>How every rotation works</h2>
  <p class="sub">Each rotation runs one day a week for six weeks with a clinical host in your own community, coordinated with the help of NSMG. Fellows keep their own practice going between on-site days, which is the point: what they see on clinical rotations goes straight into how they manage their patients.</p>
  <div class="how">
   <div><b>1</b><h3>Observe on site</h3><p>One day a week with the host service, observing live procedures, consults and clinical decision-making.</p></div>
   <div><b>2</b><h3>Read the evidence</h3><p>Work through the rotation's 30+ peer-reviewed articles and write evidence summaries that tie the literature to what you saw.</p></div>
   <div><b>3</b><h3>Apply it that week</h3><p>Bring the observations into active patient management in your own practice, the same week.</p></div>
  </div>
  <div class="weeks" aria-label="Six-week rotation cadence: one on-site day each week">{weeks}</div>
  <div class="rotlist">{rotlist}</div>
  <p class="note">Rotation order and host sites depend on the clinical services available in the fellow's community.</p>
 </div>
</section>

<section class="band quote">
 <div class="wrap">
  <blockquote>“Innovation in medical training occurs not in medical school — it occurs in residencies and fellowships. Chiropractic deserved the same.”</blockquote>
  <cite>William J. Owens Jr., DC, FSBT · President &amp; CEO, National Spine Management Group</cite>
 </div>
</section>

<section class="band">
 <div class="wrap">
  <p class="eyebrow">Clinical training sites</p>
  <h2>Training in your own community</h2>
  <p class="sub">Rotations are coordinated within your own community with the help of NSMG, so fellows train with local clinical teams, build working relationships close to their own practice and contribute real clinical value while they build their credentialing portfolio.</p>
  <div class="sites">
   <div class="site"><b>Pain management practices</b><span>Interventional spine procedures</span></div>
   <div class="site"><b>Imaging centers</b><span>MRI and radiology services</span></div>
   <div class="site"><b>Orthopedic &amp; neurosurgery offices</b><span>Spine and extremity surgical care</span></div>
   <div class="site"><b>Primary care practices</b><span>Family and internal medicine</span></div>
  </div>
  <p class="note">Host sites vary by community; NSMG helps each fellow identify and arrange them.</p>
  <div class="agree">
   <div><h3>The educational institution</h3>Sets the curriculum, tracks fellow milestones and assesses competency.</div>
   <div><h3>The clinical host</h3>Provides the on-site setting, supervision and access to the clinical team.</div>
   <div><h3>The fellow</h3>Meets attendance, reading, evidence-summary and case requirements for every rotation.</div>
  </div>
  <p class="note">Each host site's arrangement, coordinated with NSMG, defines these responsibilities, mirroring the structure of formal medical training agreements.</p>
 </div>
</section>

<section class="band tintband">
 <div class="wrap">
  <p class="eyebrow">Ideal candidates</p>
  <h2>Who should apply</h2>
  <div class="aud">
   <div><b>01</b><h3>Community-based practitioners</h3><p>Established chiropractors who want advanced imaging credentials, medicolegal standing and working relationships with health systems.</p></div>
   <div><b>02</b><h3>New graduates</h3><p>Recent graduates who want structured post-doctoral training and integrated health-system experience from the start of their careers.</p></div>
   <div><b>03</b><h3>Academic &amp; clinical leaders</h3><p>Chiropractors pursuing teaching roles, expert-witness work, or spine-care leadership in health systems and academic institutions.</p></div>
  </div>
 </div>
</section>

<section class="band">
 <div class="wrap">
  <p class="eyebrow">Program outcomes</p>
  <h2>What fellows earn and can do</h2>
  <div class="two">
   <div><h3>Clinical competencies</h3><ul class="obj"><li>Systematic MRI interpretation across spine, neurologic and MSK pathology</li><li>Evidence-based diagnostic communication with radiologists and surgeons</li><li>Interprofessional navigation developed through clinical rotations</li><li>Fluency in the ABCDE structured imaging method</li><li>A documented portfolio of 90+ submitted MRI cases</li><li>spineCAMP analytics integrated into clinical workflow</li></ul></div>
   <div><h3>Credentials</h3><ul class="obj"><li>Fellowship Completion Certificate, NSMG</li><li>Advanced Imaging Certification, with its continuing-education hours</li><li>Documented completion of six interprofessional clinical rotations</li><li>CV entry documentation for every completed module and rotation</li><li>A qualification pathway toward FSBT Fellowship designation</li></ul></div>
  </div>
 </div>
</section>
{faq_html(FS_FAQ, 'Fellowship in Spine Management: frequently asked questions')}
<section class="band tintband cta">
 <div class="wrap">
  <h2>Train where spine patients are managed</h2>
  <p>Enrollment starts with a conversation about your goals, your practice and the clinical hosts in your community.</p>
  <div class="btns center"><a class="btn gold" href="{SCHED}">Schedule a consultation</a><a class="btn navy" href="{AIC_PORTAL}">Start with the imaging year</a><a class="btn navy" href="{FS_PORTAL}">View in the Member Portal</a></div>
  <p class="contact">Questions? <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
 </div>
</section>'''

FS_URL = SITE + '/fellowship-in-spine-management/'
fs_ld = {'@context': 'https://schema.org', '@type': 'EducationalOccupationalProgram', '@id': FS_URL + '#program', 'name': 'Fellowship in Spine Management', 'url': FS_URL,
         'description': 'A two-year post-doctoral fellowship for doctors of chiropractic: the Advanced Imaging Certification in Year One, then six interprofessional clinical rotations in Year Two, coordinated within the fellow\'s own community with the help of NSMG.',
         'provider': PROVIDER, 'timeToComplete': 'P2Y', 'educationalProgramMode': 'Blended', 'programPrerequisites': 'Doctor of chiropractic',
         'occupationalCategory': 'Chiropractor',
         'educationalCredentialAwarded': {'@type': 'EducationalOccupationalCredential', 'name': 'Fellowship Completion Certificate, NSMG', 'credentialCategory': 'Certificate'},
         'hasCourse': [{'@type': 'Course', '@id': AIC_URL + '#course', 'name': 'Advanced Imaging Certification', 'url': AIC_URL, 'description': 'Year One: the complete 18-module Spine Management Pathway.', 'provider': PROVIDER}]
                      + [{'@type': 'Course', 'name': f'Rotation {i + 1}: {r["title"]}', 'description': r['desc'], 'provider': PROVIDER} for i, r in enumerate(ROTS)]}
fs = page('fellowship-in-spine-management/index.html', 'Fellowship in Spine Management | National Spine Management Group',
          'A two-year post-doctoral fellowship for chiropractors: the Advanced Imaging Certification, then clinical rotations coordinated in your own community with NSMG.',
          fs_body, [fs_ld, faq_ld(FS_FAQ), crumbs_ld([('Home', SITE + '/'), ('Fellowship in Spine Management', FS_URL)])], 'fs')

# ---------------------------------------------------------------- NATIONAL CONFERENCE
CONF_URL = SITE + '/national-conference/'
CONF_DAYS = [('Friday', 'March 5', 'Meet-and-greet happy hour', '4–6 PM', '2027-03-05T16:00:00-05:00', '2027-03-05T18:00:00-05:00'),
             ('Saturday', 'March 6', 'Full-day session', '8:30 AM–5 PM', '2027-03-06T08:30:00-05:00', '2027-03-06T17:00:00-05:00'),
             ('Sunday', 'March 7', 'Morning session', '9 AM–12 PM', '2027-03-07T09:00:00-05:00', '2027-03-07T12:00:00-05:00')]
CONF_PLACE = {'@type': 'Place', 'name': 'Fort Lauderdale, FL', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Fort Lauderdale', 'addressRegion': 'FL', 'addressCountry': 'US'}}
conf_days_html = ''.join(f'<div><b>{E(d)}</b><h3>{E(what)}</h3><p>{E(date)}, 2027 · {E(t)}</p></div>' for d, date, what, t, _, _ in CONF_DAYS)
conf_body = f'''
<section class="hero band">
 <div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="../">Home</a> › 2027 National Conference</nav>
  <div class="pace">{STAR} Registration open</div>
  <h1>2027 NSMG National Conference</h1>
  <p class="lede big">March 5–7, 2027 · Fort Lauderdale, FL</p>
  <p class="lede">Friday meet-and-greet happy hour, a Saturday full-day session and a Sunday morning session. Open to members and non-member doctors.</p>
  <div class="btns"><a class="btn gold" href="{E(CONF_REGISTER)}">Register</a><a class="btn ghost" href="{E(CONF_HOTEL)}">Book Discounted Hotel Room</a></div>
 </div>
</section>

<section class="band tintband">
 <div class="wrap">
  <p class="eyebrow">Schedule</p>
  <h2>Three days in Fort Lauderdale</h2>
  <p class="sub">All times are local (Eastern).</p>
  <div class="how">{conf_days_html}</div>
 </div>
</section>

<section class="band cta">
 <div class="wrap">
  <h2>Save your seat</h2>
  <p>Open to members and non-member doctors. Register through the NSMG Member Portal, then book your room at the discounted conference rate.</p>
  <div class="btns center"><a class="btn gold" href="{E(CONF_REGISTER)}">Register</a><a class="btn navy" href="{E(CONF_HOTEL)}">Book Discounted Hotel Room</a></div>
 </div>
</section>'''
conf_ld = {'@context': 'https://schema.org', '@type': 'Event', '@id': CONF_URL + '#event', 'name': '2027 NSMG National Conference', 'url': CONF_URL,
           'description': 'The 2027 National Spine Management Group National Conference in Fort Lauderdale, FL: a Friday meet-and-greet happy hour, a Saturday full-day session and a Sunday morning session. Open to members and non-member doctors.',
           'startDate': CONF_DAYS[0][4], 'endDate': CONF_DAYS[-1][5], 'eventStatus': 'https://schema.org/EventScheduled',
           'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode', 'location': CONF_PLACE, 'image': SITE + '/images/nsmg-share.png',
           'organizer': PROVIDER, 'audience': {'@type': 'Audience', 'audienceType': 'Doctors of chiropractic, members and non-members'},
           'offers': {'@type': 'Offer', 'url': CONF_REGISTER, 'availability': 'https://schema.org/InStock'},
           'subEvent': [{'@type': 'Event', 'name': f'{d}: {what}', 'startDate': s, 'endDate': e, 'location': CONF_PLACE,
                         'eventStatus': 'https://schema.org/EventScheduled', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode'} for d, _, what, _, s, e in CONF_DAYS]}
conf = page('national-conference/index.html', '2027 NSMG National Conference | March 5–7, 2027 · Fort Lauderdale, FL',
            'The 2027 National Spine Management Group National Conference, March 5–7, 2027 in Fort Lauderdale, FL. Open to members and non-member doctors. Register and book the discounted hotel room.',
            conf_body, [conf_ld, crumbs_ld([('Home', SITE + '/'), ('2027 National Conference', CONF_URL)])], 'conf')

# ---------------------------------------------------------------- ABOUT
ABOUT_URL = SITE + '/about/'
about_body = f'''
<section class="hero band">
 <div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="../">Home</a> › About</nav>
  <p class="kicker">About NSMG</p>
  <h1>William J. Owens Jr., DC, FSBT</h1>
  <p class="lede big">President &amp; CEO, National Spine Management Group (since 2020)</p>
  <p class="lede">A practicing clinician and educator: 28 years treating spine injury in Buffalo, and the director of NSMG's post-doctoral spine programs.</p>
  <div class="btns"><a class="btn gold" href="{SCHED}">Book a Call</a><a class="btn ghost" href="{LINKEDIN}">LinkedIn profile</a></div>
 </div>
</section>

<section class="band tintband">
 <div class="wrap">
  <div class="pillars">
   <div><span class="tag">Practice</span><h3>Clinical care</h3><p>28 years treating spine injury in Buffalo, and still practicing at Greater Buffalo Accident and Injury Chiropractic.</p></div>
   <div><span class="tag">Educate</span><h3>Program director</h3><p>Directs the <a href="../fellowship-in-spine-management/">Fellowship in Spine Management</a>, the Spine Management Residency Program and the <a href="../advanced-imaging-certification/">Advanced Imaging Certification</a>.</p></div>
   <div><span class="tag">Teach</span><h3>Faculty and physician educator</h3><p>Adjunct faculty in Parker University's MS in Interprofessional Spine Management, and the only chiropractor to complete the Royal College of Physicians Certified Physician Educator Program.</p></div>
   <div><span class="tag">Research</span><h3>Published work</h3><p>Author of a 2026 peer-reviewed study in the North American Spine Society Journal and of IEEE engineering-in-medicine papers.</p></div>
  </div>
 </div>
</section>

<section class="band">
 <div class="wrap">
  <p class="eyebrow">Medico-legal</p>
  <h2>Consulting and court testimony</h2>
  <p class="sub">Dr. Owens provides medico-legal consulting and testifies in court on spine injury.</p>
 </div>
</section>

<section class="band tintband cta">
 <div class="wrap">
  <h2>Talk with Dr. Owens and the NSMG team</h2>
  <p>Book a call about the Fellowship, the Advanced Imaging Certification or NSMG membership.</p>
  <div class="btns center"><a class="btn gold" href="{SCHED}">Book a Call</a><a class="btn navy" href="../contact/">Contact NSMG</a></div>
 </div>
</section>'''
person_ld = {'@context': 'https://schema.org', '@type': 'Person', '@id': ABOUT_URL + '#person', 'name': 'William J. Owens Jr.', 'honorificSuffix': 'DC, FSBT',
             'url': ABOUT_URL, 'sameAs': [LINKEDIN], 'jobTitle': 'President & CEO',
             'worksFor': {'@type': 'EducationalOrganization', '@id': SITE + '/#organization', 'name': ORG, 'url': SITE + '/'},
             'description': 'President & CEO of National Spine Management Group since 2020; 28 years treating spine injury in Buffalo; directs the Fellowship in Spine Management, the Spine Management Residency Program and the Advanced Imaging Certification.',
             'affiliation': [{'@type': 'CollegeOrUniversity', 'name': 'Parker University'}],
             'workLocation': {'@type': 'Place', 'address': {'@type': 'PostalAddress', 'addressLocality': 'Buffalo', 'addressRegion': 'NY', 'addressCountry': 'US'}},
             'knowsAbout': ['Spine injury', 'Spine imaging', 'Medico-legal consulting', 'Interprofessional spine management']}
about = page('about/index.html', 'William J. Owens Jr., DC, FSBT | About National Spine Management Group',
             'About Dr. William J. Owens Jr., DC, FSBT: President & CEO of National Spine Management Group, 28 years treating spine injury in Buffalo, and director of the Fellowship in Spine Management and the Advanced Imaging Certification.',
             about_body, [person_ld, crumbs_ld([('Home', SITE + '/'), ('About', ABOUT_URL)])], 'about')

# ---------------------------------------------------------------- CONTACT
CONTACT_URL = SITE + '/contact/'
contact_body = f'''
<section class="hero band">
 <div class="wrap">
  <nav class="crumb" aria-label="Breadcrumb"><a href="../">Home</a> › Contact</nav>
  <h1>Contact National Spine Management Group</h1>
  <p class="lede">Questions about the Fellowship, the Advanced Imaging Certification, the National Conference or membership? Book a call or reach us directly.</p>
  <div class="btns"><a class="btn gold" href="{SCHED}">Book a Call</a></div>
 </div>
</section>

<section class="band tintband">
 <div class="wrap">
  <div class="how">
   <div><b>Phone</b><h3><a href="tel:{PHONE_TEL}">{PHONE}</a></h3><p>Call our team.</p></div>
   <div><b>Email</b><h3><a href="mailto:{EMAIL}">{EMAIL}</a></h3><p>We reply by email.</p></div>
   <div><b>Office</b><h3>{ADDR['street']}</h3><p>{ADDR['city']}, {ADDR['region']} {ADDR['zip']}</p></div>
  </div>
  <p class="note">Locations: Buffalo, NY and Lehi, UT.</p>
 </div>
</section>

<section class="band cta">
 <div class="wrap">
  <h2>Prefer to talk it through?</h2>
  <p>Book a call with our team at a time that suits you.</p>
  <div class="btns center"><a class="btn gold" href="{SCHED}">Book a Call</a><a class="btn navy" href="{LOGIN}">Member Login</a></div>
 </div>
</section>'''
contact_ld = {'@context': 'https://schema.org', '@type': 'ContactPage', 'url': CONTACT_URL, 'name': 'Contact National Spine Management Group',
              'mainEntity': {'@type': 'EducationalOrganization', '@id': SITE + '/#organization', 'name': ORG, 'url': SITE + '/', 'telephone': PHONE_TEL, 'email': EMAIL,
                             'address': {'@type': 'PostalAddress', 'streetAddress': ADDR['street'], 'addressLocality': ADDR['city'], 'addressRegion': ADDR['region'], 'postalCode': ADDR['zip'], 'addressCountry': 'US'},
                             'contactPoint': {'@type': 'ContactPoint', 'telephone': PHONE_TEL, 'email': EMAIL, 'contactType': 'customer service', 'areaServed': 'US'}}}
contact = page('contact/index.html', 'Contact | National Spine Management Group',
               'Contact National Spine Management Group: 1275 Main Street, Suite 110, Buffalo, NY 14209 · 716-228-3847. Offices in Buffalo, NY and Lehi, UT. Book a call with our team.',
               contact_body, [contact_ld, crumbs_ld([('Home', SITE + '/'), ('Contact', CONTACT_URL)])], 'contact')

# ---------------------------------------------------------------- 404
nf_body = f'''
<section class="hero band">
 <div class="wrap">
  <p class="kicker">Page not found</p>
  <h1>We couldn't find that page</h1>
  <p class="lede">The page may have moved. These are the most-visited places on the NSMG site.</p>
  <div class="btns"><a class="btn gold" href="./">Go to the home page</a><a class="btn ghost" href="{PORTAL}">Visit the Member Portal</a><a class="btn ghost" href="{LOGIN}">Member Login</a></div>
 </div>
</section>

<section class="band tintband">
 <div class="wrap">
  <div class="pillars">
   <div><span class="tag">Certification</span><h3><a href="advanced-imaging-certification/">Advanced Imaging Certification</a></h3><p>An 18-module MRI curriculum for doctors of chiropractic.</p></div>
   <div><span class="tag">Fellowship</span><h3><a href="fellowship-in-spine-management/">Fellowship in Spine Management</a></h3><p>A two-year post-doctoral fellowship.</p></div>
   <div><span class="tag">Event</span><h3><a href="national-conference/">2027 National Conference</a></h3><p>March 5–7, 2027 · Fort Lauderdale, FL</p></div>
   <div><span class="tag">Contact</span><h3><a href="contact/">Contact NSMG</a></h3><p>{PHONE} · Book a call with our team.</p></div>
  </div>
 </div>
</section>'''
not_found = page('404.html', 'Page not found | National Spine Management Group',
                 'The page you were looking for could not be found on the National Spine Management Group site.', nf_body, [], '', not_found=True)

# ---------------------------------------------------------------- write
for p, s in [('index.html', home), ('advanced-imaging-certification/index.html', aic), ('fellowship-in-spine-management/index.html', fs),
             ('national-conference/index.html', conf), ('about/index.html', about), ('contact/index.html', contact), ('404.html', not_found)]:
    os.makedirs(os.path.dirname(os.path.join(OUT, p)) or OUT, exist_ok=True)
    open(os.path.join(OUT, p), 'w').write(s)

open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
    f'  <url><loc>{SITE}{u}</loc><lastmod>2026-11-27</lastmod></url>\n' for u in ['/', '/advanced-imaging-certification/', '/fellowship-in-spine-management/', '/national-conference/', '/about/', '/contact/']) + '</urlset>\n')

bots = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Bingbot', 'Googlebot']
open(os.path.join(OUT, 'robots.txt'), 'w').write('# National Spine Management Group public site\n# All crawlers, including AI search and assistant crawlers, are welcome.\n\nUser-agent: *\nAllow: /\n\n' + ''.join(f'User-agent: {b}\nAllow: /\n\n' for b in bots) + f'Sitemap: {SITE}/sitemap.xml\n')

open(os.path.join(OUT, 'llms.txt'), 'w').write(f'''# National Spine Management Group (NSMG)

> Leaders in Academic Spinal Care. The complete system for spine-focused chiropractic practice: clinical training, documentation that holds up to scrutiny, and referral relationships with attorneys and physicians, taught as one system by National Spine Management Group.

NSMG offers two post-doctoral programs for doctors of chiropractic. Members sign in to the NSMG Member Portal for courses, enrollment and purchases.

## Programs

- [Advanced Imaging Certification]({AIC_URL}): The Spine Management Pathway, an 18-module MRI curriculum for doctors of chiropractic built on case-based DICOM review, developed by NSMG in collaboration with Medality™. {TOTAL_H} CE hours across three six-module courses (Course I: Spine & Spinal Lesions, {C_H[0]} hours; Course II: Emergency & Brain Neuroimaging, {C_H[1]} hours; Course III: Neurovascular & Musculoskeletal, {C_H[2]} hours). Each module combines didactic lecture with DICOM review, a research review with a 350-word summary, and 5 MRI case submissions (90 cases in total). Approved for continuing education through the FCLB PACE program; NSMG is an FCLB PACE provider. Take all 18 modules at once or one course at a time.
- [Fellowship in Spine Management]({FS_URL}): A two-year post-doctoral fellowship. Year One is the Advanced Imaging Certification; Year Two is six interprofessional clinical rotations (Interventional Pain Management; MRI Physics & Neuroradiology; Orthopedic Extremity & Spine Surgery; Neurosurgery & Emergency Medicine; Family & Internal Medicine; Spine-Care Team Integration capstone), each one on-site day per week for six weeks, coordinated within the fellow's own community with the help of NSMG, with 30+ peer-reviewed articles per rotation. Credentials include a Fellowship Completion Certificate from NSMG and a qualification pathway toward FSBT Fellowship designation.

## Events

- [2027 NSMG National Conference]({CONF_URL}): March 5–7, 2027, Fort Lauderdale, FL. Friday meet-and-greet happy hour 4–6 PM, Saturday full-day session 8:30 AM–5 PM, Sunday morning session 9 AM–12 PM (Eastern). Open to members and non-member doctors. [Register]({CONF_REGISTER}).

## About

- [William J. Owens Jr., DC, FSBT]({ABOUT_URL}): President & CEO of National Spine Management Group since 2020. 28 years treating spine injury in Buffalo; still practicing at Greater Buffalo Accident and Injury Chiropractic. Directs the Fellowship in Spine Management, the Spine Management Residency Program and the Advanced Imaging Certification. Adjunct faculty, Parker University MS in Interprofessional Spine Management; the only chiropractor to complete the Royal College of Physicians Certified Physician Educator Program. Medico-legal consulting and court testimony. Author of a 2026 peer-reviewed North American Spine Society Journal study and IEEE engineering-in-medicine papers. [LinkedIn]({LINKEDIN}).

## Links

- [Home]({SITE}/)
- [Contact]({CONTACT_URL})
- [Member Portal]({PORTAL})
- [Member Login]({LOGIN})
- [Schedule a consultation]({SCHED})

## Contact

National Spine Management Group, {ADDR['street']}, {ADDR['city']}, {ADDR['region']} {ADDR['zip']}. Phone {PHONE}. Email {EMAIL}. Locations: Buffalo, NY and Lehi, UT.
''')
print('written to', OUT, '| contact email', 'SET' if EMAIL != 'EMAIL-NOT-SET' else 'NOT SET (placeholder)')
