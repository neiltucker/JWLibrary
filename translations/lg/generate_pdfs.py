import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

# Enkyusa ya Luganda. Ekola PDF za Luganda ezirina amannya ag'enjawulo ku
# PDF ez'Olungereza, ezo ezaasooka zireme kusangulibwawo.

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Unicode font setup.
# The built-in Helvetica font cannot print letters such as ŋ (used in Luganda).
# This looks for a TrueType font that contains them and uses it instead.
# To guarantee correct output on any computer, put the four DejaVu Sans files
# (DejaVuSans.ttf, DejaVuSans-Bold.ttf, DejaVuSans-Oblique.ttf,
# DejaVuSans-BoldOblique.ttf) in a folder named "fonts" next to this script.
# ---------------------------------------------------------------------------
REQUIRED_CHARS = "ŋŊ"

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

# Canvas eteeka ennamba "Olupapula X ku Y" ku Nteekateeka y'Amasomo
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
        # Waggulu ku ddyo
        self.drawRightString(letter[0] - 45, letter[1] - 30, f"Olupapula {self._pageNumber} ku {page_count}")
        # Ebikwata ku mateeka wansi ku buli lupapula
        disclaimer = "JW Library kabonero k'obusuubuzi akaawandiisibwa aka Watch Tower Bible and Tract Society of Pennsylvania. Kiyamba kyetongodde."
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

    story.append(Paragraph("ENTEEKATEEKA YA KIRAASI YA JW LIBRARY", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>WEETEGEREZE:</b> Ebiragiro ebituufu ku ngeri y'okukozesa JW Library bisangibwa ku JW.ORG (https://www.jw.org/en/online-help/jw-library/)", note_style))
    story.append(Paragraph("Kiraasi ya ddakiika 60 erimu amasomo asatu, buli limu lya ddakiika 15, n'eddakiika 10 ez'okufundikira. (Esobola okwongezebwa okutuuka ku ddakiika 75-90).", note_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=3))

    # Enteekateeka
    story.append(Paragraph("<b>Okwaniriza n'Okumanyiira Ssirini: (0:00 - 0:05)</b>", section_hdr))
    story.append(Paragraph("0:00 &nbsp; Okwaniriza; okukebera oba Bayibuli/Ekyawandiikibwa eky'Olunaku byetegefu (abayambi bayamba okuwanula).", timing_style))
    story.append(Paragraph("0:02 &nbsp; Amagezi ag'okusirisa mu kabenje: nyweza eppeesa erikendeeza eddoboozi (essimu) oba nyiga erisirisa (kompyuta); zuula olukalala olukulu.", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Essomo 1: Okuzuula Ebyawandiikibwa n'Enkuŋŋaana (0:05 - 0:20)</b>", section_hdr))
    story.append(Paragraph("0:05 &nbsp; Okwogera ku bitundu ebikulu eby'okutambuliramu (Bayibuli, Ebitabo, Enkuŋŋaana, Okwesomesa).", timing_style))
    story.append(Paragraph("0:07 &nbsp; Okuggulawo Ekyawandiikibwa eky'Olunaku n'okunyiga akabonero <b>A A</b> okugaziya ennukuta osome bulungi.", timing_style))
    story.append(Paragraph("0:10 &nbsp; Kola Okwegezaamu Okukulu 1.1 (Ekyawandiikibwa eky'Olunaku n'Obunene bw'Ennukuta).", timing_style))
    story.append(Paragraph("0:12 &nbsp; Okuggulawo ekitabo n'essuula ya Bayibuli; kola Okwegezaamu Okukulu 1.2.", timing_style))
    story.append(Paragraph("0:15 &nbsp; Okwogera ku kitundu ky'Enkuŋŋaana (akatabo k'Omu Wiiki n'okusoma Omunaala gw'Omukuumi okwa Wikendi).", timing_style))
    story.append(Paragraph("0:18 &nbsp; Kola Okwegezaamu Okukulu 1.3 (Enkuŋŋaana). (Omusomesa alaga Obubonero bw'Okujjukira ne Noonya).", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Essomo 2: Okuwanula n'Okukozesa Amaloboozi ne Vidiyo (0:20 - 0:35)</b>", section_hdr))
    story.append(Paragraph("0:20 &nbsp; Okutegeera okukozesa awatali yintaneeti: ebiwanulwa ku Wi-Fi bisigala ku kyuma awatali kwetaaga data y'essimu.", timing_style))
    story.append(Paragraph("0:22 &nbsp; Kola Okwegezaamu Okukulu 2.1 (Okukebera Wi-Fi n'okukuuma data y'essimu).", timing_style))
    story.append(Paragraph("0:24 &nbsp; Okuwanula ekintu okukisoma/okukiraba awatali yintaneeti; kola Okwegezaamu Okukulu 2.2.", timing_style))
    story.append(Paragraph("0:28 &nbsp; Ekizannya Amaloboozi (akabonero ka headphones); okusirisa amangu n'eppeesa erikendeeza eddoboozi (essimu) oba erisirisa (kompyuta).", timing_style))
    story.append(Paragraph("0:31 &nbsp; Kola Okwegezaamu Okukulu 2.3 (Okuwuliriza Amaloboozi). (Omusomesa alaga okukebera ekifo eky'okuterekamu).", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Essomo 3: Ebikozesebwa mu Kwesomesa (0:35 - 0:50)</b>", section_hdr))
    story.append(Paragraph("0:35 &nbsp; Okulonda ebigambo n'ebisentensi okussaako langi ku byokuddamu mu bitundu eby'okusoma.", timing_style))
    story.append(Paragraph("0:37 &nbsp; Kola Okwegezaamu Okukulu 3.1 (Ssaako langi ya kyenvu ku kyokuddamu).", timing_style))
    story.append(Paragraph("0:40 &nbsp; Okukyusa langi oba okugiggyawo; kola Okwegezaamu Okukulu 3.2.", timing_style))
    story.append(Paragraph("0:43 &nbsp; Okukuuma by'osoma: okukola fayiro y'ekkopi (.jwlibrary) mu Entegeka &gt; Okutereka Kkopi n'Okugizzaawo.", timing_style))
    story.append(Paragraph("0:46 &nbsp; Kola Okwegezaamu Okukulu 3.3 (Kola Kkopi). (Omusomesa alaga Ebiwandiiko ne Tags).", timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph("<b>Okufundikira, Okuddamu Okwetegereza, n'Ebibuuzo: (0:50 - 1:00)</b>", section_hdr))
    story.append(Paragraph("0:50 &nbsp; Eddakiika 10 ez'okuddamu okwetegereza, ebibuuzo, oba ekiseera eky'enyongeza. Oluvannyuma, okuyambibwa okw'eddakiika 15 ng'oli wekka okutali kwa buwaze.", timing_style))
    story.append(Spacer(1, 2))

    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=2))
    story.append(Paragraph("<b>OKWEGEZAAMU OKUKULU</b>", ex_hdr))

    story.append(Paragraph("<b>1.1</b> Nyiga <b>Ekyawandiikibwa eky'Olunaku</b> (akabonero k'enjuba). Nyiga akabonero <b>A A</b> waggulu osereze okugaziya ennukuta.", ex_style))
    story.append(Paragraph("<b>1.2</b> Nyiga <b>Bayibuli</b>. Londa ekitabo (okugeza, <i>Matayo</i>) n'essuula (okugeza, <i>5</i>) otandike okusoma.", ex_style))
    story.append(Paragraph("<b>1.3</b> Nyiga <b>Enkuŋŋaana</b>. Ggulawo butereevu ekitundu eky'okusoma mu <i>Omunaala gw'Omukuumi</i> ekya wiiki eno ng'onyize omulundi gumu.", ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>2.1</b> Kakasa nti ekyuma kyo kiyungiddwa ku Wi-Fi osobole okukekkereza data y'essimu.", ex_style))
    story.append(Paragraph("<b>2.2</b> Mu Ebitabo oba Enkuŋŋaana, nyiga <b>akabonero k'Ekire</b> ku kintu eky'okusoma okukiwanula okukikozesa awatali yintaneeti.", ex_style))
    story.append(Paragraph("<b>2.3</b> Ggulawo Ekyawandiikibwa eky'Olunaku oba Bayibuli. Nyiga <b>Headphones</b> owulirize; komya n'<b>eppeesa erikendeeza eddoboozi</b> (oba erisirisa).", ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph("<b>3.1</b> Mu katundu 1 ak'okusoma <i>Omunaala gw'Omukuumi</i>, nyiga owalule engalo ku kyokuddamu olwo onyige <b>Kyenvu</b>.", ex_style))
    story.append(Paragraph("<b>3.2</b> Ddamu onyige ebigambo by'osizzaako langi okukyusa langi (bbulu oba kiragala), oba nyiga akabonero ka kasasiro okugiggyawo.", ex_style))
    story.append(Paragraph("<b>3.3</b> Ggulawo Entegeka &gt; Okutereka Kkopi n'Okugizzaawo olwo onyige <b>Kola Kkopi</b> okutereka obubonero bwo obw'okusoma.", ex_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<i>Ebikwata ku Mateeka: JW Library kabonero k'obusuubuzi akaawandiisibwa aka Watch Tower Bible and Tract Society of Pennsylvania. Enteekateeka eno eya kiraasi kiyamba okuyiga ekyetongodde, ekitali kya kusuubula, era tekikwatagana na wadde okusiimibwa butongole Watch Tower oba Abajulirwa ba Yakuwa.</i>", disclaimer_style))

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

    # ==================== OLUPAPULA 1 ====================
    story.append(Paragraph("Enteekateeka y'Amasomo ga JW Library", doc_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>WEETEGEREZE:</b> Ebiragiro ebituufu ku ngeri y'okukozesa JW Library bisangibwa ku JW.ORG (https://www.jw.org/en/online-help/jw-library/)", note_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Ebikwata ku Kuyiga Okukozesa JW Library", h1_style))
    story.append(Paragraph(
        "Enteekateeka eno egendereddwamu oyo yenna asomesa oba alung'amya abayizi ng'akozesa "
        "<i>Okuyiga Okukozesa JW Library</i>. Amasomo gategekeddwa mu masomo asatu, buli limu lya ddakiika 15: "
        "<b>Okuzuula Ebyawandiikibwa n'Enkuŋŋaana</b>, <b>Okuwanula n'Okukozesa Amaloboozi ne Vidiyo</b>, ne <b>Ebikozesebwa mu Kwesomesa</b>. "
        "Eddakiika 10 ez'okufundikira ziwa ekiseera eky'enyongeza ekimala abasomesa baleme kuwulira nti banyigirizibwa. "
        "Nga kiraasi tennatandika, abayizi balina okuweebwa kkopi y'ebintu eby'okuyiga era "
        "n'okujjukizibwa okuteeka pulogulaamu ku kyuma kyabwe nga bukyali.",
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<i>Enteekateeka ya Kiraasi ya JW Library</i> ekozesebwa ng'ekyokulabirako ng'otegeka enteekateeka ya kiraasi. Eddakiika ttaano "
        "ziteekebwawo ku ntandikwa okumanyiiza abayizi engeri ebyuma byabwe gye bitegekeddwamu. Buli ssomo lya ddakiika 15 lissa essira ku bikolwa bisatu "
        "ebikulu eby'okwegezaamu, ate ensonga enzibu ne zilekerwa omusomesa okuziraga mangu. Kiraasi yonna etwala "
        "eddakiika 60, era esobola okwongezebwa okutuuka ku ddakiika 75 oba 90 eri ebibinja ebyetaaga obuyambi obusingawo obw'omuntu kinnoomu.",
        body_style
    ))

    story.append(Paragraph("Abagendererwamu", h1_style))
    story.append(Paragraph(
        "Okuyiga kuno kutegekeddwa abantu abamanyi ebisookerwako ku kukozesa essimu ey'omulembe, tabuleti, oba kompyuta. "
        "Abayizi balina okuba nga basobola okukozesa ssirini enyigibwa oba mawusi. Okuba nga wali okozesezza pulogulaamu ya JW Library "
        "kiyamba naye tekyetaagisa.",
        body_style
    ))

    story.append(Paragraph("By'Onoosobola Okukola", h1_style))
    story.append(Paragraph("Bwe banaamala okuyiga kuno, abayizi bajja kusobola:", body_style))
    story.append(Paragraph("&bull; Okuva mu Bayibuli, Ebitabo, Enkuŋŋaana, n'Okwesomesa okugenda mu kirala.", bullet_style))
    story.append(Paragraph("&bull; Okuggulawo Ekyawandiikibwa eky'Olunaku n'okugaziya ennukuta nga bakozesa eppeesa A A.", bullet_style))
    story.append(Paragraph("&bull; Okuzuula ebitundu eby'okusoma eby'enkuŋŋaana eza buli wiiki nga banyize omulundi gumu mu kitundu ky'Enkuŋŋaana.", bullet_style))
    story.append(Paragraph("&bull; Okutegeera okusoma awatali yintaneeti n'okuwanula ebitabo ku Wi-Fi okukekkereza data y'essimu.", bullet_style))
    story.append(Paragraph("&bull; Okukozesa ekizannya amaloboozi (akabonero ka headphones) n'okusirisa amangu eddoboozi eritasuubiddwa.", bullet_style))
    story.append(Paragraph("&bull; Okussaako langi ez'enjawulo ku byokuddamu mu bitundu eby'okusoma n'okuziggyawo.", bullet_style))
    story.append(Paragraph("&bull; Okukola kkopi (fayiro ya .jwlibrary) okukuuma ebiwandiiko by'okusoma.", bullet_style))

    story.append(Paragraph("Ebyetaagisa n'Amagezi ag'Okwetegeka", h1_style))
    story.append(Paragraph("Nga tebannajja ku kiraasi eno, abayizi balina:", body_style))
    story.append(Paragraph("&bull; Okutuuka <b>eddakiika 10–15 nga bukyali</b> abayambi babayambe ku Wi-Fi n'okutegeka Bayibuli/Ekyawandiikibwa eky'Olunaku.", bullet_style))
    story.append(Paragraph("&bull; Okuba n'ekyuma ekikozesa <b>Android 8.0+</b>, <b>iOS 15.0+</b>, <b>macOS M1+</b>, oba <b>Windows 10 v2004+</b>.", bullet_style))
    story.append(Paragraph("&bull; Okujja nga <b>bbaatule ejjudde</b> (oba okuleeta ecaajinga).", bullet_style))
    story.append(Paragraph("&bull; Okuteekawo okumala akaseera <b>ssirini ezikire oluvannyuma lw'eddakiika 2 oba 5</b> ssirini ereme kuzikira.", bullet_style))
    story.append(Paragraph("&bull; Waakiri <b>GB 2 okutuuka ku 4</b> ez'ekifo eky'okuterekamu (oba SD card eteekeddwamu) ku lwa fayiro z'amaloboozi ne vidiyo.", bullet_style))
    story.append(Paragraph("&bull; Okuyunga ku Wi-Fi nga tebannawanula vidiyo oba amaloboozi.", bullet_style))

    # ==================== OLUPAPULA 2 ====================
    story.append(PageBreak())

    story.append(Paragraph("Enteekateeka y'Amasomo ga JW Library", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Essomo 1: Okuzuula Ebyawandiikibwa n'Enkuŋŋaana (Eddakiika 15)", h1_style))
    story.append(Paragraph(
        "Essomo lino liyigiriza abayizi okuva mu kitundu ekimu ekikulu ekya pulogulaamu ya JW Library okugenda mu kirala mu ngeri ennyangu. "
        "Abasomesa balina okunnyonnyola olukalala olw'okutambuliramu we luli okusinziira ku byuma ebiriwo (wansi ku iOS "
        "ne Android ez'omulembe; waggulu ku Windows). Laga engeri okunyiga akabonero <b>A A</b> gye kugaziyaamu ennukuta okusoma "
        "obulungi, n'engeri <b>ekitundu ky'Enkuŋŋaana</b> gye kisobozesaamu okuggulawo ebitabo by'enkuŋŋaana eza buli wiiki ng'onyize omulundi gumu.",
        body_style
    ))

    story.append(Paragraph("Emitwe (eddakiika 10)", h2_style))
    story.append(Paragraph("&bull; Ebitundu Ebikulu eby'Okutambuliramu (Bayibuli, Ebitabo, Enkuŋŋaana, Okwesomesa)", bullet_style))
    story.append(Paragraph("&bull; Ekyawandiikibwa eky'Olunaku n'Okutereeza Obunene bw'Ennukuta (eppeesa A A okugaziya ennukuta)", bullet_style))
    story.append(Paragraph("&bull; Okuggulawo ekitabo n'essuula ya Bayibuli (okugeza, Matayo 5)", bullet_style))
    story.append(Paragraph("&bull; Ekitundu ky'Enkuŋŋaana (okuggulawo akatabo k'Omu Wiiki n'ekitundu eky'okusoma mu Omunaala gw'Omukuumi ekya Wikendi)", bullet_style))
    story.append(Paragraph("&bull; <i>Omusomesa Alaga:</i> Obubonero bw'Okujjukira, Ebyafaayo, ne Noonya (okwegezaamu awaka)", bullet_style))

    story.append(Paragraph("Okwegezaamu Okukulu (eddakiika 5)", h2_style))
    story.append(Paragraph("&bull; <b>Okukulu 1.1:</b> Ggulawo Ekyawandiikibwa eky'Olunaku onyige <b>A A</b> ennukuta zifuuke nnene era zitegeerekeke.", bullet_style))
    story.append(Paragraph("&bull; <b>Okukulu 1.2:</b> Nyiga Bayibuli, londa ekitabo (Matayo), oggulewo essuula 5.", bullet_style))
    story.append(Paragraph("&bull; <b>Okukulu 1.3:</b> Ggulawo ekitundu ky'Enkuŋŋaana onyige ekitundu eky'okusoma mu Omunaala gw'Omukuumi ekya wiiki eno.", bullet_style))

    story.append(Paragraph("Ebiyamba Akulembera Kiraasi ku Ssomo 1", h2_style))
    story.append(Paragraph(
        "Tegeka okuyambibwa okw'eddakiika 15 eri abatuuka kare abayambi bakakase nti Bayibuli n'Ekyawandiikibwa eky'Olunaku byetegefu. Ku ntandikwa ya kiraasi, "
        "kola okukebera okw'esikonda 30: saba abayizi bayimuse emikono bwe baba beetaaga obuyambi okuwanula abayambi "
        "babayambe mpola nga weeyongerayo. Yigiriza okusirisa ekyuma nga bukyali (eppeesa erikendeeza eddoboozi eriri ku mabbali ku ssimu; erisirisa ku kiwandiikiro kya kompyuta) "
        "okuggyawo okutya. Abayambi bakakase nti abayizi basobodde okugaziya ennukuta n'eppeesa A A.",
        body_style
    ))

    story.append(Paragraph("Bwe banaamala essomo lino, abayizi bajja kusobola:", h2_style))
    story.append(Paragraph("&bull; Okuva mu kitundu ekimu ekikulu ekya pulogulaamu okugenda mu kirala mu ngeri ennyangu.", bullet_style))
    story.append(Paragraph("&bull; Okugaziya ennukuta mu pulogulaamu yonna okusoma awatali kufuba.", bullet_style))
    story.append(Paragraph("&bull; Okuggulawo essuula yonna eya Bayibuli n'okutuuka ku bitundu by'enkuŋŋaana eza buli wiiki nga banyize omulundi gumu.", bullet_style))

    # ==================== OLUPAPULA 3 ====================
    story.append(PageBreak())

    story.append(Paragraph("Enteekateeka y'Amasomo ga JW Library", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Essomo 2: Okuwanula n'Okukozesa Amaloboozi ne Vidiyo (Eddakiika 15)", h1_style))
    story.append(Paragraph(
        "Essomo lino linnyonnyola engeri okusoma awatali yintaneeti gye kukolamu era lilaga engeri y'okuwanula ebitabo, amaloboozi ne vidiyo. "
        "Ssa essira ku nsonga nti ekintu bwe kimala okuwanulwa ku Wi-Fi, kisigala ku kyuma ennaku zonna awatali kwetaaga yintaneeti "
        "wadde data y'essimu mu nkuŋŋaana. Yanjula ekizannya amaloboozi (akabonero ka headphones) abayizi basobole okuwuliriza ebiwandiiko nga bisomebwa mu ddoboozi.",
        body_style
    ))

    story.append(Paragraph("Emitwe (eddakiika 10)", h2_style))
    story.append(Paragraph("&bull; Okutegeera Okukozesa Awatali Yintaneeti: okusoma n'okuwuliriza awatali kakwate ka ssimu", bullet_style))
    story.append(Paragraph("&bull; Okuyunga ku Wi-Fi nga tonnawanula okukekkereza data y'essimu", bullet_style))
    story.append(Paragraph("&bull; Okuwanula ebitabo, amaloboozi ne vidiyo (okumanya akabonero k'Ekire)", bullet_style))
    story.append(Paragraph("&bull; Okukozesa Ekizannya Amaloboozi n'okusirisa amangu mu kabenje (eppeesa erikendeeza eddoboozi ku ssimu; erisirisa ku kompyuta)", bullet_style))
    story.append(Paragraph("&bull; <i>Omusomesa Alaga:</i> Okusengeka ng'osinziira ku Kisinga Obunene okukebera ekifo eky'okuterekamu n'okusangulamu fayiro", bullet_style))

    story.append(Paragraph("Okwegezaamu Okukulu (eddakiika 5)", h2_style))
    story.append(Paragraph("&bull; <b>Okukulu 2.1:</b> Kakasa waggulu ku ssirini nti ekyuma kiyungiddwa ku Wi-Fi.", bullet_style))
    story.append(Paragraph("&bull; <b>Okukulu 2.2:</b> Nyiga akabonero k'Ekire ku kitabo eky'okusoma oba ku vidiyo okukiwanula.", bullet_style))
    story.append(Paragraph("&bull; <b>Okukulu 2.3:</b> Ggulawo Ekyawandiikibwa eky'Olunaku oba Bayibuli, nyiga Headphones owulirize; komya n'eppeesa erikendeeza eddoboozi oba erisirisa.", bullet_style))

    story.append(Paragraph("Ebiyamba Akulembera Kiraasi ku Ssomo 2", h2_style))
    story.append(Paragraph(
        "Gumya abayizi abalina data entono nti tebajja kukozesa data y'essimu mu nkuŋŋaana singa bawanula "
        "nga bukyali ku Wi-Fi. Mwegezeemu mu lwatu okusirisa mu kabenje: abantu abatamanyidde tekinologiya batera okutya eddoboozi eriyinza okuvaayo mu butanwa; "
        "okumanya engeri y'okusirisa amangu (okunyweza eppeesa erikendeeza eddoboozi eriri ku mabbali ku ssimu oba okunyiga erisirisa ku kompyuta) kibawa emirembe mu mutima egijjuvu.",
        body_style
    ))

    story.append(Paragraph("Bwe banaamala essomo lino, abayizi bajja kusobola:", h2_style))
    story.append(Paragraph("&bull; Okuwanula ebitabo mu ngeri ey'obukuumi ku Wi-Fi awatali kukozesa data y'essimu.", bullet_style))
    story.append(Paragraph("&bull; Okuggulawo n'okusoma ebitabo ebiwanuddwa awatali yintaneeti mu nkuŋŋaana z'ekibiina.", bullet_style))
    story.append(Paragraph("&bull; Okuzannya, okuyimiriza, n'okusirisa amangu okusoma kw'ebyawandiikibwa n'ebitundu mu ddoboozi.", bullet_style))

    # ==================== OLUPAPULA 4 ====================
    story.append(PageBreak())

    story.append(Paragraph("Enteekateeka y'Amasomo ga JW Library", doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("Essomo 3: Ebikozesebwa mu Kwesomesa (Eddakiika 15)", h1_style))
    story.append(Paragraph(
        "Essomo lino lyogera ku kussaako langi mu bitundu eby'okusoma ku lw'enkuŋŋaana n'okukuuma ebiwandiiko by'okwesomesa. "
        "Laga engeri y'okulonda ebigambo n'okubissaako langi ya kyenvu, okukyusa langi, n'okuziggyawo. "
        "Fundikira n'omutendera omukulu ogw'okukola fayiro y'ekkopi eya <code>.jwlibrary</code> mu Entegeka "
        "obubonero bw'okwesomesa bureme kubula n'akatono.",
        body_style
    ))

    story.append(Paragraph("Emitwe (eddakiika 10)", h2_style))
    story.append(Paragraph("&bull; Okulonda ebigambo ng'onyiga mpola n'owalula engalo okussaako langi", bullet_style))
    story.append(Paragraph("&bull; Okulonda langi (Kyenvu, Bbulu, Kiragala)", bullet_style))
    story.append(Paragraph("&bull; Okunyiga ebigambo by'osizzaako langi okukyusa langi oba okugiggyawo n'akabonero ka kasasiro", bullet_style))
    story.append(Paragraph("&bull; <b>Okukuuma Ebiwandiiko:</b> Okukola fayiro y'ekkopi (Entegeka &gt; Okutereka Kkopi n'Okugizzaawo)", bullet_style))
    story.append(Paragraph("&bull; <i>Omusomesa Alaga:</i> Okwongerako ebiwandiiko, Tags, n'okulaba ekitundu ky'Okwesomesa", bullet_style))

    story.append(Paragraph("Okwegezaamu Okukulu (eddakiika 5)", h2_style))
    story.append(Paragraph("&bull; <b>Okukulu 3.1:</b> Ggulawo ekitundu ekiddako mu Omunaala gw'Omukuumi oteeke langi ya kyenvu ku kyokuddamu mu katundu 1.", bullet_style))
    story.append(Paragraph("&bull; <b>Okukulu 3.2:</b> Nyiga ekyokuddamu ky'osizzaako langi okugikyusa ku bbulu, oba nyiga akabonero ka kasasiro okugiggyawo.", bullet_style))
    story.append(Paragraph("&bull; <b>Okukulu 3.3:</b> Ggulawo Entegeka &gt; Okutereka Kkopi n'Okugizzaawo olwo onyige <b>Kola Kkopi</b>.", bullet_style))

    story.append(Paragraph("Okufundikira n'Amagezi eri Akulembera Kiraasi (0:50 - 1:00)", h2_style))
    story.append(Paragraph(
        "• <b>Okuyambibwa nga Kiraasi Tennatandika:</b> Okuggulawo enzigi eddakiika 15 nga bukyali abayambi okutegeka ebyuma kiziyiza akalippagano ku Wi-Fi.<br/>"
        "• <b>Okumanyiira Okusirisa mu Kabenje:</b> Okuyigiriza eppeesa erikendeeza eddoboozi nga bukyali kiggyawo okutya eddoboozi eritasuubiddwa.<br/>"
        "• <b>Eddakiika 10 ez'Enyongeza:</b> Kozesa eddakiika zino ez'okufundikira okuddamu okwetegereza ebituukiddwako, okuddamu ebibuuzo, oba okumalira ekiseera ekisukkiridde.<br/>"
        "• <b>Abayambi ku Mmeeza:</b> Okuba n'abayambi 1 oba 2 abatambulatambula mu kisenge nga bayamba abantu kinnoomu kiziyiza kiraasi okulwawo.<br/>"
        "• <b>Kkopi Ezikubiddwa mu Kyapa (Bwe kiba kyetaagisa):</b> Okussa kkopi z'Enteekateeka ya Kiraasi ey'olupapula 1 ku mmeeza kiyamba awali ddata oba Wi-Fi entono.<br/>"
        "• <b>Koodi za QR ku Mmeeza oba ku Ssirini (Si kya buwaze):</b> Okulaga koodi ya QR ku ssirini oba okuteeka obukadi bwa QR ku mmeeza kiyamba abayizi okuggulawo ekitabo kino nga bakozesa kamera y'essimu.<br/>"
        "• <b>Yongereza ku Ssirini Ey'omu Maaso (Si kya buwaze):</b> Okulaga abayizi \"Add to Home Screen\" kiterekera ekitabo kino ku ssimu, ne kisobola okusomebwa oluvannyuma ne bwe waba tewali yintaneeti.<br/>"
        "• <b>Okuyambibwa Oluvannyuma lwa Kiraasi:</b> Weewaayo okusigalawo eddakiika 15 oluvannyuma lwa kiraasi eri oyo yenna ayagala okuyambibwa ng'ali yekka ku fayiro ye ey'ekkopi.",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("Bwe banaamala essomo lino, abayizi bajja kusobola:", h2_style))
    story.append(Paragraph("&bull; Okussaako langi ku byokuddamu eby'enkuŋŋaana n'okukyusa oba okuggyawo langi nga beekakasa.", bullet_style))
    story.append(Paragraph("&bull; Okutereka mu ngeri ey'obukuumi kkopi y'ebiwandiiko byabwe n'obubonero bw'okusoma mu fayiro ya .jwlibrary.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)


if __name__ == '__main__':
    program_pdf = 'D:/cs/JWLibrary/Enteekateeka ya Kiraasi ya JW Library.pdf'
    curriculum_pdf = "D:/cs/JWLibrary/Enteekateeka y'Amasomo ga JW Library.pdf"

    build_class_program(program_pdf)
    build_curriculum(curriculum_pdf)

    r1 = pypdf.PdfReader(program_pdf)
    r2 = pypdf.PdfReader(curriculum_pdf)
    print(f'KIWEDDE: PDF y\'Enteekateeka ya Kiraasi ekoleddwa, erina empapula {len(r1.pages)}.')
    print(f'KIWEDDE: PDF y\'Enteekateeka y\'Amasomo ekoleddwa, erina empapula {len(r2.pages)}.')
