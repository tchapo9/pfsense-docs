from docx import Document
from docx.oxml.ns import qn
from pathlib import Path
import re

INPUT_DOCX = Path(r'C:\Users\TCHEDRE\Desktop\Honorine\portsentry.docx')
OUTPUT_DOC = Path('docs/portsentry/index.mdx')
OUTPUT_IMG_DIR = Path('static/img/portsentry')

OUTPUT_IMG_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DOC.parent.mkdir(parents=True, exist_ok=True)

COMMAND_PATTERNS = [
    r'^(#|sudo |apt |apt-get |systemctl |service |nano |vi |vim |ls |cd |ip |ifconfig |route |mount |echo |cat |grep |awk |netstat |openssl |wget |curl |scp |python |chmod |chown |docker |kubectl |ufw |firewall-cmd |usermod |adduser |useradd |passwd |echo |sed |tcpdump |iptables |nmap |mysql|nginx|haproxy|apache2|systemctl|journalctl|reboot|shutdown|ping|traceroute|ssh|scp|rsync|telnet|ftp|mount|umount|curl|wget|mysqladmin|service )',
]
COMMAND_RE = re.compile('|'.join(COMMAND_PATTERNS), re.IGNORECASE)

IMAGE_REL_MAP = {}
IMAGE_COUNTER = 0


def is_command_paragraph(text: str) -> bool:
    if not text:
        return False
    if text.startswith('#'):
        return True
    if COMMAND_RE.match(text):
        return True
    if text.startswith('http://') or text.startswith('https://'):
        return False
    if '/' in text and any(segment.startswith('.') or segment.startswith('/') for segment in text.split()):
        return True
    return False


def rel_id_from_run(run):
    rel_ids = []
    for blip in run._r.xpath('.//a:blip'):
        embed = blip.get(qn('r:embed'))
        if embed:
            rel_ids.append(embed)
    return rel_ids


def save_image(rel_id: str) -> str:
    global IMAGE_COUNTER
    if rel_id in IMAGE_REL_MAP:
        return IMAGE_REL_MAP[rel_id]
    rel = doc.part.rels[rel_id]
    image_part = rel.target_part
    suffix = Path(image_part.partname).suffix
    IMAGE_COUNTER += 1
    output_name = f'image_{IMAGE_COUNTER:03d}{suffix}'
    output_path = OUTPUT_IMG_DIR / output_name
    with open(output_path, 'wb') as f:
        f.write(image_part.blob)
    IMAGE_REL_MAP[rel_id] = output_name
    return output_name


def paragraph_to_markdown(paragraph) -> str:
    text = paragraph.text.strip()
    if paragraph.style is not None:
        style_name = paragraph.style.name
    else:
        style_name = ''

    if style_name.startswith('Heading'):
        level = int(style_name.replace('Heading ', '').strip())
        if level < 1:
            level = 1
        if level > 6:
            level = 6
        return f"{'#' * level} {text}"

    if style_name in ('Intense Quote', 'Quote'):
        return f'> {text}'

    if paragraph._p.pPr is not None and paragraph._p.pPr.numPr is not None:
        return f'* {text}'

    if is_command_paragraph(text):
        return f'```bash\n{text}\n```'

    return text


def paragraph_image_markdown(paragraph) -> list[str]:
    outputs = []
    for run in paragraph.runs:
        for rel_id in rel_id_from_run(run):
            image_name = save_image(rel_id)
            outputs.append(f'![Screenshot](/img/portsentry/{image_name})')
    return outputs


def element_to_markdown(element) -> list[str]:
    tag = element.tag
    if tag == qn('w:p'):
        paragraph = Paragraph(element, doc)
        lines = []
        md = paragraph_to_markdown(paragraph)
        if md:
            lines.append(md)
        lines.extend(paragraph_image_markdown(paragraph))
        return lines
    if tag == qn('w:tbl'):
        rows = []
        for row_el in element.findall('.//w:tr', namespaces=element.nsmap):
            cols = [cell.text.strip().replace('\n', ' ') if cell.text else '' for cell in row_el.findall('.//w:t', namespaces=element.nsmap)]
            rows.append(cols)
        if not rows:
            return []
        header = rows[0]
        md = ['| ' + ' | '.join(header) + ' |', '| ' + ' | '.join('---' for _ in header) + ' |']
        for row in rows[1:]:
            md.append('| ' + ' | '.join(row) + ' |')
        return md
    return []


if not INPUT_DOCX.exists():
    raise FileNotFoundError(f'Input file not found: {INPUT_DOCX}')

doc = Document(INPUT_DOCX)

from docx.text.paragraph import Paragraph

lines = [
    '---',
    'title: "PortSentry Documentation"',
    'description: "Documentation imported from portsentry.docx"',
    '---',
    '',
    '# PortSentry Documentation',
    '',
]

for child in doc.element.body:
    element_lines = element_to_markdown(child)
    if element_lines:
        lines.extend(element_lines)
        lines.append('')

OUTPUT_DOC.write_text('\n'.join(lines), encoding='utf-8')
print(f'Wrote {OUTPUT_DOC} ({len(lines)} lines)')
print(f'Extracted {len(IMAGE_REL_MAP)} images to {OUTPUT_IMG_DIR}')
