# Translation Notes — Kiswahili

Source: https://github.com/neiltucker/JWLibrary (files as of 16 Oct 2026). Translated by Claude (AI). **Please have a fluent Swahili speaker review before distributing.**

## Changes in this version (16 Oct 2026, update 2)
* Three facilitator tips added to `JWLibrary_Class.md`, the README and page 4 of the curriculum PDF, matching the English: printed handouts, QR table cards, and Add to Home Screen. The old "Karatasi za Kugawa" PDF tip was replaced, as in the English.
* README lists the new files: `manifest-sw.json`, `sw.js`, `Table_Cards_Kiswahili_sw.pdf`, `QR_Kiswahili_sw.png/.svg`.
* Web page: the Add to Home Screen tip now says to open the new icon once while online, and that PDFs, videos and JW.ORG links still need internet. The page now uses its own `manifest-sw.json`, so a home-screen icon opens the Kiswahili page.
* Web page: long words now wrap on narrow phones instead of making the page scroll sideways.
* Please check the new sentences (see item 6 in `REVIEWER_CHECKLIST.md`).

## Changes in this version (16 Oct 2026)
* **Page renamed** from `index.html` to `sw.html` so it can sit next to the English `index.html` and the other languages. A **language menu** (English / Kiswahili / Luganda / Thuɔŋjäŋ) and matching `hreflang` tags were added; the menu works when all four pages are in the same folder.
* **The device choice is now remembered** and applied when the page opens, so the right instructions and help links show immediately (the original page only updated them after a device button was tapped).
* **`REVIEWER_CHECKLIST.md`** added: a form for native-speaker reviewers to record exactly what the app's buttons say in this language, plus terms to confirm.
* **Wording updated to match jw.org:** *Alama za Kukumbuka Ukurasa* (Bookmarks; used in jw.org's Swahili help titles), *Vibandiko* (Tags; used in jw.org's Swahili JW Library FAQ), *daftari la mkutano* (meeting workbook; jw.org's Swahili term). Also *kompyuta kibao* (tablet) and *kipakatalishi* (laptop), which are the standard Swahili words.
* **Phone and computer settings** are now given in Swahili with the English in brackets, e.g. *Muda wa Skrini Kuzima (Screen timeout)*. The Swahili setting names are my translations; the exact wording depends on the device.
* **Two more help links now go to Swahili pages**, both confirmed to exist: *Mambo Mbalimbali Kuhusu JW Library* and *Tumia Sehemu ya Zitakazochezwa* (Playlists).

## Files
| File | What was done |
| :--- | :--- |
| `README.md` | Fully translated. |
| `JWLibrary_Class.md` | Fully translated. |
| `sw.html` (was `index.html`) | All visible text, tooltips, and the device-switcher JavaScript text translated. CSS, IDs, and storage keys unchanged. `lang="sw"`. |
| `generate_pdfs.py` | All printed text translated; code unchanged except the output file names (see below). |
| `REVIEWER_CHECKLIST.md` | New: form for native-speaker reviewers. |
| `tinyurl.txt` | Copied unchanged (it only contains a link). |

The two PDFs in the repo were not translated (as requested). Running `generate_pdfs.py` produces Swahili PDFs named `Ratiba ya Darasa la JW Library.pdf` and `Mtaala wa Mafunzo ya JW Library.pdf`, so the English PDFs are not overwritten. Tested: 1 page and 4 pages, same as the original.

## Terminology
**Verified on jw.org Swahili help pages** (https://www.jw.org/sw/msaada-mtandaoni/jw-library/): Biblia, Machapisho, Andiko la Siku, Historia, Tafuta, Alama za Kukumbuka Ukurasa (Bookmarks), Vibandiko (Tags, from the FAQ), Tia Alama (highlight), Pakua (download). Bible book name *Mathayo* verified on wol.jw.org.

**Also verified on jw.org:** *Jumba la Ufalme* and *juma* for "week" (jw.org/sw/mashahidi-wa-yehova/mikutano/), *daftari la mkutano* (jw.org Swahili workbook pages).

**From my own knowledge, not verified on jw.org in this session:** Mnara wa Mlinzi (Watchtower), Mkutano wa Katikati ya Juma / Mkutano wa Mwisho wa Juma, Mashahidi wa Yehova. I am confident in these but did not confirm them.

**My own translations of app labels** (official Swahili wording not found): Mikutano (Meetings), Funzo la Kibinafsi (Personal Study), Mipangilio (Settings), Hifadhi Nakala na Rejesha (Backup and Restore), Tengeneza Nakala ya Akiba (Create Backup), Yaliyopakuliwa (Downloaded), Ukubwa Zaidi (Largest Size), Ongeza Maelezo (Add Note). The English label is shown in parentheses next to these so students can match whatever their screen shows.

**Video title** *"Kwa Nini Ujifunze Biblia?"* is my translation of *"Why Study the Bible?"*; the official Swahili title may differ.

Phone/computer settings on the web page are given in Swahili with the English in brackets (e.g. *Kujifunga Kiotomatiki (Auto-Lock)*). The Swahili names are my translations; reviewers should check them against a phone set to Swahili.

## Links
JW.ORG help links point to the Swahili pages where I confirmed they exist (index, Apple, Android, Windows, getting started, publications, highlighting, Android FAQ). The "Features" (*Mambo Mbalimbali*) and "Playlists" (*Tumia Sehemu ya Zitakazochezwa*) links now also go to Swahili pages, which I confirmed exist. Page addresses may change over time.
