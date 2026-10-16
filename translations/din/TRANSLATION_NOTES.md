# Translation Notes — Dinka (Thuɔŋjäŋ)

Source: https://github.com/neiltucker/JWLibrary (files as of 16 Oct 2026). Translated by Claude (AI).

## ⚠️ Read this first
**Confidence: low. Treat this as a rough first draft, not a finished translation.** Dinka has very little written material available, and my command of its grammar, vocabulary, and dialect differences is limited. Many sentences are likely to be unnatural or wrong. **Do not give these files to students until a fluent Dinka reader has reviewed and corrected them.** Each Dinka file carries a visible "DRAFT — NOT YET REVIEWED" notice for this reason; remove it after review.

To make review easier:
* App button and screen names are kept in **English** (e.g. **Bible**, **Meetings**, **Create Backup**). WOL's own Dinka pages also show their interface in English, and simple English labels are less likely to mislead than my guesses.
* The legal disclaimer appears in Dinka **and** in the original English, because its exact wording matters.
* A reviewer can compare line-by-line with the English files in the original repo.

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
**Seen on wol.jw.org Dinka pages:** Baibol (Bible), Yekoba (Jehovah), Nhialic (God), Kuɛ̈n ë Baibol (Bible reading), Kërthiaan (Christian), *Ɣönbrtïït* (in the Watchtower title), *amat* (appears in meeting song headings). Exact meanings were inferred from context, not confirmed.

**Everything else is my own wording and unverified.** Bible book names (e.g. Matthew) are kept in English because I could not confirm the Dinka forms.

## Links
All JW.ORG help links remain on the English pages; I did not find Dinka JW Library help pages.
