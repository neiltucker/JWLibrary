"""Make the QR codes and printable table cards for every language, and keep the
guide links in the README files pointing to the right web address.

For each language this writes to the repository root:
  QR_<Name>_<code>.png   QR code for screens and slides
  QR_<Name>_<code>.svg   QR code for printing at any size
  Table_Cards_<Name>_<code>.pdf   4 cut-out table cards on one letter-size page

Usage (run from anywhere):
  python make_qr_and_cards.py               all languages, and update README links
  python make_qr_and_cards.py sw gaa        only these languages, and update README links
  python make_qr_and_cards.py --no-readmes  QR codes and cards only

The web address comes from site_config.json ("base_url"). If it is blank, it is
worked out from this repository's GitHub address:
  github.com/<user>/<repo>  ->  https://<user>.github.io/<repo>/

Needs: pip install -r requirements.txt
"""
import glob
import json
import os
import re
import subprocess
import sys

import qrcode
import qrcode.image.svg
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Languages. "page" is the web page for that language ('' = the English home
# page). To add a language, add an entry here and to the "pages" list below.
# ---------------------------------------------------------------------------
LANGUAGES = {
    'en': dict(name='English', file='English_en', page='',
               title='JW Library Tutorial',
               text='Scan this code with your phone camera to open the practice guide.'),
    'sw': dict(name='Kiswahili', file='Kiswahili_sw', page='sw.html',
               title='Mafunzo ya JW Library',
               text='Changanua msimbo huu kwa kamera ya simu yako ili kufungua mwongozo wa mazoezi.'),
    'lg': dict(name='Luganda', file='Luganda_lg', page='lg.html',
               title='Okuyiga Okukozesa JW Library',
               text="Kozesa kamera y'essimu yo ku koodi eno okuggulawo ekitabo ky'okwegezaamu."),
    'din': dict(name='Dinka', file='Dinka_din', page='din.html',
                title='Piööc ë JW Library',
                text='Tïŋ QR code kënë ke camera ë phone du ba athör ë piööc liep. (Scan with your phone camera.)'),
    'gaa': dict(name='Ga', file='Ga_gaa', page='gaa.html',
                title='Okɛ JW Library Lɛ Atsu Nii',
                text='Okɛ ofoŋ kamera lɛ askani okadi nɛɛ koni ogbele kasemɔ wolo lɛ.'),
}
FOOTER = 'Independent training aid. Not affiliated with Watch Tower or JW.ORG.'

# Web pages of this guide. Links in the README files that end in one of these
# (or in "/") are treated as links to the guide and get the new address.
PAGES = ['index.html', 'sw.html', 'lg.html', 'din.html', 'gaa.html']


# ---------------------------------------------------------------------------
# Web address
# ---------------------------------------------------------------------------
def address_from_git():
    """Work out the GitHub Pages address from the repository's 'origin' remote."""
    try:
        remote = subprocess.run(['git', '-C', ROOT, 'config', '--get', 'remote.origin.url'],
                                capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    m = re.search(r'github\.com[:/]+([^/]+)/([^/]+?)(?:\.git)?/?$', remote)
    if not m:
        return None
    user, repo = m.group(1), m.group(2)
    if repo.lower() == f'{user.lower()}.github.io':      # a user site lives at the root
        return f'https://{user.lower()}.github.io/'
    return f'https://{user.lower()}.github.io/{repo}/'


def get_base_url():
    config_path = os.path.join(ROOT, 'site_config.json')
    base = ''
    if os.path.isfile(config_path):
        with open(config_path, encoding='utf-8') as f:
            base = (json.load(f).get('base_url') or '').strip()
    if base:
        source = 'site_config.json'
    else:
        base, source = address_from_git(), 'the GitHub address of this repository'
    if not base:
        sys.exit('Could not work out the web address. Put it in site_config.json, for example:\n'
                 '  { "base_url": "https://yourname.github.io/YourRepo/" }')
    if not base.endswith('/'):
        base += '/'
    print(f'Web address: {base}  (from {source})')
    return base


# ---------------------------------------------------------------------------
# Fonts: the shared "fonts" folder first, then installed fonts.
# ---------------------------------------------------------------------------
def setup_fonts(sample_text):
    candidates = [
        (os.path.join(ROOT, 'fonts', 'DejaVuSans.ttf'), os.path.join(ROOT, 'fonts', 'DejaVuSans-Bold.ttf')),
        ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
        ('C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/arialbd.ttf'),
        ('C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/segoeuib.ttf'),
        ('/System/Library/Fonts/Supplemental/Arial.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'),
    ]
    needed = {c for c in sample_text if not c.isspace()}
    for reg, bold in candidates:
        if not (os.path.isfile(reg) and os.path.isfile(bold)):
            continue
        try:
            f1, f2 = TTFont('CardSans', reg), TTFont('CardSans-Bold', bold)
        except Exception:
            continue
        if all(ord(c) in f.face.charToGlyph for f in (f1, f2) for c in needed):
            pdfmetrics.registerFont(f1)
            pdfmetrics.registerFont(f2)
            print(f'Font: {reg}')
            return 'CardSans', 'CardSans-Bold'
    print('WARNING: no font with all the needed letters was found, so some letters may not print. '
          'Make sure the "fonts" folder at the top of the repository contains the DejaVu Sans files.')
    return 'Helvetica', 'Helvetica-Bold'


# ---------------------------------------------------------------------------
# QR codes and cards
# ---------------------------------------------------------------------------
def make_qr(url, file_label):
    png_path = os.path.join(ROOT, f'QR_{file_label}.png')
    svg_path = os.path.join(ROOT, f'QR_{file_label}.svg')
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=24, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color='black', back_color='white').save(png_path)
    qr_svg = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4,
                           image_factory=qrcode.image.svg.SvgPathImage)
    qr_svg.add_data(url)
    qr_svg.make(fit=True)
    qr_svg.make_image().save(svg_path)
    return png_path, svg_path


def wrap(text, font, size, width):
    lines, current = [], ''
    for word in text.split():
        trial = f'{current} {word}'.strip()
        if current and pdfmetrics.stringWidth(trial, font, size) > width:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def fit_size(text, font, size, width, smallest=6):
    while size > smallest and pdfmetrics.stringWidth(text, font, size) > width:
        size -= 0.25
    return size


def make_cards(lang, url, png_path, font, font_bold):
    pdf_path = os.path.join(ROOT, f"Table_Cards_{lang['file']}.pdf")
    W, H = letter
    cw, ch = W / 2, H / 2
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setTitle(f"Table Cards — {lang['name']}")
    img = ImageReader(png_path)
    text_lines = wrap(lang['text'], font, 10.5, 236)
    for col in range(2):
        for row in range(2):
            cx = col * cw + cw / 2
            top = row * ch + ch
            c.setFillColor(colors.HexColor('#1e3a8a'))
            c.setFont(font_bold, fit_size(lang['title'], font_bold, 17, cw - 10))
            c.drawCentredString(cx, top - 50, lang['title'])
            c.setFillColor(colors.HexColor('#1e293b'))
            c.setFont(font, 10.5)
            for i, line in enumerate(text_lines):
                c.drawCentredString(cx, top - 72 - 14 * i, line)
            c.drawImage(img, cx - 100, top - 134 - 200, width=200, height=200)
            c.setFillColor(colors.HexColor('#475569'))
            c.setFont(font, fit_size(url, font, 8.5, cw - 16))
            c.drawCentredString(cx, top - 352, url)
            c.setFont(font, 6.5)
            c.drawCentredString(cx, top - 368, FOOTER)
    # dashed cutting lines
    c.setStrokeColor(colors.HexColor('#94a3b8'))
    c.setLineWidth(0.5)
    c.setDash(4, 4)
    c.line(W / 2, 0, W / 2, H)
    c.line(0, H / 2, W, H / 2)
    c.save()
    return pdf_path


# ---------------------------------------------------------------------------
# README links
# ---------------------------------------------------------------------------
def update_readmes(base):
    new_host = re.match(r'https?://([^/]+)', base).group(1).lower()
    url_re = re.compile(r'https?://[^\s<>()\[\]"\'*`]+')

    def replace(m):
        whole = m.group(0)
        url = whole.rstrip('.,;:!?')          # leave sentence punctuation alone
        trailing = whole[len(url):]
        host = re.match(r'https?://([^/]+)', url).group(1).lower()
        if not (host.endswith('.github.io') or host == new_host):
            return whole
        tail = url.rsplit('/', 1)[1]
        if tail not in ([''] + PAGES):
            return whole
        return base + tail + trailing

    changed = []
    files = [os.path.join(ROOT, 'README.md')] + sorted(glob.glob(os.path.join(ROOT, 'translations', '*', 'README.md')))
    for path in files:
        with open(path, encoding='utf-8', newline='') as f:
            text = f.read()
        new_text = url_re.sub(replace, text)
        if new_text != text:
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(new_text)
            changed.append(os.path.relpath(path, ROOT))
    print('README links updated in: ' + (', '.join(changed) if changed else 'nothing (already correct)'))


def main(args):
    do_readmes = '--no-readmes' not in args
    codes = [a for a in args if not a.startswith('--')] or list(LANGUAGES)
    unknown = [c for c in codes if c not in LANGUAGES]
    if unknown:
        sys.exit(f"Unknown language code(s): {', '.join(unknown)}. Choose from: {', '.join(LANGUAGES)}")
    base = get_base_url()
    font, font_bold = setup_fonts(''.join(LANGUAGES[c]['title'] + LANGUAGES[c]['text'] for c in codes) + FOOTER)
    for code in codes:
        lang = LANGUAGES[code]
        url = base + lang['page']
        png, svg = make_qr(url, lang['file'])
        pdf = make_cards(lang, url, png, font, font_bold)
        print(f"{lang['name']}: {url}")
        for p in (png, svg, pdf):
            print('  Written:', os.path.relpath(p, ROOT))
    if do_readmes:
        update_readmes(base)


if __name__ == '__main__':
    main(sys.argv[1:])
