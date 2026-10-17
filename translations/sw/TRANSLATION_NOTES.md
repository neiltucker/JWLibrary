# Translation Notes — Kiswahili

Source: https://github.com/neiltucker/JWLibrary (files as of 16 Oct 2026). Translated by Claude (AI). **Please have a fluent Swahili speaker review before distributing.**

## Changes in this version (17 Oct 2026, update 4)
* **Grammar:** Windows screen-timeout tip now says "ili laptop **yako ibaki ikiwaka**" (was "laptop chako kibaki kikiwaka", left over from *kipakatalishi*).
* **Derivative-works clause** added to the footer of `sw.html` (in Swahili, and in the *English original* paragraph), matching `index.html`, `lg.html` and `din.html`: *"Toleo lolote lililobadilishwa, nakala zilizotokana na mradi huu, au madarasa yanayotokana nao ni jukumu la waandishi wao wenyewe na hayamwakilishi msimamizi wa kiolezo hiki cha asili."*
* **README:** the clause was added to the legal section; its *English original* now matches the English README's disclaimer word for word; and a short section points to the English README's "Guidelines for Adapting, Customizing, or Hosting Your Own Classes" and the `LICENSE` (BSD 3-Clause).
* `sw.js` is at `jw-tutorial-v7`. If v7 has already been published, raise it to `jw-tutorial-v8` when this update goes live so phones fetch the new `sw.html`.

## Changes in this version (17 Oct 2026, update 3) — terms checked against Swahili JW.ORG / wol.jw.org (2024–2026)
Applied to `sw.html`, `JWLibrary_Class.md`, `generate_pdfs.py` (and the two Swahili PDFs it makes) and `README.md`. Sources: Swahili publications on wol.jw.org and the Swahili JW Library help pages on jw.org.
* **Tap:** *gusa* → **bofya** (*mwb26* November and May, *mwb25* November: "Bofya tabo iliyoandikwa 'Michango'…"; *w25* August p. 32; the JW Library help pages). In JW publications *gusa* means touching in general. "skrini ya kugusa" (touchscreen) is unchanged.
* **Tablet:** *kompyuta kibao* → **tablet** (25 results, e.g. "simu ya mkononi au tablet"; *kompyuta kibao* is not used). **Laptop:** *kipakatalishi* (0 results) → **laptop**.
* **Weekend meeting:** *Mkutano wa Mwisho wa Juma* → **Mkutano wa Mwisho Juma** (*w25* November and December; the JW Library features page: "mkutano wa katikati ya juma na mwisho juma"). *Mkutano wa Katikati ya Juma* is confirmed (S-38; features page).
* **Workbook:** **Daftari la Mkutano wa Huduma na Maisha** (official title, WOL Meetings page 2026). **Watchtower Study:** *Funzo la Mnara wa Mlinzi* confirmed; the study edition is *Mnara wa Mlinzi (Funzo)*.
* **App labels from the Swahili help pages:** **Vialamisho** (Bookmarks button), **Zilizopakuliwa** (Downloaded; was *Yaliyopakuliwa*), **Kubwa Zaidi** (Largest Size; was *Ukubwa Zaidi*), **alama ya wingu** (cloud icon; was *aikoni ya wingu*), **Futa** (Delete; was *aikoni ya pipa la taka*), **Ukubwa wa Herufi** (text size button; was *Mwonekano / Ukubwa wa Maandishi*), **Simamisha** (Pause; was *Sitisha*; from "Njia Rahisi za Kucheza Media").
* **Settings:** the app's Settings button is now **Mapendezi** *(Settings)* (the settings page of wol.jw.org is "Mapendezi"; help title "Panga Habari Kulingana na Mapendezi Yako"). In JW publications *mipangilio* means "arrangements", not app settings. Phone menus (e.g. *Mipangilio > Skrini*) keep *Mipangilio*, the phone's own word.
* **Internet:** written **Intaneti** with a capital I, as in most JW publications.
* **Video title confirmed:** *"Kwa Nini Ujifunze Biblia?"* (*Furahia Maisha Milele!* Lesson 1, video "Kwa Nini Ujifunze Biblia?—Video Nzima", 3:14).
* **Tags:** *Vibandiko* kept (*mwb24* May; features page "kibandiko"); *w25* June p. 32 uses *tagi*.
* **Layout brought in line with the Luganda and Dinka pages:** a link card to **JW.ORG kwa Kiswahili** (https://www.jw.org/sw/); footer link to jw.org/sw; footer heading also in English; the **English original** of the legal notice in the footer, `JWLibrary_Class.md`, README and at the end of the curriculum PDF; the draft notice now explains that button names are given in Kiswahili with the English in brackets. A jw.org/sw link was added to the class outline, README and both PDFs.
* Both Swahili PDFs regenerated; `sw.js` cache version raised to `jw-tutorial-v8`.

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

**Verified in update 3 (wol.jw.org, 2024–2026):** *Mnara wa Mlinzi (Funzo)*, *Funzo la Mnara wa Mlinzi*, *Mkutano wa Katikati ya Juma*, *mkutano wa mwisho juma*, *Daftari la Mkutano wa Huduma na Maisha*, *programu* (app), *bofya* (tap), *kupakua*, *tablet*, *simu*, *Intaneti*, *tovuti*, *Funzo la Kibinafsi*, *Zitakazochezwa* (Playlists), *Kuyachunguza Maandiko Kila Siku* (daily text book).

**App labels not found on jw.org (my own wording):** Hifadhi Nakala na Rejesha (Backup and Restore), Tengeneza Nakala ya Akiba (Create Backup), Ongeza Maelezo (Add Note). *Mikutano* and *Funzo la Kibinafsi* are now confirmed (help and features pages); *Mapendezi* (Settings) is taken from wol.jw.org, not from the app. The English label is shown in parentheses next to these so students can match whatever their screen shows.

**Video title** *"Kwa Nini Ujifunze Biblia?"* is confirmed as the official title (update 3).

Phone/computer settings on the web page are given in Swahili with the English in brackets (e.g. *Kujifunga Kiotomatiki (Auto-Lock)*). The Swahili names are my translations; reviewers should check them against a phone set to Swahili.

## Links
JW.ORG help links point to the Swahili pages where I confirmed they exist (index, Apple, Android, Windows, getting started, publications, highlighting, Android FAQ). The "Features" (*Mambo Mbalimbali*) and "Playlists" (*Tumia Sehemu ya Zitakazochezwa*) links now also go to Swahili pages, which I confirmed exist. Page addresses may change over time.
