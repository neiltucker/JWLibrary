# JW Library Tutorial

An independent, practical training guide and class schedule designed to help individuals learn how to use the **JW Library** app for personal Bible reading, congregation meetings, and the ministry.

This tutorial is structured as a comfortable **60-minute class** with a dedicated **10-minute wrap-up buffer** and can easily flex or expand to **75–90 minutes** for groups desiring extra hands-on practice.

---

## 🌐 Interactive Web Guide

An interactive, accessible version of this tutorial—optimized for all screen sizes, with selectable device instructions and large-print formatting—is available at:

**[https://neiltucker.github.io/JWLibrary/](https://neiltucker.github.io/JWLibrary/)**

The web guide includes:
* **Device Switcher:** Choose between **Apple (iOS / iPadOS)**, **Android**, or **Windows PC / Mac** to view the exact button names and menu layouts for your device.
* **Large-Print Display & Text Size Controls:** Built for effortless readability with adjustable font sizing (`A−`, `A`, `A+`, `A++`) to reduce or enlarge text size.
* **Dark Mode & Light Mode:** One-tap theme toggle in the header for strain-free reading in low-light environments.
* **Printable Quick-Reference Guide:** Format and print clean physical cheat sheets for student practice.
* **Streamlined Core Walkthroughs:** Clear, numbered 1-2-3 steps paired with visual icon cues (📖, 📚, 📅, ☀️, 🔍, 🔖, 🖍️, 🎧, 💾).

---

## 📋 Course Overview

The curriculum is structured into three focused 15-minute lessons, framed by a 15-minute pre-class setup clinic, a 5-minute welcome, and a 10-minute wrap-up buffer:

0. **Pre-Class Clinic & Orientation (5–15 Mins)**
   * **Early Arrival Setup Clinic (15 mins prior):** Helpers greet attendees, connect devices to venue Wi-Fi, and verify the Bible and current Daily Text are downloaded before start time.
   * **30-Second Readiness Check:** Quick show of hands so helpers can assist anyone still needing a Bible download while class begins.
   * **Peace of Mind ("Panic Button"):** Teaching students how to immediately silence unexpected audio using the device's physical **Volume Down** button (on phones/tablets), keyboard **Mute key (🔇)** (on computers), or on-screen Pause (⏸️).
   * Locating the main navigation bar and adjusting screen auto-lock / timeout.

1. **Lesson 1: Finding Scriptures & Meetings (15 Mins)**
   * Exploring the main navigation bar and reading today's **Daily Text**.
   * Adjusting **Text Size (`A A`)** for comfortable, effortless reading.
   * Opening a specific **Bible book and chapter**.
   * Using the **Meetings tab** for one-tap access to the Midweek Meeting workbook and Weekend *Watchtower* study article.
   * *Demonstrated by Instructor:* Bookmarks, History, and Search.

2. **Lesson 2: Downloading and Using Media (15 Mins)**
   * Connecting to Wi-Fi before downloading to preserve mobile cellular data.
   * Downloading publications or media for offline use (no internet needed at meetings once downloaded).
   * Using the **Audio Player (🎧)** to listen to Bible chapters, Daily Text, or study articles read aloud.
   * Mastering **Emergency Quick-Silencing**: Stopping sound instantly using device volume controls (holding side Volume Down on mobile; pressing keyboard Mute key on PC) or on-screen pause.
   * *Demonstrated by Instructor:* Checking storage space and sorting by **Largest Size** to remove unneeded files.

3. **Lesson 3: Personal Study Tools (15 Mins)**
   * Highlighting study paragraphs and Bible verses in yellow.
   * Changing highlight colors (e.g., to blue or green) or removing a highlight.
   * **Crucial Data Protection:** Creating a safety backup file (`.jwlibrary`) in *Settings > Backup and Restore* so study notes and markings are never lost.
   * *Demonstrated by Instructor:* Adding study notes, organizing with Tags, and navigating the central Personal Study tab.

4. **Wrap-Up, Review & Questions (10 Mins)**
   * A dedicated 10-minute buffer for review, questions, or flex time if earlier exercises run over.
   * Facilitators can remain after class for anyone wanting one-on-one assistance.

---

## 📱 Supported Devices & Prerequisites

To ensure the latest features and security updates are available, verify that your device meets the minimum operating system requirements established for the app:

| Platform | Minimum Supported Version |
| :--- | :--- |
| **Android** | Android 8.0 or later |
| **Apple iOS / iPadOS** | iOS 15.0 or later |
| **Mac** | macOS with Apple Silicon (M1 chip or newer) |
| **Windows** | Windows 10 Version 2004 or later |

### Recommendations Before Attending:
* **Early Arrival (10–15 Mins Early):** Arrive a few minutes early so table assistants can help connect to venue Wi-Fi and verify your Bible and Daily Text are ready.
* **Fully Charged Battery:** Bring your device fully charged (or bring your charging cord).
* **Screen Timeout Adjustment:** Consider temporarily setting your device's screen auto-lock or screen timeout to 2 or 5 minutes so the screen stays on during demonstrations.
* **App Installed:** Have the *JW Library* app installed on your device from the official app store prior to class.
* **Storage Space:** Ensure your device has at least **2 to 4 GB** of free internal storage (or an installed SD card) so you can download publications, audio, and videos comfortably.
* **Wi-Fi Connection:** Connect to an available Wi-Fi network before downloading large media files to conserve mobile data.
* **Emergency Mute Tip:** Remember that pressing the **Volume Down button** (on phones/tablets) or keyboard **Mute key (🔇)** (on laptops) will quickly silence audio if it ever plays unexpectedly.

---

## 📁 Repository Contents

* **`index.html`**: Complete, responsive, accessible web tutorial with device-specific toggles, text resizing, facilitator timing guide, and printable quick guide.
* **`JWLibrary_Class.md`**: Markdown curriculum containing the instructor timing breakdown, facilitator advice, and core hands-on student exercises.
* **`JW Library Class Program.pdf`**: Printable 1-page class schedule and exercise reference sheet.
* **`JW Library Tutorial Curriculum.pdf`**: Comprehensive 4-page curriculum and teaching guide for instructors.
* **`generate_pdfs.py`**: Python script using ReportLab to deterministically regenerate the English PDFs (each language has its own in `translations/<code>/`).
* **`make_qr_and_cards.py`**: Python script that makes the QR codes (`QR_*.png`, `QR_*.svg`) and printable table cards (`Table_Cards_*.pdf`) for every language, and keeps the guide links in the README files pointing to the right web address.
* **`site_config.json`**: The web address used for the QR codes, table cards, and README links. Leave it blank to use this repository's GitHub Pages address automatically.
* **`requirements.txt`**: The free Python libraries the scripts need.
* **`fonts/`**: The free DejaVu Sans fonts (with their license) used by all the PDF scripts, so the PDFs look the same and print every letter correctly on any computer.
* **`translations/`**: Kiswahili, Luganda, Dinka, and Ga versions of the class outline, README, and PDF script, with translation notes and reviewer checklists.

---

## 🛠️ Regenerating the PDFs, QR Codes & Table Cards

The scripts use only free, open-source tools and the fonts in the `fonts/` folder, so they give the same result on Windows, Mac, and Linux with no other downloads.

1. Install [Python 3](https://www.python.org/downloads/), then install the libraries once from the repository folder:
   ```
   pip install -r requirements.txt
   ```
2. Run the script you need from the repository folder (on Windows, `py` can be used instead of `python`):

| Command | What it makes |
| :--- | :--- |
| `python generate_pdfs.py` | English class program and curriculum PDFs |
| `python translations/sw/generate_pdfs.py` | Kiswahili PDFs (likewise `lg`, `din`, and `gaa`) |
| `python make_qr_and_cards.py` | QR codes and table cards for every language, and updated README links |
| `python make_qr_and_cards.py sw` | QR codes and table cards for one language only |

3. After publishing changed pages or files, raise the version number at the top of `sw.js` (for example `v19` → `v20`) so devices that saved the guide for offline use pick up the new copies.

Tested with Python 3.13, reportlab 5.0.1, pypdf 6.17.0, qrcode 8.2, and pillow 12.3.0.

---

## 🗃️ Looking for the Classic / Legacy Tutorial Materials?

For instructors and facilitators who prefer the traditional comprehensive printed workbook format and detailed touch-device walkthroughs, the complete legacy courseware is maintained in a dedicated archive:

👉 **[JWLibrary-Legacy Repository](https://github.com/neiltucker/JWLibrary-Legacy)**

The legacy repository includes:
* **Comprehensive Student Workbook:** Available in ready-to-print [PDF](https://github.com/neiltucker/JWLibrary-Legacy/blob/main/JW%20Library%20Tutorial.pdf) and fully customizable [Microsoft Word (`.docx`)](https://github.com/neiltucker/JWLibrary-Legacy/blob/main/JW%20Library%20Tutorial.docx) format.
* **Instructor Curriculum & Schedule Handouts:** Complete lesson guides and class programs in both PDF and Word formats.
* **Historical Archive (`JWLibrary-Legacy.zip`):** Complete archive of early revisions (`RevA` through `RevD`), intermediate drafts, and historical snapshots spanning 2015–2025.


---

## 🤝 Guidelines for Adapting, Customizing, or Hosting Your Own Classes

Facilitators, instructors, and communities are warmly welcomed to use, translate, adapt, or build upon this material for their local training needs. If you customize these files or publish your own version, please observe the following standards:

1. **Use as a Template (Recommended):**  
   We encourage clicking the **"Use this template"** button at the top of this repository rather than creating a standard fork. This creates a clean, independent repository under your own account without linking your local changes to this upstream repository's commit history or pull request queue.  
   Repository settings are not copied from a template, so turn on GitHub Pages in your new repository: go to **Settings → Pages**, under **Build and deployment** choose **Deploy from a branch**, select the **`main`** branch and the **`/ (root)`** folder, and click **Save**. After a minute or two your guide is published at `https://<your-user-name>.github.io/<your-repository-name>/`.

2. **Update URLs, Domains & QR Table Cards:**  
   If you publish your own web guide or print QR table cards, point all links and QR codes to your own deployment rather than `neiltucker.github.io`, so learners at your venue connect to your intended version. The web pages themselves use relative links and need no changes. On a copy of your repository on your computer, run `python make_qr_and_cards.py` (see *Regenerating the PDFs, QR Codes & Table Cards* above): it works out your GitHub Pages address from your repository, remakes every QR code and table card, and updates the guide links in the README files. If you publish somewhere else (for example a custom domain), first enter that address as `base_url` in `site_config.json`.

3. **No Implied Endorsement or Affiliation:**  
   You may reference this repository as the original source of the template, but you must not state, imply, or suggest that your modified curriculum, website, or class materials are authorized, reviewed, sponsored, or endorsed by the original author (Neil Tucker).

4. **Retain the Legal & Non-Affiliation Disclaimer:**  
   All copies, translations, and derivative works must retain the full non-affiliation notice regarding *Watch Tower Bible and Tract Society of Pennsylvania* and *Jehovah's Witnesses*. *JW Library* is a registered trademark, and all training materials must remain strictly non-commercial and educational.

5. **Focus on Digital Literacy & Official Guidance:**  
   This project exists solely to help individuals navigate the official *JW Library* app and *JW.ORG*. Any adapted classes should remain neutral, positive, and strictly aligned with officially published guidance from the app's publisher.

6. **Responsibility for Derivative Content:**  
   Anyone who forks, modifies, or redistributes these materials assumes sole responsibility for their changes, translations, and classroom delivery. The original author accepts no responsibility or liability for derivative versions created by third parties.

---

## 🔗 Official Documentation

Official, step-by-step instructions and video tutorials from the app's publisher are available at:

* **Official Online Help Index:** [https://www.jw.org/en/online-help/jw-library/](https://www.jw.org/en/online-help/jw-library/)
* **General App Features:** [https://www.jw.org/en/online-help/jw-library/features/](https://www.jw.org/en/online-help/jw-library/features/)
* **Help for Apple (iOS / iPadOS):** [https://www.jw.org/en/online-help/jw-library/apple/](https://www.jw.org/en/online-help/jw-library/apple/)
* **Help for Android:** [https://www.jw.org/en/online-help/jw-library/android/](https://www.jw.org/en/online-help/jw-library/android/)
* **Help for Windows:** [https://www.jw.org/en/online-help/jw-library/windows/](https://www.jw.org/en/online-help/jw-library/windows/)
* **Frequently Asked Questions (Android):** [https://www.jw.org/en/online-help/jw-library/android/faqs/](https://www.jw.org/en/online-help/jw-library/android/faqs/)

---

## ⚖️ Legal & Non-Affiliation Disclaimer

*JW Library* is a registered trademark of Watch Tower Bible and Tract Society of Pennsylvania. 

This repository and tutorial are an independent, non-commercial educational training project created solely for informational and personal learning purposes. This project is not affiliated with, sponsored, maintained, authorized, or endorsed by Watch Tower Bible and Tract Society of Pennsylvania or Jehovah's Witnesses. Any modified versions, downstream forks, or derivative classes are the sole responsibility of their respective authors and do not represent the original template maintainer. All official publications, media, and authoritative guidance must be obtained directly from [JW.ORG](https://www.jw.org).
