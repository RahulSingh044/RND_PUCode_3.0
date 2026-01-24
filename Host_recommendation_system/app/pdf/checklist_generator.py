from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor, black
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.units import cm

from app.utils.file_utils import get_generated_dir, build_file_path
from app.utils.time_utils import timestamp_for_filename


# ==================================================
# PDF GENERATOR
# ==================================================

def generate_checklist_pdf(
    host_id: str,
    event_context: dict,
    checklist_items: dict
) -> str:
    """
    Generates a professional, branded checklist PDF for hosts.
    """

    # --------------------------------------------------
    # File path
    # --------------------------------------------------
    base_dir = get_generated_dir("checklists")
    filename = f"host_{host_id}_checklist_{timestamp_for_filename()}.pdf"
    file_path = build_file_path(base_dir, filename)

    # --------------------------------------------------
    # Document setup
    # --------------------------------------------------
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # --------------------------------------------------
    # Custom styles (check if already exist to avoid errors)
    # --------------------------------------------------
    if "BB_CompanyName" not in styles:
        styles.add(ParagraphStyle(
            name="BB_CompanyName",
            fontSize=22,
            leading=26,
            alignment=TA_CENTER,
            textColor=HexColor("#111827"),  # dark gray
            spaceAfter=6
        ))

    if "BB_Tagline" not in styles:
        styles.add(ParagraphStyle(
            name="BB_Tagline",
            fontSize=11,
            alignment=TA_CENTER,
            textColor=HexColor("#6B7280"),  # muted gray
            spaceAfter=16
        ))

    if "BB_Title" not in styles:
        styles.add(ParagraphStyle(
            name="BB_Title",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=18
        ))

    if "BB_SectionHeader" not in styles:
        styles.add(ParagraphStyle(
            name="BB_SectionHeader",
            fontSize=13,
            leading=16,
            textColor=HexColor("#2563EB"),  # blue
            spaceBefore=14,
            spaceAfter=8
        ))

    if "BB_ChecklistItem" not in styles:
        styles.add(ParagraphStyle(
            name="BB_ChecklistItem",
            fontSize=10.5,
            leading=14,
            leftIndent=12,
            spaceAfter=6
        ))

    # --------------------------------------------------
    # Build content
    # --------------------------------------------------
    story = []

    # Branding
    story.append(Paragraph("Blockbuzz", styles["BB_CompanyName"]))
    story.append(Paragraph(
        "Never miss what’s buzzing nearby",
        styles["BB_Tagline"]
    ))

    story.append(Paragraph(
        "Host Event Success Checklist",
        styles["BB_Title"]
    ))

    # Event summary
    summary_text = (
        f"<b>Event Type:</b> {event_context['event_type']} &nbsp;&nbsp; | "
        f"<b>Participants:</b> {event_context['participant_count']} &nbsp;&nbsp; | "
        f"<b>Venue:</b> {event_context['venue_type']} &nbsp;&nbsp; | "
        f"<b>Food Provided:</b> {'Yes' if event_context.get('food_provided') else 'No'}"
    )

    story.append(Paragraph(summary_text, styles["BB_ChecklistItem"]))
    story.append(Spacer(1, 12))

    # --------------------------------------------------
    # Checklist sections
    # --------------------------------------------------
    for section, items in checklist_items.items():
        story.append(Paragraph(
            section.replace("_", " ").title(),
            styles["BB_SectionHeader"]
        ))

        for item in items:
            story.append(Paragraph(
                f"☐ {item}",
                styles["BB_ChecklistItem"]
            ))

    # --------------------------------------------------
    # Build PDF with border
    # --------------------------------------------------
    def draw_border(canvas, doc):
        canvas.setStrokeColor(HexColor("#E5E7EB"))  # light gray
        canvas.setLineWidth(1)
        canvas.rect(
            20, 20,
            A4[0] - 40,
            A4[1] - 40
        )

    doc.build(story, onFirstPage=draw_border, onLaterPages=draw_border)

    return file_path
