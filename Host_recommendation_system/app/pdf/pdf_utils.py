from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, ListFlowable, ListItem


def get_pdf_styles():
    """
    Central place to define and reuse PDF styles.
    Keeps all PDFs visually consistent.
    """
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="TitleStyle",
        fontSize=18,
        leading=22,
        spaceAfter=14
    ))

    styles.add(ParagraphStyle(
        name="SectionStyle",
        fontSize=14,
        leading=18,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name="ItemStyle",
        fontSize=10,
        leading=14
    ))

    styles.add(ParagraphStyle(
        name="MetaStyle",
        fontSize=9,
        leading=12,
        textColor="#555555"
    ))

    return styles


def checkbox_list(items, styles, left_indent=16):
    """
    Converts list of strings into checkbox-style bullet list.

    Args:
        items (list[str]): checklist items
        styles: reportlab styles
        left_indent (int): indentation

    Returns:
        ListFlowable
    """
    return ListFlowable(
        [
            ListItem(
                Paragraph(f"☐ {item}", styles["ItemStyle"])
            )
            for item in items
        ],
        bulletType="bullet",
        start="square",
        leftIndent=left_indent
    )


def section(title, styles):
    """
    Creates a section heading with checkbox indicator.
    """
    return Paragraph(f"☐ {title}", styles["SectionStyle"])


def paragraph(text, styles, style_name="ItemStyle"):
    """
    Simple wrapper for paragraph creation.
    """
    return Paragraph(text, styles[style_name])
