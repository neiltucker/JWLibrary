"""Make the Ga QR code (PNG + SVG) and the printable table cards PDF.

Writes to the repository root (two folders up from this script):
  QR_Ga_gaa.png, QR_Ga_gaa.svg, Table_Cards_Ga_gaa.pdf

Needs: pip install qrcode pillow reportlab
If you publish the guide somewhere else, change PAGE_URL first (see README guideline 2).
"""
import os
import qrcode
import qrcode.image.svg
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PAGE_URL = 'https://neiltucker.github.io/JWLibrary/gaa.html'

TITLE = 'Okɛ JW Library Lɛ Atsu Nii'
LINE1 = 'Okɛ ofoŋ kamera lɛ askani okadi nɛɛ'
LINE2 = 'koni ogbele kasemɔ wolo lɛ.'
FOOT = 'Independent training aid. Not affiliated with Watch Tower or JW.ORG.'

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

# Fonts that contain the Ga letters ɛ ɔ ŋ (same search order as generate_pdfs.py)
_DEJAVU = ('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf')
CANDIDATES = [
    tuple(os.path.join(HERE, 'fonts', n) for n in _DEJAVU),
    tuple('/usr/share/fonts/truetype/dejavu/' + n for n in _DEJAVU),
    ('C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf'),
    ('C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/segoeuib.ttf'),
    ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'),
]
FONT, FONT_BOLD = 'Helvetica', 'Helvetica-Bold'
for reg, bold in CANDIDATES:
    if os.path.isfile(reg) and os.path.isfile(bold):
        f1, f2 = TTFont('GaSans', reg), TTFont('GaSans-Bold', bold)
        if all(ord(c) in f.face.charToGlyph for f in (f1, f2) for c in 'ɛɔŋ'):
            pdfmetrics.registerFont(f1)
            pdfmetrics.registerFont(f2)
            FONT, FONT_BOLD = 'GaSans', 'GaSans-Bold'
            break
if FONT == 'Helvetica':
    print('WARNING: no font with ɛ ɔ ŋ found; put DejaVuSans.ttf and DejaVuSans-Bold.ttf in a "fonts" folder next to this script.')


def make_qr():
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=24, border=4)
    qr.add_data(PAGE_URL)
    qr.make(fit=True)
    png_path = os.path.join(ROOT, 'QR_Ga_gaa.png')
    qr.make_image(fill_color='black', back_color='white').save(png_path)

    qr_svg = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4,
                           image_factory=qrcode.image.svg.SvgPathImage)
    qr_svg.add_data(PAGE_URL)
    qr_svg.make(fit=True)
    svg_path = os.path.join(ROOT, 'QR_Ga_gaa.svg')
    qr_svg.make_image().save(svg_path)
    return png_path, svg_path


def make_cards(png_path):
    pdf_path = os.path.join(ROOT, 'Table_Cards_Ga_gaa.pdf')
    W, H = letter
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setTitle('Table Cards — Ga')
    img = ImageReader(png_path)
    cw, ch = W / 2, H / 2
    for col in range(2):
        for row in range(2):
            x0, y0 = col * cw, row * ch
            cx = x0 + cw / 2
            top = y0 + ch
            c.setFillColor(colors.HexColor('#1e3a8a'))
            c.setFont(FONT_BOLD, 15)
            c.drawCentredString(cx, top - 50, TITLE)
            c.setFillColor(colors.HexColor('#334155'))
            c.setFont(FONT, 9.5)
            c.drawCentredString(cx, top - 70, LINE1)
            c.drawCentredString(cx, top - 83, LINE2)
            size = 170
            c.drawImage(img, cx - size / 2, top - 105 - size, width=size, height=size)
            c.setFillColor(colors.HexColor('#475569'))
            c.setFont(FONT, 7.5)
            c.drawCentredString(cx, top - 105 - size - 22, PAGE_URL)
            c.setFont(FONT, 5.5)
            c.drawCentredString(cx, top - 105 - size - 36, FOOT)
    # dashed cutting lines
    c.setStrokeColor(colors.HexColor('#94a3b8'))
    c.setDash(3, 3)
    c.line(W / 2, 0, W / 2, H)
    c.line(0, H / 2, W, H / 2)
    c.save()
    return pdf_path


if __name__ == '__main__':
    png, svg = make_qr()
    pdf = make_cards(png)
    for p in (png, svg, pdf):
        print('Written:', p)
