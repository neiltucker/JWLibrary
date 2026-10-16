import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

# Unicode Font Registration for multi-language support (English, Swahili, Luganda, Dinka)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_REG = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'
FONT_ITALIC = 'Helvetica-Oblique'

for base_dir, r_file, b_file, i_file in [
    ('C:/Windows/Fonts', 'segoeui.ttf', 'segoeuib.ttf', 'segoeuii.ttf'),
    ('C:/Windows/Fonts', 'arial.ttf', 'arialbd.ttf', 'ariali.ttf'),
]:
    r_path = os.path.join(base_dir, r_file)
    b_path = os.path.join(base_dir, b_file)
    i_path = os.path.join(base_dir, i_file)
    if os.path.exists(r_path) and os.path.exists(b_path):
        try:
            pdfmetrics.registerFont(TTFont('AppRegular', r_path))
            pdfmetrics.registerFont(TTFont('AppBold', b_path))
            pdfmetrics.registerFont(TTFont('AppItalic', i_path if os.path.exists(i_path) else r_path))
            from reportlab.pdfbase.pdfmetrics import registerFontFamily
            registerFontFamily('AppRegular', normal='AppRegular', bold='AppBold', italic='AppItalic', boldItalic='AppBold')
            FONT_REG = 'AppRegular'
            FONT_BOLD = 'AppBold'
            FONT_ITALIC = 'AppItalic'
            break
        except Exception:
            pass

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
        self.setFont(FONT_REG, 8)
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
        topMargin=24,
        bottomMargin=18
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=13,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#1e3a8a')
    )

    note_style = ParagraphStyle(
        'DocNote',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=7,
        leading=9,
        alignment=1,
        textColor=colors.HexColor('#475569')
    )

    section_hdr = ParagraphStyle(
        'SectionHdr',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=1
    )

    timing_style = ParagraphStyle(
        'TimingLine',
        parent=styles['Normal'],
        fontName=FONT_REG,
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#1e293b')
    )

    ex_hdr = ParagraphStyle(
        'ExHdr',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=1,
        spaceAfter=1
    )

    ex_style = ParagraphStyle(
        'ExLine',
        parent=styles['Normal'],
        fontName=FONT_REG,
        fontSize=7,
        leading=8.8,
        textColor=colors.HexColor('#1e293b')
    )

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName=FONT_REG,
        fontSize=6,
        leading=7.5,
        alignment=1,
        textColor=colors.HexColor('#64748b')
    )

    story = []

    story.append(Paragraph('JW LIBRARY CLASS PROGRAM', title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph('<b>NOTE:</b> Official instructions on using JW Library can be found at JW.ORG (https://www.jw.org/en/online-help/jw-library/)', note_style))
    story.append(Paragraph('A 60-minute class with three 15-minute lessons and a dedicated 10-minute wrap-up buffer. (Can expand to 75-90 mins).', note_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=3))

    # Schedule
    story.append(Paragraph('<b>Welcome &amp; Screen Orientation: (0:00 - 0:05)</b>', section_hdr))
    story.append(Paragraph('0:00 &nbsp; Welcome; Bible/Daily Text readiness check (helpers assist with downloads).', timing_style))
    story.append(Paragraph('0:02 &nbsp; Emergency silence tip: hold Volume Down (mobile) or press Mute key (PC); locate main bar.', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Lesson 1: Finding Scriptures &amp; Meetings (0:05 - 0:20)</b>', section_hdr))
    story.append(Paragraph('0:05 &nbsp; Discuss main navigation tabs (Bible, Publications, Meetings, Personal Study).', timing_style))
    story.append(Paragraph('0:07 &nbsp; Access Daily Text and tap <b>A A</b> icon to enlarge print for comfortable reading.', timing_style))
    story.append(Paragraph('0:10 &nbsp; Perform Core Exercise 1.1 (Daily Text &amp; Text Size).', timing_style))
    story.append(Paragraph('0:12 &nbsp; Open a Bible book and chapter; perform Core Exercise 1.2.', timing_style))
    story.append(Paragraph('0:15 &nbsp; Discuss Meetings tab (Midweek workbook &amp; Weekend Watchtower study).', timing_style))
    story.append(Paragraph('0:18 &nbsp; Perform Core Exercise 1.3 (Meetings tab). (Instructor demonstrates Bookmarks &amp; Search).', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Lesson 2: Downloading and Using Media (0:20 - 0:35)</b>', section_hdr))
    story.append(Paragraph('0:20 &nbsp; Understanding offline use: items downloaded on Wi-Fi stay on device with no cellular data needed.', timing_style))
    story.append(Paragraph('0:22 &nbsp; Perform Core Exercise 2.1 (Wi-Fi check &amp; mobile data safety).', timing_style))
    story.append(Paragraph('0:24 &nbsp; Download an item for offline reading/viewing; perform Core Exercise 2.2.', timing_style))
    story.append(Paragraph('0:28 &nbsp; Audio Player (headphones icon); quick-silencing with Volume Down (mobile) or Mute key (PC).', timing_style))
    story.append(Paragraph('0:31 &nbsp; Perform Core Exercise 2.3 (Listen with Audio). (Instructor demonstrates storage check).', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Lesson 3: Personal Study Tools (0:35 - 0:50)</b>', section_hdr))
    story.append(Paragraph('0:35 &nbsp; Selecting words and sentences to highlight answers in study articles.', timing_style))
    story.append(Paragraph('0:37 &nbsp; Perform Core Exercise 3.1 (Highlight answer in yellow).', timing_style))
    story.append(Paragraph('0:40 &nbsp; Changing highlight color or removing highlights; perform Core Exercise 3.2.', timing_style))
    story.append(Paragraph('0:43 &nbsp; Protecting your study: creating a backup file (.jwlibrary) in Settings &gt; Backup and Restore.', timing_style))
    story.append(Paragraph('0:46 &nbsp; Perform Core Exercise 3.3 (Create Backup). (Instructor demonstrates Notes &amp; Tags).', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Wrap-Up, Review &amp; Questions: (0:50 - 1:00)</b>', section_hdr))
    story.append(Paragraph('0:50 &nbsp; 10-minute flex buffer for review, questions, or extra time. Optional 15-min one-on-one help after.', timing_style))
    story.append(Spacer(1, 2))

    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=2))
    story.append(Paragraph('<b>CORE EXERCISES</b>', ex_hdr))

    story.append(Paragraph('<b>1.1</b> Tap <b>Daily Text</b> (sun icon). Tap the <b>A A</b> icon at top and slide to enlarge the text.', ex_style))
    story.append(Paragraph('<b>1.2</b> Tap <b>Bible</b>. Select a book (e.g., <i>Matthew</i>) and chapter (e.g., <i>5</i>) to begin reading.', ex_style))
    story.append(Paragraph('<b>1.3</b> Tap <b>Meetings</b>. Open this week\'s <i>Watchtower</i> Study article directly with one tap.', ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph('<b>2.1</b> Verify your device is connected to Wi-Fi to preserve mobile cellular data.', ex_style))
    story.append(Paragraph('<b>2.2</b> In Publications or Meetings, tap the <b>Cloud icon</b> on a study item to download it for offline use.', ex_style))
    story.append(Paragraph('<b>2.3</b> Open Daily Text or Bible. Tap <b>Headphones</b> to listen; stop with <b>Volume Down</b> (or Mute key).', ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph('<b>3.1</b> In paragraph 1 of the <i>Watchtower</i> study, press and drag across an answer and tap <b>Yellow</b>.', ex_style))
    story.append(Paragraph('<b>3.2</b> Tap the highlighted text again to switch the color (blue or green), or tap the trash icon to erase.', ex_style))
    story.append(Paragraph('<b>3.3</b> Open Settings &gt; Backup and Restore and tap <b>Create Backup</b> to save your study marks.', ex_style))
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
        fontName=FONT_BOLD,
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1e3a8a')
    )

    note_style = ParagraphStyle(
        'DocNote',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#475569')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=8,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName=FONT_REG,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b')
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName=FONT_REG,
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
        '<i>JW Library Tutorial</i>. The course is organized into three focused 15-minute lessons: '
        '<b>Finding Scriptures &amp; Meetings</b>, <b>Downloading and Using Media</b>, and <b>Personal Study Tools</b>. '
        'A dedicated 10-minute wrap-up buffer provides generous flex time so instructors never feel rushed. '
        'Before the class begins, students should be provided with a copy of the tutorial materials and be '
        'reminded to have the app pre-installed on their device.',
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        'The <i>JW Library Class Program</i> serves as a template when planning a session schedule. Five minutes are '
        'designated at the beginning to orient students to their device layout. Each 15-minute lesson centers on three '
        'core hands-on actions, reserving complex topics for quick instructor demonstrations. The full session runs in '
        '60 minutes, with the option to extend to 75 to 90 minutes for groups desiring additional individual assistance.',
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
    story.append(Paragraph('&bull; Navigate between Bible, Publications, Meetings, and Personal Study.', bullet_style))
    story.append(Paragraph('&bull; Access the Daily Text and enlarge reading text using the A A button.', bullet_style))
    story.append(Paragraph('&bull; Locate weekly meeting study articles with one tap from the Meetings tab.', bullet_style))
    story.append(Paragraph('&bull; Understand offline reading and download publications on Wi-Fi to preserve mobile data.', bullet_style))
    story.append(Paragraph('&bull; Use the audio player (headphones icon) and quickly silence unexpected audio.', bullet_style))
    story.append(Paragraph('&bull; Highlight answers in study articles in various colors and remove highlights.', bullet_style))
    story.append(Paragraph('&bull; Create a safety backup (.jwlibrary file) to safeguard study records.', bullet_style))

    story.append(Paragraph('Prerequisites &amp; Setup Tips', h1_style))
    story.append(Paragraph('Before attending this course, students should have:', body_style))
    story.append(Paragraph('&bull; Arrive <b>10–15 minutes early</b> for helper assistance with Wi-Fi and Bible/Daily Text setup.', bullet_style))
    story.append(Paragraph('&bull; A supported device running <b>Android 8.0+</b>, <b>iOS 15.0+</b>, <b>macOS M1+</b>, or <b>Windows 10 v2004+</b>.', bullet_style))
    story.append(Paragraph('&bull; Arrive with a <b>fully charged battery</b> (or bring a charger).', bullet_style))
    story.append(Paragraph('&bull; Temporarily set device <b>screen timeout to 2 or 5 minutes</b> to prevent the screen turning off.', bullet_style))
    story.append(Paragraph('&bull; At least <b>2 to 4 GB</b> of available storage (or an installed SD card) for media files.', bullet_style))
    story.append(Paragraph('&bull; Connect to a Wi-Fi connection prior to downloading video or audio media.', bullet_style))

    # ==================== PAGE 2 ====================
    story.append(PageBreak())

    story.append(Paragraph('JW Library Tutorial Curriculum', doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Lesson 1: Finding Scriptures &amp; Meetings (15 Minutes)', h1_style))
    story.append(Paragraph(
        'This lesson introduces students to moving smoothly between the primary sections of the JW Library app. '
        'Instructors should explain the placement of the navigation bar based on the devices present (bottom bar on iOS '
        'and modern Android; top menu on Windows). Demonstrate how tapping the <b>A A</b> icon enlarges text for comfortable '
        'reading, and how the <b>Meetings tab</b> provides one-tap access to weekly meeting publications.',
        body_style
    ))

    story.append(Paragraph('Topics (10 minutes)', h2_style))
    story.append(Paragraph('&bull; Main Navigation Tabs (Bible, Publications, Meetings, Personal Study)', bullet_style))
    story.append(Paragraph('&bull; Daily Text &amp; Adjusting Text Size (A A button to increase font size)', bullet_style))
    story.append(Paragraph('&bull; Opening a specific Bible book and chapter (e.g., Matthew 5)', bullet_style))
    story.append(Paragraph('&bull; Meetings Tab (accessing Midweek workbook and Weekend Watchtower study article)', bullet_style))
    story.append(Paragraph('&bull; <i>Instructor Demonstration:</i> Bookmarks, History, and Search (for practice at home)', bullet_style))

    story.append(Paragraph('Hands-On Core Exercises (5 minutes)', h2_style))
    story.append(Paragraph('&bull; <b>Core 1.1:</b> Open Daily Text and tap <b>A A</b> to make the print large and clear.', bullet_style))
    story.append(Paragraph('&bull; <b>Core 1.2:</b> Tap Bible, choose a book (Matthew), and open chapter 5.', bullet_style))
    story.append(Paragraph('&bull; <b>Core 1.3:</b> Open the Meetings tab and tap this week\'s Watchtower Study article.', bullet_style))

    story.append(Paragraph('Facilitator Notes for Lesson 1', h2_style))
    story.append(Paragraph(
        'Host a 15-minute early arrival clinic so helpers ensure the Bible and Daily Text are ready. At the start of class, '
        'conduct a 30-second readiness check: have students raise hands if they need download assistance so helpers can '
        'assist quietly while you proceed. Teach device silencing early (side Volume Down on mobile; keyboard Mute key on PC) '
        'to eliminate anxiety. Have assistants verify that students successfully enlarge text with the A A button.',
        body_style
    ))

    story.append(Paragraph('After completing this lesson, students will be able to:', h2_style))
    story.append(Paragraph('&bull; Switch comfortably between all main app sections.', bullet_style))
    story.append(Paragraph('&bull; Enlarge text size across the app for strain-free reading.', bullet_style))
    story.append(Paragraph('&bull; Open any Bible chapter and reach weekly meeting articles with one tap.', bullet_style))

    # ==================== PAGE 3 ====================
    story.append(PageBreak())

    story.append(Paragraph('JW Library Tutorial Curriculum', doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Lesson 2: Downloading and Using Media (15 Minutes)', h1_style))
    story.append(Paragraph(
        'This lesson explains how offline reading works and demonstrates downloading publications and multimedia. '
        'Emphasize that once an item is downloaded on Wi-Fi, it stays on the device permanently without requiring internet '
        'or mobile data at meetings. Introduce the audio player (headphones icon) so students can listen to text read aloud.',
        body_style
    ))

    story.append(Paragraph('Topics (10 minutes)', h2_style))
    story.append(Paragraph('&bull; Understanding Offline Use: reading and listening with no cellular connection', bullet_style))
    story.append(Paragraph('&bull; Connecting to Wi-Fi before downloading to preserve mobile cellular data limits', bullet_style))
    story.append(Paragraph('&bull; Downloading publications and media (recognizing the Cloud icon)', bullet_style))
    story.append(Paragraph('&bull; Using Audio Player and emergency quick-silencing (Volume Down on mobile; Mute key on PC)', bullet_style))
    story.append(Paragraph('&bull; <i>Instructor Demonstration:</i> Sorting by Largest Size to inspect storage and delete files', bullet_style))

    story.append(Paragraph('Hands-On Core Exercises (5 minutes)', h2_style))
    story.append(Paragraph('&bull; <b>Core 2.1:</b> Confirm the device is connected to Wi-Fi at the top of the screen.', bullet_style))
    story.append(Paragraph('&bull; <b>Core 2.2:</b> Tap the Cloud icon on a study publication or video to download it.', bullet_style))
    story.append(Paragraph('&bull; <b>Core 2.3:</b> Open Daily Text or Bible, tap Headphones to listen; stop with Volume Down or Mute key.', bullet_style))

    story.append(Paragraph('Facilitator Notes for Lesson 2', h2_style))
    story.append(Paragraph(
        'Reassure students on limited data plans that they will not use cellular data at meetings if they download '
        'ahead of time on Wi-Fi. Explicitly practice emergency silencing: non-tech users often fear accidental sound; '
        'knowing how to silence immediately (holding side Volume Down on mobile or tapping Mute key on PC) gives complete peace of mind.',
        body_style
    ))

    story.append(Paragraph('After completing this lesson, students will be able to:', h2_style))
    story.append(Paragraph('&bull; Download publications safely on Wi-Fi without using mobile data.', bullet_style))
    story.append(Paragraph('&bull; Open and read downloaded publications offline at congregation meetings.', bullet_style))
    story.append(Paragraph('&bull; Play, pause, and immediately silence audio readings of scriptures and articles.', bullet_style))

    # ==================== PAGE 4 ====================
    story.append(PageBreak())

    story.append(Paragraph('JW Library Tutorial Curriculum', doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Lesson 3: Personal Study Tools (15 Minutes)', h1_style))
    story.append(Paragraph(
        'This lesson covers highlighting study articles for meetings and safeguarding personal study records. '
        'Demonstrate how to select and highlight text in yellow, change highlight colors, and delete highlights. '
        'Conclude with the vital step of creating a <code>.jwlibrary</code> safety backup file in Settings so '
        'personal study markings are never lost.',
        body_style
    ))

    story.append(Paragraph('Topics (10 minutes)', h2_style))
    story.append(Paragraph('&bull; Selecting text by gentle pressing and dragging to highlight', bullet_style))
    story.append(Paragraph('&bull; Choosing highlight colors (Yellow, Blue, Green)', bullet_style))
    story.append(Paragraph('&bull; Tapping highlighted text to switch colors or erase with the trash icon', bullet_style))
    story.append(Paragraph('&bull; <b>Data Protection:</b> Creating a backup file (Settings &gt; Backup and Restore)', bullet_style))
    story.append(Paragraph('&bull; <i>Instructor Demonstration:</i> Adding notes, Tags, and viewing the Personal Study tab', bullet_style))

    story.append(Paragraph('Hands-On Core Exercises (5 minutes)', h2_style))
    story.append(Paragraph('&bull; <b>Core 3.1:</b> Open the next Watchtower article and highlight an answer in paragraph 1 in yellow.', bullet_style))
    story.append(Paragraph('&bull; <b>Core 3.2:</b> Tap the highlighted answer to switch to blue, or tap the trash icon to erase.', bullet_style))
    story.append(Paragraph('&bull; <b>Core 3.3:</b> Open Settings &gt; Backup and Restore and tap <b>Create Backup</b>.', bullet_style))

    story.append(Paragraph('Wrap-Up &amp; Facilitator Recommendations (0:50 - 1:00)', h2_style))
    story.append(Paragraph(
        '• <b>Pre-Class Setup Clinic:</b> Opening doors 15 minutes early for helper setup prevents Wi-Fi bottlenecks.<br/>'
        '• <b>Emergency Silencing Reflex:</b> Teaching the Volume Down button early eliminates fear of unexpected audio.<br/>'
        '• <b>10-Minute Flex Buffer:</b> Use this wrap-up buffer to review accomplishments, answer questions, or absorb extra time.<br/>'
        '• <b>Table Assistants (Helpers):</b> Having 1 or 2 assistants walking the room to help individuals prevents class delays.<br/>'
        '• <b>Physical Handouts (When Beneficial):</b> Having printed 1-page Class Programs on tables helps where data/Wi-Fi is limited.<br/>'
        '• <b>Table QR Codes / Projection (Optional):</b> Projecting or placing QR cards on tables lets learners open the guide with one camera tap.<br/>'
        '• <b>Home Screen Bookmark (Optional):</b> Suggesting "Add to Home Screen" caches the practice guide for easy offline review.<br/>'
        '• <b>Stay-After Clinic:</b> Offer to stay for 15 minutes after class for anyone wanting one-on-one help with their backup file.',
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph('After completing this lesson, students will be able to:', h2_style))
    story.append(Paragraph('&bull; Highlight answers for meetings and adjust or erase highlights with confidence.', bullet_style))
    story.append(Paragraph('&bull; Safely back up their study notes and markings to a .jwlibrary file.', bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)


if __name__ == '__main__':
    program_pdf = 'D:/cs/JWLibrary/JW Library Class Program.pdf'
    curriculum_pdf = 'D:/cs/JWLibrary/JW Library Tutorial Curriculum.pdf'

    build_class_program(program_pdf)
    build_curriculum(curriculum_pdf)

    r1 = pypdf.PdfReader(program_pdf)
    r2 = pypdf.PdfReader(curriculum_pdf)
    print(f'SUCCESS: Program PDF generated with {len(r1.pages)} page(s).')
    print(f'SUCCESS: Curriculum PDF generated with {len(r2.pages)} page(s).')
