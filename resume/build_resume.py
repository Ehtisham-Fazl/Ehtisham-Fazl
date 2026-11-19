"""Edit only eight Stewart description text operators in the supplied PDF.

All font resources, text positions, page sizes, annotations, other content,
and the original four-page template are retained.
"""
import re
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, ArrayObject, ByteStringObject

source = Path(__file__).resolve().parent.parent / 'assets' / 'Ehtisham-Fazal-Profile.pdf'
target = Path(__file__).resolve().parent.parent / 'assets' / 'Ehtisham-Fazal-Resume.pdf'
reader = PdfReader(source)
writer = PdfWriter()
writer.clone_document_from_reader(reader)
page = writer.pages[0]
font = page['/Resources']['/Font']['/F15'].get_object()
cmap = font['/ToUnicode'].get_object().get_data().decode('ascii')
glyph_to_unicode = {}
for block in re.findall(r'beginbfchar(.*?)endbfchar', cmap, re.S):
    for glyph, code in re.findall(r'<([0-9a-f]+)>\s*<([0-9a-f]+)>', block):
        glyph_to_unicode[int(glyph, 16)] = bytes.fromhex(code).decode('utf-16-be')
for block in re.findall(r'beginbfrange(.*?)endbfrange', cmap, re.S):
    for start, end, value in re.findall(r'<([0-9a-f]+)>\s*<([0-9a-f]+)>\s*<([0-9a-f]+)>', block):
        for glyph in range(int(start,16), int(end,16)+1):
            glyph_to_unicode[glyph] = chr(int(value,16) + glyph-int(start,16))
unicode_to_glyph = {v:k for k,v in glyph_to_unicode.items()}
descendant = font['/DescendantFonts'][0].get_object()
w = descendant['/W']
assert int(w[0]) == 0 and len(w) == 2
widths = [int(x) for x in w[1]]

old_lines = [
    '* Working on Generative AI and LLM based solutions for real world business',
    'use cases',
    '* Building AI agents and intelligent workflows using modern agentic AI',
    'frameworks',
    '* Working on model evaluation, inference optimization, and improving AI',
    'system reliability',
    '* Working closely with engineering teams to turn AI ideas into usable,',
    'production ready solution',
]
new_lines = [
    '* Building Generative AI solutions and multi-agent systems for coding',
    'tasks using coordinated reasoning and tool integration.',
    '* Automating internal workflows and data processing through AI',
    'pipelines with engineering teams for production integration.',
    '* Evaluating open-weight models and developing evaluation frameworks',
    'for output quality, inference efficiency, and production suitability.',
    '* Optimizing inference and model reliability for production-ready AI',
    'applications and intelligent workflows.',
]
replacements = dict(zip(old_lines, new_lines))
for line in new_lines:
    assert all(c in unicode_to_glyph for c in line)
    width = sum(widths[unicode_to_glyph[c]] for c in line) * 10.5 / 1000
    assert width <= 366, (line, width)

def decode(value):
    data = value.original_bytes
    return ''.join(glyph_to_unicode[int.from_bytes(data[i:i+2], 'big')] for i in range(0,len(data),2))

stream = ContentStream(page.get_contents(), writer)
changed = []
for args, operator in stream.operations:
    if operator != b'TJ' or len(args[0]) != 1:
        continue
    value = args[0][0]
    if not hasattr(value, 'original_bytes'):
        continue
    text = decode(value)
    if text in replacements:
        new = replacements[text]
        data = b''.join(unicode_to_glyph[c].to_bytes(2, 'big') for c in new)
        args[0] = ArrayObject([ByteStringObject(data)])
        changed.append(text)
assert changed == old_lines, changed
page.replace_contents(stream)
with target.open('wb') as f:
    writer.write(f)

original = PdfReader(source)
updated = PdfReader(target)
assert len(updated.pages) == len(original.pages) == 4
for i, (before, after) in enumerate(zip(original.pages, updated.pages)):
    assert before.mediabox == after.mediabox
    before_text, after_text = before.extract_text(), after.extract_text()
    if i == 0:
        for old in old_lines:
            before_text = before_text.replace(old, '')
        for new in new_lines:
            assert new in after_text
            after_text = after_text.replace(new, '')
        assert before_text == after_text, 'Content outside Stewart changed'
    else:
        assert before_text == after_text
        assert before.get_contents().get_data() == after.get_contents().get_data()
print('PASS: original four-page template preserved; only eight Stewart text lines updated.')
print(target)
