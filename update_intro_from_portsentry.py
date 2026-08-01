from pathlib import Path

source = Path('docs/portsentry/index.mdx')
dest = Path('docs/intro.mdx')
text = source.read_text(encoding='utf-8')
start = text.find('# Introduction')
if start == -1:
    raise ValueError('Unable to find pfSense introduction heading in source file')
output = '---\nsidebar_position: 1\n---\n\n' + text[start:]
dest.write_text(output, encoding='utf-8')
print(f'Updated {dest} from {source} starting at line #Introduction')
