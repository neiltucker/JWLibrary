# Translation Notes — Kiswahili

Source: https://github.com/neiltucker/JWLibrary (files as of 16 Oct 2026). Translated by Claude (AI). **Please have a fluent Swahili speaker review before distributing.**

## Changes in this version (30 Oct 2026, update 7) — shared fonts, QR script and template setup
These changes affect every language. The translated wording of the guide is unchanged.
* **Fonts:** `generate_pdfs.py` now uses DejaVu Sans from the shared `fonts/` folder at the top of the repository (with its license file), so the PDFs look the same and print every letter correctly on any computer, with no other downloads. Installed fonts are still used as a backup. Both Kiswahili PDFs were regenerated with the same words and page counts (1 and 4 pages); only the font changed (was Helvetica, which is not embedded in the PDF).
* **Page footer:** the legal notice at the bottom of each curriculum page now shrinks slightly when needed, so it always fits across the page.
* **QR code and table cards:** now made for every language by the shared `make_qr_and_cards.py` at the top of the repository (`python make_qr_and_cards.py sw` for this language only). It reads the web address from `site_config.json`, or works it out from the repository's GitHub address. The card wording and layout are unchanged, and the QR code still opens https://neiltucker.github.io/JWLibrary/sw.html (checked by decoding it).
* **README:** the online guide link now opens the Kiswahili page (`sw.html`), with the English page on a second line, labelled *(toleo la Kiingereza)* as before. `tinyurl.txt` was removed from the repository and from the file list.
* `sw.js` cache version raised to `v19`. Each copy of the guide now keeps its own offline files, so copies published under the same GitHub account no longer remove each other's saved pages.

## Changes in this version (30 Oct 2026, update 6) — simpler words from the reviewer
The reviewer (a local Kiswahili speaker) listed the technical words she found hard for ordinary readers and suggested simpler ones. Her suggestions were checked against the Swahili JW Library help pages on jw.org, which use the same wording for most of them. Applied to `sw.html`, `JWLibrary_Class.md`, `README.md` and `generate_pdfs.py` (both Swahili PDFs regenerated; still 1 and 4 pages).
* **Main navigation:** *mstari mkuu wa urambazaji* → **menyu kuu** (e.g. "menyu kuu iko chini ya skrini"). *Vichupo vikuu vya urambazaji* in the PDFs → **sehemu kuu za programu** (jw.org: "sehemu kuu za programu").
* **Top bar:** *upau wa juu* → **sehemu ya juu ya skrini** (jw.org: "Katika sehemu ya juu ya kifaa chako, bofya Andiko la Siku").
* **Tabs:** *Bofya kichupo cha Mikutano* → **Bofya sehemu iliyoandikwa Mikutano** (jw.org: "Sehemu iliyoandikwa Biblia…", "Ukibofya sehemu iliyoandikwa Machapisho…"). Headings and short references now say **Sehemu ya Mikutano** and **sehemu ya Funzo la Kibinafsi**.
* **Bookmarks:** the reviewer suggested *Vilivyohifadhiwa*. **Vialamisho** is kept as the button name, because it is the name jw.org's help pages use ("Tumia Vialamisho, au, Alama za Kukumbuka Ukurasa") and learners need to match the word on their screen. A plain explanation was added the way jw.org does it: "(yaani, kuhifadhi ukurasa ili uupate tena kwa urahisi)" in the lessons, and "(kurasa ulizohifadhi)" in short lists. *Vilivyohifadhiwa* was not used as the label because *hifadhi* already describes downloads and backups in this guide. See item 10 in `REVIEWER_CHECKLIST.md`.
* **Icons:** *aikoni* → **alama** everywhere (Wi-Fi, cloud, `A A`, sun, speaker, headphones, History, Search, the new home-screen icon). "aikoni ya Simamisha" → **kitufe cha Simamisha** (it is a button). Fixed a leftover: update 3 changed *aikoni ya wingu* to *alama ya wingu*, but one sentence in `sw.html` (Msingi 2.2, step 3) still said *Aikoni ya wingu*.
* **Media:** *vyombo vya habari* (which means news media such as radio, TV and newspapers) → **Maudhui** in the Lesson 2 title ("Somo la 2: Kupakua na Kutumia Maudhui"). In running text it now names the items: "video au rekodi za sauti", "faili za video na sauti", "machapisho, video, na rekodi za sauti".
* **Legal sentence (README):** "Machapisho yote rasmi, vyombo vya habari, na mwongozo wenye mamlaka…" → "Machapisho yote rasmi, video na rekodi za sauti, na mwongozo wenye mamlaka…". Please confirm (item 10).
* **Windows taskbar:** *upau wa kazi* is kept, with *(taskbar)* added in brackets; the Mac menu bar line now reads *upau wa kazi/upau wa menyu (taskbar/menu bar)*.
* Output path in `generate_pdfs.py` now resolves relative to the script location instead of a hardcoded path.
* `sw.js` cache version raised from `jw-tutorial-v17` to `jw-tutorial-v18`.

## Changes in this version (28 Oct 2026, update 5) — reviewer feedback
* **One-hour wording:** the reviewer pointed out that *"Mafunzo ya saa moja"* could be read as a training **at** *saa moja* (7 o'clock in Swahili time) rather than a training **lasting** one hour. Changed to **"Mafunzo ya dakika 60"** in the opening line of `sw.html` and in the first paragraph of `JWLibrary_Class.md`. This matches the wording already used in the README, both PDFs, and the page's *Mpango Mkuu wa Dakika 60* schedule, so the PDFs did not need to be regenerated.
* The reviewer has read the rest of the document and reported that it seems okay. She mentioned that it contains many IT words she is not familiar with; she has been asked which specific words, if any, should be simpler (see item 9 in `REVIEWER_CHECKLIST.md`).
* `sw.js` cache version raised to `jw-tutorial-v17` so phones fetch the new `sw.html`.

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
