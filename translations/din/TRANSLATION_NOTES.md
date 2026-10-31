# Translation Notes — Dinka (Thuɔŋjäŋ)

Source: https://github.com/neiltucker/JWLibrary (files as of 16 Oct 2026). Translated by Claude (AI).

## ⚠️ Read this first
**Confidence: low. Treat this as a rough first draft, not a finished translation.** Dinka has very little written material available, and my command of its grammar, vocabulary, and dialect differences is limited. Many sentences are likely to be unnatural or wrong. **Do not give these files to students until a fluent Dinka reader has reviewed and corrected them.** Each Dinka file carries a visible "DRAFT — NOT YET REVIEWED" notice for this reason; remove it after review.

To make review easier:
* App button and screen names are kept in **English** (e.g. **Bible**, **Meetings**, **Create Backup**). WOL's own Dinka pages also show their interface in English, and simple English labels are less likely to mislead than my guesses.
* The legal disclaimer appears in Dinka **and** in the original English, because its exact wording matters.
* A reviewer can compare line-by-line with the English files in the original repo.

## Changes in this version (31 Oct 2026, update 7) — language help, Daily Text, Study Edition, review of jw.org/din
Applied to `din.html`, `JWLibrary_Class.md`, `README.md`, `generate_pdfs.py` (and the two Dinka PDFs it makes), `REVIEWER_CHECKLIST.md`, this file, `make_qr_and_cards.py` (Dinka card wording) and `Table_Cards_Dinka_din.pdf`. Sources were checked on jw.org/din and wol.jw.org on 31 Oct 2026.
* **Language help (all five tutorials):** one sentence added to the pre-class clinic tip on the web page, in the class outline, README and curriculum PDF page 4: *Të kɔɔr raan ye piɔ̈ɔ̈c athör ë thok dɛ̈t, tuany **Languages** icon (A/あ) ku lɔc thok kënë* (English beside it). The same sentence was added to the English, Kiswahili, Luganda and Ga tutorials. The PDFs leave out "(A/あ)" because the PDF font has no Japanese letters.
* **Daily Text:** *Examining the Scriptures Daily—2027* was published in Dinka on jw.org/din (What's New, 3 Oct 2026), but only as a PDF; it cannot be downloaded in Dinka in JW Library (checked in the app by the project owner). "Daily Text acïn ë Thuɔŋjäŋ" became **"Daily Text acïn ë Thuɔŋjäŋ në JW Library yic"** (not in Dinka *in JW Library*) in Exercises 1.1 and 2.3, the "Thok ë Baibol" tip, the class outline, README and PDF page 2. The facilitator tip now mentions the 2027 PDF on jw.org/din (opens outside the app).
* **Bible:** still no Dinka Bible (confirmed by the project owner). The default is now the ***New World Translation (Study Edition)*** in English, unless the facilitator recommends another Bible (pre-class checklist, Exercise 1.2, "Thok ë Baibol" tip, class outline, README, PDF page 2). Storage guidance is unchanged.
* **Text-size button:** "Appearance / Text Size icon" → **Text Settings / Appearance** (web page) and **Text Settings** (class outline, README, PDFs), the name used in current JW.ORG help ("Change Text Settings", iOS help). The Ga guide made the same change.
* **Dinka meanings beside English button names**, only where jw.org/din uses the word in its menus: **Bible** *(Baibol)*, **Search** *(Wïc)*, and *(Kuɔny)* (Help) on the JW.ORG help link.
* **Bible references:** examples now read *Mathayo 5*, as the Dinka meeting workbook writes references with numbers only (e.g. *JEREMIA 47-48*, 26 Oct–1 Nov 2026).
* **Exercise 2.2:** *ë pɛɛi kënë* ("this month") → *ë ëmën* *(the current issue)*, because each Dinka workbook issue covers two months (e.g. *Pɛɛi ë Dhoŋuan–Pɛɛi ë Thiëër 2026*).
* **Class Program PDF:** section heading *Tɔ̈ɔ̈k ku Nyuɔɔth ë Skrin* → *… ë Device*, as on the web page and in the outline; History added to the 0:18 demonstration (Bookmarks, History ku Search), as in the other files.
* **Class outline 0:22:** *Settings > Cellular Data* (iPhone) now also names *Mobile data* (Android).
* **Mac requirement:** "macOS 13 or later, with Apple Silicon (M1 or newer)" in the README and curriculum PDF, as on the App Store listing (version 15.9.2, checked 31 Oct 2026).
* **README:** `gaa.html` added to the "same folder" note; "four guide pages" → five.
* **Web page:** English passages marked `lang="en"` (draft notice, bracketed English notes, English legal notice, help links) so screen readers pronounce them correctly; each help link now says *(English)*. Dark/Light and Print buttons are unchanged: no Dinka words for them were found in JW publications.
* **QR table cards:** *"camera ë phone du"* → **"camera ë telapundu"** in `make_qr_and_cards.py`; `Table_Cards_Dinka_din.pdf` regenerated (QR code unchanged).
* **Reviewer checklist:** section 2 restructured like the Ga checklist: "Wording to check first (not found in any Dinka publication)", with the source of each item. The settled question about *Yakoba* / *Yekoba* was removed: the jw.org/din home page heading and the newest article (13 Oct 2026) use *Yakoba*.
* **Checked and unchanged:** *degiik* (minutes), *pɛɛi* (month) and *Athör Amat ë Lon ë Piööc ku Ciɛɛŋda* are all used in the October 2026 workbook. jw.org/din spells the *Watchtower* both *Ɣönbɛ̈ɛ̈rtïët* (Online Library) and possibly *Ɣönbɛ̈ɛ̈rtiët* (magazines page heading, as read by a text tool); the guide keeps *Ɣönbɛ̈ɛ̈rtïët*.
* `sw.js` cache version raised to `v20`.

## Changes in this version (30 Oct 2026, update 6) — shared fonts, QR script and template setup
These changes affect every language. The translated wording of the guide is unchanged.
* **Fonts:** `generate_pdfs.py` now uses DejaVu Sans from the shared `fonts/` folder at the top of the repository (with its license file), so the PDFs look the same and print every letter correctly on any computer, with no other downloads. Installed fonts are still used as a backup. Both Dinka PDFs were regenerated with the same words and page counts (1 and 4 pages); only the font changed (was Arial).
* **Output path:** the script writes its PDFs to the repository root using a path relative to the script, instead of the fixed `D:/cs/JWLibrary/` path.
* **Page footer:** the legal notice at the bottom of each curriculum page now shrinks slightly when needed, so it always fits across the page.
* **QR code and table cards:** now made for every language by the shared `make_qr_and_cards.py` at the top of the repository (`python make_qr_and_cards.py din` for this language only). It reads the web address from `site_config.json`, or works it out from the repository's GitHub address. The card wording and layout are unchanged, and the QR code still opens https://neiltucker.github.io/JWLibrary/din.html (checked by decoding it).
* **README:** the online guide link now opens the Dinka page (`din.html`), with the English page on a second line, labelled *(ë Thoŋ ë Liŋliŋ / English)* as before. `tinyurl.txt` was removed from the repository and from the file list.
* `sw.js` cache version raised to `v19`. Each copy of the guide now keeps its own offline files, so copies published under the same GitHub account no longer remove each other's saved pages.

## Changes in this version (17 Oct 2026, update 5)
* **Watchtower Study (web page, Exercise 1.3 step 3):** now *Ɣönbɛ̈ɛ̈rtïët (Watchtower Study)*, matching the Dinka-plus-English labels used elsewhere.
* **Table assistants:** "Kɔc ye Kuɔny në **Tëëbil**" in `JWLibrary_Class.md` and `generate_pdfs.py` (curriculum PDF page 4), matching the web page. "në mëth nhial" in the keyboard tip is a different phrase and was left unchanged. Neither word was found in Dinka JW publications, so the reviewer is asked to confirm.
* **Manifest:** *aguir* → **aguiɛɛr**, the usual spelling in recent Dinka JW publications (89 results, e.g. the 2026 Memorial Bible-reading schedule "Aguiɛɛr ë Cökke Baibol…"; *aguiir* has 2).
* **Reviewer checklist:** settled item on *wënh* removed; the phone item now only asks to confirm *telapundu*; the "optional" item now asks about *(Cïï kë bï cɔk looi)*; the table item asks to confirm *tëëbil*; item 2 no longer lists *gät*. Items were renumbered (old 9–12 are now 8–11); earlier entries below use the old numbers.
* Both Dinka PDFs regenerated; `sw.js` cache version raised to `jw-tutorial-v7`.

## Changes in this version (17 Oct 2026, update 4) — terms checked against Dinka JW.ORG / wol.jw.org (2024–2026)
Applied to `din.html`, `JWLibrary_Class.md`, `generate_pdfs.py` (and the two Dinka PDFs it makes), `README.md` and `manifest-din.json`. Sources are Dinka publications on wol.jw.org (Dinka library `r713/lp-di`); meanings were worked out from context, so a Dinka speaker should still confirm them.
* **Tap:** *gät* (which means "write") → **tuany** (*mwb25* November, "Tuany 'Donations'…"; *w25* August p. 32). *gät* is kept where it means "written/registered" ("trademark cï gät", "kä cï gät") and in "gät nyin" (bookmark).
* **Download:** English *download* → **jatpiny** (*mwb24* November; *mwb25* June/July and December; *w25* July). The app label **Downloaded** stays in English.
* **Phone:** *phone* → **telapun** (34 results, many from 2026); "your phone" → **telapundu**, as in *w26* June. Resolves checklist item 9 (*telepun* / *phone*).
* **Internet:** *intanet* (0 results) → **nɛt** (*w26*, *mwb26*: "ë kueer ë nɛtic", online).
* **Video:** singular **bideo** (222 results, *mwb26*); plural **Bideoth** (jw.org menu) is kept where several videos are meant.
* **Matthew:** **Mathayo** (Dinka *Enjoy Life Forever*, e.g. "Mathayo 24:14"). In the Bible exercise the screen shows the English Bible, so the text says *Matthew — Mathayo*.
* **Kingdom Hall:** *luaŋ ë Bääny Nhialic* → **luaŋ ë Bääny ë Nhialic** (*w26* June and August).
* **Meeting workbook:** **Athör Amat ë Lon ë Piööc ku Ciɛɛŋda** (official title, WOL Meetings page 2026).
* **"week":** in Dinka *week* means "you (plural)" (e.g. *w25* April, "Week Riënythii, Kiëëtkë Mak ku Timothï" = "Young Brothers—Imitate Mark and Timothy"). "amat ë week ëbën" was therefore removed; the English *(every week)* is used until a Dinka speaker supplies the right word.
* **No Daily Text or Bible in Dinka:** the Dinka library on wol.jw.org has no *Examining the Scriptures Daily* and no New World Translation; Dinka scripture links on JW sites open the **English** Bible (e.g. the 2026 Memorial Bible-reading schedule). Exercise 1.1 now practises text size on this week's Dinka *Ɣönbɛ̈ɛ̈rtïët*; Exercise 1.2 uses the New World Translation **in English by default, or another language the facilitator judges best**; Exercise 2.3 uses the Bible in that language or a short Dinka video. A facilitator tip, the checklist and early-arrival wording were updated to match.
* **Video title:** *"Why Study the Bible?"* = **"Ye Wɛ̈tŋö Ye Yïn Baibol Piɔ̈ɔ̈cë?"** (Dinka *Enjoy Life Forever* Lesson 1, 3:14 video).
* **PDFs:** both Dinka PDFs now carry a "DRAFT — NOT YET REVIEWED" line (on every page of the curriculum) and a link to https://www.jw.org/din/; the curriculum ends with the English original of the legal notice.
* **Manifest:** "program de JW Library" → "app de JW Library".
* **Jehovah's Witnesses:** *Ciëëtke Yakoba* is kept. The newest 2026 publications (July–August) use *Yakoba*; *Yekoba* also still appears in 2026 and in the jw.org/din header. (This corrects the conflicting note in the first 16 Oct update.)
* **Not changed (for the reviewer):** *ka* vs JW's *awu* ("or"); *amat* vs JW's plural *amɛtmɛɛt*; *cuɔ̈ɔ̈t ë röl* vs JW's "dhuɔ̈k röl piny" (turn the sound down, *w26* June). `Table_Cards_Dinka_din.pdf` still says "phone"; the script that made it is not in this repository. *(Fixed in update 7: the card now says* telapundu*.)*
* **App interface:** JW Library has no Dinka interface (Dinka is not in the App Store's language list), so English button names remain correct.

## Changes in this version (16 Oct 2026, update 3)
*Note (update 4): this update said terms were "aligned with modern JW.ORG Dinka literature", but tap, download, phone and internet were not; they were aligned in update 4.*
* **Standardized terminology aligned with modern JW.ORG Dinka literature (last 2–3 years):**
  * Time units updated from the English loanword *minit* to modern Dinka *degiik* across schedules and tips.
  * Media terms updated from *video* to standard localized *bideoth*.
  * Theocratic terms aligned with official modern usage: *Watchtower* -> *Ɣönbɛ̈ɛ̈rtïët*, *Kingdom Hall* -> *luaŋ ë Bääny Nhialic*, *paragraph* -> *abër*, and *Jehovah's Witnesses* -> *Ciëëtke Yakoba*.
  * Standardized breathy and diphthong orthography: *ëbën* (replacing *ëbɛ̈n*) and *apiɛth* (replacing *apieth*).
  * Generated PDFs refreshed with updated vocabulary.

## Changes in this version (16 Oct 2026, update 2)
* Three facilitator tips added to `JWLibrary_Class.md`, the README and page 4 of the curriculum PDF, matching the English: printed handouts, QR table cards, and Add to Home Screen. The Dinka wording reuses the phrases from the web page, with the English in brackets. The old "Athör bï Gam Kɔc" PDF tip was replaced, as in the English.
* README lists the new files: `manifest-din.json`, `sw.js`, `Table_Cards_Dinka_din.pdf`, `QR_Dinka_din.png/.svg`.
* Web page: the Add to Home Screen tip now adds, in English, that learners should open the new icon once while online, and that PDFs, videos and JW.ORG links still need internet. The page now uses its own `manifest-din.json`, so a home-screen icon opens the Dinka page.
* Web page: long words now wrap on narrow phones instead of making the page scroll sideways.
* Wording questions for reviewers are listed as items 6–11 in `REVIEWER_CHECKLIST.md`.

## Changes in this version (16 Oct 2026)
* **Page renamed** from `index.html` to `din.html` so it can sit next to the English `index.html` and the other languages. A **language menu** (English / Kiswahili / Luganda / Thuɔŋjäŋ) and matching `hreflang` tags were added; the menu works when all four pages are in the same folder.
* **The device choice is now remembered** and applied when the page opens, so the right instructions and help links show immediately (the original page only updated them after a device button was tapped).
* **`REVIEWER_CHECKLIST.md`** added: a form for native-speaker reviewers to record exactly what the app's buttons say in this language, plus terms to confirm.
* **Jehovah's Witnesses** is now *Ciëëtke Yekoba* in the Dinka text, as used on jw.org/din. The English original of the disclaimer is kept alongside.
* **Link to jw.org in Dinka** (https://www.jw.org/din/) added to the help links, README and class outline.
* The text-size control is labelled in Dinka with the English in brackets.

## Files
| File | What was done |
| :--- | :--- |
| `README.md` | Translated (draft), with notice. |
| `JWLibrary_Class.md` | Translated (draft), with notice. |
| `din.html` (was `index.html`) | Visible text and device-switcher text translated (draft); draft notice added under the header; CSS, IDs, and storage keys unchanged. `lang="din"`. |
| `generate_pdfs.py` | Printed text translated (draft). Code changes: output file names and a Unicode font setup. |
| `REVIEWER_CHECKLIST.md` | New: form for native-speaker reviewers. |

Running `generate_pdfs.py` creates `JW Library Class Program (Dinka).pdf` and `JW Library Tutorial Curriculum (Dinka).pdf` without overwriting the English PDFs. Tested: 1 page and 4 pages.

**Fonts:** Helvetica cannot print Dinka letters such as ɛ, ɔ, ɣ, ŋ, or ɛ̈/ɔ̈. The script uses DejaVu Sans from the shared `fonts/` folder at the top of the repository (see update 6) and warns if no suitable font is found.

## Terminology
**Seen in recent Dinka JW publications (2024–2026, wol.jw.org):** Baibol (Bible), Nhialic (God), Yakoba / Yekoba (Jehovah; both spellings occur), *Ciëëtke Yakoba* (Jehovah's Witnesses), *Ɣönbɛ̈ɛ̈rtïët* (Watchtower; study edition *Ɣönbɛ̈ɛ̈rtïët (Awereŋ ë piööc)*), *Athör Amat ë Lon ë Piööc ku Ciɛɛŋda* (meeting workbook), Kërthiaan (Christian), *amat* / *amɛtmɛɛt* (meeting / meetings), *degiik* (minutes), *abër* (paragraph), *luaŋ ë Bääny ë Nhialic* (Kingdom Hall), *app*, *liep* (open), *tuany* (tap), *jatpiny* (download), *telapun* (phone), *nɛt* (internet), *bideo* / *Bideoth* (video / videos), *Mathayo* (Matthew), *pɛɛi* (month), *Wïc* (Search) and *Kuɔny* (Help) (jw.org/din menus), *thanduŋ* (box; seen in the tag tip, not confirmed as "tag"). Meanings were inferred from context.

**Everything else is my own wording and unverified**, including the new sentences added in updates 4 and 7 (they carry the English in brackets).

## Links
All JW.ORG help links remain on the English pages; I did not find Dinka JW Library help pages.
