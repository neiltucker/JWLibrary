import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

# Dangme version (layout copied from the Ga script). It makes the Dangme PDFs under their own
# file names, so the English, Kiswahili, Luganda, Dinka and Ga PDFs are not overwritten.
# The PDFs are written to the repository root (two folders up from this script).

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Unicode font setup.
# The built-in Helvetica font cannot print the Dangme letters ɛ and ɔ.
# This looks for a TrueType font that contains them and uses it instead.
# It uses DejaVu Sans from the shared "fonts" folder at the top of the
# repository first, so the PDFs look the same on every computer and carry
# their own font. If that folder is missing, an installed font is used.
# ---------------------------------------------------------------------------
REQUIRED_CHARS = "ɛɔƐƆ"

_HERE = os.path.dirname(os.path.abspath(__file__))
_DEJAVU = ('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSans-Oblique.ttf', 'DejaVuSans-BoldOblique.ttf')
FONT_CANDIDATES = [
    tuple(os.path.join(_HERE, '..', '..', 'fonts', n) for n in _DEJAVU),
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
          'Make sure the "fonts" folder at the top of the repository contains the DejaVu Sans .ttf files.')
    return ('Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique')



FONT, FONT_BOLD, FONT_ITALIC, FONT_BOLD_ITALIC = setup_fonts()

# Remove this line, and its two uses below, after a fluent Dangme speaker has reviewed the text.
DRAFT_LINE = "<b>DRAFT TRANSLATION — NOT YET REVIEWED.</b> Nɛ ɔ ji sisije tsɔɔmi nɛ a pee ngɛ Dangme mi."

# Numbered canvas for the curriculum: "Bf. X / Y" (page X of Y)
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
        # Top right
        self.drawRightString(letter[0] - 45, letter[1] - 30, f"Bf. {self._pageNumber} / {page_count}")
        # Legal line at the bottom of every page
        disclaimer = "JW Library ji Watch Tower Bible and Tract Society of Pennsylvania okadi nɛ a kɛ wo mlaa sisi. Ní tsumi nɛ da e he."
        # Shrink the notice slightly if needed so it always fits across the page.
        size = 8
        while size > 5 and pdfmetrics.stringWidth(disclaimer, FONT, size) > letter[0] - 60:
            size -= 0.25
        self.setFont(FONT, size)
        self.drawCentredString(letter[0] / 2.0, 20, disclaimer)
        self.setFont(FONT, 8)
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


    # ---- Dangme: Class Program (1 page) ----
    story = []

    story.append(Paragraph("JW LIBRARY KLAS Ɔ HE BLƆ NYA TOMI", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph(DRAFT_LINE, note_style))
    story.append(Paragraph("<b>KAI:</b> Blɔ tsɔɔmihi nɛ je asafo ɔ ngɔ ngɛ bɔ nɛ a kɛ JW Library tsuɔ ní ha a he ngɛ JW.ORG nɔ (https://www.jw.org/ada/intanɛti-nɔ-yemi-kɛ-buami/jw-library/ kɛ https://www.jw.org/en/online-help/jw-library/)", note_style))
    story.append(Paragraph("Klas nɛ maa ye hɛngm. 60: ní kasemihi etɛ, nɛ eko tsuaa eko maa ye hɛngm. 15, kɛ hɛngm. 10 kɛ ha nyagbe. (A ma nyɛ maa pee hɛngm. 75-90.)", note_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=3))

    story.append(Paragraph("<b>Sisije: (0:00 - 0:05)</b>", section_hdr))
    story.append(Paragraph("0:00 &nbsp; Mo Hee; a hyɛ kaa nɔ tsuaa nɔ gbla Baiblo ɔ kɛ Daa Ligbi Ngmami ɔ lo (nihi nɛ yeɔ bua a yeɔ nihi nɛ e sa kaa a gbla a bua).", timing_style))
    story.append(Paragraph("0:02 &nbsp; Ga womi kɛ ha bɔ nɛ a haa gbi nɛ kpa ha: moo nyɛ Volume Down nɔ nɛ o kɛ o nine nɛ pi nɔ (fon), loo moo nyɛ Mute (kɔmpiuta); hyɛ he nɛ navigation bar ɔ ngɛ.", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Ní Kasemi 1: Bɔ Nɛ O Maa Na Ngmami Ɔmɛ Kɛ Asafo Mi Kpehi A Níhi Ha (0:05 - 0:20)</b>", section_hdr))
    story.append(Paragraph("0:05 &nbsp; A susu fãhi ɔmɛ a he (Bible, Publications, Meetings, Personal Study).", timing_style))
    story.append(Paragraph("0:07 &nbsp; A bli Daa Ligbi Ngmami ɔ, nɛ a nyɛ <b>Text Settings</b> (<b>A A</b>) okadi ɔ nɔ konɛ ningma amɛ nɛ hi agbo.", timing_style))
    story.append(Paragraph("0:10 &nbsp; Nyɛɛ pee Ní Peemi 1.1 (Daa Ligbi Ngmami ɔ kɛ ningma amɛ a klemi).", timing_style))
    story.append(Paragraph("0:12 &nbsp; A bli Baiblo womi ko kɛ yi ko; nyɛɛ pee Ní Peemi 1.2.", timing_style))
    story.append(Paragraph("0:15 &nbsp; A susu Meetings fã ɔ he (Ní Kasemi Womi kɛ ha Si Himi Kɛ Sɔmɔmi Ní Tsumi Kpe [Midweek Meeting], kɛ Hwɔɔmi Mɔ Ní Kasemi kɛ ha Otsi Nyagbe Kpe [Weekend Meeting]).", timing_style))
    story.append(Paragraph("0:18 &nbsp; Nyɛɛ pee Ní Peemi 1.3 (Meetings). (Tsɔɔlɔ ɔ tsɔɔ Bookmark kɛ Search.)", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Ní Kasemi 2: Níhi Nɛ A Gblaa Kɛ Bɔ Nɛ A Kɛ Tsuɔ Ní Ha (0:20 - 0:35)</b>", section_hdr))
    story.append(Paragraph("0:20 &nbsp; Níhi nɛ o gbla be nɛ o ngɛ Wi-Fi ɔ nɔ ɔ hiɔ o klama a nɔ; e he hia we kaa o ngɔ mobail data ke o ngɛ ní tsue.", timing_style))
    story.append(Paragraph("0:22 &nbsp; Nyɛɛ pee Ní Peemi 2.1 (Wi-Fi ɔ hyɛmi konɛ mobail data a ko puɛ).", timing_style))
    story.append(Paragraph("0:24 &nbsp; A gbla nɔ́ ko konɛ a kane loo a hyɛ ke intanɛti be; nyɛɛ pee Ní Peemi 2.2.", timing_style))
    story.append(Paragraph("0:28 &nbsp; Munyuhi nɛ a buɔ tue (headphones okadi); bɔ nɛ a haa gbi nɛ kpa ha amlɔ nɛ ɔ kɛ gu Volume Down (fon) loo Mute (kɔmpiuta) nɔ.", timing_style))
    story.append(Paragraph("0:31 &nbsp; Nyɛɛ pee Ní Peemi 2.3 (Bu tue). (Tsɔɔlɔ ɔ tsɔɔ bɔ nɛ a hyɛɛ blɔ nɛ ngɛ klama a nɔ ha.)", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Ní Kasemi 3: Níhi Nɛ O Ma Nyɛ Maa Kɛ Tsu Ní Ngɛ Dɛ He Ní Kasemi Mi (0:35 - 0:50)</b>", section_hdr))
    story.append(Paragraph("0:35 &nbsp; Bɔ nɛ a ngɔɔ kɔla kɛ kadiɔ hetohi ngɛ munyuhi nɛ a kaseɔ ɔ a mi ha.", timing_style))
    story.append(Paragraph("0:37 &nbsp; Nyɛɛ pee Ní Peemi 3.1 (Ngɔɔ yɛlo kɔla kɛ kadi heto ko).", timing_style))
    story.append(Paragraph("0:40 &nbsp; Bɔ nɛ a tsakeɔ kɔla a loo a jeɔ ha; nyɛɛ pee Ní Peemi 3.2.", timing_style))
    story.append(Paragraph("0:43 &nbsp; Bɔ nɛ a poɔ o níhi a he piɛ ha: backup (.jwlibrary) peemi ngɛ Settings &gt; Backup and Restore.", timing_style))
    story.append(Paragraph("0:46 &nbsp; Nyɛɛ pee Ní Peemi 3.3 (Create Backup). (Tsɔɔlɔ ɔ tsɔɔ níhi nɛ a ngmaa kɛ Tags.)", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Nyagbe, Wa Maa Hyɛ Nɔ́ Nɛ Wa Kase ɔ Ekohu, Kɛ Sane Bimihi: (0:50 - 1:00)</b>", section_hdr))
    story.append(Paragraph("0:50 &nbsp; Hɛngm. 10 kɛ ha nɔ́ nɛ a kase ɔ hyɛmi ekohu, sane bimihi, loo be nɛ he maa hia. Klas ɔ se ɔ, a maa ye nɔ tsuaa nɔ nɛ ngɛ yemi kɛ buami hlae ɔ bua hɛngm. 15 (ke o suɔ).", timing_style))
    story.append(Spacer(1, 2))

    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=2))
    story.append(Paragraph("<b>NÍ PEEMIHI</b>", ex_hdr))

    story.append(Paragraph("<b>1.1</b> Moo nyɛ <b>Daily Text</b> (Daa Ligbi Ngmami; hulu okadi) nɔ. Moo nyɛ <b>Text Settings</b> (<b>A A</b>) okadi nɛ ngɛ yiti je ɔ nɔ, nɛ o gbla kpɔ ɔ kɛ ya hɛ mi konɛ ningma amɛ nɛ hi agbo.", ex_style))
    story.append(Paragraph("<b>1.2</b> Moo nyɛ <b>Bible</b> (Baiblo) nɔ. Hla Baiblo womi ko (kaa nɔ́ hyɛmi nɔ́ ɔ, <i>Mateo</i>) kɛ yi ko (kaa nɔ́ hyɛmi nɔ́ ɔ, <i>5</i>) nɛ o kane.", ex_style))
    story.append(Paragraph("<b>1.3</b> Moo nyɛ <b>Meetings</b> (Asafo Mi Kpehi) nɔ. Moo nyɛ otsi nɛ ɔ <i>Hwɔɔmi Mɔ</i> Ní Kasemi munyu ɔ nɔ si kake konɛ e bli amlɔ nɛ ɔ.", ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>2.1</b> Hyɛ kaa o fon, o tablɛti, loo o kɔmpiuta a ngɛ Wi-Fi ɔ nɔ lo, konɛ o mobail data a ko puɛ.", ex_style))
    story.append(Paragraph("<b>2.2</b> Ngɛ Publications loo Meetings mi ɔ, moo nyɛ <b>okadi nɛ ngɛ kaa bɔku ɔ</b> nɔ ngɛ nɔ́ ko nɛ o kɛ kaseɔ ní ɔ he, konɛ o gbla nɛ o kɛ tsu ní ke intanɛti be.", ex_style))
    story.append(Paragraph("<b>2.3</b> Bli Baiblo yi ko. Moo nyɛ <b>Headphones</b> nɔ nɛ o bu tue; ngɔɔ <b>Volume Down</b> (loo Mute) kɛ ha gbi ɔ nɛ kpa.", ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>3.1</b> Ngɛ <i>Hwɔɔmi Mɔ</i> Ní Kasemi munyu ɔ kuku 1 ɔ mi ɔ, o kɛ o nine nɛ pi heto ɔ nɔ nɛ o ngɔ o nine kɛ pi nɔ bɔɔ, nɛ o nyɛ <b>yɛlo</b> nɔ.", ex_style))
    story.append(Paragraph("<b>3.2</b> Moo nyɛ munyu nɛ o kɛ kɔla kadi ɔ nɔ ekohu konɛ o tsake kɔla a (bluu loo grin), loo moo nyɛ Delete okadi ɔ nɔ konɛ o je.", ex_style))
    story.append(Paragraph("<b>3.3</b> Bli Settings &gt; Backup and Restore, nɛ o nyɛ <b>Create Backup</b> nɔ konɛ o ngɔ o níhi ɔmɛ kɛ to.", ex_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<i>Mlaa He Sanehi: JW Library ji Watch Tower Bible and Tract Society of Pennsylvania okadi nɛ a kɛ wo mlaa sisi. Klas ɔ he blɔ nya tomi nɛ ɔ ji ní tsumi nɛ da e he nɛ pi jua yemi ní tsumi, nɛ e kɛ Watch Tower loo Yehowa Odasefohi be weku ko, nɛ a kplɛɛ we nɔ. English: JW Library is a registered trademark of Watch Tower Bible and Tract Society of Pennsylvania. Independent, non-commercial training outline; not affiliated with or endorsed by Watch Tower or Jehovah's Witnesses.</i>", disclaimer_style))

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


    # ---- Dangme: Curriculum (4 pages) ----
    story = []

    # ==================== BF. 1 ====================
    story.append(Paragraph("JW Library Ní Kasemihi ɔ He Blɔ Nya Tomi", doc_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph(DRAFT_LINE, note_style))
    story.append(Paragraph("<b>KAI:</b> Blɔ tsɔɔmihi nɛ je asafo ɔ ngɔ ngɛ bɔ nɛ a kɛ JW Library tsuɔ ní ha a he ngɛ JW.ORG nɔ (https://www.jw.org/ada/intanɛti-nɔ-yemi-kɛ-buami/jw-library/ kɛ https://www.jw.org/en/online-help/jw-library/)", note_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Ní Kasemihi Nɛ ɔmɛ A He Sanehi", h1_style))
    story.append(Paragraph(
        "Blɔ nya tomi nɛ ɔ ji kɛ ha nɔ tsuaa nɔ nɛ tsɔɔ loo e nyɛɛɔ ní kaseli a hɛ ngɛ "
        "<i>Ngɔɔ JW Library ɔ Kɛ Tsu Ní</i> ní kasemi womi ɔ mi. Ní kasemihi etɛ ngɛ mi, nɛ eko tsuaa eko yeɔ hɛngm. 15: "
        "<b>Bɔ Nɛ O Maa Na Ngmami Ɔmɛ Kɛ Asafo Mi Kpehi A Níhi Ha</b>, <b>Níhi Nɛ A Gblaa Kɛ Bɔ Nɛ A Kɛ Tsuɔ Ní Ha</b>, kɛ <b>Níhi Nɛ O Ma Nyɛ Maa Kɛ Tsu Ní Ngɛ Dɛ He Ní Kasemi Mi</b>. "
        "A to hɛngm. 10 kɛ ha nyagbe, konɛ tsɔɔli ko ngmɛ fo. "
        "Loko klas ɔ maa je sisi ɔ, e sa kaa a ha ní kaseli ɔmɛ ní kasemi womi ɔ eko, nɛ a kai mɛ "
        "konɛ a ngɔ app ɔ kɛ wo a fon, a tablɛti, loo a kɔmpiuta a nɔ momo.",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "O ma nyɛ maa ngɔ <i>JW Library Klas ɔ He Blɔ Nya Tomi</i> ɔ kɛ tsu ní ke o ngɛ klas ɔ he blɔ nya tue. A to hɛngm. enuɔ "
        "kɛ ha sisije ɔ konɛ ní kaseli ɔmɛ nɛ na bɔ nɛ a to a fon, a tablɛti, loo a kɔmpiuta a he blɔ nya ha. Ngɛ ní kasemi tsuaa ní kasemi nɛ yeɔ hɛngm. 15 ɔ mi ɔ, "
        "ní kaseli ɔmɛ peeɔ ní peemihi etɛ, nɛ tsɔɔlɔ ɔ tsɔɔ níhi nɛ a wa a ngɛ be kuku mi. Klas ɔ tsuo yeɔ "
        "hɛngm. 60, nɛ a ma nyɛ maa pee hɛngm. 75 loo 90 ke kuu ɔ ngɛ yemi kɛ buami babauu hlae.",
        body_style
    ))

    story.append(Paragraph("Nihi Nɛ A Pee Kɛ Ha", h1_style))
    story.append(Paragraph(
        "A pee ní kasemihi nɛ ɔmɛ kɛ ha nihi nɛ a le bɔ nɛ a kɛ fon, tablɛti, loo kɔmpiuta tsuɔ ní ha bɔɔ. "
        "E sa kaa ní kaseli ɔmɛ nɛ nyɛ nɛ a nyɛ skrin ɔ nɔ, loo a ngɔ maus kɛ tsu ní. Ke nɔ ko kɛ JW Library app ɔ tsu ní momo ɔ, "
        "e yeɔ bua, se e he hia we.",
        body_style
    ))

    story.append(Paragraph("Nɔ́ Nɛ Ní Kaseli ɔmɛ Ma Nyɛ Maa Pee", h1_style))
    story.append(Paragraph("Ke a gbe ní kasemihi nɛ ɔmɛ a nya a, ní kaseli ɔmɛ ma nyɛ maa:", body_style))
    story.append(Paragraph("&bull; Ya Bible, Publications, Meetings, kɛ Personal Study fãhi ɔmɛ a nɔ.", bullet_style))
    story.append(Paragraph("&bull; Bli Daa Ligbi Ngmami ɔ, nɛ a ngɔ A A okadi ɔ kɛ ha ningma amɛ nɛ hi agbo.", bullet_style))
    story.append(Paragraph("&bull; Na munyuhi nɛ a kaseɔ ngɛ asafo mi kpehi daa otsi ɔ ngɛ Meetings fã ɔ nɔ amlɔ nɛ ɔ.", bullet_style))
    story.append(Paragraph("&bull; Le bɔ nɛ a kaneɔ ní ha ke intanɛti be, nɛ a gbla womihi ngɛ Wi-Fi nɔ konɛ mobail data a ko puɛ.", bullet_style))
    story.append(Paragraph("&bull; Bu munyuhi nɛ a buɔ tue ɔ tue (headphones okadi), nɛ a ha gbi nɛ a hyɛ we blɔ ɔ nɛ kpa amlɔ nɛ ɔ.", bullet_style))
    story.append(Paragraph("&bull; Ngɔ kɔlahi slɔɔtohi kɛ kadi hetohi ngɛ munyuhi nɛ a kaseɔ ɔ a mi, nɛ a je kɔla a.", bullet_style))
    story.append(Paragraph("&bull; Pee backup (.jwlibrary) konɛ níhi nɛ a kase ɔ ko laa.", bullet_style))

    story.append(Paragraph("Níhi Nɛ E Sa Kaa A Pee Loko Klas ɔ Maa Je Sisi", h1_style))
    story.append(Paragraph("Loko ní kaseli ɔmɛ maa ba klas ɔ, e sa kaa:", body_style))
    story.append(Paragraph("&bull; A ba <b>hɛngm. 10–15 loko klas ɔ maa je sisi</b> konɛ nihi nɛ yeɔ bua a nɛ ye a bua ngɛ Wi-Fi kɛ Baiblo ɔ/Daa Ligbi Ngmami ɔ he.", bullet_style))
    story.append(Paragraph("&bull; A fon, a tablɛti, loo a kɔmpiuta a ji <b>Android 8.0+</b>, <b>iOS 15.0+</b>, <b>macOS 13+ (M1+)</b>, loo <b>Windows 10 v2004+</b>.", bullet_style))
    story.append(Paragraph("&bull; Batri ɔ <b>nɛ ye</b> loko a maa ba (loo a ngɔ a chaaja kɛ ba).", bullet_style))
    story.append(Paragraph("&bull; A tsake <b>be nɛ skrin ɔ gbeɔ ɔ kɛ ya hɛngm. 2 loo 5</b> konɛ skrin ɔ ko gbe.", bullet_style))
    story.append(Paragraph("&bull; Blɔ nɛ se <b>GB 2 kɛ ya si 4</b> nɛ hi a klama a nɔ (loo SD card) kɛ ha videohi kɛ munyuhi nɛ a buɔ tue.", bullet_style))
    story.append(Paragraph("&bull; A ya Wi-Fi nɔ loko a maa gbla videohi loo munyuhi nɛ a buɔ tue.", bullet_style))

    # ==================== BF. 2 ====================
    story.append(PageBreak())

    story.append(Paragraph("JW Library Ní Kasemihi ɔ He Blɔ Nya Tomi", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Ní Kasemi 1: Bɔ Nɛ O Maa Na Ngmami Ɔmɛ Kɛ Asafo Mi Kpehi A Níhi Ha (Hɛngm. 15)", h1_style))
    story.append(Paragraph(
        "Ní kasemi nɛ ɔ tsɔɔ ní kaseli ɔmɛ bɔ nɛ a maa ya JW Library app ɔ fãhi ɔmɛ a nɔ ha. "
        "E sa kaa tsɔɔli nɛ tsɔɔ he nɛ navigation bar ɔ ngɛ ngɛ fon, tablɛti, loo kɔmpiuta nɛ nihi ɔmɛ hɛɛ ɔ nɔ (sisi ngɛ iOS "
        "kɛ Android nɛ ngɛ amlɔ nɛ ɔ nɔ; yiti je ngɛ Windows nɔ). Tsɔɔ bɔ nɛ ke a nyɛ <b>A A</b> okadi ɔ nɔ ɔ, ningma amɛ hiɔ agbo konɛ a kane ha, "
        "kɛ bɔ nɛ <b>Meetings fã</b> ɔ haa nɛ a naa asafo mi kpehi daa otsi ɔ a womihi amlɔ nɛ ɔ ha.",
        body_style
    ))

    story.append(Paragraph("Sanehi Nɛ A Maa Susu He (hɛngm. 10)", h2_style))
    story.append(Paragraph("&bull; Fãhi Ɔmɛ (Bible, Publications, Meetings, Personal Study)", bullet_style))
    story.append(Paragraph("&bull; Daa Ligbi Ngmami ɔ kɛ ningma amɛ a klemi (Text Settings / A A okadi ɔ konɛ ningma amɛ nɛ hi agbo)", bullet_style))
    story.append(Paragraph("&bull; Baiblo womi ko kɛ yi ko blimi (kaa nɔ́ hyɛmi nɔ́ ɔ, Mateo 5)", bullet_style))
    story.append(Paragraph("&bull; Meetings fã ɔ (Ní Kasemi Womi kɛ ha Si Himi Kɛ Sɔmɔmi Ní Tsumi Kpe [Midweek Meeting], kɛ Hwɔɔmi Mɔ Ní Kasemi munyu kɛ ha Otsi Nyagbe Kpe [Weekend Meeting])", bullet_style))
    story.append(Paragraph("&bull; <i>Nɔ́ Nɛ Tsɔɔlɔ ɔ Maa Tsɔɔ:</i> Bookmark, History, kɛ Search (a kase ngɛ we)", bullet_style))

    story.append(Paragraph("Ní Peemihi (hɛngm. 5)", h2_style))
    story.append(Paragraph("&bull; <b>Ní Peemi 1.1:</b> Bli Daa Ligbi Ngmami ɔ, nɛ o nyɛ <b>Text Settings</b> (<b>A A</b>) nɔ konɛ ningma amɛ nɛ hi agbo nɛ a pee faa.", bullet_style))
    story.append(Paragraph("&bull; <b>Ní Peemi 1.2:</b> Moo nyɛ Bible nɔ, hla Baiblo womi ko (Mateo), nɛ o bli yi 5.", bullet_style))
    story.append(Paragraph("&bull; <b>Ní Peemi 1.3:</b> Bli Meetings fã ɔ, nɛ o nyɛ otsi nɛ ɔ Hwɔɔmi Mɔ Ní Kasemi munyu ɔ nɔ.", bullet_style))

    story.append(Paragraph("Ga Womihi Kɛ Ha Klas ɔ Hɛ Nyɛɛlɔ Ngɛ Ní Kasemi 1 ɔ He", h2_style))
    story.append(Paragraph(
        "To blɔ nya konɛ nihi nɛ yeɔ bua a nɛ ye nihi nɛ ba ngɛ be mi ɔ a bua hɛngm. 15 loko klas ɔ maa je sisi, konɛ a hyɛ kaa nɔ tsuaa nɔ gbla Baiblo ɔ kɛ Daa Ligbi Ngmami ɔ momo lo. Ngɛ klas ɔ sisije ɔ, "
        "hyɛ ngɛ sɛkɛnd 30 mi: bi ní kaseli ɔmɛ nɛ a wo a nine nɔ ke a ngɛ yemi kɛ buami hlae konɛ a gbla nɔ́ ko, konɛ nihi nɛ yeɔ bua a nɛ ye a bua blɛuu "
        "be nɛ o ngɛ nɔ yae ɔ. Tsɔɔ bɔ nɛ a haa gbi nɛ kpa ha ngɛ sisije ɔ (Volume Down nɛ ngɛ fon ɔ he; Mute ngɛ kɔmpiuta kiibɔd ɔ nɔ) "
        "konɛ a ko ye gbeye. Nihi nɛ yeɔ bua a nɛ hyɛ kaa ní kaseli ɔmɛ nyɛ nɛ a ngɔ A A okadi ɔ kɛ ha ningma amɛ hi agbo lo.",
        body_style
    ))

    story.append(Paragraph("Ke a gbe ní kasemi nɛ ɔ nya a, ní kaseli ɔmɛ ma nyɛ maa:", h2_style))
    story.append(Paragraph("&bull; Ya app ɔ fãhi ɔmɛ tsuo a nɔ.", bullet_style))
    story.append(Paragraph("&bull; Ha ningma amɛ nɛ hi agbo ngɛ app ɔ tsuo mi konɛ a kane ha.", bullet_style))
    story.append(Paragraph("&bull; Bli Baiblo yi tsuaa yi, nɛ a na asafo mi kpehi daa otsi ɔ a sanehi amlɔ nɛ ɔ.", bullet_style))

    # ==================== BF. 3 ====================
    story.append(PageBreak())

    story.append(Paragraph("JW Library Ní Kasemihi ɔ He Blɔ Nya Tomi", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Ní Kasemi 2: Níhi Nɛ A Gblaa Kɛ Bɔ Nɛ A Kɛ Tsuɔ Ní Ha (Hɛngm. 15)", h1_style))
    story.append(Paragraph(
        "Ní kasemi nɛ ɔ tsɔɔ bɔ nɛ a kaneɔ ní ha ke intanɛti be, nɛ e tsɔɔ bɔ nɛ a gblaa womihi, videohi, kɛ munyuhi nɛ a buɔ tue ha. "
        "Ha nɛ a na kaa ke a gbla nɔ́ ko ngɛ Wi-Fi nɔ ɔ, e hiɔ fon, tablɛti, loo kɔmpiuta a nɔ, nɛ e he hia we intanɛti "
        "loo mobail data ngɛ asafo mi kpehi a sisi. Tsɔɔ munyuhi nɛ a buɔ tue ɔ (headphones okadi) konɛ ní kaseli ɔmɛ nɛ nyɛ nɛ a bu nɔ́ nɛ a ngɛ kanee ɔ tue.",
        body_style
    ))

    story.append(Paragraph("Sanehi Nɛ A Maa Susu He (hɛngm. 10)", h2_style))
    story.append(Paragraph("&bull; Bɔ nɛ a kaneɔ ní kɛ a buɔ tue ha ke intanɛti be", bullet_style))
    story.append(Paragraph("&bull; Wi-Fi nɔ yami loko a maa gbla konɛ mobail data a ko puɛ", bullet_style))
    story.append(Paragraph("&bull; Womihi, videohi, kɛ munyuhi nɛ a buɔ tue gblami (okadi nɛ ngɛ kaa bɔku ɔ)", bullet_style))
    story.append(Paragraph("&bull; Munyuhi nɛ a buɔ tue kɛ bɔ nɛ a haa gbi nɛ kpa ha amlɔ nɛ ɔ (Volume Down ngɛ fon nɔ; Mute ngɛ kɔmpiuta nɔ)", bullet_style))
    story.append(Paragraph("&bull; <i>Nɔ́ Nɛ Tsɔɔlɔ ɔ Maa Tsɔɔ:</i> Bɔ nɛ a toɔ níhi a nya kɛ Largest Size ha konɛ a hyɛ blɔ nɛ ngɛ nɔ, nɛ a je níhi", bullet_style))

    story.append(Paragraph("Ní Peemihi (hɛngm. 5)", h2_style))
    story.append(Paragraph("&bull; <b>Ní Peemi 2.1:</b> Hyɛ skrin ɔ yiti je ɔ konɛ o na kaa fon, tablɛti, loo kɔmpiuta a ngɛ Wi-Fi ɔ nɔ.", bullet_style))
    story.append(Paragraph("&bull; <b>Ní Peemi 2.2:</b> Moo nyɛ okadi nɛ ngɛ kaa bɔku ɔ nɔ ngɛ womi loo video ko he konɛ o gbla.", bullet_style))
    story.append(Paragraph("&bull; <b>Ní Peemi 2.3:</b> Bli Baiblo yi ko, moo nyɛ Headphones nɔ nɛ o bu tue; ngɔɔ Volume Down loo Mute kɛ ha gbi ɔ nɛ kpa.", bullet_style))

    story.append(Paragraph("Ga Womihi Kɛ Ha Klas ɔ Hɛ Nyɛɛlɔ Ngɛ Ní Kasemi 2 ɔ He", h2_style))
    story.append(Paragraph(
        "Ha ní kaseli nɛ a mobail data be babauu ɔ nɛ na kaa ke a gbla níhi ngɛ Wi-Fi nɔ momo ɔ, a mobail data a puɛ we ngɛ asafo mi kpehi a sisi. "
        "Nyɛ ko kpa bɔ nɛ a haa gbi nɛ kpa ha a tsɔɔmi: nihi nɛ a le fon he ní bɔɔ ɔ yeɔ gbeye kaa gbi ko maa je kpo be nɛ a hyɛ we blɔ; "
        "ke a le bɔ nɛ a maa ha gbi ɔ nɛ kpa ha amlɔ nɛ ɔ (Volume Down nɛ ngɛ fon ɔ he, loo Mute ngɛ kɔmpiuta nɔ) ɔ, a tue mi jɔɔ.",
        body_style
    ))

    story.append(Paragraph("Ke a gbe ní kasemi nɛ ɔ nya a, ní kaseli ɔmɛ ma nyɛ maa:", h2_style))
    story.append(Paragraph("&bull; Gbla womihi ngɛ Wi-Fi nɔ nɛ a mobail data a ko puɛ.", bullet_style))
    story.append(Paragraph("&bull; Bli womihi nɛ a gbla a nɛ a kane ngɛ asafo mi kpehi a sisi ke intanɛti be.", bullet_style))
    story.append(Paragraph("&bull; Bu ngmami ɔmɛ kɛ munyuhi nɛ a kaneɔ ɔ tue, a tsi (Pause), nɛ a ha gbi ɔ nɛ kpa amlɔ nɛ ɔ.", bullet_style))

    # ==================== BF. 4 ====================
    story.append(PageBreak())

    story.append(Paragraph("JW Library Ní Kasemihi ɔ He Blɔ Nya Tomi", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Ní Kasemi 3: Níhi Nɛ O Ma Nyɛ Maa Kɛ Tsu Ní Ngɛ Dɛ He Ní Kasemi Mi (Hɛngm. 15)", h1_style))
    story.append(Paragraph(
        "Ní kasemi nɛ ɔ tsɔɔ bɔ nɛ a ngɔɔ kɔla kɛ kadiɔ hetohi ngɛ munyuhi nɛ a kaseɔ kɛ ha asafo mi kpehi ɔ a mi ha, kɛ bɔ nɛ a poɔ dɛ he ní kasemi he níhi a he piɛ ha. "
        "Tsɔɔ bɔ nɛ a ngɔɔ yɛlo kɔla kɛ kadiɔ munyuhi ha, bɔ nɛ a tsakeɔ kɔla a ha, kɛ bɔ nɛ a jeɔ ha. "
        "Ngɔɔ nyagbe ɔ kɛ tsɔɔ bɔ nɛ a peeɔ <code>.jwlibrary</code> backup ngɛ Settings mi ha, "
        "konɛ níhi nɛ ní kaseli ɔmɛ kadi ngɛ a dɛ he ní kasemi mi ɔ ko laa.",
        body_style
    ))

    story.append(Paragraph("Sanehi Nɛ A Maa Susu He (hɛngm. 10)", h2_style))
    story.append(Paragraph("&bull; Bɔ nɛ a kɛ nine piɔ munyungu nɔ, nɛ a ngɔɔ nine kɛ piɔ nɔ bɔɔ kɛ kadiɔ ha", bullet_style))
    story.append(Paragraph("&bull; Kɔlahi hlami (yɛlo, bluu, grin)", bullet_style))
    story.append(Paragraph("&bull; Bɔ nɛ a nyɛɛ munyu nɛ a kɛ kɔla kadi ɔ nɔ kɛ tsakeɔ kɔla a ha, loo a ngɔɔ Delete okadi ɔ kɛ jeɔ", bullet_style))
    story.append(Paragraph("&bull; <b>Bɔ Nɛ A Poɔ O Níhi A He Piɛ Ha:</b> Backup peemi (Settings &gt; Backup and Restore)", bullet_style))
    story.append(Paragraph("&bull; <i>Nɔ́ Nɛ Tsɔɔlɔ ɔ Maa Tsɔɔ:</i> Níhi nɛ a ngmaa kɛ piɛɛ he, Tags, kɛ Personal Study fã ɔ", bullet_style))

    story.append(Paragraph("Ní Peemihi (hɛngm. 5)", h2_style))
    story.append(Paragraph("&bull; <b>Ní Peemi 3.1:</b> Bli Hwɔɔmi Mɔ Ní Kasemi munyu nɛ maa ba a, nɛ o ngɔ yɛlo kɔla kɛ kadi heto nɛ ngɛ kuku 1 ɔ mi.", bullet_style))
    story.append(Paragraph("&bull; <b>Ní Peemi 3.2:</b> Moo nyɛ heto nɛ o kɛ kɔla kadi ɔ nɔ konɛ o tsake kɛ ya bluu, loo moo nyɛ Delete okadi ɔ nɔ konɛ o je.", bullet_style))
    story.append(Paragraph("&bull; <b>Ní Peemi 3.3:</b> Bli Settings &gt; Backup and Restore, nɛ o nyɛ <b>Create Backup</b> nɔ.", bullet_style))

    story.append(Paragraph("Nyagbe Kɛ Ga Womihi Kɛ Ha Klas ɔ Hɛ Nyɛɛlɔ (0:50 - 1:00)", h2_style))
    story.append(Paragraph(
        "• <b>Yemi Kɛ Buami Loko Klas ɔ Maa Je Sisi:</b> Ke a bli agbo ɔmɛ hɛngm. 15 loko klas ɔ maa je sisi konɛ nihi nɛ yeɔ bua a nɛ ye bua ɔ, nihi tsuo hlaa we Wi-Fi be kake. Ke ní kaselɔ ko ngɛ womihi hlae ngɛ gbi kpa ko mi ɔ, moo nyɛ <b>Languages</b> okadi ɔ (Gbi) nɔ, nɛ o hla gbi ɔ.<br/>"
        "• <b>Bɔ Nɛ A Haa Gbi Nɛ Kpa Ha:</b> Ke a tsɔɔ ní kaseli ɔmɛ Volume Down ɔ ngɛ sisije ɔ, a yeɔ we gbeye kaa gbi ko maa je kpo.<br/>"
        "• <b>Nyagbe Hɛngm. 10 ɔ:</b> Ngɔɔ hɛngm. nɛ ɔmɛ kɛ tsu ní kɛ hyɛ nɔ́ nɛ a kase ɔ ekohu, kɛ ha sane bimihi a heto, loo ke ní peemi ko he be pe bɔ nɛ a hyɛ blɔ ɔ.<br/>"
        "• <b>Nihi Nɛ Yeɔ Bua Nɛ A Ngɛ Okplɔ Ɔmɛ A He:</b> Ke nihi 1 loo 2 nyɛɛɔ tsu ɔ mi kɛ yeɔ nihi a bua ɔ, klas ɔ daa we si.<br/>"
        "• <b>Womihi Nɛ A Printi (Ke E He Maa Hia):</b> Ke a ngɔ Klas ɔ He Blɔ Nya Tomi nɛ ngɛ bf. kake nɔ ɔ kɛ to okplɔ ɔmɛ a nɔ ɔ, e yeɔ bua he nɛ data loo Wi-Fi be babauu.<br/>"
        "• <b>QR Okadihi Ngɛ Okplɔ Ɔmɛ A Nɔ / Skrin ɔ Nɔ (Ke O Suɔ):</b> Ke a je QR okadi ɔ kpo ngɛ skrin ɔ nɔ loo a ngɔ QR womi nyafii kɛ to okplɔ ɔmɛ a nɔ ɔ, ní kaseli ɔmɛ ma nyɛ maa ngɔ a fon kamera a kɛ bli ní kasemi womi nɛ ɔ.<br/>"
        "• <b>Add to Home Screen (Ke O Suɔ):</b> Ke o tsɔɔ ní kaseli ɔmɛ \"Add to Home Screen\" ɔ, ní kasemi womi nɛ ɔ maa hi a fon ɔ nɔ, nɛ a ma nyɛ maa kane ke intanɛti be po ɔ.<br/>"
        "• <b>Yemi Kɛ Buami Ngɛ Klas ɔ Se:</b> Hi jamɛ a he hɛngm. 15 ngɛ klas ɔ se kɛ ha nɔ tsuaa nɔ nɛ ngɛ yemi kɛ buami hlae ngɛ e backup ɔ he.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Ke a gbe ní kasemi nɛ ɔ nya a, ní kaseli ɔmɛ ma nyɛ maa:", h2_style))
    story.append(Paragraph("&bull; Ngɔ kɔla kɛ kadi hetohi kɛ ha asafo mi kpehi, nɛ a tsake kɔla a loo a je.", bullet_style))
    story.append(Paragraph("&bull; Ngɔ níhi nɛ a ngma kɛ níhi nɛ a kɛ kɔla kadi ɔ kɛ wo .jwlibrary backup mi konɛ a ko laa.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)


if __name__ == '__main__':
    repo_root = os.path.normpath(os.path.join(_HERE, '..', '..'))
    program_pdf = os.path.join(repo_root, 'JW Library Class Program (Dangme).pdf')
    curriculum_pdf = os.path.join(repo_root, 'JW Library Tutorial Curriculum (Dangme).pdf')

    build_class_program(program_pdf)
    build_curriculum(curriculum_pdf)

    r1 = pypdf.PdfReader(program_pdf)
    r2 = pypdf.PdfReader(curriculum_pdf)
    print(f'Class Program PDF ({len(r1.pages)} page(s)): {program_pdf}')
    print(f'Curriculum PDF ({len(r2.pages)} page(s)): {curriculum_pdf}')
