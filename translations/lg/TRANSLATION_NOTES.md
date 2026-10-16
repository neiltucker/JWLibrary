# Translation Notes — Luganda

Source: https://github.com/neiltucker/JWLibrary (files as of 16 Oct 2026). Translated by Claude (AI). **Confidence: moderate. A fluent Luganda speaker should review and correct this before it is distributed** — expect some unnatural phrasing and grammar errors.

## Changes in this version (16 Oct 2026, update 2)
* Three facilitator tips added to `JWLibrary_Class.md`, the README and page 4 of the curriculum PDF, matching the English: printed handouts, QR table cards, and Add to Home Screen. The old "Empapula ez'Okugaba" PDF tip was replaced, as in the English.
* README lists the new files: `manifest-lg.json`, `sw.js`, `Table_Cards_Luganda_lg.pdf`, `QR_Luganda_lg.png/.svg`.
* Web page: the Add to Home Screen tip now says to open the new icon once while online, and that PDFs, videos and JW.ORG links still need internet. The page now uses its own `manifest-lg.json`, so a home-screen icon opens the Luganda page.
* Web page: long words such as *Ebyawandiikibwa* now wrap on narrow phones instead of making the page scroll sideways (this happened even at normal text size).
* Please check the new sentences (see items 6–7 in `REVIEWER_CHECKLIST.md`).

## Changes in this version (16 Oct 2026)
* **Page renamed** from `index.html` to `lg.html` so it can sit next to the English `index.html` and the other languages. A **language menu** (English / Kiswahili / Luganda / Thuɔŋjäŋ) and matching `hreflang` tags were added; the menu works when all four pages are in the same folder.
* **The device choice is now remembered** and applied when the page opens, so the right instructions and help links show immediately (the original page only updated them after a device button was tapped).
* **`REVIEWER_CHECKLIST.md`** added: a form for native-speaker reviewers to record exactly what the app's buttons say in this language, plus terms to confirm.
* No wording changes in this version. The comparison with another Luganda translation did not show wording worth adopting; the open questions are listed in `REVIEWER_CHECKLIST.md`.

## Files
| File | What was done |
| :--- | :--- |
| `README.md` | Fully translated. |
| `JWLibrary_Class.md` | Fully translated. |
| `lg.html` (was `index.html`) | All visible text, tooltips, and device-switcher JavaScript text translated. CSS, IDs, and storage keys unchanged. `lang="lg"`. |
| `generate_pdfs.py` | All printed text translated. Two code changes: output file names, and a Unicode font setup (see below). |
| `REVIEWER_CHECKLIST.md` | New: form for native-speaker reviewers. |
| `tinyurl.txt` | Copied unchanged (it only contains a link). |

The repo's PDFs were not translated (as requested). Running `generate_pdfs.py` creates `Enteekateeka ya Kiraasi ya JW Library.pdf` and `Enteekateeka y'Amasomo ga JW Library.pdf` without overwriting the English PDFs. Tested: 1 page and 4 pages, same as the original.

**Font change:** the original script uses Helvetica, which cannot print the Luganda letter **ŋ** (as in *Enkuŋŋaana*). The translated script looks for a font that contains it (DejaVu Sans, Arial, or Segoe UI) and prints a warning if none is found. For guaranteed results, put the four DejaVu Sans `.ttf` files in a `fonts` folder next to the script.

## Terminology
**Verified on jw.org / wol.jw.org (Luganda):** Bayibuli, Matayo, *Omunaala gw'Omukuumi* (Watchtower), Abajulirwa ba Yakuwa, Enkuŋŋaana (meetings), Ebitabo n'Obutabo (publications), Noonya (search), Vidiyo.

**From my own knowledge, not verified:** Ekizimbe ky'Obwakabaka (Kingdom Hall), Olubereberye (Genesis), Ekyawandiikibwa eky'Olunaku (Daily Text), Olukuŋŋaana olw'Omu Wiiki / Olukuŋŋaana olwa Wikendi (midweek / weekend meeting), akatabo k'olukuŋŋaana (meeting workbook).

**My own translations of app labels:** I did not find Luganda JW Library help pages, so I don't know whether the app's buttons appear in Luganda or English for these users. Every app label is therefore written in Luganda with the English label in parentheses (e.g. **Okwesomesa** *(Personal Study)*, **Entegeka** *(Settings)*). Video title *"Lwaki Oyiga Bayibuli?"* is my own translation.

Phone/computer system menus (e.g. *Settings > Display*) are left in English.

## Links
All JW.ORG help links remain on the English pages (labelled *mu Lungereza*), since I did not find Luganda versions of the JW Library help pages.
