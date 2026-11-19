"""Generate a selectable-text, two-page resume. Requires reportlab and pypdf."""
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, HRFlowable

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / 'Ehtisham-Fazal-Resume.pdf'
font_dir = Path('C:/Windows/Fonts')
if (font_dir / 'calibri.ttf').exists():
    for name, filename in [('Resume', 'calibri.ttf'), ('ResumeBold', 'calibrib.ttf'), ('ResumeItalic', 'calibrii.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily('Resume', normal='Resume', bold='ResumeBold', italic='ResumeItalic', boldItalic='ResumeBold')
    FONT, BOLD = 'Resume', 'ResumeBold'
else:
    FONT, BOLD = 'Helvetica', 'Helvetica-Bold'

GREEN = colors.HexColor('#245541')
INK = colors.HexColor('#1d2925')
GRAY = colors.HexColor('#53635b')
LINE = colors.HexColor('#d9e3dc')
styles = {
    'name': ParagraphStyle('name', fontName=BOLD, fontSize=29, leading=33, textColor=INK, spaceAfter=4),
    'tagline': ParagraphStyle('tagline', fontName=FONT, fontSize=12, leading=16, textColor=GREEN, spaceAfter=9),
    'contact': ParagraphStyle('contact', fontName=FONT, fontSize=9.2, leading=13.5, textColor=GRAY),
    'section': ParagraphStyle('section', fontName=BOLD, fontSize=10, leading=13, textColor=GREEN, spaceBefore=12, spaceAfter=6, keepWithNext=True),
    'body': ParagraphStyle('body', fontName=FONT, fontSize=10.4, leading=14.4, textColor=INK, spaceAfter=5),
    'role': ParagraphStyle('role', fontName=BOLD, fontSize=11.5, leading=15, textColor=INK, spaceAfter=2, keepWithNext=True),
    'meta': ParagraphStyle('meta', fontName=FONT, fontSize=9.4, leading=13, textColor=GRAY, spaceAfter=6, keepWithNext=True),
    'bullet': ParagraphStyle('bullet', fontName=FONT, fontSize=10.2, leading=13.7, textColor=INK, leftIndent=11, firstLineIndent=-9, spaceAfter=4),
    'small': ParagraphStyle('small', fontName=FONT, fontSize=9.8, leading=13.5, textColor=INK, spaceAfter=4),
}
story = []
markdown = ['# Ehtisham Fazal', '', 'Senior AI Engineer | Generative AI, Multi-Agent Systems & Computer Vision', '',
            'Lahore, Pakistan | ehtishamfazal68@gmail.com',
            'LinkedIn: https://www.linkedin.com/in/ehtisham-fazal-72a036182/',
            'GitHub: https://github.com/Ehtisham-Fazl',
            'Portfolio: https://ehtisham-fazl.github.io/Ehtisham-Fazl/', '']

def p(text, style='body'):
    return Paragraph(text, styles[style])

def section(title):
    story.append(p(title.upper(), 'section'))
    markdown.extend(['## ' + title, ''])

def body(text, style='body'):
    story.append(p(text, style))
    import re
    markdown.extend([re.sub('<[^>]+>', '', text), ''])

def role(title, company, dates, location, bullets):
    story.append(p(escape(title) + ' | ' + escape(company), 'role'))
    story.append(p(escape(dates + '  |  ' + location), 'meta'))
    markdown.extend(['### ' + title + ' | ' + company, dates + ' | ' + location, ''])
    for text in bullets:
        story.append(p('&#8226; ' + escape(text), 'bullet'))
        markdown.append('- ' + text)
    markdown.append('')
    story.append(Spacer(1, 6))

story.extend([
    p('Ehtisham Fazal', 'name'),
    p('Senior AI Engineer | Generative AI, Multi-Agent Systems &amp; Computer Vision', 'tagline'),
    p('Lahore, Pakistan  |  <link href="mailto:ehtishamfazal68@gmail.com" color="#245541">ehtishamfazal68@gmail.com</link>', 'contact'),
    p('<link href="https://www.linkedin.com/in/ehtisham-fazal-72a036182/" color="#245541">linkedin.com/in/ehtisham-fazal-72a036182</link>  |  <link href="https://github.com/Ehtisham-Fazl" color="#245541">github.com/Ehtisham-Fazl</link>  |  <link href="https://ehtisham-fazl.github.io/Ehtisham-Fazl/" color="#245541">Portfolio</link>', 'contact'),
    Spacer(1, 12),
    HRFlowable(width='100%', thickness=1, color=GREEN),
])
section('Profile')
body('Senior AI Engineer building production generative AI applications, retrieval-augmented generation (RAG) systems, and multi-agent workflows. Experience spans coding agents, workflow automation, document intelligence, computer vision, and model evaluation. Combines a signal processing foundation with system design that balances quality, latency, reliability, and cost.')
section('Technical Focus')
body('<b>AI systems:</b> LLM applications, RAG, embeddings, vector search, multi-agent orchestration, tool integration, reasoning and memory, coding agents, workflow automation.', 'small')
body('<b>Evaluation &amp; engineering:</b> Open-weight model evaluation, evaluation frameworks, guardrails, error analysis, inference optimization, internal data processing, production ML.', 'small')
body('<b>Applied ML &amp; tools:</b> Python, NLP, computer vision, OpenCV, YOLOv7, Detectron, BERT, BART, neural networks, signal processing, Selenium.', 'small')
section('Professional Experience')
role('Senior AI Engineer', 'Stewart Pakistan Private Limited', 'Jun 2026 - Present', 'Lahore, Pakistan', [
    'Build generative AI and LLM-powered business solutions with engineering teams, from design to production integration.',
    'Develop multi-agent systems for coding tasks, coordinating tools and multi-step reasoning across engineering workflows.',
    'Build AI-powered automation pipelines for internal workflows and data processing.',
    'Develop evaluation frameworks for open-weight models, comparing task quality, inference efficiency, and production suitability.',
    'Optimize inference and evaluate models to improve the reliability of AI-driven workflows.',
])
role('Senior Machine Learning Engineer', 'PixelEdge', 'Jan 2024 - May 2026', 'Lahore, Pakistan', [
    'Owned RAG system design and deployment for finance and environmental platforms, enabling document intelligence and data validation.',
    'Deployed retrieval-backed LLM pipelines with production p95 latency below 900 ms within infrastructure cost constraints.',
    'Improved document extraction and classification by 8+ F1 points through error analysis and feature engineering.',
    'Built knowledge layers, evaluation frameworks, and guardrails for consistent responses and business acceptance criteria.',
    'Developed automated healthcare shift scheduling and real-time, vision-enabled conversational assistants.',
    'Mentored junior engineers in production ML, debugging, and system design; translated stakeholder requirements into deployable features.',
])

story.append(PageBreak())
section('Professional Experience - Continued')
role('Machine Learning Engineer', 'PixelEdge', 'May 2023 - Jan 2024', 'Karachi, Pakistan', [
    'Curated and preprocessed environmental datasets, prioritizing training and validation data quality, integrity, and relevance.',
    'Experimented with neural architectures, optimization techniques, and hyperparameters; collaborated with domain experts to frame environmental challenges as ML problems.',
])
role('Machine Learning Engineer', 'Lambda Theta', 'Oct 2022 - May 2023', 'Karachi, Pakistan', [
    'Developed automated surveillance models, camera-based distance estimation, and perspective transformations for dashcam footage using OpenCV.',
    'Fine-tuned YOLOv7 and Detectron for detection and segmentation; used semi-supervised label propagation and edge detection for visual analysis.',
    'Built NLP applications with BART and BERT for text generation, classification, similarity estimation, and conversational assistance.',
])
role('AI Researcher', 'NCBC Heterocloud Project, PAF-KIET', 'Nov 2021 - Jun 2022', 'Karachi, Pakistan', [
    'Researched and developed machine learning models for face recognition.',
])
role('Machine Learning Engineer', 'Cloudee.ai', 'Mar 2021 - Feb 2022', 'Karachi, Pakistan', [
    'Developed facial expression recognition for attendance, speech emotion recognition for fraud detection, and handwritten character recognition for automated quiz checking.',
    'Used Python for network packet analysis, URL pattern automation, synthetic test data generation, and Selenium-based SaaS testing.',
])
body('<b>Earlier experience:</b> Digital Signal Processing Engineering Intern, Cloudee.ai, Jan-Feb 2021. Worked on image processing, facial and speech expression recognition, object detection, and character recognition.', 'small')
section('Education')
body('<b>Master\'s degree in Electronics</b> | PAF-Karachi Institute of Economics &amp; Technology<br/>Jan 2021 - Feb 2023 | Signal processing foundation', 'small')
section('Publication')
body('<b>Anticancer Peptides Classification using Kernel Sparse Representation Classifier</b>', 'small')
body('Applied sparse representation and kernel methods to anticancer peptide classification, using CKSAAP features, KPCA, SMOTE, and an efficient matching pursuit solver.', 'small')
body('<link href="https://github.com/ehtisham-Fazal/ACP-Kernel-SRC" color="#245541">Research implementation: github.com/ehtisham-Fazal/ACP-Kernel-SRC</link>', 'small')
section('Certifications')
body('Generative AI with Large Language Models | Neural Networks and Deep Learning | Machine Learning | Crash Course on Python | Databricks Fundamentals Accreditation', 'small')

def footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(.5)
    canvas.line(42, 35, w-42, 35)
    canvas.setFont(FONT, 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(42, 22, 'Ehtisham Fazal | Senior AI Engineer')
    canvas.drawRightString(w-42, 22, str(doc.page))
    if doc.page > 1:
        canvas.setFont(BOLD, 10)
        canvas.setFillColor(GREEN)
        canvas.drawString(42, h-32, 'EHTISHAM FAZAL')
        canvas.setFont(FONT, 9)
        canvas.setFillColor(GRAY)
        canvas.drawRightString(w-42, h-32, 'Senior AI Engineer')
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=42, leftMargin=42,
                        topMargin=42, bottomMargin=47,
                        title='Ehtisham Fazal - Senior AI Engineer - Resume',
                        author='Ehtisham Fazal', subject='Generative AI, Multi-Agent Systems, RAG, Evaluation and Computer Vision')
doc.build(story, onFirstPage=footer, onLaterPages=footer)
(HERE/'Ehtisham-Fazal-Resume.md').write_text('\n'.join(markdown), encoding='utf-8')
from pypdf import PdfReader
reader = PdfReader(str(OUTPUT))
assert len(reader.pages) == 2, f'Expected 2 pages; found {len(reader.pages)}'
text = '\n'.join(page.extract_text() for page in reader.pages)
for term in ['Stewart Pakistan Private Limited', 'Jun 2026 - Present', 'multi-agent', 'open-weight', '8+ F1', '900 ms']:
    assert term in text, f'Missing expected content: {term}'
assert len(reader.pages[0].extract_text()) > 2500
assert len(reader.pages[1].extract_text()) > 2000
print(f'Created {OUTPUT}: 2 pages; content checks passed.')
