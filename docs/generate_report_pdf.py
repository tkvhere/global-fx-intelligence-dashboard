from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'docs' / 'Global_FX_Intelligence_Report.pdf'


def build_pdf():
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    story = []

    title = 'Global FX Intelligence - FIN623 Project Report'
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 18))

    summary = (
        'This report summarises the completed Global FX Intelligence project, a full-stack currency '
        'dashboard combining live exchange data, market analytics, a machine learning forecasting '
        'module, and alerting functionality. The solution was implemented as a Flask backend and '
        'a React frontend to satisfy the assignment requirements.'
    )
    story.append(Paragraph(summary, styles['BodyText']))
    story.append(Spacer(1, 18))

    sections = [
        ('Project objective', 'The platform provides real-time FX monitoring, pair analysis, conversion tools, volatility scoring, forecasting, and local alert tracking for an academic finance dashboard case study.'),
        ('Architecture', 'The application uses Flask Blueprints for modular API routing, SQLite for persistence, and a React UI with Tailwind for the presentation layer.'),
        ('ML Forecasting', 'A supervised time-series regression workflow generates short-term forecasts using lag-based features and chronological data validation.'),
        ('Front-end Validation', 'The project includes a production build check and API health validation to confirm the system is operational.'),
        ('Submission Outcome', 'The dashboard is working, documented, and ready for live demonstration and academic review.'),
    ]

    for heading, content in sections:
        story.append(Paragraph(f'<b>{heading}</b>', styles['Heading2']))
        story.append(Paragraph(content, styles['BodyText']))
        story.append(Spacer(1, 12))

    doc.build(story)
    print(f'PDF generated: {OUTPUT}')


if __name__ == '__main__':
    build_pdf()
