import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import pypdf

# Toleo la Kiswahili. Hutengeneza PDF za Kiswahili zenye majina tofauti
# na PDF za Kiingereza, ili zisiandikwe juu ya faili za asili.

# Canvas yenye namba "Ukurasa X kati ya Y" kwa ajili ya Mtaala
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
        # Kichwa cha juu kulia
        self.drawRightString(letter[0] - 45, letter[1] - 30, f"Ukurasa {self._pageNumber} kati ya {page_count}")
        # Taarifa ya kisheria chini ya kila ukurasa
        disclaimer = "JW Library ni alama ya biashara iliyosajiliwa ya Watch Tower Bible and Tract Society of Pennsylvania. Msaada wa mafunzo unaojitegemea, usio wa kibiashara."
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

    story.append(Paragraph('RATIBA YA DARASA LA JW LIBRARY', title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph('<b>KUMBUKA:</b> Maelekezo rasmi kuhusu kutumia JW Library yanapatikana kwenye JW.ORG (https://www.jw.org/sw/msaada-mtandaoni/jw-library/)', note_style))
    story.append(Paragraph('Darasa la dakika 60 lenye masomo matatu ya dakika 15 kila moja na dakika 10 za kuhitimisha zilizotengwa. (Linaweza kurefushwa hadi dakika 75-90).', note_style))
    story.append(Spacer(1, 3))
    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=3))

    # Ratiba
    story.append(Paragraph('<b>Kuwakaribisha na Kuonyesha Skrini: (0:00 - 0:05)</b>', section_hdr))
    story.append(Paragraph('0:00 &nbsp; Kuwakaribisha; kukagua kama Biblia/Andiko la Siku viko tayari (wasaidizi wanasaidia kupakua).', timing_style))
    story.append(Paragraph('0:02 &nbsp; Dokezo la kunyamazisha wakati wa dharura: shikilia Kupunguza Sauti (simu) au bonyeza Kunyamazisha (kompyuta); tafuta mstari mkuu.', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Somo la 1: Kutafuta Maandiko na Mikutano (0:05 - 0:20)</b>', section_hdr))
    story.append(Paragraph('0:05 &nbsp; Kuzungumzia vichupo vikuu vya urambazaji (Biblia, Machapisho, Mikutano, Funzo la Kibinafsi).', timing_style))
    story.append(Paragraph('0:07 &nbsp; Kufungua Andiko la Siku na kugusa aikoni ya <b>A A</b> ili kuongeza ukubwa wa maandishi kwa ajili ya kusoma kwa starehe.', timing_style))
    story.append(Paragraph('0:10 &nbsp; Fanya Zoezi la Msingi 1.1 (Andiko la Siku na Ukubwa wa Maandishi).', timing_style))
    story.append(Paragraph('0:12 &nbsp; Kufungua kitabu na sura ya Biblia; fanya Zoezi la Msingi 1.2.', timing_style))
    story.append(Paragraph('0:15 &nbsp; Kuzungumzia kichupo cha Mikutano (daftari la Katikati ya Juma na funzo la Mnara wa Mlinzi la Mwisho wa Juma).', timing_style))
    story.append(Paragraph('0:18 &nbsp; Fanya Zoezi la Msingi 1.3 (Kichupo cha Mikutano). (Mwalimu anaonyesha Alama za Kukumbuka Ukurasa na Tafuta).', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Somo la 2: Kupakua na Kutumia Vyombo vya Habari (0:20 - 0:35)</b>', section_hdr))
    story.append(Paragraph('0:20 &nbsp; Kuelewa matumizi bila intaneti: vitu vilivyopakuliwa kwa Wi-Fi vinabaki kwenye kifaa bila kuhitaji data ya simu.', timing_style))
    story.append(Paragraph('0:22 &nbsp; Fanya Zoezi la Msingi 2.1 (Kukagua Wi-Fi na usalama wa data ya simu).', timing_style))
    story.append(Paragraph('0:24 &nbsp; Kupakua kitu ili kukisoma/kukitazama bila intaneti; fanya Zoezi la Msingi 2.2.', timing_style))
    story.append(Paragraph('0:28 &nbsp; Kicheza Sauti (aikoni ya vipokea-sauti); kunyamazisha haraka kwa Kupunguza Sauti (simu) au Kunyamazisha (kompyuta).', timing_style))
    story.append(Paragraph('0:31 &nbsp; Fanya Zoezi la Msingi 2.3 (Kusikiliza Sauti). (Mwalimu anaonyesha jinsi ya kukagua nafasi ya kuhifadhi).', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Somo la 3: Vifaa vya Funzo la Kibinafsi (0:35 - 0:50)</b>', section_hdr))
    story.append(Paragraph('0:35 &nbsp; Kuchagua maneno na sentensi ili kutia alama majibu katika makala za funzo.', timing_style))
    story.append(Paragraph('0:37 &nbsp; Fanya Zoezi la Msingi 3.1 (Tia alama ya njano kwenye jibu).', timing_style))
    story.append(Paragraph('0:40 &nbsp; Kubadili rangi ya alama au kuondoa alama; fanya Zoezi la Msingi 3.2.', timing_style))
    story.append(Paragraph('0:43 &nbsp; Kulinda funzo lako: kutengeneza faili ya nakala ya akiba (.jwlibrary) katika Mipangilio &gt; Hifadhi Nakala na Rejesha.', timing_style))
    story.append(Paragraph('0:46 &nbsp; Fanya Zoezi la Msingi 3.3 (Tengeneza Nakala ya Akiba). (Mwalimu anaonyesha Maelezo na Vibandiko).', timing_style))
    story.append(Spacer(1, 2))

    story.append(Paragraph('<b>Kuhitimisha, Kupitia Tena na Maswali: (0:50 - 1:00)</b>', section_hdr))
    story.append(Paragraph('0:50 &nbsp; Dakika 10 za ziada kwa ajili ya kupitia tena, maswali, au muda zaidi. Msaada wa hiari wa mtu mmoja mmoja kwa dakika 15 baadaye.', timing_style))
    story.append(Spacer(1, 2))

    story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=2))
    story.append(Paragraph('<b>MAZOEZI YA MSINGI</b>', ex_hdr))

    story.append(Paragraph('<b>1.1</b> Gusa <b>Andiko la Siku</b> (aikoni ya jua). Gusa aikoni ya <b>A A</b> iliyo juu kisha telezesha ili kuongeza ukubwa wa maandishi.', ex_style))
    story.append(Paragraph('<b>1.2</b> Gusa <b>Biblia</b>. Chagua kitabu (kwa mfano, <i>Mathayo</i>) na sura (kwa mfano, <i>5</i>) ili uanze kusoma.', ex_style))
    story.append(Paragraph('<b>1.3</b> Gusa <b>Mikutano</b>. Fungua moja kwa moja makala ya Funzo la <i>Mnara wa Mlinzi</i> la juma hili kwa mguso mmoja.', ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph('<b>2.1</b> Hakikisha kifaa chako kimeunganishwa kwenye Wi-Fi ili kuokoa data ya simu.', ex_style))
    story.append(Paragraph('<b>2.2</b> Katika Machapisho au Mikutano, gusa <b>aikoni ya Wingu</b> kwenye kitu cha funzo ili ukipakue na kukitumia bila intaneti.', ex_style))
    story.append(Paragraph('<b>2.3</b> Fungua Andiko la Siku au Biblia. Gusa <b>Vipokea-sauti</b> ili kusikiliza; zima kwa <b>Kupunguza Sauti</b> (au kitufe cha Kunyamazisha).', ex_style))
    story.append(Spacer(1, 1.5))

    story.append(Paragraph('<b>3.1</b> Katika fungu la 1 la funzo la <i>Mnara wa Mlinzi</i>, bonyeza na uburute kidole kwenye jibu kisha gusa <b>Njano</b>.', ex_style))
    story.append(Paragraph('<b>3.2</b> Gusa tena maandishi yenye alama ili kubadili rangi (bluu au kijani), au gusa aikoni ya pipa la taka ili kufuta.', ex_style))
    story.append(Paragraph('<b>3.3</b> Fungua Mipangilio &gt; Hifadhi Nakala na Rejesha kisha gusa <b>Tengeneza Nakala ya Akiba</b> ili kuhifadhi alama zako za funzo.', ex_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph('<i>Taarifa ya Kisheria: JW Library ni alama ya biashara iliyosajiliwa ya Watch Tower Bible and Tract Society of Pennsylvania. Ratiba hii ya darasa ni msaada wa mafunzo unaojitegemea, usio wa kibiashara, na haihusiani na wala haikubaliwi rasmi na Watch Tower au Mashahidi wa Yehova.</i>', disclaimer_style))

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

    # ==================== UKURASA 1 ====================
    story.append(Paragraph('Mtaala wa Mafunzo ya JW Library', doc_title))
    story.append(Spacer(1, 4))
    story.append(Paragraph('<b>KUMBUKA:</b> Maelekezo rasmi kuhusu kutumia JW Library yanapatikana kwenye JW.ORG (https://www.jw.org/sw/msaada-mtandaoni/jw-library/)', note_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Kuhusu Mafunzo ya JW Library', h1_style))
    story.append(Paragraph(
        'Mtaala huu umekusudiwa kwa ajili ya yeyote anayefundisha au kuwaongoza wanafunzi kwa kutumia '
        '<i>Mafunzo ya JW Library</i> yanayoambatana nao. Kozi imepangwa katika masomo matatu ya dakika 15 kila moja: '
        '<b>Kutafuta Maandiko na Mikutano</b>, <b>Kupakua na Kutumia Vyombo vya Habari</b>, na <b>Vifaa vya Funzo la Kibinafsi</b>. '
        'Dakika 10 za kuhitimisha zilizotengwa hutoa muda wa ziada wa kutosha ili walimu wasihisi wakiharakishwa kamwe. '
        'Kabla darasa halijaanza, wanafunzi wanapaswa kupewa nakala ya vitu vya mafunzo na '
        'kukumbushwa kuwa wamesakinisha programu kwenye kifaa chao mapema.',
        body_style
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        '<i>Ratiba ya Darasa la JW Library</i> hutumika kama kielelezo wakati wa kupanga ratiba ya kipindi. Dakika tano '
        'zimetengwa mwanzoni ili kuwaonyesha wanafunzi mpangilio wa kifaa chao. Kila somo la dakika 15 linakazia matendo matatu '
        'ya msingi ya vitendo, huku mada ngumu zikiachiwa maonyesho mafupi ya mwalimu. Kipindi kizima huchukua '
        'dakika 60, na kinaweza kurefushwa hadi dakika 75 au 90 kwa vikundi vinavyotaka msaada zaidi wa mtu mmoja mmoja.',
        body_style
    ))

    story.append(Paragraph('Wanaolengwa', h1_style))
    story.append(Paragraph(
        'Mafunzo haya yameandaliwa kwa ajili ya watu wanaojua mambo ya msingi ya kutumia simu janja, kompyuta kibao, au kompyuta. '
        'Wanafunzi wanapaswa kuwa wanaweza kutumia skrini ya kugusa au kipanya. Uzoefu wa awali wa kutumia programu ya JW Library '
        'unasaidia lakini hauhitajiki.',
        body_style
    ))

    story.append(Paragraph('Matokeo ya Kujifunza', h1_style))
    story.append(Paragraph('Baada ya kukamilisha mafunzo haya, wanafunzi wataweza:', body_style))
    story.append(Paragraph('&bull; Kuhama kati ya Biblia, Machapisho, Mikutano, na Funzo la Kibinafsi.', bullet_style))
    story.append(Paragraph('&bull; Kufungua Andiko la Siku na kuongeza ukubwa wa maandishi kwa kutumia kitufe cha A A.', bullet_style))
    story.append(Paragraph('&bull; Kupata makala za funzo za mikutano ya kila juma kwa mguso mmoja kutoka kwenye kichupo cha Mikutano.', bullet_style))
    story.append(Paragraph('&bull; Kuelewa usomaji bila intaneti na kupakua machapisho kwa Wi-Fi ili kuokoa data ya simu.', bullet_style))
    story.append(Paragraph('&bull; Kutumia kicheza sauti (aikoni ya vipokea-sauti) na kunyamazisha haraka sauti isiyotarajiwa.', bullet_style))
    story.append(Paragraph('&bull; Kutia alama majibu katika makala za funzo kwa rangi mbalimbali na kuondoa alama.', bullet_style))
    story.append(Paragraph('&bull; Kutengeneza nakala ya akiba (faili ya .jwlibrary) ili kulinda kumbukumbu za funzo.', bullet_style))

    story.append(Paragraph('Mahitaji ya Awali na Madokezo ya Maandalizi', h1_style))
    story.append(Paragraph('Kabla ya kuhudhuria kozi hii, wanafunzi wanapaswa:', body_style))
    story.append(Paragraph('&bull; Kufika <b>dakika 10–15 mapema</b> ili wasaidizi wawasaidie kuhusu Wi-Fi na kuandaa Biblia/Andiko la Siku.', bullet_style))
    story.append(Paragraph('&bull; Kuwa na kifaa kinachotumika chenye <b>Android 8.0+</b>, <b>iOS 15.0+</b>, <b>macOS M1+</b>, au <b>Windows 10 v2004+</b>.', bullet_style))
    story.append(Paragraph('&bull; Kufika wakiwa na <b>betri yenye chaji kamili</b> (au walete chaja).', bullet_style))
    story.append(Paragraph('&bull; Kuweka kwa muda <b>skrini izime baada ya dakika 2 au 5</b> ili skrini isizime.', bullet_style))
    story.append(Paragraph('&bull; Kuwa na angalau <b>GB 2 hadi 4</b> za nafasi ya kuhifadhi (au kadi ya SD iliyowekwa) kwa ajili ya faili za vyombo vya habari.', bullet_style))
    story.append(Paragraph('&bull; Kuunganisha kwenye Wi-Fi kabla ya kupakua video au rekodi za sauti.', bullet_style))

    # ==================== UKURASA 2 ====================
    story.append(PageBreak())

    story.append(Paragraph('Mtaala wa Mafunzo ya JW Library', doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Somo la 1: Kutafuta Maandiko na Mikutano (Dakika 15)', h1_style))
    story.append(Paragraph(
        'Somo hili linawajulisha wanafunzi jinsi ya kuhama kwa urahisi kati ya sehemu kuu za programu ya JW Library. '
        'Walimu wanapaswa kueleza mahali mstari wa urambazaji ulipo kulingana na vifaa vilivyopo (mstari wa chini kwenye iOS '
        'na Android za kisasa; menyu ya juu kwenye Windows). Onyesha jinsi kugusa aikoni ya <b>A A</b> kunavyoongeza ukubwa wa maandishi ili '
        'kusoma kwa starehe, na jinsi <b>kichupo cha Mikutano</b> kinavyowezesha kufungua kwa mguso mmoja machapisho ya mikutano ya kila juma.',
        body_style
    ))

    story.append(Paragraph('Mada (dakika 10)', h2_style))
    story.append(Paragraph('&bull; Vichupo Vikuu vya Urambazaji (Biblia, Machapisho, Mikutano, Funzo la Kibinafsi)', bullet_style))
    story.append(Paragraph('&bull; Andiko la Siku na Kurekebisha Ukubwa wa Maandishi (kitufe cha A A ili kuongeza ukubwa wa herufi)', bullet_style))
    story.append(Paragraph('&bull; Kufungua kitabu na sura fulani ya Biblia (kwa mfano, Mathayo 5)', bullet_style))
    story.append(Paragraph('&bull; Kichupo cha Mikutano (kufungua daftari la Katikati ya Juma na makala ya funzo la Mnara wa Mlinzi la Mwisho wa Juma)', bullet_style))
    story.append(Paragraph('&bull; <i>Mwalimu Anaonyesha:</i> Alama za Kukumbuka Ukurasa, Historia, na Tafuta (kwa ajili ya kuzoeza nyumbani)', bullet_style))

    story.append(Paragraph('Mazoezi ya Msingi ya Vitendo (dakika 5)', h2_style))
    story.append(Paragraph('&bull; <b>Msingi 1.1:</b> Fungua Andiko la Siku na ugusa <b>A A</b> ili maandishi yawe makubwa na wazi.', bullet_style))
    story.append(Paragraph('&bull; <b>Msingi 1.2:</b> Gusa Biblia, chagua kitabu (Mathayo), na ufungue sura ya 5.', bullet_style))
    story.append(Paragraph('&bull; <b>Msingi 1.3:</b> Fungua kichupo cha Mikutano na ugusa makala ya Funzo la Mnara wa Mlinzi la juma hili.', bullet_style))

    story.append(Paragraph('Maelezo kwa Mwezeshaji kwa Ajili ya Somo la 1', h2_style))
    story.append(Paragraph(
        'Andaa kliniki ya dakika 15 kwa wanaofika mapema ili wasaidizi wahakikishe kwamba Biblia na Andiko la Siku viko tayari. Mwanzoni mwa darasa, '
        'fanya ukaguzi wa utayari wa sekunde 30: waombe wanafunzi wainue mikono ikiwa wanahitaji msaada wa kupakua ili wasaidizi '
        'wawasaidie kwa utulivu huku ukiendelea. Fundisha jinsi ya kunyamazisha kifaa mapema (Kupunguza Sauti kilicho kando kwenye simu; Kunyamazisha kwenye kibodi ya kompyuta) '
        'ili kuondoa wasiwasi. Wasaidizi wahakikishe kwamba wanafunzi wamefaulu kuongeza ukubwa wa maandishi kwa kitufe cha A A.',
        body_style
    ))

    story.append(Paragraph('Baada ya kukamilisha somo hili, wanafunzi wataweza:', h2_style))
    story.append(Paragraph('&bull; Kuhama kwa urahisi kati ya sehemu zote kuu za programu.', bullet_style))
    story.append(Paragraph('&bull; Kuongeza ukubwa wa maandishi katika programu yote ili kusoma bila kujikaza.', bullet_style))
    story.append(Paragraph('&bull; Kufungua sura yoyote ya Biblia na kufikia makala za mikutano ya kila juma kwa mguso mmoja.', bullet_style))

    # ==================== UKURASA 3 ====================
    story.append(PageBreak())

    story.append(Paragraph('Mtaala wa Mafunzo ya JW Library', doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Somo la 2: Kupakua na Kutumia Vyombo vya Habari (Dakika 15)', h1_style))
    story.append(Paragraph(
        'Somo hili linaeleza jinsi usomaji bila intaneti unavyofanya kazi na linaonyesha jinsi ya kupakua machapisho na vyombo vya habari. '
        'Kazia kwamba kitu kikishapakuliwa kwa Wi-Fi, kinabaki kwenye kifaa daima bila kuhitaji intaneti '
        'wala data ya simu mikutanoni. Tambulisha kicheza sauti (aikoni ya vipokea-sauti) ili wanafunzi waweze kusikiliza maandishi yakisomwa kwa sauti.',
        body_style
    ))

    story.append(Paragraph('Mada (dakika 10)', h2_style))
    story.append(Paragraph('&bull; Kuelewa Matumizi Bila Intaneti: kusoma na kusikiliza bila mtandao wa simu', bullet_style))
    story.append(Paragraph('&bull; Kuunganisha kwenye Wi-Fi kabla ya kupakua ili kuokoa kiwango cha data ya simu', bullet_style))
    story.append(Paragraph('&bull; Kupakua machapisho na vyombo vya habari (kutambua aikoni ya Wingu)', bullet_style))
    story.append(Paragraph('&bull; Kutumia Kicheza Sauti na kunyamazisha haraka wakati wa dharura (Kupunguza Sauti kwenye simu; Kunyamazisha kwenye kompyuta)', bullet_style))
    story.append(Paragraph('&bull; <i>Mwalimu Anaonyesha:</i> Kupanga kulingana na Ukubwa Zaidi ili kukagua nafasi ya kuhifadhi na kufuta faili', bullet_style))

    story.append(Paragraph('Mazoezi ya Msingi ya Vitendo (dakika 5)', h2_style))
    story.append(Paragraph('&bull; <b>Msingi 2.1:</b> Hakikisha juu ya skrini kwamba kifaa kimeunganishwa kwenye Wi-Fi.', bullet_style))
    story.append(Paragraph('&bull; <b>Msingi 2.2:</b> Gusa aikoni ya Wingu kwenye chapisho la funzo au video ili kulipakua.', bullet_style))
    story.append(Paragraph('&bull; <b>Msingi 2.3:</b> Fungua Andiko la Siku au Biblia, gusa Vipokea-sauti ili kusikiliza; zima kwa Kupunguza Sauti au Kunyamazisha.', bullet_style))

    story.append(Paragraph('Maelezo kwa Mwezeshaji kwa Ajili ya Somo la 2', h2_style))
    story.append(Paragraph(
        'Wahakikishie wanafunzi wenye vifurushi vidogo vya data kwamba hawatatumia data ya simu mikutanoni ikiwa watapakua '
        'mapema kwa Wi-Fi. Zoezeni waziwazi jinsi ya kunyamazisha wakati wa dharura: watu wasiozoea teknolojia mara nyingi huogopa sauti inayocheza kwa bahati mbaya; '
        'kujua jinsi ya kunyamazisha mara moja (kushikilia Kupunguza Sauti kilicho kando kwenye simu au kubonyeza Kunyamazisha kwenye kompyuta) kunawapa utulivu kamili wa akili.',
        body_style
    ))

    story.append(Paragraph('Baada ya kukamilisha somo hili, wanafunzi wataweza:', h2_style))
    story.append(Paragraph('&bull; Kupakua machapisho kwa usalama kwa Wi-Fi bila kutumia data ya simu.', bullet_style))
    story.append(Paragraph('&bull; Kufungua na kusoma machapisho yaliyopakuliwa bila intaneti kwenye mikutano ya kutaniko.', bullet_style))
    story.append(Paragraph('&bull; Kucheza, kusitisha, na kunyamazisha mara moja usomaji wa sauti wa maandiko na makala.', bullet_style))

    # ==================== UKURASA 4 ====================
    story.append(PageBreak())

    story.append(Paragraph('Mtaala wa Mafunzo ya JW Library', doc_title))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width='100%', thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    story.append(Paragraph('Somo la 3: Vifaa vya Funzo la Kibinafsi (Dakika 15)', h1_style))
    story.append(Paragraph(
        'Somo hili linazungumzia kutia alama makala za funzo kwa ajili ya mikutano na kulinda kumbukumbu za funzo la kibinafsi. '
        'Onyesha jinsi ya kuchagua na kutia alama ya njano kwenye maandishi, kubadili rangi za alama, na kufuta alama. '
        'Malizia kwa hatua muhimu ya kutengeneza faili ya nakala ya akiba ya <code>.jwlibrary</code> katika Mipangilio ili '
        'alama za funzo la kibinafsi zisipotee kamwe.',
        body_style
    ))

    story.append(Paragraph('Mada (dakika 10)', h2_style))
    story.append(Paragraph('&bull; Kuchagua maandishi kwa kubonyeza taratibu na kuburuta ili kutia alama', bullet_style))
    story.append(Paragraph('&bull; Kuchagua rangi za alama (Njano, Bluu, Kijani)', bullet_style))
    story.append(Paragraph('&bull; Kugusa maandishi yenye alama ili kubadili rangi au kufuta kwa aikoni ya pipa la taka', bullet_style))
    story.append(Paragraph('&bull; <b>Ulinzi wa Habari:</b> Kutengeneza faili ya nakala ya akiba (Mipangilio &gt; Hifadhi Nakala na Rejesha)', bullet_style))
    story.append(Paragraph('&bull; <i>Mwalimu Anaonyesha:</i> Kuongeza maelezo, Vibandiko, na kuangalia kichupo cha Funzo la Kibinafsi', bullet_style))

    story.append(Paragraph('Mazoezi ya Msingi ya Vitendo (dakika 5)', h2_style))
    story.append(Paragraph('&bull; <b>Msingi 3.1:</b> Fungua makala inayofuata ya Mnara wa Mlinzi na utie alama ya njano kwenye jibu katika fungu la 1.', bullet_style))
    story.append(Paragraph('&bull; <b>Msingi 3.2:</b> Gusa jibu lenye alama ili kubadili kuwa bluu, au gusa aikoni ya pipa la taka ili kufuta.', bullet_style))
    story.append(Paragraph('&bull; <b>Msingi 3.3:</b> Fungua Mipangilio &gt; Hifadhi Nakala na Rejesha kisha gusa <b>Tengeneza Nakala ya Akiba</b>.', bullet_style))

    story.append(Paragraph('Kuhitimisha na Mapendekezo kwa Mwezeshaji (0:50 - 1:00)', h2_style))
    story.append(Paragraph(
        '• <b>Kliniki ya Maandalizi Kabla ya Darasa:</b> Kufungua milango dakika 15 mapema ili wasaidizi waandae vifaa kunazuia msongamano wa Wi-Fi.<br/>'
        '• <b>Mazoea ya Kunyamazisha Wakati wa Dharura:</b> Kufundisha kitufe cha Kupunguza Sauti mapema kunaondoa hofu ya sauti isiyotarajiwa.<br/>'
        '• <b>Dakika 10 za Ziada:</b> Tumia dakika hizi za kuhitimisha kupitia tena yaliyotimizwa, kujibu maswali, au kufidia muda wa ziada.<br/>'
        '• <b>Wasaidizi wa Mezani:</b> Kuwa na wasaidizi 1 au 2 wanaozunguka chumbani kuwasaidia watu mmoja mmoja kunazuia darasa lisicheleweshwe.<br/>'
        '• <b>Karatasi za Kugawa (Inapofaa):</b> Kuwa na nakala zilizochapishwa za Ratiba ya Darasa ya ukurasa 1 mezani husaidia mahali ambapo data au Wi-Fi ni haba.<br/>'
        '• <b>Kadi za QR Mezani au Kwenye Skrini (Hiari):</b> Kuonyesha msimbo wa QR kwenye skrini au kuweka kadi za QR mezani huwaruhusu wanafunzi kufungua mwongozo kwa kamera ya simu.<br/>'
        '• <b>Weka Kwenye Skrini ya Kwanza (Hiari):</b> Kupendekeza "Weka Kwenye Skrini ya Kwanza" (Add to Home Screen) huhifadhi mwongozo kwenye simu ili kuupitia baadaye hata bila intaneti.<br/>'
        '• <b>Kliniki ya Baada ya Darasa:</b> Jitolee kubaki dakika 15 baada ya darasa kwa ajili ya yeyote anayetaka msaada wa mtu mmoja mmoja kuhusu faili yake ya nakala ya akiba.',
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph('Baada ya kukamilisha somo hili, wanafunzi wataweza:', h2_style))
    story.append(Paragraph('&bull; Kutia alama majibu kwa ajili ya mikutano na kurekebisha au kufuta alama kwa uhakika.', bullet_style))
    story.append(Paragraph('&bull; Kuhifadhi kwa usalama nakala ya akiba ya maelezo na alama zao za funzo katika faili ya .jwlibrary.', bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)


if __name__ == '__main__':
    program_pdf = 'D:/cs/JWLibrary/Ratiba ya Darasa la JW Library.pdf'
    curriculum_pdf = 'D:/cs/JWLibrary/Mtaala wa Mafunzo ya JW Library.pdf'

    build_class_program(program_pdf)
    build_curriculum(curriculum_pdf)

    r1 = pypdf.PdfReader(program_pdf)
    r2 = pypdf.PdfReader(curriculum_pdf)
    print(f'IMEFANIKIWA: PDF ya Ratiba imetengenezwa ikiwa na ukurasa/kurasa {len(r1.pages)}.')
    print(f'IMEFANIKIWA: PDF ya Mtaala imetengenezwa ikiwa na ukurasa/kurasa {len(r2.pages)}.')
