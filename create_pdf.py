"""
create_pdf.py
-------------
Generates a polished PDF guide:
"Sales_Data_Analysis_Project_Guide.pdf"
Covering Workflow, Tech Stack, and Interview Preparation.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

pdf_filename = "Sales_Data_Analysis_Project_Guide.pdf"
doc = SimpleDocTemplate(
    pdf_filename,
    pagesize=letter,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40,
)

styles = getSampleStyleSheet()

# Custom Palette & Typography Styles
NAVY = colors.HexColor("#1E293B")
BLUE = colors.HexColor("#2563EB")
CYAN = colors.HexColor("#0284C7")
DARK_GRAY = colors.HexColor("#334155")
LIGHT_BG = colors.HexColor("#F8FAFC")
ACCENT_BG = colors.HexColor("#EFF6FF")
BORDER_COLOR = colors.HexColor("#CBD5E1")

title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=26,
    textColor=NAVY,
    spaceAfter=4,
)

subtitle_style = ParagraphStyle(
    "DocSubTitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=14,
    textColor=CYAN,
    spaceAfter=15,
)

h1_style = ParagraphStyle(
    "Heading1Custom",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=14,
    leading=18,
    textColor=BLUE,
    spaceBefore=14,
    spaceAfter=6,
)

h2_style = ParagraphStyle(
    "Heading2Custom",
    parent=styles["Heading3"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=15,
    textColor=NAVY,
    spaceBefore=8,
    spaceAfter=4,
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=13.5,
    textColor=DARK_GRAY,
    spaceAfter=6,
)

bold_body = ParagraphStyle(
    "BoldBodyCustom",
    parent=body_style,
    fontName="Helvetica-Bold",
)

bullet_style = ParagraphStyle(
    "BulletCustom",
    parent=body_style,
    leftIndent=12,
    spaceAfter=3,
)

code_style = ParagraphStyle(
    "CodeStyle",
    parent=styles["Normal"],
    fontName="Courier-Bold",
    fontSize=8.5,
    leading=11,
    textColor=colors.HexColor("#0F172A"),
)

story = []

# --- HEADER BANNER ---
story.append(Paragraph("Sales Data Analysis & Web Dashboard", title_style))
story.append(Paragraph("Complete Project Guide, End-to-End Workflow, Tech Stack & Interview Script", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceAfter=12))

# --- SECTION 1: PROJECT OVERVIEW ---
story.append(Paragraph("1. Executive Summary & Project Overview", h1_style))
story.append(Paragraph(
    "This project is an <b>end-to-end data engineering and analytics solution</b>. It processes raw sales transactions containing real-world data noise (duplicates, missing fields, case inconsistencies, negative values), cleans and engineers features, performs exploratory data analysis (EDA), generates automated reports and charts, and serves an interactive web dashboard on <b>localhost</b>.",
    body_style
))

# --- SECTION 2: TECH STACK TABLE ---
story.append(Paragraph("2. Technology Stack", h1_style))

tech_data = [
    [Paragraph("<b>Category</b>", bold_body), Paragraph("<b>Technology / Library</b>", bold_body), Paragraph("<b>Role & Purpose in Project</b>", bold_body)],
    [Paragraph("Language", body_style), Paragraph("Python 3.12", code_style), Paragraph("Core programming language for data generation, analysis, and dashboard backend.", body_style)],
    [Paragraph("Data Processing", body_style), Paragraph("pandas, numpy", code_style), Paragraph("Data manipulation, vector calculations, cleaning nulls/duplicates, and feature engineering.", body_style)],
    [Paragraph("Data Visualization", body_style), Paragraph("matplotlib, Plotly Express", code_style), Paragraph("Static chart exporting (PNGs) and interactive dynamic charts for web dashboard.", body_style)],
    [Paragraph("Web Application", body_style), Paragraph("Streamlit", code_style), Paragraph("Lightweight Python framework powering the localhost interactive web dashboard.", body_style)],
    [Paragraph("Version Control", body_style), Paragraph("Git, GitHub", code_style), Paragraph("Source control management, remote repository tracking, and portfolio hosting.", body_style)],
]

t_tech = Table(tech_data, colWidths=[1.2*inch, 1.8*inch, 4.3*inch])
t_tech.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), ACCENT_BG),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 5),
]))
story.append(t_tech)
story.append(Spacer(1, 10))

# --- SECTION 3: WORKFLOW ---
story.append(Paragraph("3. End-to-End Project Workflow", h1_style))

wf_steps = [
    ("Step 1: Raw Data Generation (generate_data.py)",
     "Creates a realistic dataset of 5,000+ orders with synthetic messiness: stray whitespaces, mixed casing (lowercase/uppercase), null prices/quantities, duplicate OrderIDs, and negative quantities to mirror production database flaws."),
    
    ("Step 2: Data Cleaning Pipeline (analysis.py & app.py)",
     "• Text Standardization: Applied <code>str.strip().str.title()</code> to Region, Category, PaymentMethod.<br/>"
     "• Deduplication: Removed duplicate <code>OrderID</code> entries.<br/>"
     "• Anomaly Correction: Converted invalid negative quantities using <code>abs()</code>.<br/>"
     "• Missing Value Strategy: Dropped missing key metrics (UnitPrice/Quantity) and imputed missing ages with column median."),
    
    ("Step 3: Feature Engineering",
     "Engineered business-critical columns: <code>Revenue = UnitPrice * Quantity * (1 - DiscountPct/100)</code>, <code>Year</code>, and <code>Month</code> (YYYY-MM)."),
    
    ("Step 4: Statistical EDA & Insights Generation",
     "Aggregated total revenue ($5.82M), total order volume (4,701), average order value ($1,238.55), top 5 revenue-generating products, category breakdowns, and peak sales months."),
    
    ("Step 5: Visualizations & Reporting",
     "Generated 5 static PNG charts saved into <code>/charts</code> directory and generated a formatted executive summary report <code>sales_report.txt</code>."),
    
    ("Step 6: Interactive Localhost Web Dashboard (app.py)",
     "Built a full Streamlit web app displaying live KPI metric cards, interactive Plotly charts, sidebar date/region/category filters, and an interactive data table with CSV export."),
    
    ("Step 7: Version Control & CI/CD",
     "Maintained codebase version control via Git and pushed the complete project to GitHub repository <code>Mamatak16/sales-data-analysis-project</code>.")
]

for title, desc in wf_steps:
    story.append(Paragraph(f"<b>{title}</b>", h2_style))
    story.append(Paragraph(desc, bullet_style))

story.append(Spacer(1, 10))

# --- SECTION 4: INTERVIEW EXPLANATION GUIDE ---
story.append(Paragraph("4. How to Explain this Project in an Interview", h1_style))

story.append(Paragraph("A. The 30-Second Elevator Pitch", h2_style))
pitch_text = (
    "<i>\"I built an end-to-end Sales Data Analytics solution using Python, pandas, Plotly, and Streamlit. "
    "The project mimics a real-world enterprise pipeline: it ingests messy sales transaction data, cleans nulls and duplicate entries, "
    "engineers net revenue metrics, exports statistical reports, and serves an interactive web dashboard on localhost where stakeholders "
    "can slice and dice revenue by region, category, and date range in real time.\"</i>"
)
story.append(Paragraph(pitch_text, body_style))

story.append(Spacer(1, 6))
story.append(Paragraph("B. STAR Method Breakdown (Situation, Task, Action, Result)", h2_style))

star_data = [
    [Paragraph("<b>STAR Component</b>", bold_body), Paragraph("<b>Interview Script Content</b>", bold_body)],
    [Paragraph("Situation", bold_body), Paragraph("Businesses often struggle to extract actionable insights from raw transactional data due to duplicate records, incomplete values, and static reporting tools.", body_style)],
    [Paragraph("Task", bold_body), Paragraph("Design a robust data pipeline to clean messy records, compute business KPIs, generate visualization charts, and provide an interactive dashboard for decision-makers.", body_style)],
    [Paragraph("Action", bold_body), Paragraph("1. Developed a pandas data pipeline to handle deduplication, text normalization, and median imputation.<br/>2. Engineered Net Revenue and time features.<br/>3. Designed interactive Plotly charts and built a responsive Streamlit dashboard on localhost.", body_style)],
    [Paragraph("Result", bold_body), Paragraph("Processed 5,000+ orders, identified key revenue drivers ($5.82M total revenue, Toys & Clothing as top categories), and reduced reporting latency by serving real-time filters via a local web app.", body_style)],
]

t_star = Table(star_data, colWidths=[1.5*inch, 5.8*inch])
t_star.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), ACCENT_BG),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 5),
]))
story.append(t_star)

story.append(Spacer(1, 8))
story.append(Paragraph("C. Technical Q&A Questions You Can Answer", h2_style))

qna = [
    ("Q1: How did you handle messy real-world data?",
     "<b>Answer:</b> I built a multi-stage cleaning pipeline in pandas. I trimmed stray whitespace and standardized casing using vectorized string operations. I deduplicated OrderIDs, converted negative quantities to absolute values, dropped rows missing core price data, and filled missing customer ages using median imputation to maintain distribution balance."),
    
    ("Q2: Why did you choose Streamlit over traditional frameworks like Flask/Django?",
     "<b>Answer:</b> Streamlit allows rapid prototyping of data applications purely in Python without needing HTML/CSS/JS boilerplate. It integrates seamlessly with pandas and Plotly, enabling real-time reactive filtering with built-in caching via <code>@st.cache_data</code> for high performance on localhost."),
    
    ("Q3: What key business findings did your analysis uncover?",
     "<b>Answer:</b> Analysis revealed total revenue of $5.82M across 4,701 clean orders with an Average Order Value of $1,238.55. Toys ($1.21M) and Clothing ($1.18M) were the highest revenue categories, North was the top region ($1.52M), and September 2024 was the peak sales month ($292.7K).")
]

for q, a in qna:
    story.append(Paragraph(f"<b>{q}</b>", body_style))
    story.append(Paragraph(a, bullet_style))

# --- SECTION 5: COMMAND CHEAT-SHEET ---
story.append(Spacer(1, 8))
story.append(Paragraph("5. Local Execution Commands", h1_style))

cmd_data = [
    [Paragraph("<b>Task</b>", bold_body), Paragraph("<b>Command Line</b>", bold_body)],
    [Paragraph("Install Dependencies", body_style), Paragraph("<code>pip install -r requirements.txt</code>", code_style)],
    [Paragraph("Generate Raw Dataset", body_style), Paragraph("<code>python generate_data.py</code>", code_style)],
    [Paragraph("Run Analysis & Visuals", body_style), Paragraph("<code>python analysis.py</code>", code_style)],
    [Paragraph("Launch Localhost Web App", body_style), Paragraph("<code>streamlit run app.py</code>", code_style)],
]

t_cmd = Table(cmd_data, colWidths=[2.2*inch, 5.1*inch])
t_cmd.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), ACCENT_BG),
    ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_cmd)

# Build Document
doc.build(story)
print(f"PDF successfully generated -> {pdf_filename}")
