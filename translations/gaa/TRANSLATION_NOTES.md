# Translation Notes — Ga

**Status: DRAFT — NOT YET REVIEWED.** Translated by Claude (AI) on 26 Oct 2026 from the English files in https://github.com/neiltucker/JWLibrary (as of 26 Oct 2026). Two Ga speakers are lined up to audit it. A visible draft notice is shown on `gaa.html`, in `JWLibrary_Class.md` and in `README.md`; remove it only after the review is complete.

Ga is a language with far less written material online than English, Kiswahili or Luganda, and the translator is not a fluent Ga speaker. Every sentence was built as far as possible from wording found in Ga publications on JW.ORG and the Ga Online Library (wol.jw.org/gaa). Sentences that could not be modelled on a published example are listed in `REVIEWER_CHECKLIST.md` section 2 so the reviewers can check them first.

## 1. How the app's button names are shown

**Decision: English button names in bold, with the Ga meaning in brackets where JW.ORG gives one.** Examples: **Bible** *(Biblia)*, **Publications** *(Woji kɛ Nibii)*, **Meetings** *(Asafoŋ Kpeei)*, **Daily Text** *(Daa Gbi Ŋmalɛ Lɛ)*, **Largest Size** *(Edalɛ)*.

Evidence:
* **JW.ORG's Ga JW Library help pages** (Android): https://www.jw.org/gaa/sait-l%C9%9B-n%C9%94-yelik%C9%9Bbuam%C9%94/jw-library/ . They keep the app's labels in English and sometimes add Ga in brackets: "Bible (Biblia)", "Publications (Woji kɛ Nibii)", "Languages (Wiemɔi)", "Text Settings (Niŋmai lɛ adaramɔ)", "Frequently Used (Nɔ ni Okɛfɔɔ Nitsumɔ)", "Largest Size (Edalɛ)", "Open in (Gbelemɔ yɛ)". Other labels appear in English only: Daily Text, Bookmark, History, Search, Highlight, Delete, Downloaded, Download, More, Menu, Clear.
  *Caution:* these help pages describe JW Library 1.2–1.6 (May 2014 – November 2015), so they are older than the three-year window. They were used for the label convention and for instruction wording, not for today's screen layout.
* **Recent Ga publications (2023–2026) do the same:**
  * *w23* March p. 32 — "Article Series", "What's New" and "Favorite" in English for JW Library ("Nibii Hee Ni Akɛwo Nɔ" is given only for jw.org). https://wol.jw.org/gaa/wol/d/r121/lp-ga/2023328
  * *mwb24* May (May 6-12) — "fã ni ji 'Personal Study'" (the section called "Personal Study"). https://wol.jw.org/gaa/wol/d/r121/lp-ga/202024161
  * *w25* June p. 32 — "Okɛ tag awo he yɛ JW Library® lɛ mli" ("tag" in English). https://wol.jw.org/gaa/wol/d/r121/lp-ga/2025447

Not confirmed: whether the JW Library app itself can show a Ga interface. See `REVIEWER_CHECKLIST.md` section 1.

## 2. Files

| File | What was done |
| :--- | :--- |
| `gaa.html` (repository root) | New. Built from the current English `index.html` (not from `lg.html`, so the Luganda reviewer's Luganda-only choices are not carried over). All visible text, tooltips and device-switcher JavaScript text translated. CSS, element IDs and storage keys unchanged. `lang="gaa"`, own manifest, draft notice, English original of the legal notice kept under the Ga version. |
| `manifest-gaa.json` (root) | New. Home-screen icon opens `gaa.html`. |
| `sw.js` (root) | `gaa.html` and `manifest-gaa.json` added to the files saved for offline use; Ga QR and table-card files added to the facilitator list; cache version raised `jw-tutorial-v10` → `jw-tutorial-v11`. |
| `index.html`, `sw.html`, `lg.html`, `din.html` (root) | Two lines each: "Ga" added to the language menu and a `hreflang="gaa"` link added. Nothing else changed. |
| `QR_Ga_gaa.png`, `QR_Ga_gaa.svg`, `Table_Cards_Ga_gaa.pdf` (root) | New. QR code for https://neiltucker.github.io/JWLibrary/gaa.html (checked by decoding the PNG, the SVG and all four cards). Same size and layout as the other languages. |
| `JW Library Class Program (Ga).pdf`, `JW Library Tutorial Curriculum (Ga).pdf` (root) | New. Made by `generate_pdfs.py`: 1 page and 4 pages, same as the English. ASCII file names (as for Dinka) so links and downloads work everywhere. |
| `translations/gaa/README.md`, `JWLibrary_Class.md` | Translated in full from the English. |
| `translations/gaa/generate_pdfs.py` | Ga text; same layout as the English. Uses the Unicode font search from the Luganda script (now requiring ɛ ɔ ŋ). Writes the PDFs to the repository root using a path relative to the script, instead of the fixed `D:/cs/JWLibrary/` path used in the other scripts. |
| `translations/gaa/make_qr_and_cards.py` | New helper that makes the QR code and the table cards (there was no script for these in the repository). Change `PAGE_URL` if the guide is hosted elsewhere. |
| `translations/gaa/REVIEWER_CHECKLIST.md` | Form for the Ga reviewers. |

## 3. Terminology

### 3a. Verified in Ga publications from the last three years (Oct 2023 – Oct 2026) or current Ga JW.ORG / WOL pages
| English | Ga used | Source |
| :--- | :--- | :--- |
| Bible (New World Translation) | *Biblia*; *Ŋmalɛ Krɔŋkrɔŋ Lɛ Jeŋ Hee Shishitsɔɔmɔ* | Ga Bible on WOL: https://wol.jw.org/gaa/wol/binav/r121/lp-ga/nwt |
| Matthew / Genesis / chapters | *Mateo* / *1 Mose* / *Yitsei* (sing. *yitso*) | same |
| Meetings (WOL menu) | *Asafoŋ Kpeei* | WOL menu, https://wol.jw.org/gaa/wol/h/r121/lp-ga |
| Midweek meeting | *otsi teŋ kpee* | *w23* April pp. 20-25, par. 2 (https://wol.jw.org/gaa/wol/d/r121/lp-ga/2023365); *od* chap. 7 heading "OTSI TEŊ KPEE" |
| Weekend meeting | *otsi naagbee kpee* | *od* chap. 7 heading "OTSI NAAGBEE KPEE" (https://wol.jw.org/gaa/wol/d/r121/lp-ga/1102014937); *w23* April p. 20, par. 2 ("asafoŋ kpee yɛ otsi lɛ naagbee"); *w27* January pp. 8-13, par. 13 https://wol.jw.org/gaa/wol/d/r121/lp-ga/2027244 |
| Watchtower Study | *Buu-Mɔɔ Nikasemɔ* | *w23* April pp. 20-25; *w25* February pp. 20-24; *w26* October pp. 24-29 |
| Watchtower study article (Meetings page) | *Buu-Mɔɔ Lɛ Mli Sane Ni Abaakase* | WOL meetings page, week of Oct 26 – Nov 1, 2026 |
| Meeting workbook | *Wɔshiɛmɔ Kɛ Wɔshihilɛ Kpee Nifeemɔ Wolo* | same page (*mwb26* September) |
| Daily text book | *Ŋmalɛi Lɛ Amli Ni Wɔɔkwɛ Daa—2026* | WOL home page |
| Online Library | *Buu-Mɔɔ INTANƐT NƆ WOJIATOOHE* | WOL site title |
| Jehovah's Witnesses | *Yehowa Odasefoi* | jw.org/gaa |
| tag | *tag* (English) | *w25* June p. 32 |
| Personal Study | "Personal Study" (English) | *mwb24* May |
| screen | *skrin* | *mwb24* May; *mwb25* January; *mwb26* January ("Hã ajie mfoniri lɛ yɛ skrin lɛ nɔ") |
| battery | *batri* | *w26* June pp. 26-30 |
| print | *printi* | *w24* March pp. 26-31 |
| registered trademark; non-commercial | *kadimɔnii ni akɛwo mla shishi*; *jeee jarayeli nifeemɔi* | Ga Terms of Use on jw.org (https://www.jw.org/finder?prefer=content&wtlocale=GA&docid=1011511) |

### 3b. Verified on JW.ORG's Ga JW Library help pages (older: app versions of 2014–2015)
*nyɛɛ … nɔ* (tap), *nyɛɛ … nɔ fioo* (press briefly), *gbala* (drag), *tsi kpɔ nɛɛ kɛya hiɛ loo sɛɛ* (move the slider), *gbelemɔ* (open), *taipimɔ* (type), *halamɔ* (choose), *ŋɔ / daunlodi* (download), *ŋwɛigbɛ* (top), *shishigbɛ* (bottom/below), *abɛkugbɛ* (left), *ninejurɔgbɛ* (right), *okadi* (icon), *atatu okadi* (cloud icon), *laaje* (disappears), *kpɔbii etɛ* (three dots, "More"), *okiibɔd* (keyboard), *okɛ kɔla akadi* (highlight), *kɔlai* (colours), *nibii ni atswaa aboɔ toi* (audio recordings), *vidioi* (videos), *oná gbɛ yɛ ofoŋ loo tablɛt lɛ nɔ* (free up space), *Daa Gbi Ŋmalɛ Lɛ* (daily text), *Woji kɛ Nibii* (publications), *Edalɛ* (largest size). Tip 1.1 copies a sentence pattern from the "Text Settings" help page.

### 3c. From older Ga publications (before Oct 2023), used only where no recent wording was found
* *mwb16* May pp. 2, 8: *okɛ kɔla akadi hetoi* (highlight answers), *kadimɔnii ni atsɛɔ lɛ bookmark*, *ehe ehiaaa ni oya Intanɛt lɛ nɔ dani onyɛ okɛtsu nii* (no internet needed once downloaded), *aŋkro nikasemɔ* (personal study), *Maŋtsɛyeli Asa* (Kingdom Hall). https://wol.jw.org/gaa/wol/d/r121/lp-ga/202016173 and .../202016164
* Video title *"Mɛni Hewɔ Esa akɛ Okase Biblia Lɛ?"* (*Why Study the Bible?*): *km* 9/14 p. 3 and *mwb16* May p. 8. A newer Ga title was not found; please confirm.
* *hdu* story 16 (dated September 1, 2021): *daa gbi ŋmalɛ*, *ilɛtrɔniki tsɔji*. https://wol.jw.org/gaa/wol/d/r121/lp-ga/502500213
* Colours *yɛlo*, *bluu*, *grin* (*w11* 2/15; *rr* chap. 3; *hdu*); *hulu* (sun); *ŋmɛlɛtswaa kome* (one hour); *kamera*; *blɛoo* (slowly); *dioo* (quietly); *Ojekoo* (greeting); *duŋ* / *la* (dark / light); *Too gbɛjianɔ* (arrange).

### 3d. My own wording — not found in any Ga publication (please check first)
* **Nifeemɔ 1.1** etc. for "Core Exercise 1.1" (from *Kpee Nifeemɔ Wolo*, "meeting workbook"); **Nikasemɔ 1** for "Lesson 1"; **Klas Lɛ Hiɛnyiɛlɔ** for "facilitator"; **Nɔkwɛmɔnɔ Ni Tsɔɔlɔ Lɛ Baafee** for "Instructor Demonstration".
* **kpɔ ni fãi titrii lɛ yɔɔ nɔ** for "main navigation bar".
* **Hã gbee lɛ sɛɛ afo** for "silence the sound" — built on the Bible's *"ahã afɔlei asɛɛ afo"* ("cause sacrifices to cease", Daniel 9:27). The English word "emergency" was not translated, to avoid alarming wording (the Luganda reviewer made the same choice).
* **nyɛɛ … nɔ ni oshi onine yɛ nɔ** for "press and hold".
* Loanwords not found: *mobail data* (found: *mobail foŋ*), *chaaja*, *fail* / *backup fail*, *Wi-Fi okadi*, *sisitɛm*, *speaker okadi*, *taskbar*.
* Glosses in brackets that are not app labels: *(Asafoŋ Kpeei)* for Meetings (WOL menu), *(Aŋkro Nikasemɔ)* for Personal Study (*mwb16*), *(Biblia)* and *(Woji kɛ Nibii)* (help pages).
* **Legal notice.** The Ga version follows the Terms of Use wording for "registered trademark" and "non-commercial", but the negative verbs (*amɛfeee, amɛhãaa gbɛ, amɛkwɛɛɛ nɔ, amɛwoooo he shika, amɛkpɛlɛɛɛ nɔ*) are my own. The English original is kept under it on every page.
* Phone and computer system menus (*Settings > Display*, *Auto-Lock*, *Screen timeout*) and "Share > Add to Home Screen" are left in English, as in the other translations.

## 4. Links
* The three "official tutorial" buttons and most help links stay on the current **English** JW.ORG pages (labelled *Blɔfo*), because the Ga help pages describe the 2014–2015 app.
* Added to the links card: JW.ORG in Ga (https://www.jw.org/gaa/), the Ga JW Library help pages, and the Ga Online Library (https://wol.jw.org/gaa/wol/h/r121/lp-ga). The footer "JW.ORG" link points to jw.org/gaa.

## 5. Checks done
* `gaa.html` rendered in a headless browser at 1200 px and 360 px wide: no script errors, no sideways scrolling (also at the largest text size), all three device buttons update the text, dark/light toggle and language menu work.
* PDFs: 1 and 4 pages; Ga letters ɛ, ɔ, ŋ and the tone marks in *kɛ́*, *afɔ̃* print correctly (DejaVu Sans).
* QR code decoded from the PNG, the SVG and all four table cards: `https://neiltucker.github.io/JWLibrary/gaa.html`.
