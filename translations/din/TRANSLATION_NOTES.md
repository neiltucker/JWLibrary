# Translation Notes — Dinka (Thuɔŋjäŋ)

Source: https://github.com/neiltucker/JWLibrary (files as of 16 Oct 2026). Translated by Claude (AI).

## ⚠️ Read this first
**Confidence: low. Treat this as a rough first draft, not a finished translation.** Dinka has very little written material available, and my command of its grammar, vocabulary, and dialect differences is limited. Many sentences are likely to be unnatural or wrong. **Do not give these files to students until a fluent Dinka reader has reviewed and corrected them.** Each Dinka file carries a visible "DRAFT — NOT YET REVIEWED" notice for this reason; remove it after review.

To make review easier:
* App button and screen names are kept in **English** (e.g. **Bible**, **Meetings**, **Create Backup**). WOL's own Dinka pages also show their interface in English, and simple English labels are less likely to mislead than my guesses.
* The legal disclaimer appears in Dinka **and** in the original English, because its exact wording matters.
* A reviewer can compare line-by-line with the English files in the original repo.

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
* **Not changed (for the reviewer):** *ka* vs JW's *awu* ("or"); *amat* vs JW's plural *amɛtmɛɛt*; *cuɔ̈ɔ̈t ë röl* vs JW's "dhuɔ̈k röl piny" (turn the sound down, *w26* June). `Table_Cards_Dinka_din.pdf` still says "phone"; the script that made it is not in this repository.
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
| `tinyurl.txt` | Copied unchanged. |

Running `generate_pdfs.py` creates `JW Library Class Program (Dinka).pdf` and `JW Library Tutorial Curriculum (Dinka).pdf` without overwriting the English PDFs. Tested: 1 page and 4 pages.

**Font change:** Helvetica cannot print Dinka letters such as ɛ, ɔ, ɣ, ŋ, or ɛ̈/ɔ̈. The script looks for a font that contains them and warns if none is found. Arial on Windows may not contain them all; for guaranteed results, put the four DejaVu Sans `.ttf` files in a `fonts` folder next to the script.

## Terminology
**Seen in recent Dinka JW publications (2024–2026, wol.jw.org):** Baibol (Bible), Nhialic (God), Yakoba / Yekoba (Jehovah; both spellings occur), *Ciëëtke Yakoba* (Jehovah's Witnesses), *Ɣönbɛ̈ɛ̈rtïët* (Watchtower; study edition *Ɣönbɛ̈ɛ̈rtïët (Awereŋ ë piööc)*), *Athör Amat ë Lon ë Piööc ku Ciɛɛŋda* (meeting workbook), Kërthiaan (Christian), *amat* / *amɛtmɛɛt* (meeting / meetings), *degiik* (minutes), *abër* (paragraph), *luaŋ ë Bääny ë Nhialic* (Kingdom Hall), *app*, *liep* (open), *tuany* (tap), *jatpiny* (download), *telapun* (phone), *nɛt* (internet), *bideo* / *Bideoth* (video / videos), *Mathayo* (Matthew), *thanduŋ* (box; seen in the tag tip, not confirmed as "tag"). Meanings were inferred from context.

**Everything else is my own wording and unverified**, including the new sentences added in update 4 (they carry the English in brackets).

## Links
All JW.ORG help links remain on the English pages; I did not find Dinka JW Library help pages.
