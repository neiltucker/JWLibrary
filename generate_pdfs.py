import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

# Numbered canvas for "Page X of Y" on Curriculum
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748b'))
        # Top right header
        self.drawRightString(letter[0] - 45, letter[1] - 30, f"Page {self._pageNumber} of {page_count}")
        # Bottom disclaimer on each page
        disclaimer = "JW Library is a registered trademark of Watch Tower Bible and Tract Society of Pennsylvania. Independent, non-commercial training aid."
        self.drawCentredString(letter[0] / 2.0, 20, disclaimer)
        self.restoreState()


def build_class_program(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=26,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#1e3a8a')
    )

    note_style = ParagraphStyle(
        'DocNote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7,
        leading=9,
        alignment=1,
        textColor=colors.HexColor('#475569')
    )

    section_hdr = ParagraphStyle(
        'SectionHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=1
    )

    timing_style = ParagraphStyle(
        'TimingLine',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#1e293b')
    )

    ex_hdr = ParagraphStyle(
        'ExHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=1,
        spaceAfter=1
    )

    ex_style = ParagraphStyle(
        'ExLine',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=8.8,
        textColor=colors.HexColor('#1e293b')
    )

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6,
        leading=7.5,
        alignment=1,
        textColor=colors.HexColor('#64748b')
    )

    story = []

    story.append(Paragraph('JW LIBRARY CLASS PROGRAM', title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph('<b>NOTE:</b> Official instructions on using JW Library can be found at JW.ORG (https://www.jw.org/en/online-help/jw-library/)', note_style))
    story.append(Paragraph('This is a one-hour class. Additional time may be added for video viewing, interactive practice, and questions.', note_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=3))

    # Schedule
    story.append(Paragraph('<b>Introduction:</b>', section_hdr))
    story.append(Paragraph('0:00 &nbsp; Introduction to JW Library (Orientation to navigation and screen layout)', timing_style))
    story.append(Paragraph('0:05 &nbsp; End of Introduction', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Lesson 1: (Navigation & Meetings)</b>', section_hdr))
    story.append(Paragraph('0:00 &nbsp; Discuss main navigation tabs (Bible, Publications, Meetings, Personal Study)', timing_style))
    story.append(Paragraph('0:02 &nbsp; Perform Exercise 1.1 (Daily Text)', timing_style))
    story.append(Paragraph('0:04 &nbsp; Discuss Meetings tab (Midweek Meeting & Weekend Watchtower study)', timing_style))
    story.append(Paragraph('0:07 &nbsp; Perform Exercise 1.2 (Meetings tab)', timing_style))
    story.append(Paragraph('0:09 &nbsp; Discuss Bookmarks and History', timing_style))
    story.append(Paragraph('0:13 &nbsp; Perform Exercises 1.3 & 1.4 (Bookmarks & History)', timing_style))
    story.append(Paragraph('0:15 &nbsp; Discuss Search feature (finding verses, words, and topics)', timing_style))
    story.append(Paragraph('0:18 &nbsp; Perform Exercise 1.5 (Search)', timing_style))
    story.append(Paragraph('0:20 &nbsp; Review of Lesson 1', timing_style))
    story.append(Paragraph('0:22 &nbsp; End of Lesson 1', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Lesson 2: (Downloading Files & Storage Management)</b>', section_hdr))
    story.append(Paragraph('0:00 &nbsp; Wi-Fi connection recommendation before downloading media', timing_style))
    story.append(Paragraph('0:02 &nbsp; Discuss downloading Bibles and Study Editions', timing_style))
    story.append(Paragraph('0:06 &nbsp; Perform Exercise 2.1 (Download Bible translation)', timing_style))
    story.append(Paragraph('0:09 &nbsp; Discuss downloading Publications and Videos (language options)', timing_style))
    story.append(Paragraph('0:13 &nbsp; Perform Exercises 2.2 & 2.3 (Download video in English and another language)', timing_style))
    story.append(Paragraph('0:16 &nbsp; Managing storage: sorting by Largest Size and removing unneeded files', timing_style))
    story.append(Paragraph('0:19 &nbsp; Perform Exercise 2.4 (Find largest downloaded file)', timing_style))
    story.append(Paragraph('0:21 &nbsp; Review of Lesson 2', timing_style))
    story.append(Paragraph('0:23 &nbsp; End of Lesson 2', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Lesson 3: (Highlighting, Personal Study & Data Safety)</b>', section_hdr))
    story.append(Paragraph('0:00 &nbsp; Discuss Highlighting feature (selecting text, colors, removing highlights)', timing_style))
    story.append(Paragraph('0:04 &nbsp; Perform Exercises 3.1 & 3.2 (Highlight text, then change color or delete)', timing_style))
    story.append(Paragraph('0:07 &nbsp; Creating personal notes and categorizing with Tags', timing_style))
    story.append(Paragraph('0:10 &nbsp; Perform Exercises 3.3 & 3.4 (Add note, tag, and view in Personal Study tab)', timing_style))
    story.append(Paragraph('0:12 &nbsp; Protecting your study data: creating a backup file (.jwlibrary)', timing_style))
    story.append(Paragraph('0:14 &nbsp; Perform Exercise 3.5 (Create a backup file in Settings)', timing_style))
    story.append(Paragraph('0:15 &nbsp; Review of Lesson 3 & Final Q&A', timing_style))
    story.append(Spacer(1, 2))

    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=2))
    story.append(Paragraph('<b>EXERCISES</b>', ex_hdr))

    story.append(Paragraph('<b>1.1</b> Navigate to today\'s Daily Text and read the day\'s scripture and comments.', ex_style))
    story.append(Paragraph('<b>1.2</b> Open the Meetings tab and locate this week\'s Watchtower Study article.', ex_style))
    story.append(Paragraph('<b>1.3</b> Create a bookmark in a Bible chapter you frequently use.', ex_style))
    story.append(Paragraph('<b>1.4</b> Use the History feature to return to a scripture you previously read.', ex_style))
    story.append(Paragraph('<b>1.5</b> Search for a scripture containing the phrase <i>"draw close to God"</i> or choose your own expression.', ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph('<b>2.1</b> Tap Bible &gt; Languages and download an additional translation (e.g., King James Version).', ex_style))
    story.append(Paragraph('<b>2.2</b> Download an introductory video (such as <i>"Why Study the Bible?"</i>) in 720p or 480p resolution.', ex_style))
    story.append(Paragraph('<b>2.3</b> Download the same video in another language (e.g., Spanish).', ex_style))
    story.append(Paragraph('<b>2.4</b> In Publications &gt; Downloaded, sort by <b>Largest Size</b> to check storage use and locate large files.', ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph('<b>3.1</b> Open the next Watchtower study article and highlight the answer for paragraph 1 in yellow.', ex_style))
    story.append(Paragraph('<b>3.2</b> Change the color used to highlight your answer from the previous step, or delete it.', ex_style))
    story.append(Paragraph('<b>3.3</b> Add a personal study note to a highlighted answer and attach a tag.', ex_style))
    story.append(Paragraph('<b>3.4</b> Open the Personal Study tab to review your collected notes and highlights.', ex_style))
    story.append(Paragraph('<b>3.5</b> Open Settings &gt; Backup and Restore and select <b>Create Backup</b> to protect your study notes.', ex_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph('<i>Disclaimer: JW Library is a registered trademark of Watch Tower Bible and Tract Society of Pennsylvania. This class program is an independent, non-commercial training aid and is not affiliated with or endorsed by Watch Tower or Jehovah\'s Witnesses.</i>', disclaimer_style))

    doc.build(story)


def build_curriculum(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=40,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    doc_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1e3a8a')
    )

    note_style = ParagraphStyle(
        'DocNote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=8,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b')
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        leftIndent=15,
        textColor=colors.HexColor('#1e293b')
    )

    story = []

    # ==================== PAGE 1 ====================
    story.append(Paragraph('JW Library Tutorial Curriculum', doc_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>NOTE:</b> Official instructions on using JW Library can be found at JW.ORG (https://www.jw.org/en/online-help/jw-library/)', note_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('About the JW Library Tutorial', h1_style))
    story.append(Paragraph(
        'This curriculum is intended for anyone instructing or guiding students using the accompanying '
        '<i>JW Library Tutorial</i>. The course consists of three practical, hands-on lessons covering '
        '<b>Navigation &amp; Meetings</b>, <b>Downloading Files &amp; Media</b>, and <b>Highlighting &amp; Personal Study</b>. '
        'Before the class begins, students should be provided with a copy of the tutorial materials and be '
        'reminded to have the app pre-installed on their device.',
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'The <i>JW Library Class Program</i> serves as a template when planning a session schedule. Five to ten minutes '
        'are designated at the beginning to orient students to their device layout. The recommended time for each '
        'lesson is 15 to 30 minutes, reserving 5 to 10 minutes for individual practice exercises and 2 to 5 minutes '
        'for review. The full course can comfortably be covered in 60 to 90 minutes. For further reinforcement after class, '
        'refer students to the official tutorials on JW.ORG.',
        body_style
    ))

    story.append(Paragraph('Audience', h1_style))
    story.append(Paragraph(
        'This tutorial is crafted for individuals with basic smartphone, tablet, or desktop computer familiarity. '
        'Students should be comfortable using a touchscreen or mouse. Prior experience with the JW Library app '
        'is helpful but not required.',
        body_style
    ))

    story.append(Paragraph('Learning Outcomes', h1_style))
    story.append(Paragraph('Upon completing this tutorial, students will be able to:', body_style))
    story.append(Paragraph('&bull; Navigate between Bibles, Publications, Meetings, and Personal Study.', bullet_style))
    story.append(Paragraph('&bull; Access the Daily Text and locate weekly meeting study articles with one tap.', bullet_style))
    story.append(Paragraph('&bull; Use Bookmarks and History to quickly find and return to scriptures.', bullet_style))
    story.append(Paragraph('&bull; Search for words, exact phrases, and topics across publications.', bullet_style))
    story.append(Paragraph('&bull; Download Bible translations, videos, and media in primary and secondary languages.', bullet_style))
    story.append(Paragraph('&bull; Manage device storage space by sorting and deleting downloaded files.', bullet_style))
    story.append(Paragraph('&bull; Highlight text, create personal study notes, and organize content with Tags.', bullet_style))
    story.append(Paragraph('&bull; Create a safety backup (.jwlibrary file) to safeguard study records.', bullet_style))

    story.append(Paragraph('Prerequisites', h1_style))
    story.append(Paragraph('Before attending this course, students should have:', body_style))
    story.append(Paragraph('&bull; A supported device running <b>Android 8.0+</b>, <b>iOS 15.0+</b>, <b>macOS with M1+ chip</b>, or <b>Windows 10 v2004+</b>.', bullet_style))
    story.append(Paragraph('&bull; At least <b>2 to 4 GB</b> of available storage (or an installed SD card) for media files.', bullet_style))
    story.append(Paragraph('&bull; Access to a Wi-Fi connection prior to downloading video or audio media.', bullet_style))

    # ==================== PAGE 2 ====================
    story.append(PageBreak())

    story.append(Paragraph('JW Library Tutorial Curriculum', doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Lesson 1: Navigation &amp; Meetings (15 - 30 Minutes)', h1_style))
    story.append(Paragraph(
        'This lesson introduces students to moving smoothly between the primary sections of the JW Library app. '
        'Instructors should explain the placement of the navigation bar based on the devices present (bottom bar on iOS '
        'and modern Android; top menu on Windows). Demonstrate how the <b>Meetings tab</b> simplifies finding meeting '
        'materials each week, and how Bookmarks, History, and Search enable rapid scripture retrieval. '
        'Have students perform the practice exercises immediately following each topic demonstration.',
        body_style
    ))

    story.append(Paragraph('Topics (10 - 15 minutes)', h2_style))
    story.append(Paragraph('&bull; Main Navigation Tabs (Bible, Publications, Meetings, Personal Study)', bullet_style))
    story.append(Paragraph('&bull; Daily Text (locating and reading today\'s scripture and comment)', bullet_style))
    story.append(Paragraph('&bull; Meetings Tab (Midweek Life &amp; Ministry Meeting and Weekend Watchtower Study)', bullet_style))
    story.append(Paragraph('&bull; Bookmarks (setting chapter or verse-level bookmarks)', bullet_style))
    story.append(Paragraph('&bull; History (reviewing recent reading list)', bullet_style))
    story.append(Paragraph('&bull; Search (searching for words, exact phrases, or Insight topics)', bullet_style))

    story.append(Paragraph('Exercise 1: Navigation &amp; Meetings (5 - 10 minutes)', h2_style))
    story.append(Paragraph('&bull; <b>1.1</b> Navigate to today\'s Daily Text.', bullet_style))
    story.append(Paragraph('&bull; <b>1.2</b> Open the Meetings tab and tap this week\'s Watchtower Study article.', bullet_style))
    story.append(Paragraph('&bull; <b>1.3</b> Set a bookmark in a Bible chapter used in ministry.', bullet_style))
    story.append(Paragraph('&bull; <b>1.4</b> Use the History feature to return to a previously viewed passage.', bullet_style))
    story.append(Paragraph('&bull; <b>1.5</b> Search for a scripture with the phrase <i>"draw close to God"</i>.', bullet_style))

    story.append(Paragraph('Review (2 - 5 minutes)', h2_style))
    story.append(Paragraph(
        'Ask students how the Meetings tab helps them prepare during the week. Solicit questions regarding '
        'how to clear search history or replace an existing bookmark.',
        body_style
    ))

    story.append(Paragraph('After completing this lesson, students will be able to:', h2_style))
    story.append(Paragraph('&bull; Switch comfortably between all main app sections.', bullet_style))
    story.append(Paragraph('&bull; Access weekly meeting publications in one step without manual searching.', bullet_style))
    story.append(Paragraph('&bull; Save their reading location using bookmarks and revisit past scriptures using history.', bullet_style))
    story.append(Paragraph('&bull; Perform word and phrase searches in the Bible and publications.', bullet_style))

    # ==================== PAGE 3 ====================
    story.append(PageBreak())

    story.append(Paragraph('JW Library Tutorial Curriculum', doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Lesson 2: Downloading Files &amp; Storage Management (15 - 30 Minutes)', h1_style))
    story.append(Paragraph(
        'This lesson explains how to download Bibles, publications, and multimedia for offline reading and viewing. '
        'Emphasize downloading over Wi-Fi to preserve mobile cellular data. Explain how to choose lower video resolutions '
        '(such as 480p or 720p) to preserve storage on devices with limited memory. Walk students through viewing their '
        'downloaded library and sorting by <b>Largest Size</b> to manage storage responsibly.',
        body_style
    ))

    story.append(Paragraph('Topics (10 - 15 minutes)', h2_style))
    story.append(Paragraph('&bull; Connecting to Wi-Fi before initiating large downloads', bullet_style))
    story.append(Paragraph('&bull; Downloading Bible translations and Study Editions', bullet_style))
    story.append(Paragraph('&bull; Downloading Video and Audio media (choosing resolution: 480p / 720p)', bullet_style))
    story.append(Paragraph('&bull; Downloading resources in multiple languages', bullet_style))
    story.append(Paragraph('&bull; Managing storage space (Publications &gt; Downloaded &gt; sort by Largest Size)', bullet_style))
    story.append(Paragraph('&bull; Deleting outdated or rarely used media files', bullet_style))

    story.append(Paragraph('Exercise 2: Downloading &amp; Storage (5 - 10 minutes)', h2_style))
    story.append(Paragraph('&bull; <b>2.1</b> Download an additional Bible translation (e.g., King James Version).', bullet_style))
    story.append(Paragraph('&bull; <b>2.2</b> Download an introductory video (such as <i>"Why Study the Bible?"</i>).', bullet_style))
    story.append(Paragraph('&bull; <b>2.3</b> Download the same video in another language (e.g., Spanish).', bullet_style))
    story.append(Paragraph('&bull; <b>2.4</b> Sort downloaded publications by <b>Largest Size</b> and inspect storage use.', bullet_style))

    story.append(Paragraph('Review (2 - 5 minutes)', h2_style))
    story.append(Paragraph(
        'Discuss why sorting by Largest Size is helpful when storage is nearly full. Confirm that students '
        'know how to delete a large video once they are finished with it.',
        body_style
    ))

    story.append(Paragraph('After completing this lesson, students will be able to:', h2_style))
    story.append(Paragraph('&bull; Download Bibles and publications for offline use without using cellular data.', bullet_style))
    story.append(Paragraph('&bull; Choose sensible video resolutions to save device storage.', bullet_style))
    story.append(Paragraph('&bull; Locate, inspect, and delete large downloaded media when storage is tight.', bullet_style))

    # ==================== PAGE 4 ====================
    story.append(PageBreak())

    story.append(Paragraph('JW Library Tutorial Curriculum', doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Lesson 3: Highlighting, Personal Study &amp; Data Safety (15 - 30 Minutes)', h1_style))
    story.append(Paragraph(
        'This lesson covers preparing study articles, marking key thoughts, and safeguarding personal notes. '
        'Demonstrate how to select and highlight text in different colors, modify or remove highlights, and attach '
        'notes with <b>Tags</b>. Introduce the central <b>Personal Study</b> tab where all highlights and notes '
        'are assembled. Finally, emphasize that personal study data is stored locally on the device, and demonstrate '
        'how to create a safety backup file (<code>.jwlibrary</code>) in Settings so notes are never lost.',
        body_style
    ))

    story.append(Paragraph('Topics (10 - 15 minutes)', h2_style))
    story.append(Paragraph('&bull; Selecting words and sentences to highlight', bullet_style))
    story.append(Paragraph('&bull; Using and switching highlight colors (Yellow, Blue, Green, etc.)', bullet_style))
    story.append(Paragraph('&bull; Adding personal study notes to highlighted text', bullet_style))
    story.append(Paragraph('&bull; Categorizing notes with Tags for talks and ministry', bullet_style))
    story.append(Paragraph('&bull; Navigating the Personal Study hub (Notes, Bookmarks, Highlights)', bullet_style))
    story.append(Paragraph('&bull; <b>Data Safety:</b> Creating a backup file (Settings &gt; Backup and Restore)', bullet_style))

    story.append(Paragraph('Exercise 3: Highlighting, Study &amp; Backup (5 - 10 minutes)', h2_style))
    story.append(Paragraph('&bull; <b>3.1</b> Open the next Watchtower study article and highlight an answer in paragraph 1.', bullet_style))
    story.append(Paragraph('&bull; <b>3.2</b> Change the highlight color, or tap delete to practice removing it.', bullet_style))
    story.append(Paragraph('&bull; <b>3.3</b> Add a personal study note to a highlighted answer and attach a tag.', bullet_style))
    story.append(Paragraph('&bull; <b>3.4</b> Open the Personal Study tab to view your collected notes.', bullet_style))
    story.append(Paragraph('&bull; <b>3.5</b> Open Settings &gt; Backup and Restore and tap <b>Create Backup</b>.', bullet_style))

    story.append(Paragraph('Review (2 - 5 minutes)', h2_style))
    story.append(Paragraph(
        'Emphasize the importance of creating a regular backup file so years of personal study markings '
        'are safe if a tablet or phone is replaced or updated.',
        body_style
    ))

    story.append(Paragraph('After completing this lesson, students will be able to:', h2_style))
    story.append(Paragraph('&bull; Highlight answers and key scriptures in various colors.', bullet_style))
    story.append(Paragraph('&bull; Create, edit, and tag personal study notes for quick retrieval.', bullet_style))
    story.append(Paragraph('&bull; Access all personal study items in the Personal Study tab.', bullet_style))
    story.append(Paragraph('&bull; Safely back up their study notes and highlights to a .jwlibrary file.', bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph('Note: Continued Independent Learning', h2_style))
    story.append(Paragraph(
        'Students wishing to explore advanced features (such as Playlists and the Study Pane) should be directed '
        'to the official tutorials on JW.ORG. Encourage students to master one simple skill and become comfortable '
        'using it regularly before attempting new ones.',
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)


if __name__ == '__main__':
    program_pdf = 'D:/cs/JWLibrary/JW Library Class Program.pdf'
    curriculum_pdf = 'D:/cs/JWLibrary/JW Library Tutorial Curriculum.pdf'

    build_class_program(program_pdf)
    build_curriculum(curriculum_pdf)

    # Verification
    r1 = pypdf.PdfReader(program_pdf)
    r2 = pypdf.PdfReader(curriculum_pdf)
    print(f'SUCCESS: Program PDF generated with {len(r1.pages)} page(s).')
    print(f'SUCCESS: Curriculum PDF generated with {len(r2.pages)} page(s).')
