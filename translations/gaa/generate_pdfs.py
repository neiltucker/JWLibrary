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

# Ga version (draft, not yet reviewed). It makes the Ga PDFs under their own
# file names, so the English, Kiswahili, Luganda and Dinka PDFs are not overwritten.
# The PDFs are written to the repository root (two folders up from this script).

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Unicode font setup.
# The built-in Helvetica font cannot print the Ga letters ɛ, ɔ and ŋ.
# This looks for a TrueType font that contains them and uses it instead.
# To guarantee correct output on any computer, put the four DejaVu Sans files
# (DejaVuSans.ttf, DejaVuSans-Bold.ttf, DejaVuSans-Oblique.ttf,
# DejaVuSans-BoldOblique.ttf) in a folder named "fonts" next to this script.
# ---------------------------------------------------------------------------
REQUIRED_CHARS = "ɛɔŋƐƆŊ"

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

# Numbered canvas for the curriculum: "Baafa X / Y" (page X of Y)
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
        self.drawRightString(letter[0] - 45, letter[1] - 30, f"Baafa {self._pageNumber} / {page_count}")
        # Legal line at the bottom of every page
        disclaimer = "JW Library ji Watch Tower Bible and Tract Society of Pennsylvania kadimɔnɔ ni akɛwo mla shishi. Nitsumɔ ni yɔɔ ehe."
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


    # ---- Ga: Class Program (1 page) ----
    story = []

    story.append(Paragraph("JW LIBRARY KLAS LƐ HE GBƐJIANƆTOO", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>KADIMƆ:</b> Gbɛtsɔɔmɔi ni jɛ asafo lɛ ŋɔɔ yɛ bɔ ni akɛ JW Library tsuɔ nii lɛ he yɛ JW.ORG nɔ (https://www.jw.org/gaa/sait-lɛ-nɔ-yelikɛbuamɔ/jw-library/ kɛ https://www.jw.org/en/online-help/jw-library/)", note_style))
    story.append(Paragraph("Klas ni baaye miniti 60: nikasemɔi etɛ, ni eko fɛɛ eko baaye miniti 15, kɛ miniti 10 kɛhã naagbee. (Abaanyɛ afee lɛ miniti 75-90.)", note_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=3))

    story.append(Paragraph("<b>Shishijee: (0:00 - 0:05)</b>", section_hdr))
    story.append(Paragraph("0:00 &nbsp; Ojekoo; akwɛ akɛ mɔ fɛɛ mɔ edaunlodi Biblia lɛ kɛ Daa Gbi Ŋmalɛ Lɛ lo (yelikɛbualɔi yeɔ amɛbuaa mɛi ni esa akɛ amɛdaunlodi).", timing_style))
    story.append(Paragraph("0:02 &nbsp; Ŋaawoo kɛhã bɔ ni akɛhãa gbee sɛɛ foɔ: nyɛɛ Volume Down nɔ ni oshi onine yɛ nɔ (foŋ), loo nyɛɛ Mute (kɔmpiuta); kwɛmɔ he ni kpɔ ni fãi titrii lɛ yɔɔ nɔ lɛ yɔɔ.", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Nikasemɔ 1: Bɔ Ni Obaafee Ona Ŋmalɛi Kɛ Asafoŋ Kpeei Anibii (0:05 - 0:20)</b>", section_hdr))
    story.append(Paragraph("0:05 &nbsp; Asusu fãi titrii lɛ ahe (Bible, Publications, Meetings, Personal Study).", timing_style))
    story.append(Paragraph("0:07 &nbsp; Agbele Daa Gbi Ŋmalɛ Lɛ, ni anyɛ <b>Text Settings</b> (<b>A A</b>) okadi lɛ nɔ koni niŋmai lɛ adara.", timing_style))
    story.append(Paragraph("0:10 &nbsp; Afee Nifeemɔ 1.1 (Daa Gbi Ŋmalɛ Lɛ kɛ niŋmai lɛ adaramɔ).", timing_style))
    story.append(Paragraph("0:12 &nbsp; Agbele Biblia wolo ko kɛ yitso ko; afee Nifeemɔ 1.2.", timing_style))
    story.append(Paragraph("0:15 &nbsp; Asusu Meetings fã lɛ he (Kpee Nifeemɔ Wolo kɛhã Otsi Teŋ Kpee [Midweek Meeting], kɛ Buu-Mɔɔ Nikasemɔ kɛhã Otsi Naagbee Kpee [Weekend Meeting]).", timing_style))
    story.append(Paragraph("0:18 &nbsp; Afee Nifeemɔ 1.3 (Meetings). (Tsɔɔlɔ lɛ tsɔɔ Bookmark kɛ Search.)", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Nikasemɔ 2: Nibii Ni Adaunlodiɔ Kɛ Bɔ Ni Akɛtsuɔ Nii (0:20 - 0:35)</b>", section_hdr))
    story.append(Paragraph("0:20 &nbsp; Nibii ni odaunlodi be ni oyɛ Wi-Fi lɛ nɔ lɛ hiɔ ofoŋ lɛ nɔ; ehe ehiaaa mobail data kɛ́ ookɛtsu nii.", timing_style))
    story.append(Paragraph("0:22 &nbsp; Afee Nifeemɔ 2.1 (Wi-Fi lɛ kwɛmɔ koni akafite mobail data).", timing_style))
    story.append(Paragraph("0:24 &nbsp; Adaunlodi nɔ ko koni akane loo akwɛ kɛ́ Intanɛt bɛ; afee Nifeemɔ 2.2.", timing_style))
    story.append(Paragraph("0:28 &nbsp; Nibii ni atswaa aboɔ toi (headphones okadi); bɔ ni akɛhãa gbee sɛɛ foɔ oya nɔŋŋ kɛtsɔ Volume Down (foŋ) loo Mute (kɔmpiuta) nɔ.", timing_style))
    story.append(Paragraph("0:31 &nbsp; Afee Nifeemɔ 2.3 (Bo toi). (Tsɔɔlɔ lɛ tsɔɔ bɔ ni akwɛɔ gbɛ ni yɔɔ ofoŋ lɛ nɔ.)", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Nikasemɔ 3: Nibii Ni Obaanyɛ Okɛtsu Nii Yɛ Aŋkro Nikasemɔ Mli (0:35 - 0:50)</b>", section_hdr))
    story.append(Paragraph("0:35 &nbsp; Bɔ ni akɛ kɔla kadiɔ hetoi yɛ saji ni akaseɔ lɛ amli.", timing_style))
    story.append(Paragraph("0:37 &nbsp; Afee Nifeemɔ 3.1 (Okɛ yɛlo kɔla akadi hetoo ko).", timing_style))
    story.append(Paragraph("0:40 &nbsp; Bɔ ni atsakeɔ kɔla lɛ loo ajieɔ; afee Nifeemɔ 3.2.", timing_style))
    story.append(Paragraph("0:43 &nbsp; Bɔ ni abuɔ onibii lɛ ahe: backup (.jwlibrary) feemɔ yɛ Settings &gt; Backup and Restore.", timing_style))
    story.append(Paragraph("0:46 &nbsp; Afee Nifeemɔ 3.3 (Create Backup). (Tsɔɔlɔ lɛ tsɔɔ nibii ni aŋmalaa kɛ Tags.)", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Naagbee, Nɔ Ni Wɔkase Lɛ Akwɛ Ekoŋŋ, Kɛ Sanebimɔi: (0:50 - 1:00)</b>", section_hdr))
    story.append(Paragraph("0:50 &nbsp; Miniti 10 kɛhã nɔ ni akase lɛ kwɛmɔ ekoŋŋ, sanebimɔi, loo be ni he baahia. Klas lɛ sɛɛ lɛ, abaaye abua mɔ fɛɛ mɔ ni miitao yelikɛbuamɔ pɔtɛɛ miniti 15 (kɛ́ osumɔ).", timing_style))
    story.append(Spacer(1, 2))

    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=2))
    story.append(Paragraph("<b>NIFEEMƆI</b>", ex_hdr))

    story.append(Paragraph("<b>1.1</b> Nyɛɛ <b>Daily Text</b> (Daa Gbi Ŋmalɛ Lɛ; hulu okadi) nɔ. Nyɛɛ <b>Text Settings</b> (<b>A A</b>) okadi ni yɔɔ ŋwɛigbɛ lɛ nɔ, ni otsi kpɔ lɛ kɛya hiɛ koni niŋmai lɛ adara.", ex_style))
    story.append(Paragraph("<b>1.2</b> Nyɛɛ <b>Bible</b> (Biblia) nɔ. Halamɔ Biblia wolo ko (akɛ nɔkwɛmɔnɔ lɛ, <i>Mateo</i>) kɛ yitso ko (akɛ nɔkwɛmɔnɔ lɛ, <i>5</i>) ni okane.", ex_style))
    story.append(Paragraph("<b>1.3</b> Nyɛɛ <b>Meetings</b> (Asafoŋ Kpeei) nɔ. Nyɛɛ otsi nɛɛ <i>Buu-Mɔɔ</i> Nikasemɔ sane lɛ nɔ shii kome koni egbele oya nɔŋŋ.", ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>2.1</b> Kwɛmɔ akɛ ofoŋ, otablɛt, loo okɔmpiuta lɛ yɛ Wi-Fi lɛ nɔ lo, koni okafite omobail data.", ex_style))
    story.append(Paragraph("<b>2.2</b> Yɛ Publications loo Meetings mli lɛ, nyɛɛ <b>atatu okadi</b> lɛ nɔ yɛ nɔ ko ni okɛkaseɔ nii lɛ he, koni odaunlodi ni okɛtsu nii kɛ́ Intanɛt bɛ.", ex_style))
    story.append(Paragraph("<b>2.3</b> Gbelemɔ Daa Gbi Ŋmalɛ Lɛ loo Biblia lɛ. Nyɛɛ <b>Headphones</b> nɔ ni obo toi; okɛ <b>Volume Down</b> (loo Mute) ahã gbee lɛ sɛɛ afo.", ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>3.1</b> Yɛ <i>Buu-Mɔɔ</i> Nikasemɔ sane lɛ kuku 1 lɛ mli lɛ, nyɛɛ hetoo lɛ nɔ fioo ni ogbala onine lɛ kɛnyiɛ nɔ, ni onyɛ <b>yɛlo</b> nɔ.", ex_style))
    story.append(Paragraph("<b>3.2</b> Nyɛɛ wiemɔi ni okɛ kɔla kadi lɛ nɔ ekoŋŋ koni otsake kɔla lɛ (bluu loo grin), loo nyɛɛ Delete okadi lɛ nɔ koni ojie.", ex_style))
    story.append(Paragraph("<b>3.3</b> Gbelemɔ Settings &gt; Backup and Restore, ni onyɛ <b>Create Backup</b> nɔ koni okɛ onibii lɛ afɔ̃ shi.", ex_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<i>Mla He Saji: JW Library ji Watch Tower Bible and Tract Society of Pennsylvania kadimɔnɔ ni akɛwo mla shishi. Klas lɛ he gbɛjianɔtoo nɛɛ ji nitsumɔ ni yɔɔ ehe ni jeee jarayeli nifeemɔ, ni ekɛ Watch Tower loo Yehowa Odasefoi bɛ wekukpaa ko, ni amɛkpɛlɛɛɛ nɔ.</i>", disclaimer_style))

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


    # ---- Ga: Curriculum (4 pages) ----
    story = []

    # ==================== BAAFA 1 ====================
    story.append(Paragraph("JW Library Nikasemɔi Lɛ Ahe Gbɛjianɔtoo", doc_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>KADIMƆ:</b> Gbɛtsɔɔmɔi ni jɛ asafo lɛ ŋɔɔ yɛ bɔ ni akɛ JW Library tsuɔ nii lɛ he yɛ JW.ORG nɔ (https://www.jw.org/gaa/sait-lɛ-nɔ-yelikɛbuamɔ/jw-library/ kɛ https://www.jw.org/en/online-help/jw-library/)", note_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Nikasemɔi Nɛɛ Ahe Saji", h1_style))
    story.append(Paragraph(
        "Gbɛjianɔtoo nɛɛ ji kɛhã mɔ fɛɛ mɔ ni tsɔɔ loo nyiɛɔ nikaselɔi ahiɛ yɛ "
        "<i>Okɛ JW Library Lɛ Atsu Nii</i> kasemɔ wolo lɛ mli. Nikasemɔi etɛ yɛ mli, ni eko fɛɛ eko yeɔ miniti 15: "
        "<b>Bɔ Ni Obaafee Ona Ŋmalɛi Kɛ Asafoŋ Kpeei Anibii</b>, <b>Nibii Ni Adaunlodiɔ Kɛ Bɔ Ni Akɛtsuɔ Nii</b>, kɛ <b>Nibii Ni Obaanyɛ Okɛtsu Nii Yɛ Aŋkro Nikasemɔ Mli</b>. "
        "Akɛ miniti 10 eshwie shi kɛhã naagbee, koni tsɔɔlɔi akajo foi. "
        "Dani klas lɛ bɔi lɛ, esa akɛ ahã nikaselɔi lɛ kasemɔ wolo lɛ eko, ni akai amɛ "
        "koni amɛkɛ app lɛ awo amɛfoŋ, amɛtablɛt, loo amɛkɔmpiuta nɔ momo.",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Obaanyɛ okɛ <i>JW Library Klas Lɛ He Gbɛjianɔtoo</i> lɛ atsu nii kɛ́ ootao oto klas lɛ he gbɛjianɔ. Akɛ miniti enumɔ "
        "eto shishijee lɛ koni nikaselɔi lɛ ana bɔ ni ato amɛfoŋ, amɛtablɛt, loo amɛkɔmpiuta lɛ he gbɛjianɔ. Yɛ nikasemɔ fɛɛ nikasemɔ ni yeɔ miniti 15 lɛ mli lɛ, "
        "nikaselɔi lɛ feɔ nifeemɔi etɛ diɛŋtsɛ, ni tsɔɔlɔ lɛ tsɔɔ nibii ni wa yɛ be kukuoo mli. Klas lɛ muu fɛɛ yeɔ "
        "miniti 60, ni abaanyɛ afee lɛ miniti 75 loo 90 kɛ́ kuu lɛ miitao yelikɛbuamɔ pɔtɛɛ ni fa.",
        body_style
    ))

    story.append(Paragraph("Mɛi Ni Afee Kɛhã", h1_style))
    story.append(Paragraph(
        "Afee nikasemɔi nɛɛ kɛhã mɛi ni le bɔ ni akɛ foŋ, tablɛt, loo kɔmpiuta tsuɔ nii fioo. "
        "Esa akɛ nikaselɔi lɛ anyɛ anyɛ skrin lɛ nɔ, loo amɛkɛ maus atsu nii. Kɛ́ mɔ ko ekɛ JW Library app lɛ etsu nii momo lɛ, "
        "eeye ebua, shi ehe ehiaaa.",
        body_style
    ))

    story.append(Paragraph("Nɔ Ni Nikaselɔi Lɛ Baanyɛ Afee", h1_style))
    story.append(Paragraph("Kɛ́ amɛgbe nikasemɔi nɛɛ anaa lɛ, nikaselɔi lɛ baanyɛ:", body_style))
    story.append(Paragraph("&bull; Amɛya Bible, Publications, Meetings, kɛ Personal Study fãi lɛ anɔ mlɛo.", bullet_style))
    story.append(Paragraph("&bull; Amɛgbele Daa Gbi Ŋmalɛ Lɛ, ni amɛkɛ A A okadi lɛ ahã niŋmai lɛ adara.", bullet_style))
    story.append(Paragraph("&bull; Amɛna saji ni akaseɔ yɛ asafoŋ kpeei daa otsi lɛ yɛ Meetings fã lɛ nɔ oya nɔŋŋ.", bullet_style))
    story.append(Paragraph("&bull; Amɛnu bɔ ni akaneɔ nii kɛ́ Intanɛt bɛ shishi, ni amɛdaunlodi woji yɛ Wi-Fi nɔ koni amɛkafite mobail data.", bullet_style))
    story.append(Paragraph("&bull; Amɛbo nibii ni atswaa aboɔ toi lɛ toi (headphones okadi), ni amɛhã gbee ni amɛkpaaa gbɛ lɛ sɛɛ afo oya nɔŋŋ.", bullet_style))
    story.append(Paragraph("&bull; Amɛkɛ kɔlai srɔtoi akadi hetoi yɛ saji ni akaseɔ lɛ amli, ni amɛjie kɔla lɛ.", bullet_style))
    story.append(Paragraph("&bull; Amɛfee backup fail (.jwlibrary fail) koni nibii ni amɛkase lɛ akalaaje.", bullet_style))

    story.append(Paragraph("Nibii Ni Esa Akɛ Afee Dani Klas Lɛ Bɔi", h1_style))
    story.append(Paragraph("Dani nikaselɔi lɛ baaba klas lɛ, esa akɛ:", body_style))
    story.append(Paragraph("&bull; Amɛba <b>miniti 10–15 dani klas lɛ bɔi</b> koni yelikɛbualɔi aye amɛbua amɛ yɛ Wi-Fi kɛ Biblia lɛ/Daa Gbi Ŋmalɛ Lɛ he.", bullet_style))
    story.append(Paragraph("&bull; Amɛfoŋ, amɛtablɛt, loo amɛkɔmpiuta lɛ ji <b>Android 8.0+</b>, <b>iOS 15.0+</b>, <b>macOS M1+</b>, loo <b>Windows 10 v2004+</b>.", bullet_style))
    story.append(Paragraph("&bull; Batri lɛ <b>eyi obɔ</b> dani amɛba (loo amɛkɛ amɛchaaja aba).", bullet_style))
    story.append(Paragraph("&bull; Amɛtsake <b>be ni skrin lɛ gbeɔ lɛ kɛya miniti 2 loo 5</b> koni skrin lɛ akagbe.", bullet_style))
    story.append(Paragraph("&bull; Gbɛ ni shɛɔ <b>GB 2 kɛyashi 4</b> yɛ amɛfoŋ lɛ nɔ (loo SD card) kɛhã vidioi kɛ nibii ni atswaa aboɔ toi.", bullet_style))
    story.append(Paragraph("&bull; Amɛya Wi-Fi nɔ dani amɛdaunlodi vidioi loo nibii ni atswaa aboɔ toi.", bullet_style))

    # ==================== BAAFA 2 ====================
    story.append(PageBreak())

    story.append(Paragraph("JW Library Nikasemɔi Lɛ Ahe Gbɛjianɔtoo", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Nikasemɔ 1: Bɔ Ni Obaafee Ona Ŋmalɛi Kɛ Asafoŋ Kpeei Anibii (Miniti 15)", h1_style))
    story.append(Paragraph(
        "Nikasemɔ nɛɛ tsɔɔ nikaselɔi lɛ bɔ ni amɛaafee amɛya JW Library app lɛ fãi titrii lɛ anɔ mlɛo. "
        "Esa akɛ tsɔɔlɔi atsɔɔ he ni kpɔ ni fãi titrii lɛ yɔɔ nɔ lɛ yɔɔ yɛ foŋ, tablɛt, loo kɔmpiuta ni mɛi lɛ hiɛ lɛ nɔ (shishigbɛ yɛ iOS "
        "kɛ Android ni yɔɔ amrɔ nɛɛ lɛ nɔ; ŋwɛigbɛ yɛ Windows nɔ). Tsɔɔmɔ bɔ ni kɛ́ anyɛ <b>A A</b> okadi lɛ nɔ lɛ, niŋmai lɛ daraa koni akane mlɛo, "
        "kɛ bɔ ni <b>Meetings fã</b> lɛ hãa anaa asafoŋ kpeei daa otsi lɛ awoji oya nɔŋŋ.",
        body_style
    ))

    story.append(Paragraph("Saji Ni Abaasusu He (miniti 10)", h2_style))
    story.append(Paragraph("&bull; Fãi Titrii Lɛ (Bible, Publications, Meetings, Personal Study)", bullet_style))
    story.append(Paragraph("&bull; Daa Gbi Ŋmalɛ Lɛ kɛ niŋmai lɛ adaramɔ (Text Settings / A A okadi lɛ koni niŋmai lɛ adara)", bullet_style))
    story.append(Paragraph("&bull; Biblia wolo ko kɛ yitso ko gbelemɔ (akɛ nɔkwɛmɔnɔ lɛ, Mateo 5)", bullet_style))
    story.append(Paragraph("&bull; Meetings fã lɛ (Kpee Nifeemɔ Wolo kɛhã Otsi Teŋ Kpee [Midweek Meeting], kɛ Buu-Mɔɔ Nikasemɔ sane kɛhã Otsi Naagbee Kpee [Weekend Meeting])", bullet_style))
    story.append(Paragraph("&bull; <i>Nɔkwɛmɔnɔ Ni Tsɔɔlɔ Lɛ Baafee:</i> Bookmark, History, kɛ Search (amɛkase yɛ shĩa)", bullet_style))

    story.append(Paragraph("Nifeemɔi (miniti 5)", h2_style))
    story.append(Paragraph("&bull; <b>Nifeemɔ 1.1:</b> Gbelemɔ Daa Gbi Ŋmalɛ Lɛ, ni onyɛ <b>Text Settings</b> (<b>A A</b>) nɔ koni niŋmai lɛ adara ni ekã shi faŋŋ.", bullet_style))
    story.append(Paragraph("&bull; <b>Nifeemɔ 1.2:</b> Nyɛɛ Bible nɔ, halamɔ Biblia wolo ko (Mateo), ni ogbele yitso 5.", bullet_style))
    story.append(Paragraph("&bull; <b>Nifeemɔ 1.3:</b> Gbelemɔ Meetings fã lɛ, ni onyɛ otsi nɛɛ Buu-Mɔɔ Nikasemɔ sane lɛ nɔ.", bullet_style))

    story.append(Paragraph("Ŋaawoi Kɛhã Klas Lɛ Hiɛnyiɛlɔ Yɛ Nikasemɔ 1 Lɛ He", h2_style))
    story.append(Paragraph(
        "Too gbɛjianɔ koni yelikɛbualɔi aye abua mɛi ni ba mra lɛ miniti 15 dani klas lɛ bɔi, koni amɛkwɛ akɛ mɔ fɛɛ mɔ edaunlodi Biblia lɛ kɛ Daa Gbi Ŋmalɛ Lɛ momo lo. Yɛ klas lɛ shishijee lɛ, "
        "kwɛmɔ yɛ sekɛnd 30 mli: bi nikaselɔi lɛ ni amɛwo amɛnine nɔ kɛ́ amɛmiitao yelikɛbuamɔ koni amɛdaunlodi nɔ ko, koni yelikɛbualɔi lɛ aye amɛbua amɛ dioo "
        "be ni oyaa nɔ lɛ. Tsɔɔmɔ bɔ ni akɛhãa gbee sɛɛ foɔ yɛ shishijee lɛ (Volume Down ni yɔɔ foŋ lɛ he; Mute yɛ kɔmpiuta okiibɔd lɛ nɔ) "
        "koni amɛshe gbeyei. Yelikɛbualɔi lɛ akwɛ akɛ nikaselɔi lɛ enyɛ amɛkɛ A A okadi lɛ ehã niŋmai lɛ edara lo.",
        body_style
    ))

    story.append(Paragraph("Kɛ́ amɛgbe nikasemɔ nɛɛ naa lɛ, nikaselɔi lɛ baanyɛ:", h2_style))
    story.append(Paragraph("&bull; Amɛya app lɛ fãi titrii lɛ fɛɛ anɔ mlɛo.", bullet_style))
    story.append(Paragraph("&bull; Amɛhã niŋmai lɛ adara yɛ app lɛ fɛɛ mli koni amɛkane mlɛo.", bullet_style))
    story.append(Paragraph("&bull; Amɛgbele Biblia yitso fɛɛ yitso, ni amɛna asafoŋ kpeei daa otsi lɛ asaji oya nɔŋŋ.", bullet_style))

    # ==================== BAAFA 3 ====================
    story.append(PageBreak())

    story.append(Paragraph("JW Library Nikasemɔi Lɛ Ahe Gbɛjianɔtoo", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Nikasemɔ 2: Nibii Ni Adaunlodiɔ Kɛ Bɔ Ni Akɛtsuɔ Nii (Miniti 15)", h1_style))
    story.append(Paragraph(
        "Nikasemɔ nɛɛ tsɔɔ bɔ ni akaneɔ nii kɛ́ Intanɛt bɛ, ni etsɔɔ bɔ ni adaunlodiɔ woji, vidioi, kɛ nibii ni atswaa aboɔ toi. "
        "Ha amɛna akɛ kɛ́ adaunlodi nɔ ko yɛ Wi-Fi nɔ lɛ, ehiɔ foŋ, tablɛt, loo kɔmpiuta lɛ nɔ, ni ehe ehiaaa Intanɛt "
        "loo mobail data yɛ asafoŋ kpeei ashishi. Tsɔɔmɔ nibii ni atswaa aboɔ toi lɛ (headphones okadi) koni nikaselɔi lɛ anyɛ abo nɔ ni akaneɔ lɛ toi.",
        body_style
    ))

    story.append(Paragraph("Saji Ni Abaasusu He (miniti 10)", h2_style))
    story.append(Paragraph("&bull; Bɔ ni akaneɔ nii kɛ abo toi kɛ́ Intanɛt bɛ", bullet_style))
    story.append(Paragraph("&bull; Wi-Fi nɔ yaa dani adaunlodi koni akafite mobail data", bullet_style))
    story.append(Paragraph("&bull; Woji, vidioi, kɛ nibii ni atswaa aboɔ toi daunlodimɔ (atatu okadi lɛ)", bullet_style))
    story.append(Paragraph("&bull; Nibii ni atswaa aboɔ toi kɛ bɔ ni akɛhãa gbee sɛɛ foɔ oya nɔŋŋ (Volume Down yɛ foŋ nɔ; Mute yɛ kɔmpiuta nɔ)", bullet_style))
    story.append(Paragraph("&bull; <i>Nɔkwɛmɔnɔ Ni Tsɔɔlɔ Lɛ Baafee:</i> Bɔ ni atoɔ nibii anaa yɛ Largest Size (Edalɛ) naa koni akwɛ gbɛ ni yɔɔ nɔ, ni ajie nibii", bullet_style))

    story.append(Paragraph("Nifeemɔi (miniti 5)", h2_style))
    story.append(Paragraph("&bull; <b>Nifeemɔ 2.1:</b> Kwɛmɔ skrin lɛ ŋwɛigbɛ koni ona akɛ foŋ, tablɛt, loo kɔmpiuta lɛ yɛ Wi-Fi lɛ nɔ.", bullet_style))
    story.append(Paragraph("&bull; <b>Nifeemɔ 2.2:</b> Nyɛɛ atatu okadi lɛ nɔ yɛ wolo loo vidio ko he koni odaunlodi.", bullet_style))
    story.append(Paragraph("&bull; <b>Nifeemɔ 2.3:</b> Gbelemɔ Daa Gbi Ŋmalɛ Lɛ loo Biblia lɛ, nyɛɛ Headphones nɔ ni obo toi; okɛ Volume Down loo Mute ahã gbee lɛ sɛɛ afo.", bullet_style))

    story.append(Paragraph("Ŋaawoi Kɛhã Klas Lɛ Hiɛnyiɛlɔ Yɛ Nikasemɔ 2 Lɛ He", h2_style))
    story.append(Paragraph(
        "Ha nikaselɔi ni amɛmobail data fa lɛ ana akɛ kɛ́ amɛdaunlodi nibii yɛ Wi-Fi nɔ momo lɛ, amɛfiteŋ mobail data yɛ asafoŋ kpeei ashishi. "
        "Nyɛkasea bɔ ni akɛhãa gbee sɛɛ foɔ faŋŋ: mɛi ni le foŋ he nii fioo lɛ shea gbeyei akɛ gbee ko baaje kpo be ni amɛkpaaa gbɛ; "
        "kɛ́ amɛle bɔ ni amɛaafee amɛhã gbee lɛ sɛɛ afo oya nɔŋŋ (Volume Down ni yɔɔ foŋ lɛ he, loo Mute yɛ kɔmpiuta nɔ) lɛ, amɛjwɛŋmɔ jɔɔ.",
        body_style
    ))

    story.append(Paragraph("Kɛ́ amɛgbe nikasemɔ nɛɛ naa lɛ, nikaselɔi lɛ baanyɛ:", h2_style))
    story.append(Paragraph("&bull; Amɛdaunlodi woji yɛ Wi-Fi nɔ ni amɛfiteŋ mobail data.", bullet_style))
    story.append(Paragraph("&bull; Amɛgbele woji ni amɛdaunlodi lɛ ni amɛkane yɛ asafoŋ kpeei ashishi kɛ́ Intanɛt bɛ.", bullet_style))
    story.append(Paragraph("&bull; Amɛbo ŋmalɛi kɛ saji ni akaneɔ lɛ toi, amɛtsi (Pause), ni amɛhã gbee lɛ sɛɛ afo oya nɔŋŋ.", bullet_style))

    # ==================== BAAFA 4 ====================
    story.append(PageBreak())

    story.append(Paragraph("JW Library Nikasemɔi Lɛ Ahe Gbɛjianɔtoo", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Nikasemɔ 3: Nibii Ni Obaanyɛ Okɛtsu Nii Yɛ Aŋkro Nikasemɔ Mli (Miniti 15)", h1_style))
    story.append(Paragraph(
        "Nikasemɔ nɛɛ tsɔɔ bɔ ni akɛ kɔla kadiɔ hetoi yɛ saji ni akaseɔ kɛhã asafoŋ kpeei lɛ amli, kɛ bɔ ni abuɔ aŋkro nikasemɔ he nibii ahe. "
        "Tsɔɔmɔ bɔ ni akɛ yɛlo kɔla kadiɔ wiemɔi, bɔ ni atsakeɔ kɔla lɛ, kɛ bɔ ni ajieɔ. "
        "Ŋɔɔ naagbee lɛ kɛtsɔɔ bɔ ni afeɔ <code>.jwlibrary</code> backup fail yɛ Settings mli, "
        "koni nibii ni nikaselɔi lɛ kadi yɛ amɛ aŋkro nikasemɔ mli lɛ akalaaje.",
        body_style
    ))

    story.append(Paragraph("Saji Ni Abaasusu He (miniti 10)", h2_style))
    story.append(Paragraph("&bull; Bɔ ni anyɛɔ wiemɔ nɔ fioo ni agbalaa kɛkɔlaa", bullet_style))
    story.append(Paragraph("&bull; Kɔlai halamɔ (yɛlo, bluu, grin)", bullet_style))
    story.append(Paragraph("&bull; Bɔ ni anyɛɔ wiemɔi ni akɛ kɔla kadi lɛ anɔ kɛtsakeɔ kɔla lɛ, loo akɛ Delete okadi lɛ jieɔ", bullet_style))
    story.append(Paragraph("&bull; <b>Bɔ Ni Abuɔ Onibii Ahe:</b> Backup feemɔ (Settings &gt; Backup and Restore)", bullet_style))
    story.append(Paragraph("&bull; <i>Nɔkwɛmɔnɔ Ni Tsɔɔlɔ Lɛ Baafee:</i> Nibii ni aŋmalaa afatamɔ he, Tags, kɛ Personal Study fã lɛ", bullet_style))

    story.append(Paragraph("Nifeemɔi (miniti 5)", h2_style))
    story.append(Paragraph("&bull; <b>Nifeemɔ 3.1:</b> Gbelemɔ Buu-Mɔɔ Nikasemɔ sane ni baaba lɛ, ni okɛ yɛlo kɔla akadi hetoo ni yɔɔ kuku 1 lɛ mli.", bullet_style))
    story.append(Paragraph("&bull; <b>Nifeemɔ 3.2:</b> Nyɛɛ hetoo ni okɛ kɔla kadi lɛ nɔ koni otsake kɛya bluu, loo onyɛ Delete okadi lɛ nɔ koni ojie.", bullet_style))
    story.append(Paragraph("&bull; <b>Nifeemɔ 3.3:</b> Gbelemɔ Settings &gt; Backup and Restore, ni onyɛ <b>Create Backup</b> nɔ.", bullet_style))

    story.append(Paragraph("Naagbee Kɛ Ŋaawoi Kɛhã Klas Lɛ Hiɛnyiɛlɔ (0:50 - 1:00)", h2_style))
    story.append(Paragraph(
        "• <b>Yelikɛbuamɔ Dani Klas Lɛ Bɔi:</b> Kɛ́ agbele shinai lɛ miniti 15 dani klas lɛ bɔi koni yelikɛbualɔi aye abua lɛ, mɛi fɛɛ ataoŋ Wi-Fi be kome.<br/>"
        "• <b>Bɔ Ni Akɛhãa Gbee Sɛɛ Foɔ:</b> Kɛ́ atsɔɔ nikaselɔi lɛ Volume Down lɛ yɛ shishijee lɛ, amɛsheŋ gbeyei akɛ gbee ko baaje kpo.<br/>"
        "• <b>Naagbee Miniti 10 Lɛ:</b> Okɛ miniti nɛɛ atsu nii kɛkwɛ nɔ ni akase lɛ ekoŋŋ, kɛhã sanebimɔi ahetoo, loo kɛ́ nifeemɔ ko ye be fe bɔ ni akpa gbɛ.<br/>"
        "• <b>Yelikɛbualɔi Ni Yɔɔ Okpɔlɔi Lɛ Ahe:</b> Kɛ́ yelikɛbualɔi 1 loo 2 nyiɛɔ tsũ lɛ mli kɛyeɔ amɛbuaa mɛi pɔtɛɛ lɛ, klas lɛ damɔŋ shi.<br/>"
        "• <b>Woji Ni Aprinti (Kɛ́ Ehe Baahia):</b> Kɛ́ akɛ Klas Lɛ He Gbɛjianɔtoo ni yɔɔ baafa kome nɔ lɛ fɔ̃ okpɔlɔi lɛ anɔ lɛ, eyeɔ ebuaa he ni data loo Wi-Fi fa.<br/>"
        "• <b>QR Okadii Yɛ Okpɔlɔi Lɛ Anɔ / Skrin Lɛ Nɔ (Kɛ́ Osumɔ):</b> Kɛ́ ajie QR okadi lɛ yɛ skrin lɛ nɔ loo akɛ QR wolo bibii fɔ̃ okpɔlɔi lɛ anɔ lɛ, nikaselɔi lɛ baanyɛ amɛkɛ amɛfoŋ kamera lɛ agbele kasemɔ wolo nɛɛ.<br/>"
        "• <b>Add to Home Screen (Kɛ́ Osumɔ):</b> Kɛ́ otsɔɔ nikaselɔi lɛ \"Add to Home Screen\" lɛ, kasemɔ wolo nɛɛ baahi amɛfoŋ lɛ nɔ, ni amɛbaanyɛ amɛkane kɛ́ Intanɛt bɛ po.<br/>"
        "• <b>Yelikɛbuamɔ Yɛ Klas Lɛ Sɛɛ:</b> Hi jɛmɛ miniti 15 yɛ klas lɛ sɛɛ kɛhã mɔ fɛɛ mɔ ni miitao yelikɛbuamɔ pɔtɛɛ yɛ ebackup fail lɛ he.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Kɛ́ amɛgbe nikasemɔ nɛɛ naa lɛ, nikaselɔi lɛ baanyɛ:", h2_style))
    story.append(Paragraph("&bull; Amɛkɛ kɔla akadi hetoi kɛhã asafoŋ kpeei, ni amɛtsake kɔla lɛ loo amɛjie mlɛo.", bullet_style))
    story.append(Paragraph("&bull; Amɛkɛ nibii ni amɛŋmala kɛ nibii ni amɛkɛ kɔla kadi lɛ awo .jwlibrary backup fail mli koni amɛkalaaje.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)


if __name__ == '__main__':
    repo_root = os.path.normpath(os.path.join(_HERE, '..', '..'))
    program_pdf = os.path.join(repo_root, 'JW Library Class Program (Ga).pdf')
    curriculum_pdf = os.path.join(repo_root, 'JW Library Tutorial Curriculum (Ga).pdf')

    build_class_program(program_pdf)
    build_curriculum(curriculum_pdf)

    r1 = pypdf.PdfReader(program_pdf)
    r2 = pypdf.PdfReader(curriculum_pdf)
    print(f'EGBE NAA: Klas Lɛ He Gbɛjianɔtoo PDF (baafa {len(r1.pages)}): {program_pdf}')
    print(f'EGBE NAA: Nikasemɔi Lɛ Ahe Gbɛjianɔtoo PDF (baafa {len(r2.pages)}): {curriculum_pdf}')
