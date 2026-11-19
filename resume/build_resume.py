"""Insert Stewart into the supplied two-page PDF using its embedded fonts.

Existing text and rules retain their original drawing operators; only body
positions/page breaks and PixelEdge's employment end date change.
"""
from pathlib import Path
from copy import deepcopy
import re
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (ContentStream, ArrayObject, ByteStringObject,
                           FloatObject, NameObject, DecodedStreamObject)

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'EhtishamFazal-Original.pdf'
OUTPUT = HERE.parent / 'assets' / 'EhtishamFazal-Updated.pdf'
reader = PdfReader(SOURCE)
fonts = reader.pages[0]['/Resources']['/Font']
SIZE = 10.9091

def raw(value):
    return value.original_bytes if hasattr(value, 'original_bytes') else bytes(value)

def advance(array, font, size):
    f = fonts[font].get_object()
    start = int(f['/FirstChar'])
    widths = f['/Widths']
    width = 0
    for v in array:
        if isinstance(v, (int, float, FloatObject)):
            width -= float(v)
        else:
            width += sum(float(widths[c-start]) for c in raw(v))
    return width * size / 1000

def flatten(page):
    runs, graphics = [], []
    text, group = False, []
    x = y = cx = 0.
    font, size = None, 0.
    for args, op in ContentStream(page.get_contents(), reader).operations:
        if op == b'BT':
            text = True; x = y = cx = 0.
        elif op == b'ET': text = False
        elif text:
            if op == b'Tf': font, size = str(args[0]), float(args[1])
            elif op == b'Td':
                x += float(args[0]); y += float(args[1]); cx = x
            elif op == b'TJ':
                runs.append(dict(font=font, size=size, x=cx, y=y, array=deepcopy(args[0]), shear=0))
                cx += advance(args[0],font,size)
            else: raise ValueError(f'Unexpected text operator {op}')
        else:
            group.append((deepcopy(args),op))
            if op == b'Q': graphics.append(group); group=[]
    assert not group
    return runs, graphics

def operations(runs, graphics, graphics_shift=0):
    result=[]
    if graphics_shift:
        result += [([],b'q'),([FloatObject(1),FloatObject(0),FloatObject(0),FloatObject(1),FloatObject(0),FloatObject(graphics_shift)],b'cm')]
    for group in graphics: result.extend(group)
    if graphics_shift: result.append(([],b'Q'))
    for run in runs:
        result.extend([
            ([], b'BT'),
            ([NameObject(run['font']), FloatObject(run['size'])], b'Tf'),
            ([FloatObject(1), FloatObject(0), FloatObject(run.get('shear',0)), FloatObject(1), FloatObject(run['x']), FloatObject(run['y'])], b'Tm'),
            ([run['array']], b'TJ'), ([],b'ET'),
        ])
    return result

def write_pages(path, page_runs, page_graphics, shifts=(0,0), annotation_shift=0, prefix1=None):
    writer = PdfWriter(clone_from=reader)
    for i,page in enumerate(writer.pages):
        stream = ContentStream(None,writer)
        stream.operations=(prefix1+operations(page_runs[i],[],0)) if i==0 and prefix1 is not None else operations(page_runs[i],page_graphics[i],shifts[i])
        page.replace_contents(stream)
        if i==1 and annotation_shift:
            for ref in page.get('/Annots',[]):
                a=ref.get_object(); rect=a['/Rect']
                a[NameObject('/Rect')]=ArrayObject([FloatObject(rect[0]),FloatObject(float(rect[1])+annotation_shift),FloatObject(rect[2]),FloatObject(float(rect[3])+annotation_shift)])
    with path.open('wb') as f: writer.write(f)

page1, graphics1 = flatten(reader.pages[0])
page2, graphics2 = flatten(reader.pages[1])
source_operations=ContentStream(reader.pages[0].get_contents(),reader).operations
block_start=0
for i,(args,op) in enumerate(source_operations):
    if op==b'BT': block_start=i
    if op==b'Tf': current_font=str(args[0])
    if op==b'TJ' and current_font=='/F44' and any(hasattr(a,'original_bytes') and b'Senior' in raw(a) for a in args[0]):
        break
else: raise ValueError('Original experience section not found')
prefix1=deepcopy(source_operations[:block_start])
# QA baseline: reconstruct the original without moving or changing any content.
# Baseline generation is performed separately during visual QA.

def encode(text):
    # Computer Modern's original TeX encoding; spaces use TJ word positioning.
    text=text.replace('ffi','\x0e').replace('ff','\x0b').replace('fi','\x0c').replace('fl','\x0d').replace('\u2013','{')
    return text.encode('ascii')

def text_run(text, font, x, y, justify=None, shear=0):
    words=text.split(' ')
    wordspace=383 if font=='/F44' else 333
    array=ArrayObject()
    for i,word in enumerate(words):
        if i: array.append(FloatObject(-wordspace))
        array.append(ByteStringObject(encode(word)))
    if justify and len(words)>1:
        gap=(justify-advance(array,font,SIZE))*1000/SIZE/(len(words)-1)
        array=ArrayObject([FloatObject(float(a)-gap) if isinstance(a,FloatObject) else a for a in array])
    return dict(font=font,size=SIZE,x=x,y=y,array=array,shear=shear)

new_role=[
    text_run('Senior AI Engineer','/F44',88.936,447.418),
    text_run('Jun 2026 \u2013 Present','/F41',0,447.418),
    # Same Computer Modern family with an italic transform for the new employer.
    # The original italic subset lacks the S and w in Stewart; existing italic
    # runs remain untouched.
    text_run('Stewart Pakistan Private Limited, Lahore, Pakistan','/F41',72,433.869,shear=.2),
]
new_role[1]['x']=523.276-advance(new_role[1]['array'],'/F41',SIZE)
new_bullets=[
    'Build multi-agent systems for coding tasks and generative AI applications',
    'Automate internal workflows and data processing through AI pipelines',
    'Develop evaluation frameworks for open-weight models to assess output quality,',
    'inference efficiency, and reliability, and optimize production inference',
]
for i,line in enumerate(new_bullets):
    y=411.353-i*13.549
    if i<3: new_role.append(dict(font='/F48',size=SIZE,x=72,y=y,array=ArrayObject([ByteStringObject(b'\x88')]),shear=0))
    run=text_run(line,'/F41',82.878,y,justify=440.398 if i==2 else None)
    assert advance(run['array'],'/F41',SIZE)<=440.5
    new_role.append(run)

SHIFT1=99.193
old_ml=[deepcopy(run) for run in page1 if run['y']<170]
kept=[deepcopy(run) for run in page1 if run['y']>=170]
senior=[r for r in kept if 170<=r['y']<460]
date_changes=0
for run in senior:
    # The existing right-hand date is a separate normal-font TJ run.
    blob=b''.join(raw(a) for a in run['array'] if not isinstance(a,(int,float,FloatObject)))
    if run['font']=='/F41' and abs(run['y']-447.418)<.1 and b'2024' in blob:
        replacement=text_run('Jan 2024 \u2013 May 2026','/F41',0,run['y'])
        replacement['x']=523.276-advance(replacement['array'],'/F41',SIZE)
        run.update(replacement); date_changes+=1
    run['y']-=SHIFT1
assert date_changes==1
header=[r for r in kept if r not in senior]
# Copy the complete earlier PixelEdge role to the top of page 2. Its final
# original bullet already starts page 2, so the existing content follows it.
offset=758.931-max(r['y'] for r in old_ml)
for run in old_ml: run['y']+=offset
next_y=min(r['y'] for r in old_ml)-13.549
SHIFT2=max(r['y'] for r in page2)-next_y
remaining2=deepcopy(page2)
for run in remaining2: run['y']-=SHIFT2
write_pages(OUTPUT,[new_role+senior,old_ml+remaining2],[graphics1,graphics2],shifts=(0,-SHIFT2),annotation_shift=-SHIFT2,prefix1=prefix1)

result=PdfReader(OUTPUT)
assert len(result.pages)==2
text='\n'.join(p.extract_text() for p in result.pages)
assert 'Stewart Pakistan Private Limited' in text
assert 'Jun 2026' in text and 'May 2026' in text
assert min(r['y'] for r in senior)>80
assert min(r['y'] for r in remaining2)>100
# Original run arrays are reused exactly, except the one employment date.
assert len(header)+len(senior)+len(old_ml)==len(page1)
assert len(remaining2)==len(page2)
print('PASS: original embedded fonts and existing text retained; Stewart added; PixelEdge end date updated; 2 pages.')
print(OUTPUT)

import shutil
shutil.copy2(OUTPUT, OUTPUT.with_name("Ehtisham-Fazal-Resume.pdf"))
