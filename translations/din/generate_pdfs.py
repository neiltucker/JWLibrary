import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

# Dinka (Thuɔŋjäŋ) version -- DRAFT TRANSLATION, NOT YET REVIEWED.
# The Dinka text below is an AI-produced first draft and must be checked by a
# fluent Dinka speaker before the PDFs are shared. App button names are kept
# in English on purpose. Output files get "(Dinka)" in their names so the
# English PDFs are not overwritten.

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Unicode font setup.
# The built-in Helvetica font cannot print letters such as ɛ, ɔ, ɣ, ŋ and ɛ̈/ɔ̈ (used in Dinka).
# This looks for a TrueType font that contains them and uses it instead.
# To guarantee correct output on any computer, put the four DejaVu Sans files
# (DejaVuSans.ttf, DejaVuSans-Bold.ttf, DejaVuSans-Oblique.ttf,
# DejaVuSans-BoldOblique.ttf) in a folder named "fonts" next to this script.
# ---------------------------------------------------------------------------
REQUIRED_CHARS = "ɛɔɣŋƐƆƔŊäëïö̈"

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEJAVU = ('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSans-Oblique.ttf', 'DejaVuSans-BoldOblique.ttf')
FONT_CANDIDATES = [
    tuple(os.path.join(_HERE, 'fonts', n) for n in _DEJAVU),
    tuple('/usr/share/fonts/truetype/dejavu/' + n for n in _DEJAVU),
    ('C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf', 'C:/Windows/Fonts/ariali.ttf', 'C:/Windows/Fonts/arialbi.ttf'),
    ('C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/segoeuib.ttf', 'C:/Windows/Fonts/segoeuii.ttf', 'C:/Windows/Fonts/segoeuiz.ttf'),
    ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
     '/System/Library/Fonts/Supplemental/Arial Italic.ttf', '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf'),
]


def setup_fonts():
    names = ('UniSans', 'UniSans-Bold', 'UniSans-Italic', 'UniSans-BoldItalic')
    for paths in FONT_CANDIDATES:
        if not all(os.path.isfile(p) for p in paths):
            continue
        try:
            fonts = [TTFont(n, p) for n, p in zip(names, paths)]
        except Exception:
            continue
        if not all(ord(c) in f.face.charToGlyph for f in fonts for c in REQUIRED_CHARS):
            continue
        for f in fonts:
            pdfmetrics.registerFont(f)
        pdfmetrics.registerFontFamily(names[0], normal=names[0], bold=names[1], italic=names[2], boldItalic=names[3])
        print(f'Font: {paths[0]}')
        return names
    print('WARNING: no installed font contains all the required letters (' + REQUIRED_CHARS + '). '
          'Falling back to Helvetica, so some letters will not print correctly. '
          'Place the DejaVu Sans .ttf files in a "fonts" folder next to this script.')
    return ('Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique')


FONT, FONT_BOLD, FONT_ITALIC, FONT_BOLD_ITALIC = setup_fonts()

# Canvas with "Page X of Y" numbers for the Curriculum
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
        self.setFont(FONT, 8)
        self.setFillColor(colors.HexColor('#64748b'))
        # Top right header
        self.drawRightString(letter[0] - 45, letter[1] - 30, f"Page {self._pageNumber} / {page_count}")
        # Bottom disclaimer on each page
        disclaimer = "JW Library ee trademark cï gät tënë Watch Tower Bible and Tract Society of Pennsylvania. Kuɔny ë piööc ë rɔt, ke cïn ɣɔɔc thïn."
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
        fontName=FONT,
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
        fontName=FONT,
        fontSize=7,
        leading=8.8,
        textColor=colors.HexColor('#1e293b')
    )

    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Normal'],
        fontName=FONT,
        fontSize=6,
        leading=7.5,
        alignment=1,
        textColor=colors.HexColor('#64748b')
    )

    story = []

    story.append(Paragraph("THAA Ë CLASS Ë JW LIBRARY", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>TAK:</b> Wël cï gam ë luɔ̈i ë JW Library atɔ̈ në JW.ORG (https://www.jw.org/en/online-help/jw-library/)", note_style))
    story.append(Paragraph("Class ë minit 60 ke nɔŋ piööc kadiäk ë minit 15 ku minit 10 ë thök. (Alëu bï juak agut cï minit 75-90).", note_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=3))

    # Schedule
    story.append(Paragraph("<b>Tɔ̈ɔ̈k ku Nyuɔɔth ë Skrin: (0:00 - 0:05)</b>", section_hdr))
    story.append(Paragraph("0:00 &nbsp; Tɔ̈ɔ̈k; thëm ë Baibol/Daily Text (kɔc ye kuɔny aye download kuɔny).", timing_style))
    story.append(Paragraph("0:02 &nbsp; Cuɔ̈ɔ̈t ë röl: muk Volume Down (phone) ka nyiɛ̈n Mute key (PC); yök navigation bar.", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Piööc 1: Yök ë Wël ë Baibol ku Amat (0:05 - 0:20)</b>", section_hdr))
    story.append(Paragraph("0:05 &nbsp; Jam ë navigation tabs dïït (Bible, Publications, Meetings, Personal Study).", timing_style))
    story.append(Paragraph("0:07 &nbsp; Liep Daily Text ku gät <b>A A</b> icon bï wël ya dït ku kuɛ̈n ya piɛth.", timing_style))
    story.append(Paragraph("0:10 &nbsp; Looi Them 1.1 (Daily Text ku Text Size).", timing_style))
    story.append(Paragraph("0:12 &nbsp; Liep athör ku chapter ë Baibol; looi Them 1.2.", timing_style))
    story.append(Paragraph("0:15 &nbsp; Jam ë Meetings tab (athör ë Midweek ku piööc ë Watchtower ë Weekend).", timing_style))
    story.append(Paragraph("0:18 &nbsp; Looi Them 1.3 (Meetings tab). (Raan ye piööc abï Bookmarks ku Search nyuɔɔth).", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Piööc 2: Download ku Luɔ̈i ë Röl ku Video (0:20 - 0:35)</b>", section_hdr))
    story.append(Paragraph("0:20 &nbsp; Deet ë luɔ̈i ke cïn intanet: kä cï download në Wi-Fi aye döŋ në device ke data ë phone cïï kɔɔr.", timing_style))
    story.append(Paragraph("0:22 &nbsp; Looi Them 2.1 (Tïŋ Wi-Fi ku tiit ë data ë phone).", timing_style))
    story.append(Paragraph("0:24 &nbsp; Download kë bï kuɛ̈n/tïŋ ke cïn intanet; looi Them 2.2.", timing_style))
    story.append(Paragraph("0:28 &nbsp; Audio Player (headphones icon); cuɔ̈ɔ̈t ë röl enɔn ke Volume Down (phone) ka Mute key (PC).", timing_style))
    story.append(Paragraph("0:31 &nbsp; Looi Them 2.3 (Piŋ Röl). (Raan ye piööc abï tïŋ ë storage nyuɔɔth).", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Piööc 3: Kä ë Piööc ë Rɔt (0:35 - 0:50)</b>", section_hdr))
    story.append(Paragraph("0:35 &nbsp; Lɔc wël bï bër highlight në piööc yic.", timing_style))
    story.append(Paragraph("0:37 &nbsp; Looi Them 3.1 (Highlight bër ke yellow).", timing_style))
    story.append(Paragraph("0:40 &nbsp; Waar color ë highlight ka nyaai highlight; looi Them 3.2.", timing_style))
    story.append(Paragraph("0:43 &nbsp; Tiit ë piööc du: looi backup file (.jwlibrary) në Settings &gt; Backup and Restore.", timing_style))
    story.append(Paragraph("0:46 &nbsp; Looi Them 3.3 (Create Backup). (Raan ye piööc abï Notes ku Tags nyuɔɔth).", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Thök, Dhuk Cök, ku Thiëc: (0:50 - 1:00)</b>", section_hdr))
    story.append(Paragraph("0:50 &nbsp; Minit 10 tënë dhuk cök, thiëc, ka thaa juak. Kuɔny ë rɔt ë minit 15 të cï class thök, tënë raan kɔɔr.", timing_style))
    story.append(Spacer(1, 2))

    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=2))
    story.append(Paragraph("<b>THEM DÏÏT</b>", ex_hdr))

    story.append(Paragraph("<b>1.1</b> Gät <b>Daily Text</b> (sun icon). Gät <b>A A</b> icon nhial ku cuɔ̈ɔ̈t bï wël ya dït.", ex_style))
    story.append(Paragraph("<b>1.2</b> Gät <b>Bible</b>. Lɔc athör (cït <i>Matthew</i>) ku chapter (cït <i>5</i>) ba kuɛ̈n jɔ̈k.", ex_style))
    story.append(Paragraph("<b>1.3</b> Gät <b>Meetings</b>. Liep piööc ë <i>Watchtower</i> ë week kënë enɔn ë gät tök.", ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>2.1</b> Tïŋ lɔn cï device du mat në Wi-Fi bï data ë phone du cïï thök.", ex_style))
    story.append(Paragraph("<b>2.2</b> Në Publications ka Meetings, gät <b>Cloud icon</b> në kë ë piööc bï download ku luɔ̈ɔ̈i ke cïn intanet.", ex_style))
    story.append(Paragraph("<b>2.3</b> Liep Daily Text ka Bible. Gät <b>Headphones</b> ba piŋ; cuɔ̈ɔ̈t ke <b>Volume Down</b> (ka Mute key).", ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>3.1</b> Në paragraph 1 ë piööc ë <i>Watchtower</i>, nyiɛ̈n ku cuɔ̈ɔ̈t cin du në bër ku gät <b>Yellow</b>.", ex_style))
    story.append(Paragraph("<b>3.2</b> Gät wël cï highlight aya bï color waar (blue ka green), ka gät trash icon bï nyaai.", ex_style))
    story.append(Paragraph("<b>3.3</b> Liep Settings &gt; Backup and Restore ku gät <b>Create Backup</b> bï kä cï gät në piööc du muk.", ex_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<i>Wël ë Löŋ: JW Library ee trademark cï gät tënë Watch Tower Bible and Tract Society of Pennsylvania. Thaa ë class kënë ee kuɔny ë piööc ë rɔt ke cïn ɣɔɔc thïn, ku acïï mat ke ka leec ë Watch Tower ka Ciëëtke Yekoba. (English: an independent, non-commercial training aid, not affiliated with or endorsed by Watch Tower or Jehovah's Witnesses.)</i>", disclaimer_style))

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
        fontName=FONT,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b')
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName=FONT,
        fontSize=9.5,
        leading=13.5,
        leftIndent=15,
        textColor=colors.HexColor('#1e293b')
    )

    story = []

    # ==================== PAGE 1 ====================
    story.append(Paragraph("Piööc ë JW Library: Athör tënë Kɔc ye Piööc", doc_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>TAK:</b> Wël cï gam ë luɔ̈i ë JW Library atɔ̈ në JW.ORG (https://www.jw.org/en/online-help/jw-library/)", note_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Wël ë Piööc ë JW Library", h1_style))
    story.append(Paragraph(
        "Athör kënë ee tënë raan ëbɛ̈n ye kɔc piööc ka ye kɔc wɛ̈t ke <i>Piööc ë JW Library</i>. "
        "Piööc anɔŋ piööc kadiäk ë minit 15: "
        "<b>Yök ë Wël ë Baibol ku Amat</b>, <b>Download ku Luɔ̈i ë Röl ku Video</b>, ku <b>Kä ë Piööc ë Rɔt</b>. "
        "Minit 10 ë thök aye thaa juak gam, bï kɔc ye piööc cïï yäc. "
        "Ke class ŋoot ke kën jɔ̈k, kɔc ye piɔ̈ɔ̈c abï athör ë piööc gam, "
        "ku abï ke lueel bïk app tääu në device ke ke ŋoot.",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<i>Thaa ë Class ë JW Library</i> aye luɔ̈ɔ̈i të ye thaa ë class guiir. Minit dhïc "
        "atɔ̈ të jɔ̈k bï kɔc device ken nyuɔɔth. Piööc ëbɛ̈n ë minit 15 anɔŋ kä kadiäk dïït bï them, "
        "ku kä ril aye raan ye piööc nyuɔɔth enɔn. Class ëbɛ̈n aye dɔm "
        "minit 60, ku alëu bï juak agut cï minit 75 ka 90 tënë kɔc kɔɔr kuɔny ë rɔt juëc.",
        body_style
    ))

    story.append(Paragraph("Kɔc cï Piööc Guiir Tënë Keek", h1_style))
    story.append(Paragraph(
        "Piööc kënë acï guiir tënë kɔc ŋic kä koor ë smartphone, tablet, ka computer. "
        "Kɔc ye piɔ̈ɔ̈c alëu bïk touchscreen ka mouse luɔ̈ɔ̈i. Të cï raan JW Library app luɔ̈ɔ̈i thɛɛ, "
        "ka kuɔny, ku acïï kɔɔr.",
        body_style
    ))

    story.append(Paragraph("Kë bï Kɔc Lëu", h1_style))
    story.append(Paragraph("Të cï kek piööc kënë thök, kɔc ye piɔ̈ɔ̈c abï lëu:", body_style))
    story.append(Paragraph("&bull; Bïk lɔ në Bible, Publications, Meetings, ku Personal Study.", bullet_style))
    story.append(Paragraph("&bull; Bïk Daily Text liep ku wël juak ke A A button.", bullet_style))
    story.append(Paragraph("&bull; Bïk piööc ë amat ë week ëbɛ̈n yök ë gät tök në Meetings tab.", bullet_style))
    story.append(Paragraph("&bull; Bïk kuɛ̈n ke cïn intanet deet ku athör download në Wi-Fi bï data cïï thök.", bullet_style))
    story.append(Paragraph("&bull; Bïk audio player (headphones icon) luɔ̈ɔ̈i ku röl cï bɔ̈ ke kën ye tak cuɔ̈ɔ̈t enɔn.", bullet_style))
    story.append(Paragraph("&bull; Bïk bër highlight në piööc yic ke color kɔ̈k ku bïk highlight nyaai.", bullet_style))
    story.append(Paragraph("&bull; Bïk backup (.jwlibrary file) looi bï kä ë piööc tiit.", bullet_style))

    story.append(Paragraph("Kä Kɔɔr ku Kuɔny ë Guiir", h1_style))
    story.append(Paragraph("Ke kek ŋoot ke kën class bɛ̈n, kɔc ye piɔ̈ɔ̈c abï:", body_style))
    story.append(Paragraph("&bull; Bïk bɛ̈n <b>minit 10–15 ke ŋoot</b> bï kɔc ye kuɔny ke kuɔny ë Wi-Fi ku Baibol/Daily Text.", bullet_style))
    story.append(Paragraph("&bull; Bïk device nɔŋ <b>Android 8.0+</b>, <b>iOS 15.0+</b>, <b>macOS M1+</b>, ka <b>Windows 10 v2004+</b>.", bullet_style))
    story.append(Paragraph("&bull; Bïk bɛ̈n ke <b>battery cï thiäŋ</b> (ka bïk charger bɛ̈ɛ̈i).", bullet_style))
    story.append(Paragraph("&bull; Bïk <b>screen timeout guiir bï ya minit 2 ka 5</b> bï skrin cïï thiök.", bullet_style))
    story.append(Paragraph("&bull; Bïk <b>GB 2 agut 4</b> ë storage (ka SD card) tënë file ë röl ku video.", bullet_style))
    story.append(Paragraph("&bull; Bïk device mat në Wi-Fi ke kek ŋoot ke kën video ka röl download.", bullet_style))

    # ==================== PAGE 2 ====================
    story.append(PageBreak())

    story.append(Paragraph("Piööc ë JW Library: Athör tënë Kɔc ye Piööc", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Piööc 1: Yök ë Wël ë Baibol ku Amat (Minit 15)", h1_style))
    story.append(Paragraph(
        "Piööc kënë aye kɔc nyuɔɔth të ye kek lɔ në kä dïït ë JW Library app yic apieth. "
        "Kɔc ye piööc abï tɛ̈ tɔ̈ navigation bar thïn lueel në device tɔ̈ thïn (piny në iOS "
        "ku Android yam; nhial në Windows). Nyuɔɔth të ye gät ë <b>A A</b> icon wël juak bï kuɛ̈n "
        "ya piɛth, ku të ye <b>Meetings tab</b> athör ë amat ë week ëbɛ̈n liep ë gät tök.",
        body_style
    ))

    story.append(Paragraph("Kä bï Piööc (minit 10)", h2_style))
    story.append(Paragraph("&bull; Navigation Tabs Dïït (Bible, Publications, Meetings, Personal Study)", bullet_style))
    story.append(Paragraph("&bull; Daily Text ku Guiir ë Text Size (A A button bï wël juak)", bullet_style))
    story.append(Paragraph("&bull; Liep ë athör ku chapter ë Baibol (cït Matthew 5)", bullet_style))
    story.append(Paragraph("&bull; Meetings Tab (liep ë athör ë Midweek ku piööc ë Watchtower ë Weekend)", bullet_style))
    story.append(Paragraph("&bull; <i>Raan ye Piööc Abï Nyuɔɔth:</i> Bookmarks, History, ku Search (bï them baai)", bullet_style))

    story.append(Paragraph("Them Dïït (minit 5)", h2_style))
    story.append(Paragraph("&bull; <b>Them 1.1:</b> Liep Daily Text ku gät <b>A A</b> bï wël ya dït ku tïŋ apieth.", bullet_style))
    story.append(Paragraph("&bull; <b>Them 1.2:</b> Gät Bible, lɔc athör (Matthew), ku liep chapter 5.", bullet_style))
    story.append(Paragraph("&bull; <b>Them 1.3:</b> Liep Meetings tab ku gät piööc ë Watchtower ë week kënë.", bullet_style))

    story.append(Paragraph("Wël tënë Raan ye Class Wɛ̈t: Piööc 1", h2_style))
    story.append(Paragraph(
        "Guiir kuɔny ë minit 15 tënë kɔc bɔ̈ ë thɛɛ bï kɔc ye kuɔny tïŋ lɔn cï Baibol ku Daily Text guiir. Të jɔ̈k class, "
        "looi thëm ë second 30: lueel tënë kɔc bïk ciin ke jɔt të kɔɔr kek kuɔny ë download, bï kɔc ye kuɔny "
        "ke kuɔny amääth ke yïn ŋoot ke piööc. Piööc cuɔ̈ɔ̈t ë röl enɔn (Volume Down në lɔ̈ŋ ë phone; Mute key në keyboard ë PC) "
        "bï riɔ̈ɔ̈c thök. Kɔc ye kuɔny abï tïŋ lɔn cï kɔc wël juak ke A A button.",
        body_style
    ))

    story.append(Paragraph("Të cï kek piööc kënë thök, kɔc ye piɔ̈ɔ̈c abï lëu:", h2_style))
    story.append(Paragraph("&bull; Bïk lɔ në kä dïït ëbɛ̈n ë app yic apieth.", bullet_style))
    story.append(Paragraph("&bull; Bïk wël juak në app ëbɛ̈n bï kuɛ̈n cïn riɛl.", bullet_style))
    story.append(Paragraph("&bull; Bïk chapter ë Baibol liep ku piööc ë amat ë week ëbɛ̈n yök ë gät tök.", bullet_style))

    # ==================== PAGE 3 ====================
    story.append(PageBreak())

    story.append(Paragraph("Piööc ë JW Library: Athör tënë Kɔc ye Piööc", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Piööc 2: Download ku Luɔ̈i ë Röl ku Video (Minit 15)", h1_style))
    story.append(Paragraph(
        "Piööc kënë aye të ye kuɛ̈n ke cïn intanet luui thïn lueel, ku aye download ë athör, röl, ku video nyuɔɔth. "
        "Lueel lɔn të cï kë download në Wi-Fi, ka döŋ në device aköl ëbɛ̈n ke intanet "
        "ka data ë phone cïï kɔɔr në amat. Nyuɔɔth audio player (headphones icon) bï kɔc wël piŋ ke ye kuɛ̈n ë röl.",
        body_style
    ))

    story.append(Paragraph("Kä bï Piööc (minit 10)", h2_style))
    story.append(Paragraph("&bull; Deet ë Luɔ̈i ke Cïn Intanet: kuɛ̈n ku piŋ ke cïn network ë phone", bullet_style))
    story.append(Paragraph("&bull; Mat në Wi-Fi ke yïn ŋoot ke kën download bï data ë phone cïï thök", bullet_style))
    story.append(Paragraph("&bull; Download ë athör, röl, ku video (ŋic ë Cloud icon)", bullet_style))
    story.append(Paragraph("&bull; Luɔ̈i ë Audio Player ku cuɔ̈ɔ̈t ë röl enɔn (Volume Down në phone; Mute key në PC)", bullet_style))
    story.append(Paragraph("&bull; <i>Raan ye Piööc Abï Nyuɔɔth:</i> Lɔc Largest Size bï storage tïŋ ku file nyaai", bullet_style))

    story.append(Paragraph("Them Dïït (minit 5)", h2_style))
    story.append(Paragraph("&bull; <b>Them 2.1:</b> Tïŋ nhial në skrin lɔn cï device mat në Wi-Fi.", bullet_style))
    story.append(Paragraph("&bull; <b>Them 2.2:</b> Gät Cloud icon në athör ë piööc ka video bï download.", bullet_style))
    story.append(Paragraph("&bull; <b>Them 2.3:</b> Liep Daily Text ka Bible, gät Headphones ba piŋ; cuɔ̈ɔ̈t ke Volume Down ka Mute key.", bullet_style))

    story.append(Paragraph("Wël tënë Raan ye Class Wɛ̈t: Piööc 2", h2_style))
    story.append(Paragraph(
        "Lueel tënë kɔc nɔŋ data koor lɔn acïï data ë phone bï luɔ̈ɔ̈i në amat të cï kek download "
        "ke ŋoot në Wi-Fi. Them cuɔ̈ɔ̈t ë röl ëtök: kɔc cïï ŋic technology ariɔ̈ɔ̈c arak juëc lɔn bï röl bɛ̈n ke kën ye tak; "
        "të ŋic kek të bï röl cuɔ̈ɔ̈t enɔn (muk Volume Down në lɔ̈ŋ ë phone ka nyiɛ̈n Mute key në PC), ka piɔ̈ŋ ke abï dɔ̈ɔ̈r.",
        body_style
    ))

    story.append(Paragraph("Të cï kek piööc kënë thök, kɔc ye piɔ̈ɔ̈c abï lëu:", h2_style))
    story.append(Paragraph("&bull; Bïk athör download apieth në Wi-Fi ke data ë phone cïï luɔ̈ɔ̈i.", bullet_style))
    story.append(Paragraph("&bull; Bïk athör cï download liep ku kuɛ̈n ke cïn intanet në amat ë akutnhom.", bullet_style))
    story.append(Paragraph("&bull; Bïk kuɛ̈n ë röl ë wël ë Baibol ku piööc play, pause, ku cuɔ̈ɔ̈t enɔn.", bullet_style))

    # ==================== PAGE 4 ====================
    story.append(PageBreak())

    story.append(Paragraph("Piööc ë JW Library: Athör tënë Kɔc ye Piööc", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Piööc 3: Kä ë Piööc ë Rɔt (Minit 15)", h1_style))
    story.append(Paragraph(
        "Piööc kënë aye highlight ë piööc tënë amat ku tiit ë kä ë piööc ë rɔt nyuɔɔth. "
        "Nyuɔɔth të ye wël lɔc ku highlight ke yellow, të ye color waar, ku të ye highlight nyaai. "
        "Thök ke kë dït: looi <code>.jwlibrary</code> backup file në Settings bï "
        "kä cï gät në piööc ë rɔt cïï määr.",
        body_style
    ))

    story.append(Paragraph("Kä bï Piööc (minit 10)", h2_style))
    story.append(Paragraph("&bull; Lɔc wël ke nyiɛ̈n amääth ku cuɔ̈ɔ̈t bï highlight", bullet_style))
    story.append(Paragraph("&bull; Lɔc color ë highlight (Yellow, Blue, Green)", bullet_style))
    story.append(Paragraph("&bull; Gät wël cï highlight bï color waar ka nyaai ke trash icon", bullet_style))
    story.append(Paragraph("&bull; <b>Tiit ë Kä:</b> Looi backup file (Settings &gt; Backup and Restore)", bullet_style))
    story.append(Paragraph("&bull; <i>Raan ye Piööc Abï Nyuɔɔth:</i> Mat notes, Tags, ku tïŋ Personal Study tab", bullet_style))

    story.append(Paragraph("Them Dïït (minit 5)", h2_style))
    story.append(Paragraph("&bull; <b>Them 3.1:</b> Liep piööc ë Watchtower bɔ̈ tueŋ ku highlight bër në paragraph 1 ke yellow.", bullet_style))
    story.append(Paragraph("&bull; <b>Them 3.2:</b> Gät bër cï highlight bï waar ë blue, ka gät trash icon bï nyaai.", bullet_style))
    story.append(Paragraph("&bull; <b>Them 3.3:</b> Liep Settings &gt; Backup and Restore ku gät <b>Create Backup</b>.", bullet_style))

    story.append(Paragraph("Thök ku Wël tënë Raan ye Class Wɛ̈t (0:50 - 1:00)", h2_style))
    story.append(Paragraph(
        "• <b>Kuɔny ke Class Ŋoot ke Kën Jɔ̈k:</b> Liep ë ɣöt minit 15 ke ŋoot bï kɔc ye kuɔny device guiir, ka Wi-Fi acïï bï cuɔ̈ɔ̈t.<br/>"
        "• <b>Cuɔ̈ɔ̈t ë Röl Tueŋ:</b> Piööc ë Volume Down button ke ŋoot aye riɔ̈ɔ̈c ë röl cï bɔ̈ ke kën ye tak nyaai.<br/>"
        "• <b>Minit 10 ë Juak:</b> Luɔ̈ɔ̈i minit kɔ̈k ë thök bï dhuk cök në kä cï looi, bï thiëc bëër, ka bï thaa juak dɔm.<br/>"
        "• <b>Kɔc ye Kuɔny në Mëth:</b> Kɔc 1 ka 2 ye kuɔny ke cath në ɣöt yic ke kɔc kuɔny ë rɔt, ka class acïï bï kääc.<br/>"
        "• <b>Awereek cï Gɔ̈r në Piny (Të wïc kɔc):</b> Tääu de awereek ke 1-page Class Program në tëëbil nhial akony kɔc të cïn data ka Wi-Fi apath.<br/>"
        "• <b>QR Codes në Tëëbil ka në Skrin:</b> Nyuɔɔth QR code në skrin ka tääu awereek ke QR në tëëbil bï kɔc piööc liep në camera ë phone.<br/>"
        "• <b>Mat në Home Screen:</b> Nyuɔɔth kɔc \"Add to Home Screen\" bï piööc kënë tɔ̈ në phone yic ku liep të cïn intanet.<br/>"
        "• <b>Kuɔny ë Cök ë Class:</b> Döŋ minit 15 të cï class thök tënë raan kɔɔr kuɔny ë rɔt ë backup file.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Të cï kek piööc kënë thök, kɔc ye piɔ̈ɔ̈c abï lëu:", h2_style))
    story.append(Paragraph("&bull; Bïk bër highlight tënë amat ku bïk highlight waar ka nyaai ke cïn riɔ̈ɔ̈c.", bullet_style))
    story.append(Paragraph("&bull; Bïk note ku kä cï gät në piööc ken muk apieth në .jwlibrary file.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)


if __name__ == '__main__':
    program_pdf = 'D:/cs/JWLibrary/JW Library Class Program (Dinka).pdf'
    curriculum_pdf = 'D:/cs/JWLibrary/JW Library Tutorial Curriculum (Dinka).pdf'

    build_class_program(program_pdf)
    build_curriculum(curriculum_pdf)

    r1 = pypdf.PdfReader(program_pdf)
    r2 = pypdf.PdfReader(curriculum_pdf)
    print(f'SUCCESS: Dinka Program PDF generated with {len(r1.pages)} page(s).')
    print(f'SUCCESS: Dinka Curriculum PDF generated with {len(r2.pages)} page(s).')
