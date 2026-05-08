from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "BROKER_OPS_PROJECT_PLAN.md"
OUTPUT = ROOT / "outputs" / "Broker_Ops_Exception_Report_Project_Plan.pdf"


def _clean(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<font face='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


def _footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(0.75 * inch, 0.45 * inch, "Broker Operations Exception Report Generator")
    canvas.drawRightString(7.75 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf() -> Path:
    text = SOURCE.read_text(encoding="utf-8")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "PlanTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=16,
    )
    h1 = ParagraphStyle(
        "PlanH1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=12,
        spaceAfter=7,
    )
    h2 = ParagraphStyle(
        "PlanH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#334155"),
        spaceBefore=9,
        spaceAfter=5,
    )
    body = ParagraphStyle(
        "PlanBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.4,
        leading=13,
        textColor=colors.HexColor("#111827"),
        spaceAfter=5,
    )
    bullet = ParagraphStyle(
        "PlanBullet",
        parent=body,
        leftIndent=18,
        firstLineIndent=-10,
        spaceAfter=3,
    )
    checked = ParagraphStyle(
        "PlanChecked",
        parent=bullet,
        textColor=colors.HexColor("#166534"),
    )
    todo = ParagraphStyle(
        "PlanTodo",
        parent=bullet,
        textColor=colors.HexColor("#374151"),
    )
    source_style = ParagraphStyle(
        "PlanSource",
        parent=bullet,
        fontSize=8.4,
        leading=11.5,
        textColor=colors.HexColor("#475569"),
    )

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title="Broker Operations Exception Report Generator - Project Plan",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates([PageTemplate(id="plan", frames=[frame], onPage=_footer)])

    story = []
    in_sources = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            story.append(Spacer(1, 4))
            continue
        if line.startswith("# "):
            story.append(Paragraph(_clean(line[2:]), title))
            continue
        if line.startswith("## "):
            in_sources = line == "## Sources"
            story.append(Paragraph(_clean(line[3:]), h1))
            continue
        if line.startswith("### "):
            story.append(Paragraph(_clean(line[4:]), h2))
            continue
        if line.startswith("- [x]"):
            story.append(Paragraph("[x] " + _clean(line[6:].strip()), checked))
            continue
        if line.startswith("- [ ]"):
            story.append(Paragraph("[ ] " + _clean(line[6:].strip()), todo))
            continue
        if line.startswith("- "):
            style = source_style if in_sources else bullet
            story.append(Paragraph("- " + _clean(line[2:]), style))
            continue
        if line.startswith("  - "):
            story.append(Paragraph("&nbsp;&nbsp;- " + _clean(line[4:]), bullet))
            continue
        story.append(Paragraph(_clean(line), body))

    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    print(build_pdf())
