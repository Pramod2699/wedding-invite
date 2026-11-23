#!/usr/bin/env python3
"""Build the Marathi invite (mr/index.html) from the English one (index.html).

Run from the repo root after any change to index.html:

    python3 tools/build_mr.py

Every translation below names the exact English text it replaces and how many
times that text must appear. If the English page changes and a phrase can no
longer be found, the build stops and says which one, so the two versions never
drift apart silently.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "mr" / "index.html"

# (English, Marathi, expected count)
T = [
    # ---- Page head and WhatsApp preview ----
    ('<html lang="en">', '<html lang="mr">', 1),
    ('<title>Pramod &amp; Shruti are getting married</title>', '<title>प्रमोद व श्रुती यांचा शुभविवाह</title>', 1),
    ('content="Engagement &amp; Haldi on Tue 29 Dec, Wedding on Wed 30 Dec 2026 at Shivkamal Lawns. Tap to open your invitation."',
     'content="साखरपुडा व हळदी समारंभ: मंगळवार, 29 डिसेंबर · शुभविवाह: बुधवार, 30 डिसेंबर 2026 · शिवकमल लॉन्स. निमंत्रण उघडण्यासाठी टॅप करा."', 2),
    ('<meta property="og:title" content="Pramod &amp; Shruti are getting married">',
     '<meta property="og:title" content="प्रमोद व श्रुती यांचा शुभविवाह">', 1),
    ('<meta property="og:image:alt" content="Illustration of Pramod and Shruti in wedding clothes under a marigold arch">',
     '<meta property="og:image:alt" content="विवाहाच्या पोशाखात प्रमोद व श्रुती, झेंडूच्या फुलांच्या कमानीखाली">', 1),
    ('<meta property="og:site_name" content="Pramod &amp; Shruti">', '<meta property="og:site_name" content="प्रमोद व श्रुती">', 1),
    ('<meta property="og:locale" content="en_IN">', '<meta property="og:locale" content="mr_IN">', 1),
    ('&family=Tiro+Devanagari+Marathi&display=swap', '&family=Tiro+Devanagari+Marathi&family=Rozha+One&display=swap', 1),

    # ---- Opening screen ----
    ('<p class="gate-invite">With the blessings of our elders, we warmly invite you and your family to celebrate the wedding of</p>',
     '<p class="gate-invite">वडीलधाऱ्यांच्या शुभाशीर्वादाने, आमच्या शुभविवाह सोहळ्यास आपण सहकुटुंब सहपरिवार उपस्थित राहावे, ही नम्र विनंती.</p>', 1),
    ('aria-label="Open the invitation"', 'aria-label="निमंत्रण उघडा"', 1),
    ('<span class="names">Pramod &amp; Shruti</span>', '<span class="names">प्रमोद व श्रुती</span>', 1),
    ('type="button">Open the invitation</button>', 'type="button">निमंत्रण उघडा</button>', 1),
    ('<a class="gate-lang" id="langLink" href="mr/" lang="mr">मराठीत पाहा</a>',
     '<a class="gate-lang" id="langLink" href="../" lang="en">Read in English</a>', 1),

    # ---- Names page ----
    ('alt="Illustration of Pramod and Shruti standing together under a marigold arch"',
     'alt="झेंडूच्या फुलांच्या कमानीखाली एकत्र उभे प्रमोद व श्रुती"', 1),
    ('<h1 class="names" id="names" aria-label="Pramod and Shruti"><span class="word" aria-hidden="true">Pramod</span><span class="amp" aria-hidden="true">&amp;</span><span class="word" aria-hidden="true">Shruti</span></h1>',
     '<h1 class="names" id="names" aria-label="प्रमोद व श्रुती"><span class="word" aria-hidden="true">प्रमोद</span><span class="amp" aria-hidden="true">व</span><span class="word" aria-hidden="true">श्रुती</span></h1>', 1),
    ('<p class="hero-sub hero-in">are getting married</p>', '<p class="hero-sub hero-in">विवाहबंधनात अडकत आहेत</p>', 1),
    ('aria-label="Scroll to continue"', 'aria-label="पुढे पाहा"', 1),

    # ---- Groom ----
    ('alt="Illustrated portrait of Pramod"', 'alt="प्रमोद यांचे चित्र"', 1),
    ('<p class="honorific rv">The Groom</p>', '<p class="honorific rv">वर</p>', 1),
    ('<h2 class="person-name rv" id="groom-h">Pramod</h2>',
     '<h2 class="person-name rv" id="groom-h"><small class="chi">चि.</small>प्रमोद</h2>', 1),
    ('<p class="lineage-of">Son of</p>\n      <p class="lineage-names"><span>Sau. Vijaya</span><span class="amp">&amp;</span><span>Shri Balasaheb Manik Gunaware</span></p>',
     '<p class="lineage-names"><span>सौ. विजया</span><span class="amp">व</span><span>श्री. बाळासाहेब माणिक गुणवरे</span></p>\n      <p class="lineage-of lineage-after">यांचे सुपुत्र</p>', 1),

    # ---- Bride ----
    ('alt="Illustrated portrait of Shruti"', 'alt="श्रुती यांचे चित्र"', 1),
    ('<p class="honorific rv">The Bride</p>', '<p class="honorific rv">वधू</p>', 1),
    ('<h2 class="person-name rv" id="bride-h">Shruti</h2>',
     '<h2 class="person-name rv" id="bride-h"><small class="chi">चि. सौ. कां.</small>श्रुती</h2>', 1),
    ('<p class="lineage-of">Daughter of</p>\n      <p class="lineage-names"><span>Sau. Meera</span><span class="amp">&amp;</span><span>Shri Dhanraj Ramdas Kaldate</span></p>',
     '<p class="lineage-names"><span>सौ. मीरा</span><span class="amp">व</span><span>श्री. धनराज रामदास काळदाते</span></p>\n      <p class="lineage-of lineage-after">यांची सुकन्या</p>', 1),

    # ---- Date reveal ----
    ('id="reveal-h">Save the date</h2>', 'id="reveal-h">शुभदिनांक</h2>', 1),
    ('Scratch the gold card to reveal it.', 'सोनेरी कार्ड घासून तारीख पाहा.', 1),
    ('<span class="sd-dow">Wednesday</span>', '<span class="sd-dow">बुधवार</span>', 1),
    ('<span class="sd-date">30 December</span>', '<span class="sd-date">30 डिसेंबर</span>', 1),
    ('type="button">Reveal without scratching</button>', 'type="button">न घासता तारीख पाहा</button>', 1),
    ('aria-label="Time until the wedding"', 'aria-label="विवाहासाठी उरलेला वेळ"', 1),
    ('<span class="lbl">days</span>', '<span class="lbl">दिवस</span>', 1),
    ('<span class="lbl">hours</span>', '<span class="lbl">तास</span>', 1),
    ('<span class="lbl">minutes</span>', '<span class="lbl">मिनिटे</span>', 1),
    ('<span class="lbl">seconds</span>', '<span class="lbl">सेकंद</span>', 1),
    ("id=\"countdownDone\">Today's the day</p>", 'id="countdownDone">आज तो शुभदिवस!</p>', 1),
    ('Celebrations begin on Tuesday, 29&nbsp;December.', 'सोहळ्याची सुरुवात मंगळवार, 29&nbsp;डिसेंबर रोजी.', 1),

    # ---- Events ----
    ('<p class="ev-day rv">Tuesday, 29 December</p>', '<p class="ev-day rv">मंगळवार, 29 डिसेंबर</p>', 2),
    ('id="eng-h">The engagement</h2>', 'id="eng-h">साखरपुडा</h2>', 1),
    ('alt="Illustration of Pramod and Shruti at their engagement, in a navy bandhgala and a lilac saree, in front of a floral arch"',
     'alt="साखरपुड्याच्या दिवशी प्रमोद व श्रुती, फुलांच्या कमानीसमोर"', 1),
    ('<p class="ev-big rv">5:00 pm</p>', '<p class="ev-big rv">सायं. 5:00 वा.</p>', 1),
    ('<p class="ev-place rv">Shivkamal Lawns</p>', '<p class="ev-place rv">शिवकमल लॉन्स</p>', 3),
    ('      Add to calendar\n', '      कॅलेंडरमध्ये जोडा\n', 3),
    ('id="haldi-h">Haldi</h2>', 'id="haldi-h">हळदी समारंभ</h2>', 1),
    ('alt="Illustration of Pramod and Shruti in yellow at their haldi, laughing as family apply turmeric"',
     'alt="हळदीच्या दिवशी पिवळ्या पोशाखात हसणारे प्रमोद व श्रुती"', 1),
    ('<p class="ev-big rv">After the engagement, onwards</p>', '<p class="ev-big rv">साखरपुड्यानंतर</p>', 1),
    ('<p class="ev-day rv">Wednesday, 30 December</p>', '<p class="ev-day rv">बुधवार, 30 डिसेंबर</p>', 1),
    ('id="wedding-h">The wedding</h2>', 'id="wedding-h">शुभविवाह</h2>', 1),
    ('alt="Illustration of Pramod and Shruti in ivory and gold exchanging flower garlands under a marigold arch"',
     'alt="झेंडूच्या कमानीखाली वरमाला घालताना प्रमोद व श्रुती"', 1),
    ('<p class="ev-big rv">5:45 pm</p>', '<p class="ev-big rv">शुभमुहूर्त: सायं. 5:45 वा.</p>', 1),
    ("<p class=\"forever rv\">Next comes forever,<br>and we'd love you there.</p>",
     '<p class="forever rv">सात जन्मांच्या सोबतीची सुरुवात,<br>आपल्या आशीर्वादाने.</p>', 1),

    # ---- Venue ----
    ('id="venue-h">Getting there</h2>', 'id="venue-h">विवाहस्थळ</h2>', 1),
    ('<h3>Shivkamal Lawns</h3>', '<h3>शिवकमल लॉन्स</h3>', 1),
    ('<p>Open the location in Google Maps for directions.</p>', '<p>मार्गदर्शनासाठी Google Maps मध्ये ठिकाण उघडा.</p>', 1),
    ('        Get directions\n', '        मार्ग पाहा\n', 1),

    # ---- Closing note ----
    ('Your presence and blessings are the most precious gifts we could ask for.',
     'आपली उपस्थिती आणि आशीर्वाद हीच आमच्यासाठी सर्वात मौल्यवान भेट.', 1),
    ('We look forward to celebrating with you and your family.',
     'आपल्यासोबत हा आनंद साजरा करण्याची आम्ही आतुरतेने वाट पाहत आहोत.', 1),
    ('<p class="closing-with">With love,</p>', '<p class="closing-with">स्नेहपूर्वक,</p>', 1),
    ('<p class="closing-names">Pramod &amp; Shruti</p>', '<p class="closing-names">प्रमोद व श्रुती</p>', 1),
    ('<p class="closing-fam">Gunaware &amp; Kaldate families</p>', '<p class="closing-fam">गुणवरे व काळदाते परिवार</p>', 1),

    # ---- Buttons ----
    ('</svg>Directions</a>', '</svg>मार्ग</a>', 1),
    ('aria-label="Quick actions"', 'aria-label="त्वरित पर्याय"', 1),
    ('Pause auto-scroll', 'आपोआप पुढे जाणे थांबवा', 2),
    ('Resume auto-scroll', 'आपोआप पुढे जाणे सुरू करा', 1),
    ('Pause music', 'संगीत थांबवा', 2),
    ('Play music', 'संगीत सुरू करा', 1),

    # ---- Script text ----
    ("'Dear ' + guest", "'प्रिय ' + guest", 1),
    ("\"Pramod & Shruti's wedding celebrations. Directions: \"", '"प्रमोद व श्रुती यांचा विवाह सोहळा. मार्ग: "', 1),
    ("location: 'Shivkamal Lawns'", "location: 'शिवकमल लॉन्स'", 1),
    ('gcal("Pramod & Shruti: Engagement"', 'gcal("प्रमोद व श्रुती: साखरपुडा"', 1),
    ('gcal("Pramod & Shruti: Haldi"', 'gcal("प्रमोद व श्रुती: हळदी समारंभ"', 1),
    ('gcal("Pramod & Shruti: Wedding"', 'gcal("प्रमोद व श्रुती: शुभविवाह"', 1),
    ("ctx.font = 'italic 500 26px Fraunces, Georgia, serif';", "ctx.font = '26px \"Tiro Devanagari Marathi\", serif';", 1),
    ("ctx.fillText('Scratch here'", "ctx.fillText('येथे घासा'", 1),
    ("ctx.fillText('to reveal the big day'", "ctx.fillText('शुभदिवस पाहण्यासाठी'", 1),
]

# Devanagari needs its own faces and a little more line height
MR_CSS = r"""
  /* ================= Marathi ================= */
  html[lang="mr"]{ font-synthesis:none; }
  html[lang="mr"] .names, html[lang="mr"] .person-name, html[lang="mr"] .ev-title, html[lang="mr"] .reveal h2,
  html[lang="mr"] .section-head h2, html[lang="mr"] .closing-names, html[lang="mr"] .sd-date, html[lang="mr"] .venue-card h3{
    font-family:'Fraunces', 'Rozha One', 'Tiro Devanagari Marathi', serif; letter-spacing:0;
  }
  html[lang="mr"] .names{ line-height:1.2; font-size:clamp(3rem, 14vw, 4.4rem); }
  html[lang="mr"] .names .amp{ font-size:.5em; line-height:1.3; }
  html[lang="mr"] .person-name{ line-height:1.25; font-size:clamp(3rem, 15vw, 4rem); }
  html[lang="mr"] .person-name .chi{ display:block; font-family:'Tiro Devanagari Marathi', serif; font-size:.34em; line-height:1.5; color:var(--sindoor); }
  html[lang="mr"] .ev-title, html[lang="mr"] .reveal h2{ line-height:1.3; }
  html[lang="mr"] .lineage-names:first-child{ margin-top:0; }
  html[lang="mr"] .lineage-after{ margin-top:8px; }
  html[lang="mr"] .gate-invite{ font-size:1.1rem; line-height:1.75; }
  html[lang="mr"] .closing-msg{ line-height:1.6; }
  html[lang="mr"] .ev-big{ line-height:1.5; }
"""

# Words that must not survive in the visible Marathi page
LEFTOVER = ["Groom", "Bride", "Son of", "Daughter of", "December", "engagement", "Haldi",
            "Add to calendar", "Directions", "With love", "Getting there", "Save the date",
            "Open the invitation", "are getting married", "Wednesday", "Tuesday", "Shivkamal"]


def main():
    h = SRC.read_text(encoding="utf-8")
    problems = []
    for en, mr, n in T:
        c = h.count(en)
        if c != n:
            problems.append(f"expected {n}x, found {c}x: {en[:90]!r}")
            continue
        h = h.replace(en, mr)
    if problems:
        sys.exit("Marathi build stopped; these English phrases changed:\n  " + "\n  ".join(problems))

    # Fraunces has no Devanagari letters, so fall back to Tiro Devanagari Marathi
    h = re.sub(r"font-family:\s*'Fraunces',\s*(?:Georgia,\s*)?serif",
               "font-family:'Fraunces', 'Tiro Devanagari Marathi', serif", h)
    # Shared files live one folder up
    h = re.sub(r'((?:src|href)=")(img|audio)/', r'\1../\2/', h)
    h = h.replace("  @media (min-width:600px){", MR_CSS + "\n  @media (min-width:600px){", 1)

    # Check only what guests see: text between tags, alt text and labels
    page = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    head = page[:page.index("<body")]
    body = re.sub(r"<script>.*?</script>", "", page[page.index("<body"):], flags=re.S)
    seen = " ".join(re.findall(r">([^<]+)<", body))
    seen += " " + " ".join(re.findall(r'(?:alt|aria-label)="([^"]*)"', body))
    seen += " " + " ".join(m for pair in re.findall(r'<title>(.*?)</title>|(?:og:(?:title|description|image:alt)|name="description") content="([^"]*)"', head) for m in pair)
    left = [w for w in LEFTOVER if w.lower() in seen.lower()]
    if left:
        sys.exit("Marathi build stopped; untranslated text found: " + ", ".join(left))

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(h, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(T)} translations)")


if __name__ == "__main__":
    main()
