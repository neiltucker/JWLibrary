# Translation Notes — Luganda

Source: https://github.com/neiltucker/JWLibrary (files as of 16 Oct 2026). Translated by Claude (AI); reviewed and refined by Andrew Kalinaki (native Luganda speaker) on 22 Oct 2026.

## Changes in this version (22 Oct 2026, update 5) — Review by Andrew Kalinaki (PR #1) with refinements
Applied to `lg.html`, `JWLibrary_Class.md`, `generate_pdfs.py` (and the two regenerated Luganda PDFs), `README.md`, and `sw.js`:
* **Screen:** *ssirini* → **sikuliini** (natural phonetic borrowing in Luganda).
* **Keyboard:** *kiwandiikiro* → **kibodi** (natural contemporary usage).
* **Emergency Silence:** *Okusirisa mu Kabenje* → **Okusirisa amaloboozi** (removes the alarming word *kabenje*, which literally denotes traffic disasters/catastrophes).
* **Facilitator:** *Akulembera Kiraasi* → **Omulungamya** (accurate standard term from *okulungamya*).
* **Exercise headings:** simplified from *Okwegezaamu Okukulu* (Core Exercise) to **Okwegezaamu** (Exercise).
* **Backup:** *fayiro y'ekkopi* → **kkopi ya fayiro** (*kola kkopi ya fayiro*).
* **Grammar & flow:** *Jjira essimu* → *Jangu n'essimu*; legal notice improved (*tewagirwa mu butongole kibiina kya Watch Tower...*); projector screen in Kingdom Hall facilitator tips rendered as *olutimbe*.
* **Refinements on PR #1:** corrected domain `JW.RG` → `JW.ORG`; fixed missing period in silence tip; fixed stray apostrophe on line 1052; corrected orthography `koppi` → `kkopi`, `mweli` → `mw'eri`, and plural `Massimu` → `Amasimu`; standardized on `Intaneeti` (matching wol.jw.org); synchronized JavaScript device switcher strings to match new terms.
* Both Luganda PDFs regenerated; `sw.js` cache version raised to `jw-tutorial-v9`.

## Changes in this version (17 Oct 2026, update 4)
* **Settings:** the app's Settings button is now **By'Oyagala** *(Settings)* instead of *Entegeka*. *By'Oyagala* is the heading of the settings (preferences) page on the Luganda Online Library, wol.jw.org. In Luganda JW publications *entegeka* (128 results) and *ensengeka* (14 results) mean "arrangement" / "order" (e.g. *w22* October; *es22*; *mwbr26* January), never device or app settings. Where *entegeka* means "arrangement" (code comments; the phone's screen-timeout setting in `JWLibrary_Class.md`) it is unchanged.
* **Elision:** *bwa apu* → **bw'apu** and *ekya apu* → **eky'apu**, following the usual Luganda spelling before a vowel (as in *Akatabo k'Enkuŋŋaana*, *Omunaala gw'Omukuumi*).
* Both Luganda PDFs regenerated; `sw.js` cache version raised to `jw-tutorial-v6`.

## Changes in this version (17 Oct 2026, update 3) — terminology checked against Luganda JW.ORG / wol.jw.org
Applied to `lg.html`, `JWLibrary_Class.md`, `generate_pdfs.py` (and the two Luganda PDFs it makes), `README.md` and `manifest-lg.json`:
* **Device:** *ekyuma* replaced by the words Luganda JW publications use: *essimu*, *tabbuleeti*, *kompyuta* (e.g. *mwbr23* May; *w25* June p. 32).
* **Spelling:** *tabuleti* → **tabbuleeti** (*w23* November p. 31); *yintaneeti* → **Intaneeti** (2026 daily text; WOL site title).
* **App:** *pulogulaamu* → **apu** (*w25* June p. 32; *w25* July). In README, "Pulogulaamu ya Python" (a computer program) is unchanged.
* **Meetings:** *Olukuŋŋaana olw'Omu Wiiki* → **olukuŋŋaana olwa wakati mu wiiki** (*mwb17* November); weekend → **olukuŋŋaana olwa wiikendi** (spelling not confirmed). English *(Midweek)* / *(Weekend)* added in brackets.
* **Watchtower Study:** "ekitundu ky'*Omunaala gw'Omukuumi* ekisomebwa mu kibiina" (*w23* June p. 32). **Workbook:** *Akatabo k'Enkuŋŋaana* (official title *Obulamu bw'Ekikristaayo Akatabo k'Enkuŋŋaana*).
* **Bookmarks:** "akabonero akalaga w'okomye okusoma" / plural "obubonero obulaga w'okomye okusoma" (*mwb16* May p. 8). **History:** *Ebyafaayo* (= history as past events) replaced by the English button name **History**. **Tags:** **Ttaaga** (*w25* June p. 32).
* **"Official":** *-tuufu* (= correct) → **-tongole** (as in jw.org's "Omukutu Omutongole").
* **Answer:** *ekyokuddamu* → **eky'okuddamu** (apostrophe, as in JW publications); step 3.1 now says "ekigambo ekisooka mu ky'okuddamu".
* **Early:** *kare* → **nga bukyali** ("kare" does not occur in any Luganda publication on wol.jw.org, 1982–2026; "nga bukyali" is common, e.g. *w22* April).
* **Draft notice:** *eya luwalo* removed (in Luganda JW publications *luwalo* means doing something out of mere duty). Now: *Enkyusa esooka — tennakeberebwa.* A sentence was added explaining that app button names are also given in English.
* **Exercise label:** **Okwegezaamu Okukulu 1.1** etc. everywhere (the web page previously used *Okukulu 1.1* alone).
* **Video title confirmed:** *"Lwaki Kikulu Okuyiga Bayibuli?"* (*Nyumirwa Obulamu Emirembe Gyonna!* Lesson 1; *mwb16* May p. 8). Replaces the guess *"Lwaki Oyiga Bayibuli?"*.
* **Web page:** link card to **JW.ORG mu Luganda** (https://www.jw.org/lg/); footer link now points to jw.org/lg; English original of the legal notice added (as in `din.html`). Same additions in `JWLibrary_Class.md` and README.
* **`sw.js`:** cache version raised to `jw-tutorial-v5` so phones refresh their saved copies.
* Still to be confirmed by a Luganda speaker: see section 2 of `REVIEWER_CHECKLIST.md`.

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
**Verified on jw.org / wol.jw.org (Luganda):** Bayibuli, Matayo, *Omunaala gw'Omukuumi* (Watchtower), Abajulirwa ba Yakuwa, Enkuŋŋaana (meetings), Ebitabo n'Obutabo (publications), Noonya (search), Vidiyo, Ekizimbe ky'Obwakabaka (Kingdom Hall), Ekyawandiikibwa eky'olunaku (*mwb16*; the book is *Okwekenneenya Ebyawandiikibwa Buli Lunaku*), olukuŋŋaana olwa wakati mu wiiki, *Akatabo k'Enkuŋŋaana*, apu, okuwanula (download), essimu, tabbuleeti, kompyuta, Intaneeti, ttaaga (tag), nyiga / koona (tap), nga bukyali (early), *Lwaki Kikulu Okuyiga Bayibuli?* (video).

**From my own knowledge, not verified:** Olubereberye (Genesis), olukuŋŋaana olwa wiikendi (weekend meeting — spelling), okussaako langi (highlight), By'Oyagala (Settings — taken from wol.jw.org's own settings page, not the app), Kola Kkopi (Create Backup), data y'essimu (mobile data).

**My own translations of app labels:** I did not find Luganda JW Library help pages, so I don't know whether the app's buttons appear in Luganda or English for these users. Every app label is therefore written in Luganda with the English label in parentheses (e.g. **Okwesomesa** *(Personal Study)*, **By'Oyagala** *(Settings)*). Luganda JW publications themselves often quote the app's English labels ("Donations", "What's New", "Favorites"). The Apple App Store lists "Ganda" among JW Library's languages, so a Luganda interface may exist; the reviewer checklist asks someone to check this on a phone.

Phone/computer system menus (e.g. *Settings > Display*) are left in English.

## Links
All JW.ORG help links remain on the English pages (labelled *mu Lungereza*), since I did not find Luganda versions of the JW Library help pages. A link to the Luganda home page, https://www.jw.org/lg/, was added for Luganda publications, videos and songs.
