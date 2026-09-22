# -*- coding: utf-8 -*-
"""
Generates the complete 20-slide NirmalNode Capstone Defense presentation in PowerPoint (.pptx).
Strictly based on the thesis source of truth.
"""
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

output_pptx = r"c:\Users\ASUS\Downloads\capstone 3.2\NirmalNode_Capstone_Defense_NEW.pptx"
base_dir = r"c:\Users\ASUS\Downloads\capstone 3.2"

def get_path(rel):
    return os.path.join(base_dir, rel)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors
NAVY = RGBColor(30, 58, 138)        # #1E3A8A
NAVY_LIGHT = RGBColor(37, 99, 235)  # #2563EB
TEAL = RGBColor(15, 118, 110)       # #0F766E
EMERALD = RGBColor(21, 128, 61)     # #15803D
AMBER = RGBColor(180, 83, 9)        # #B45309
ROSE = RGBColor(190, 18, 60)        # #BE123C
DARK_TEXT = RGBColor(15, 23, 42)    # #0F172A
MUTED_TEXT = RGBColor(100, 116, 139)# #64748B
SLATE_BG = RGBColor(248, 250, 252)  # #F8FAFC
CARD_BG = RGBColor(255, 255, 255)
WHITE = RGBColor(255, 255, 255)
BORDER_COL = RGBColor(226, 232, 240)# #E2E8F0
LIGHT_BLUE = RGBColor(239, 246, 255)
LIGHT_TEAL = RGBColor(240, 253, 250)

def add_header(slide, tag_text, title_text, subtitle_text, category_badge):
    # Top progress bar accent
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = NAVY
    top_bar.line.fill.background()

    # Header text container
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.22), Inches(10.0), Inches(1.15))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    p0.text = tag_text.upper()
    p0.font.name = 'Arial'
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = TEAL

    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = 'Arial'
    p1.font.size = Pt(20.5)
    p1.font.bold = True
    p1.font.color.rgb = NAVY

    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.name = 'Arial'
    p2.font.size = Pt(11)
    p2.font.color.rgb = MUTED_TEXT

    # Category Badge on Right
    badge_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.6), Inches(0.32), Inches(2.1), Inches(0.42))
    badge_box.fill.solid()
    badge_box.fill.fore_color.rgb = SLATE_BG
    badge_box.line.color.rgb = BORDER_COL
    badge_box.line.width = Pt(1)
    btf = badge_box.text_frame
    btf.word_wrap = False
    bp = btf.paragraphs[0]
    bp.alignment = PP_ALIGN.CENTER
    bp.text = category_badge
    bp.font.name = 'Arial'
    bp.font.size = Pt(9.5)
    bp.font.bold = True
    bp.font.color.rgb = NAVY

    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.4), Inches(12.133), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_COL
    line.line.fill.background()

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COL, border_width=1):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

# ==========================================
# SLIDE 1: TITLE SLIDE
# ==========================================
s1 = prs.slides.add_slide(blank_layout)

# Left Content Box
tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(6.8), Inches(5.8))
tf1 = tb1.text_frame
tf1.word_wrap = True

# Logo + University
if os.path.exists(get_path("extracted_figs/uft_logo.png")):
    s1.shapes.add_picture(get_path("extracted_figs/uft_logo.png"), Inches(0.8), Inches(0.7), height=Inches(0.7))

p_uni = tf1.paragraphs[0]
p_uni.text = "\n\nUNIVERSITY OF FRONTIER TECHNOLOGY, BANGLADESH"
p_uni.font.name = 'Arial'
p_uni.font.size = Pt(12)
p_uni.font.bold = True
p_uni.font.color.rgb = NAVY

p_dept = tf1.add_paragraph()
p_dept.text = "Department of Internet of Things and Robotics Engineering"
p_dept.font.name = 'Arial'
p_dept.font.size = Pt(11)
p_dept.font.color.rgb = MUTED_TEXT

p_cap = tf1.add_paragraph()
p_cap.text = "B.Sc. Capstone Defense Presentation"
p_cap.font.name = 'Arial'
p_cap.font.size = Pt(10)
p_cap.font.bold = True
p_cap.font.color.rgb = TEAL

p_title = tf1.add_paragraph()
p_title.text = "\nNirmalNode"
p_title.font.name = 'Arial'
p_title.font.size = Pt(38)
p_title.font.bold = True
p_title.font.color.rgb = NAVY

p_sub = tf1.add_paragraph()
p_sub.text = "Green IoT and Adaptive AI-Assisted Local Air Purification and Pollution Prediction System for Industrial Hotspots in Bangladesh"
p_sub.font.name = 'Arial'
p_sub.font.size = Pt(13)
p_sub.font.bold = True
p_sub.font.color.rgb = TEAL

p_meta = tf1.add_paragraph()
p_meta.text = "\nPresented by: Aar Raisatunnesa Hridika | Md Rakib Hassan Dipu\nSupervisor: Md. Ashiqussalehin (Lecturer, Dept. of IoT & Robotics Engineering)\nSeptember 2026"
p_meta.font.name = 'Arial'
p_meta.font.size = Pt(11)
p_meta.font.color.rgb = DARK_TEXT

# Right Picture Card
add_card(s1, Inches(7.8), Inches(0.7), Inches(4.9), Inches(6.1), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("real_world_hotspots.jpg")):
    s1.shapes.add_picture(get_path("real_world_hotspots.jpg"), Inches(7.9), Inches(0.8), width=Inches(4.7), height=Inches(5.4))
tb_cap = s1.shapes.add_textbox(Inches(7.9), Inches(6.25), Inches(4.7), Inches(0.5))
tb_cap.text_frame.word_wrap = True
p_c = tb_cap.text_frame.paragraphs[0]
p_c.text = "Figure 1.1: Representative Industrial Hotspots in Bangladesh"
p_c.font.size = Pt(9.5)
p_c.font.italic = True
p_c.font.color.rgb = MUTED_TEXT

# ==========================================
# SLIDE 2: THE PROBLEM
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "1. Problem Motivation", "Why Industrial Air Pollution Needs a Local Solution", "The spatial mismatch between macro-scale monitoring and localized worker exposure", "Background & Context")

# Left: Hotspot Image
add_card(s2, Inches(0.6), Inches(1.6), Inches(5.6), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("real_world_hotspots.jpg")):
    s2.shapes.add_picture(get_path("real_world_hotspots.jpg"), Inches(0.7), Inches(1.7), width=Inches(5.4), height=Inches(4.7))
tb_s2c = s2.shapes.add_textbox(Inches(0.7), Inches(6.45), Inches(5.4), Inches(0.4))
p_s2c = tb_s2c.text_frame.paragraphs[0]
p_s2c.text = "Figure 1.1: Welding bay metal-fume hazards & boiler-room combustion plumes"
p_s2c.font.size = Pt(9.5)
p_s2c.font.italic = True
p_s2c.font.color.rgb = MUTED_TEXT

# Right: Academic Problem Points
add_card(s2, Inches(6.4), Inches(1.6), Inches(6.3), Inches(5.3), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_s2 = s2.shapes.add_textbox(Inches(6.6), Inches(1.75), Inches(5.9), Inches(5.0))
tf_s2 = tb_s2.text_frame
tf_s2.word_wrap = True

def add_bullet(tf, title, body, dot_col=NAVY):
    p = tf.add_paragraph() if tf.paragraphs[0].text else tf.paragraphs[0]
    p.space_after = Pt(8)
    run_t = p.add_run()
    run_t.text = "• " + title + ": "
    run_t.font.bold = True
    run_t.font.size = Pt(11)
    run_t.font.color.rgb = dot_col
    run_b = p.add_run()
    run_b.text = body
    run_b.font.size = Pt(10.5)
    run_b.font.color.rgb = DARK_TEXT

add_bullet(tf_s2, "WHO 2021 Tighter Standard", "Annual PM2.5 threshold lowered to 5 μg/m³. Non-anthropogenic background in Bangladesh already nears this limit, leaving near-zero margin for industrial emissions (Pai et al., 2022).", ROSE)
add_bullet(tf_s2, "Localized Industrial Hotspots", "Pollution is not uniform across cities or factories—it concentrates acutely at welding stations, boiler rooms, generator bays, and chemical storage areas (Ali et al., 2025; Basak et al., 2025).", NAVY)
add_bullet(tf_s2, "Severe Occupational Exposure", "Stationed workers suffer direct inhalation of toxic particulates & gases, causing lung function impairment (Nasri et al., 2023) and elevated mental health risks (Alhadhrami et al., 2024).", ROSE)
add_bullet(tf_s2, "Plant-Wide Filtration Infeasible", "Centralized HVAC purification is cost-prohibitive for small/medium enterprises (SMEs). Adoption in Bangladesh is <1% due to prohibitive capex and misconceptions (Chowdhury et al., 2025).", AMBER)
add_bullet(tf_s2, "The Necessary Solution", "Mitigation must target the localized breathing zone of the worker, predict hazards pre-emptively, and operate at low cost rather than attempting plant-wide filtration.", TEAL)

# ==========================================
# SLIDE 3: WHERE TRADITIONAL APPROACHES FALL SHORT
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "2. Limitations of Existing Systems", "Where Traditional Approaches Fall Short", "The fundamental fragmentation between sensing, prediction, and physical purification", "Literature Critique")

cards = [
    ("Traditional Monitoring", "APPROACH 1",
     "Measures ambient pollutants and displays data on web dashboards or logs to cloud.\n\n• Sense Ambient Air\n• Display / Cloud Log\n• ❌ Zero Physical Action\n\nPassive observation informs workers of hazard but provides no physical remediation.",
     SLATE_BG, NAVY),
    ("Conventional Purification", "APPROACH 2",
     "Room/factory-scale mechanical air cleaners operating on reactive feedback.\n\n• Room-Scale Air Volume\n• High Continuous Power\n• ❌ Reactive Lag\n\nActivates only after hazardous peak has already entered the worker breathing zone; excessive power.",
     SLATE_BG, AMBER),
    ("Static AI Prediction", "APPROACH 3",
     "Machine learning models trained once on fixed offline historical datasets.\n\n• Offline Batch Training\n• Frozen Parameters\n• ❌ No Site Adaptation\n\nAccuracy rapidly degrades when moved to new industrial sites with different pollutant signatures.",
     SLATE_BG, ROSE)
]

for i, (title, tag, body, bg, col) in enumerate(cards):
    left = Inches(0.6 + i * 4.1)
    card = add_card(s3, left, Inches(1.6), Inches(3.9), Inches(4.3), bg_color=bg, border_color=BORDER_COL)
    tb = s3.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.5), Inches(3.9))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = tag
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = col
    
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    
    p2 = tf.add_paragraph()
    p2.text = body
    p2.font.size = Pt(10)
    p2.font.color.rgb = DARK_TEXT

# Bottom Synthesis Bar
bot = add_card(s3, Inches(0.6), Inches(6.05), Inches(12.133), Inches(0.85), bg_color=LIGHT_BLUE, border_color=NAVY_LIGHT)
tb_bot = s3.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.65))
tb_bot.text_frame.word_wrap = True
p_b = tb_bot.text_frame.paragraphs[0]
p_b.text = "The Core Engineering Mismatch: Spatial (Room-scale ≠ Hotspot) • Temporal (Reactive ≠ Pre-emptive) • Intelligence (Static ≠ Adaptive) • Economic (Industrial HVAC ≠ SME Budget)"
p_b.font.size = Pt(10.5)
p_b.font.bold = True
p_b.font.color.rgb = NAVY

# ==========================================
# SLIDE 4: RECENT RESEARCH LANDSCAPE (2024–2026)
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "3. Literature Review", "Recent Research Landscape (2024–2026)", "Comparative analysis of recent studies verifying the persistence of the research gap", "State of the Art")

# Table for Slide 4
rows, cols = 10, 7
left = Inches(0.6)
top = Inches(1.6)
width = Inches(12.133)
height = Inches(4.5)

table_shape = s4.shapes.add_table(rows, cols, left, top, width, height)
t = table_shape.table
t.columns[0].width = Inches(2.2) # Paper
t.columns[1].width = Inches(0.8) # Year
t.columns[2].width = Inches(2.5) # Approach
t.columns[3].width = Inches(1.1) # Prediction
t.columns[4].width = Inches(1.2) # Purification
t.columns[5].width = Inches(1.2) # Adaptivity
t.columns[6].width = Inches(3.133) # Limitation

headers = ["Recent Study", "Year", "Main Approach", "Prediction?", "Purification?", "Adaptivity", "Identified Gap / Limitation"]
for c, h in enumerate(headers):
    cell = t.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(9.5)
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER if c in [1,3,4,5] else PP_ALIGN.LEFT

papers = [
    ("Alam et al. (JARSET)", "2025", "Fixed IoT node developing areas", "No", "No", "Static", "Observation only; no prediction or physical action"),
    ("Ramadhani et al. (IEEE IAICT)", "2025", "Low-cost sensor IoT air monitoring", "No", "No", "Static", "Alert threshold only; lacks predictive automation"),
    ("Ali et al. (Air Qual. Atmos.)", "2025", "Long-term PM2.5 hotspots in Bangladesh", "No", "No", "N/A", "Satellite mapping; lacks real-time worker intervention"),
    ("Basak et al. (J. Agrofor. Env.)", "2025", "Spatial PM2.5/PM10 Tejgaon Dhaka", "No", "No", "N/A", "Quantifies exposure; proposes no engineering mitigation"),
    ("Aurnab & Khanam (WAS Poll.)", "2026", "Landfill gas emission/dispersion in Dhaka", "No", "No", "Static", "Dispersion model only; no localized worker protection"),
    ("Ghosh et al. (Heliyon)", "2026", "Atmospheric CO₂ remote sensing over BD", "No", "No", "N/A", "Macro observation; disconnected from localized action"),
    ("Jaegle (EngRxiv)", "2026", "Innovative particulate filtration technologies", "No", "Yes (Mat.)", "Static", "Filter materials evaluation; lacks sensor-AI closed-loop"),
    ("Kabir et al. (Pollution)", "2026", "PM2.5 mortality & economic loss in 6 BD cities", "Statistical", "No", "N/A", "Macro public health loss ($23B); no hotspot mitigation"),
    ("NirmalNode (This Work)", "2026", "Hotspot Green IoT + Adaptive AI Purifier", "Yes (1-2h)", "Yes (Pred.)", "Incremental", "First closed-loop, adaptive, pre-emptive hotspot system ($67)")
]

for r, row_data in enumerate(papers):
    for c, val in enumerate(row_data):
        cell = t.cell(r + 1, c)
        if r in [4, 5, 6, 7]: # 4 papers from 2026
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(254, 249, 195)
        elif r == 8: # NirmalNode
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(224, 242, 254)
        else:
            cell.fill.solid()
            cell.fill.fore_color.rgb = SLATE_BG if r % 2 == 0 else WHITE

        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(8.5)
        p.font.name = 'Arial'
        if r == 8 or (r in [6, 7] and c == 1):
            p.font.bold = True
        if r == 8:
            p.font.color.rgb = NAVY
        elif c in [3, 4] and val == "No":
            p.font.color.rgb = ROSE
        elif c in [3, 4] and "Yes" in val:
            p.font.color.rgb = EMERALD
            p.font.bold = True
        else:
            p.font.color.rgb = DARK_TEXT
        p.alignment = PP_ALIGN.CENTER if c in [1,3,4,5] else PP_ALIGN.LEFT

tb_s4_bot = s4.shapes.add_textbox(Inches(0.6), Inches(6.25), Inches(12.133), Inches(0.6))
p_s4b = tb_s4_bot.text_frame.paragraphs[0]
p_s4b.text = "Authoritative Synthesis: Even recent 2026 studies primarily address monitoring, prediction or spatial analysis, while NirmalNode focuses on closing the loop from prediction to localized physical mitigation."
p_s4b.font.size = Pt(10)
p_s4b.font.italic = True
p_s4b.font.bold = True
p_s4b.font.color.rgb = TEAL

# ==========================================
# SLIDE 5: RESEARCH GAP
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "4. Research Gap", "What Still Remains Unsolved?", "Synthesizing the exact technical voids identified in literature and Table 2.2", "Identified Research Gap")

# Flow banner at top
add_card(s5, Inches(0.6), Inches(1.6), Inches(12.133), Inches(0.9), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_flow = s5.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.7), Inches(0.7))
tf_flow = tb_flow.text_frame
tf_flow.word_wrap = True
p_fl = tf_flow.paragraphs[0]
p_fl.text = "IoT Multi-Sensing  ➔  AI Forecasting  ➔  [ CRITICAL RESEARCH GAP ]  ➔  Local Physical Purification  ➔  Adaptive Learning"
p_fl.font.size = Pt(12)
p_fl.font.bold = True
p_fl.font.color.rgb = NAVY
p_fl.alignment = PP_ALIGN.CENTER

gaps = [
    ("1. Decoupled Systems", "Monitoring and prediction systems end at visualization; they do not trigger automated physical mitigation."),
    ("2. Room-Scale Focus", "Purification literature evaluates whole rooms/vehicles, requiring excessive power, neglecting worker hotspots."),
    ("3. Reactive Latency", "Conventional air cleaners react only after high pollutant levels are reached; workers inhale the toxic plume."),
    ("4. Static AI Models", "AI models are trained once and frozen; they cannot adapt to sensor drift or relocation between industrial areas."),
    ("5. Missing Engineering", "Occupational studies prove severe health risks at hotspots but propose no low-cost retrofittable engineering solution."),
    ("6. High Adoption Cost", "High retail purifier prices lead to <1% adoption in Bangladesh. An ultra-low-cost, integrated solution is missing.")
]

for i, (title, desc) in enumerate(gaps):
    row = i // 3
    col = i % 3
    x = Inches(0.6 + col * 4.1)
    y = Inches(2.7 + row * 1.8)
    add_card(s5, x, y, Inches(3.9), Inches(1.6), bg_color=WHITE, border_color=ROSE, border_width=1.5)
    tb_g = s5.shapes.add_textbox(x + Inches(0.15), y + Inches(0.15), Inches(3.6), Inches(1.3))
    tf_g = tb_g.text_frame
    tf_g.word_wrap = True
    p0 = tf_g.paragraphs[0]
    p0.text = title
    p0.font.bold = True
    p0.font.size = Pt(11)
    p0.font.color.rgb = ROSE
    p1 = tf_g.add_paragraph()
    p1.text = desc
    p1.font.size = Pt(9.5)
    p1.font.color.rgb = DARK_TEXT

tb_s5_b = s5.shapes.add_textbox(Inches(0.6), Inches(6.4), Inches(12.133), Inches(0.5))
p_s5b = tb_s5_b.text_frame.paragraphs[0]
p_s5b.text = "🎯 NirmalNode Mandate: Bridge this gap with localized, predictively-triggered, incrementally-learning air purification for $67."
p_s5b.font.size = Pt(11)
p_s5b.font.bold = True
p_s5b.font.color.rgb = TEAL
p_s5b.alignment = PP_ALIGN.CENTER

# ==========================================
# SLIDE 6: WHAT MAKES NIRMALNODE DIFFERENT (CORE NOVELTY)
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "5. Core Novelty", "What Makes NirmalNode Different?", "The central answer to: What did you actually add beyond traditional systems?", "Core Innovation")

# Left: Traditional Approach
add_card(s6, Inches(0.6), Inches(1.6), Inches(4.5), Inches(4.5), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_trad = s6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.1), Inches(4.1))
tf_trad = tb_trad.text_frame
tf_trad.word_wrap = True
p_tr0 = tf_trad.paragraphs[0]
p_tr0.text = "TRADITIONAL APPROACH"
p_tr0.font.size = Pt(12)
p_tr0.font.bold = True
p_tr0.font.color.rgb = MUTED_TEXT

trad_steps = "\n• Sense (Coarse / Room scale)\n   ↓\n• Display / Predict (Static model)\n   ↓\n• Manual or Reactive Response\n\nCharacteristics:\n- City/Plant-wide scale\n- Static offline AI (frozen)\n- Reactive cleanup lag\n- Fragmented systems\n- Prohibitive cost ($500–$2000)"
p_tr1 = tf_trad.add_paragraph()
p_tr1.text = trad_steps
p_tr1.font.size = Pt(10)
p_tr1.font.color.rgb = DARK_TEXT

# Center VS badge
vs = s6.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.3), Inches(3.5), Inches(0.8), Inches(0.8))
vs.fill.solid()
vs.fill.fore_color.rgb = NAVY
vs.line.fill.background()
p_vs = vs.text_frame.paragraphs[0]
p_vs.text = "VS"
p_vs.font.bold = True
p_vs.font.size = Pt(12)
p_vs.font.color.rgb = WHITE
p_vs.alignment = PP_ALIGN.CENTER

# Right: NirmalNode Approach
add_card(s6, Inches(6.3), Inches(1.6), Inches(6.4), Inches(4.5), bg_color=LIGHT_TEAL, border_color=TEAL, border_width=2)
tb_nn = s6.shapes.add_textbox(Inches(6.5), Inches(1.8), Inches(6.0), Inches(4.1))
tf_nn = tb_nn.text_frame
tf_nn.word_wrap = True
p_nn0 = tf_nn.paragraphs[0]
p_nn0.text = "NIRMALNODE CLOSED-LOOP ARCHITECTURE"
p_nn0.font.size = Pt(12)
p_nn0.font.bold = True
p_nn0.font.color.rgb = NAVY

nn_steps = "\nSense ➔ Filter (EMA) ➔ Predict (1-2h) ➔ Decide ➔ Purify ➔ Learn ➔ Adapt\n\n8 Explicit Technical Novelties:\n1. Hotspot-Targeted Purification: Direct worker breathing zone protection\n2. Predictive Activation: Pre-emptive fan triggering 1–2 hours in advance\n3. Green IoT Architecture: Ultra-low-power ESP32 controller (1.8W standby)\n4. Green AI: Lightweight streaming models; zero GPU / deep learning overhead\n5. Incremental / Online Learning: River/scikit-learn partial-fit; zero full retraining\n6. Area-Specific Adaptation: Automatically re-tunes when moved to new sites\n7. Edge + Cloud Co-Design: Time-critical actuation local; heavy storage cloud\n8. Ultra-Low Cost Deployment: 7,400 BDT (~$67.27 USD), affordable for SMEs"
p_nn1 = tf_nn.add_paragraph()
p_nn1.text = nn_steps
p_nn1.font.size = Pt(9.5)
p_nn1.font.color.rgb = DARK_TEXT

tb_s6_b = s6.shapes.add_textbox(Inches(0.6), Inches(6.25), Inches(12.133), Inches(0.5))
p_s6b = tb_s6_b.text_frame.paragraphs[0]
p_s6b.text = "Key Takeaway: NirmalNode closes the broken loop between sensing, prediction, physical purification, and continuous learning."
p_s6b.font.size = Pt(10.5)
p_s6b.font.bold = True
p_s6b.font.color.rgb = NAVY
p_s6b.alignment = PP_ALIGN.CENTER

# ==========================================
# SLIDE 7: RESEARCH OBJECTIVES
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "6. Research Roadmap", "Research Objectives", "Clear, measurable engineering targets guiding system design and evaluation", "Research Goals")

objectives = [
    ("O1", "Low-Cost Multi-Sensor Node", "Design and assemble an ESP32-based hardware node continuously measuring PM1.0, PM2.5, PM10, CO, NO₂, VOC, NH₃, H₂S, and ambient temp/humidity/pressure at worker micro-zones.", NAVY),
    ("O2", "Cloud Telemetry Pipeline", "Construct an edge-to-cloud data pipeline transmitting JSON payloads via Wi-Fi (HTTP REST / MQTT) with time-, day-, and location-tagged circular storage and web dashboarding.", TEAL),
    ("O3", "1–2 Hour Ahead Forecasting", "Develop an Adaptive AI model initially pre-trained on historical Bangladesh air-quality records, capable of forecasting hotspot PM2.5 concentrations 1–2 hours in advance.", AMBER),
    ("O4", "Incremental Adaptive Learning", "Implement stream-learning estimators (SGD Regressor, Passive-Aggressive, Hoeffding Trees) to update weights continuously without full retraining, adapting to relocations.", RGBColor(109, 40, 217)),
    ("O5", "3-Stage Purification Unit", "Engineer and prototype a localized filtration train (cyclone separator, HEPA-H13 filter, activated-carbon pad, 12V fan) triggered automatically ahead of hazard threshold crossings.", EMERALD),
    ("O6", "Multi-Dimensional Evaluation", "Rigorously evaluate predictive accuracy (MAE, RMSE, R², F1), prequential convergence, physical filtration efficiency (PM1.0, PM2.5, PM10), power profile, and BOM economics.", ROSE)
]

for i, (num, title, desc, col) in enumerate(objectives):
    row = i // 2
    c = i % 2
    x = Inches(0.6 + c * 6.2)
    y = Inches(1.6 + row * 1.65)
    add_card(s7, x, y, Inches(5.9), Inches(1.45), bg_color=SLATE_BG, border_color=BORDER_COL)
    
    # Num circle
    num_shape = s7.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.15), y + Inches(0.15), Inches(0.5), Inches(0.5))
    num_shape.fill.solid()
    num_shape.fill.fore_color.rgb = col
    num_shape.line.fill.background()
    p_num = num_shape.text_frame.paragraphs[0]
    p_num.text = num
    p_num.font.bold = True
    p_num.font.size = Pt(11)
    p_num.font.color.rgb = WHITE
    p_num.alignment = PP_ALIGN.CENTER
    
    tb = s7.shapes.add_textbox(x + Inches(0.75), y + Inches(0.12), Inches(5.0), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.bold = True
    p0.font.size = Pt(11)
    p0.font.color.rgb = col
    p1 = tf.add_paragraph()
    p1.text = desc
    p1.font.size = Pt(9.5)
    p1.font.color.rgb = DARK_TEXT

tb_s7_b = s7.shapes.add_textbox(Inches(0.6), Inches(6.6), Inches(12.133), Inches(0.4))
p_s7b = tb_s7_b.text_frame.paragraphs[0]
p_s7b.text = "Roadmap Structure: O1–O5 define Methodology (Chapter 3), O6 governs Experimental Evaluation (Chapter 4)."
p_s7b.font.size = Pt(10)
p_s7b.font.bold = True
p_s7b.font.color.rgb = MUTED_TEXT
p_s7b.alignment = PP_ALIGN.CENTER

# ==========================================
# SLIDE 8: END-TO-END SYSTEM
# ==========================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "7. System Methodology", "NirmalNode: End-to-End System", "Layered technical architecture and the complete physical-to-intelligence loop", "System Architecture")

# Left: 5-Layer Architecture Image
add_card(s8, Inches(0.6), Inches(1.6), Inches(6.2), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("figures_academic/five_layer_architecture_academic.png")):
    s8.shapes.add_picture(get_path("figures_academic/five_layer_architecture_academic.png"), Inches(0.7), Inches(1.7), width=Inches(6.0), height=Inches(4.7))
tb_s8a = s8.shapes.add_textbox(Inches(0.7), Inches(6.45), Inches(6.0), Inches(0.4))
tb_s8a.text_frame.paragraphs[0].text = "Figure 3.1: Five-layer system architecture (Sensors → MCU → Cloud → AI → Actuator)"
tb_s8a.text_frame.paragraphs[0].font.size = Pt(9)
tb_s8a.text_frame.paragraphs[0].font.italic = True
tb_s8a.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right: System Workflow Image + Summary
add_card(s8, Inches(7.0), Inches(1.6), Inches(5.7), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/system_workflow.png")):
    s8.shapes.add_picture(get_path("extracted_figs/system_workflow.png"), Inches(7.1), Inches(1.7), width=Inches(5.5), height=Inches(3.2))
tb_s8b = s8.shapes.add_textbox(Inches(7.1), Inches(4.95), Inches(5.5), Inches(1.8))
tf_s8b = tb_s8b.text_frame
tf_s8b.word_wrap = True
p0 = tf_s8b.paragraphs[0]
p0.text = "Figure 3.2: Complete closed-loop operational workflow"
p0.font.size = Pt(9)
p0.font.italic = True
p0.font.color.rgb = MUTED_TEXT

p1 = tf_s8b.add_paragraph()
p1.text = "1. Environmental Sensing: 12 raw channels sampled continuously\n2. Edge Filtering: Exponential Moving Average on ESP32 (α=0.25)\n3. Cloud Dispatch: Ingestion to database and streaming model arena\n4. Predictive Action: Relay triggers fan pre-emptively ahead of hazard\n5. Continuous Learning: Stream gradients update model weights in real time"
p1.font.size = Pt(9)
p1.font.color.rgb = DARK_TEXT

# ==========================================
# SLIDE 9: HARDWARE IMPLEMENTATION
# ==========================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "8. Hardware Engineering", "Hardware Implementation", "Multi-sensor hardware integration centered on a single low-power ESP32 controller", "Hardware Subsystem")

# Left: Composite Hardware Diagram
add_card(s9, Inches(0.6), Inches(1.6), Inches(7.8), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("fig01_hardware_composite.png")):
    s9.shapes.add_picture(get_path("fig01_hardware_composite.png"), Inches(0.7), Inches(1.7), width=Inches(7.6), height=Inches(4.8))
tb_s9c = s9.shapes.add_textbox(Inches(0.7), Inches(6.55), Inches(7.6), Inches(0.3))
tb_s9c.text_frame.paragraphs[0].text = "Figure 3.5: NirmalNode hardware interfacing diagram (Source: Project Prototype / Thesis)"
tb_s9c.text_frame.paragraphs[0].font.size = Pt(9)
tb_s9c.text_frame.paragraphs[0].font.italic = True
tb_s9c.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right: Component Specifications
add_card(s9, Inches(8.6), Inches(1.6), Inches(4.1), Inches(5.3), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_hw = s9.shapes.add_textbox(Inches(8.8), Inches(1.75), Inches(3.7), Inches(5.0))
tf_hw = tb_hw.text_frame
tf_hw.word_wrap = True
p_hw0 = tf_hw.paragraphs[0]
p_hw0.text = "Key Components (Table 3.1)"
p_hw0.font.bold = True
p_hw0.font.size = Pt(13)
p_hw0.font.color.rgb = NAVY

hw_items = [
    ("ESP32 Dev Module", "Xtensa 32-bit dual-core 240MHz, Wi-Fi/BLE, ADC1, UART2"),
    ("PMS5003 Laser", "PM1.0, PM2.5, PM10 mass concentration (UART2)"),
    ("MiCS-4514 Dual", "CO (RED pin) & NO₂ (OX pin) analog ADC channels"),
    ("MQ135 Gas Sensor", "VOC, NH₃, Smoke, broad-spectrum air quality"),
    ("MQ136 Gas Sensor", "H₂S / Sulphur gas detection for chemical hotspots"),
    ("MP135 Sensor", "Supplementary relative VOC air quality channel"),
    ("BME280 (Optional)", "Ambient Temperature, Humidity, and Pressure (I2C)"),
    ("Relay & 12V DC Fan", "Optocoupled 5V relay driving 12V 0.5A exhaust fan"),
    ("Power Subsystem", "3S Li-Po (11.1V, 55.5 Wh) + BMS + Buck (5V 3A)")
]

for title, desc in hw_items:
    p = tf_hw.add_paragraph()
    p.text = f"• {title}: {desc}"
    p.font.size = Pt(8.5)
    p.font.color.rgb = DARK_TEXT

# ==========================================
# SLIDE 10: HARDWARE ARCHITECTURE & DATA FLOW
# ==========================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "9. Signal Processing", "From Sensors to the AI Engine", "Data acquisition flow, on-device noise filtering, and edge-to-cloud telemetry dispatch", "Sensor Data Pipeline")

# Left: Hardware Block Diagram
add_card(s10, Inches(0.6), Inches(1.6), Inches(6.8), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/hardware_block_diagram.png")):
    s10.shapes.add_picture(get_path("extracted_figs/hardware_block_diagram.png"), Inches(0.7), Inches(1.7), width=Inches(6.6), height=Inches(4.8))
tb_s10c = s10.shapes.add_textbox(Inches(0.7), Inches(6.55), Inches(6.6), Inches(0.3))
tb_s10c.text_frame.paragraphs[0].text = "Figure 3.5b: Physical block diagram and bus-level interfacing between sensors, MCU, and actuators"
tb_s10c.text_frame.paragraphs[0].font.size = Pt(9)
tb_s10c.text_frame.paragraphs[0].font.italic = True
tb_s10c.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right: Technical Flow
add_card(s10, Inches(7.6), Inches(1.6), Inches(5.1), Inches(5.3), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_pipe = s10.shapes.add_textbox(Inches(7.8), Inches(1.75), Inches(4.7), Inches(5.0))
tf_pipe = tb_pipe.text_frame
tf_pipe.word_wrap = True

p_p0 = tf_pipe.paragraphs[0]
p_p0.text = "Edge Signal Flow (Algorithm 1)"
p_p0.font.bold = True
p_p0.font.size = Pt(13)
p_p0.font.color.rgb = NAVY

pipe_steps = [
    ("1. Synchronous Sampling (Δt = 2s)", "ESP32 polls digital UART2 packets from PMS5003 and 12-bit ADC values from analog MOS gas array synchronously."),
    ("2. On-Device EMA Filtering", "Raw MOS gas readings undergo Exponential Moving Average noise filtering:\n   x̂[k] = α · x_raw[k] + (1 - α) · x̂[k-1]\nSmoothing constant α = 0.25 suppresses sensor jitter while maintaining fast response to industrial spikes."),
    ("3. JSON Record Packetization", "Calibrated values assemble into structured telemetry payload with timestamp, node ID, and multi-gas feature vector."),
    ("4. Wireless Dispatch & Feedback", "Record is HTTP-POSTed to Flask backend (/api/ingest); relay state (FAN_ON / FAN_OFF) returned in HTTP response.")
]

for title, desc in pipe_steps:
    p = tf_pipe.add_paragraph()
    p.text = f"{title}\n{desc}\n"
    p.font.size = Pt(9.5)
    p.font.color.rgb = DARK_TEXT

# ==========================================
# SLIDE 11: SOFTWARE & DATA PROCESSING PIPELINE
# ==========================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "10. Software Architecture", "Software and Data Processing Pipeline", "Firmware routines, server-side ingestion, and the closed-loop actuator feedback cycle", "Software Architecture")

# Left: Software Block Diagram
add_card(s11, Inches(0.6), Inches(1.6), Inches(6.8), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("software_block_diagram.png")):
    s11.shapes.add_picture(get_path("software_block_diagram.png"), Inches(0.7), Inches(1.7), width=Inches(6.6), height=Inches(4.8))
tb_s11c = s11.shapes.add_textbox(Inches(0.7), Inches(6.55), Inches(6.6), Inches(0.3))
tb_s11c.text_frame.paragraphs[0].text = "Figure 3.6: Software block diagram spanning device-side firmware and server-side cloud services"
tb_s11c.text_frame.paragraphs[0].font.size = Pt(9)
tb_s11c.text_frame.paragraphs[0].font.italic = True
tb_s11c.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right: Dual-Partition Breakdown
add_card(s11, Inches(7.6), Inches(1.6), Inches(5.1), Inches(5.3), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_sw = s11.shapes.add_textbox(Inches(7.8), Inches(1.75), Inches(4.7), Inches(5.0))
tf_sw = tb_sw.text_frame
tf_sw.word_wrap = True

p_sw0 = tf_sw.paragraphs[0]
p_sw0.text = "Pipeline Subsystems"
p_sw0.font.bold = True
p_sw0.font.size = Pt(13)
p_sw0.font.color.rgb = NAVY

sw_blocks = [
    ("ESP32 Firmware (AirGuard_WiFi.ino)", "• 48-hour burn-in clean-air calibration (calibrateSensors())\n• 2-second non-blocking timer interrupt loop\n• On-device EMA noise filtering & temperature compensation\n• Direct GPIO25 relay driver switching 12V fan"),
    ("Python Flask Backend (server.py)", "• REST endpoint /api/ingest parses incoming JSON\n• Synchronous call to AdaptiveAIEngine.predict_and_learn()\n• In-memory circular buffer (500 records) & SQLite logging\n• Returns fan relay command in the same HTTP transaction (<15ms)"),
    ("Client Dashboard (app.js / index.html)", "• 2-second polling of /api/latest telemetry\n• US EPA AQI gauge, multi-gas bars, Chart.js time-series\n• Auto-AI / Manual purifier control override toggles")
]

for title, desc in sw_blocks:
    p = tf_sw.add_paragraph()
    p.text = f"{title}\n{desc}\n"
    p.font.size = Pt(9)
    p.font.color.rgb = DARK_TEXT

# ==========================================
# SLIDE 12: ADAPTIVE AI ENGINE
# ==========================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "11. Machine Learning", "Adaptive AI: Prediction That Keeps Learning", "Streaming incremental learning algorithms that eliminate batch retraining overhead", "Machine Learning Pipeline")

# Left: AI Pipeline Diagram
add_card(s12, Inches(0.6), Inches(1.6), Inches(6.5), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/ai_model_arena_pipeline.png")):
    s12.shapes.add_picture(get_path("extracted_figs/ai_model_arena_pipeline.png"), Inches(0.7), Inches(1.7), width=Inches(6.3), height=Inches(4.8))
tb_s12c = s12.shapes.add_textbox(Inches(0.7), Inches(6.55), Inches(6.3), Inches(0.3))
tb_s12c.text_frame.paragraphs[0].text = "Figure 3.7: Adaptive AI pipeline: Initial batch pre-training to streaming incremental prequential learning"
tb_s12c.text_frame.paragraphs[0].font.size = Pt(9)
tb_s12c.text_frame.paragraphs[0].font.italic = True
tb_s12c.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right: AI Arena & Adaptivity
add_card(s12, Inches(7.3), Inches(1.6), Inches(5.4), Inches(5.3), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_ai = s12.shapes.add_textbox(Inches(7.5), Inches(1.75), Inches(5.0), Inches(5.0))
tf_ai = tb_ai.text_frame
tf_ai.word_wrap = True

p_ai0 = tf_ai.paragraphs[0]
p_ai0.text = "Key Principle: NO FULL RETRAINING"
p_ai0.font.bold = True
p_ai0.font.size = Pt(13)
p_ai0.font.color.rgb = TEAL

p_ai_desc = tf_ai.add_paragraph()
p_ai_desc.text = "Model parameters update sample-by-sample via the prequential (test-then-train) protocol using River & scikit-learn partial_fit."
p_ai_desc.font.size = Pt(10)
p_ai_desc.font.color.rgb = DARK_TEXT

ai_points = [
    ("9 Models Evaluated in Arena:", "• M1–M3: SGD Ridge, Lasso, ElasticNet\n• M4: SGD Huber (Robust against smoke outliers)\n• M5: SGD Support Vector Regressor (SVR)\n• M6–M7: Passive-Aggressive Regressors (C=1.0, C=0.1)\n• M8 (Champion): SGD + PA Blend (Lowest MAE = 10.62)\n• M9: Baseline Exponential Moving Average"),
    ("Area-Specific Adaptation:", "When relocated across different industrial clusters (e.g., Gazipur garment cluster to Narayanganj textile dyeing), incoming stream gradients automatically shift model weights without human intervention."),
    ("Green AI Compute:", "Linear and stream-tree estimators require <5 ms inference and minimal RAM, making them ideal for edge deployment.")
]

for title, desc in ai_points:
    p = tf_ai.add_paragraph()
    p.text = f"\n{title}\n{desc}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = DARK_TEXT

# ==========================================
# SLIDE 13: PREDICTIVE DECISION ENGINE
# ==========================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "12. Actuation Logic", "From Prediction to Physical Action", "Threshold-based predictive activation closing the loop between AI forecasts and hardware", "Actuation Logic")

# Left: Decision Flowchart
add_card(s13, Inches(0.6), Inches(1.6), Inches(5.4), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/purifier_decision_flowchart.png")):
    s13.shapes.add_picture(get_path("extracted_figs/purifier_decision_flowchart.png"), Inches(0.7), Inches(1.7), width=Inches(5.2), height=Inches(4.8))
tb_s13c = s13.shapes.add_textbox(Inches(0.7), Inches(6.55), Inches(5.2), Inches(0.3))
tb_s13c.text_frame.paragraphs[0].text = "Figure 3.9: Threshold-based closed-loop purifier decision flowchart (Algorithm 2)"
tb_s13c.text_frame.paragraphs[0].font.size = Pt(9)
tb_s13c.text_frame.paragraphs[0].font.italic = True
tb_s13c.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right: Logic & Pre-emptive Comparison
add_card(s13, Inches(6.2), Inches(1.6), Inches(6.5), Inches(5.3), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_dec = s13.shapes.add_textbox(Inches(6.4), Inches(1.75), Inches(6.1), Inches(5.0))
tf_dec = tb_dec.text_frame
tf_dec.word_wrap = True

p_d0 = tf_dec.paragraphs[0]
p_d0.text = "The Closed-Loop Decision Engine"
p_d0.font.bold = True
p_d0.font.size = Pt(13)
p_d0.font.color.rgb = NAVY

dec_text = "\nThreshold Decision Rule (Equation 3.12):\n   d_t = FAN_ON   if ŷ_(t+h) ≥ τ_hazard (35.5 μg/m³)\n   d_t = FAN_OFF  if ŷ_(t+h) < τ_hazard\n\nReactive vs. Predictive Operation:\n\n• Reactive (Traditional Failure):\n  Pollution rises ➔ Crosses threshold ➔ Sensor detects ➔ Fan starts ➔ Worker has already inhaled the peak toxic plume.\n\n• Predictive (NirmalNode Advantage):\n  AI forecasts spike 1–2h ahead ➔ Fan triggers pre-emptively ➔ Chamber airflow establishes ➔ Breathing zone cleared BEFORE peak hazard materializes!\n\nExperimental Verification:\n• In bench laboratory tests with sudden point-source incense smoke, the predictive trigger fired 4–6 seconds before PM2.5 reached 35.5 μg/m³ at the sensor inlet.\n• Built-in hysteresis buffer prevents fan chatter during marginal threshold crossings."
p_d1 = tf_dec.add_paragraph()
p_d1.text = dec_text
p_d1.font.size = Pt(9.5)
p_d1.font.color.rgb = DARK_TEXT

# ==========================================
# SLIDE 14: PURIFICATION SUBSYSTEM
# ==========================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "13. Filtration Train", "Localized 3-Stage Air Purification", "Sequential physical separation: Cyclone pre-filter → HEPA-H13 → Activated Carbon bed", "Filtration Train")

# Top: Purification Pipeline Image
add_card(s14, Inches(0.6), Inches(1.6), Inches(12.133), Inches(2.5), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/purification_pipeline.png")):
    s14.shapes.add_picture(get_path("extracted_figs/purification_pipeline.png"), Inches(0.7), Inches(1.7), width=Inches(11.9), height=Inches(2.0))
tb_s14c = s14.shapes.add_textbox(Inches(0.7), Inches(3.75), Inches(11.9), Inches(0.3))
tb_s14c.text_frame.paragraphs[0].text = "Figure 3.3: Local air purification train (Cyclone separator → HEPA-H13 filter → Activated carbon bed)"
tb_s14c.text_frame.paragraphs[0].font.size = Pt(9)
tb_s14c.text_frame.paragraphs[0].font.italic = True
tb_s14c.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Bottom: 3 Stage Cards
stages = [
    ("Stage 1: Cyclone Separator", "Centrifugal Pre-Filter",
     "• Tangential swirl induces centrifugal force: F_c = m·v_t² / r\n• Extracts coarse particles (>10 μm: metal dust, grit, soot)\n• Critical Role: Extends expensive HEPA filter lifespan by 3×–5× by preventing dust caking.", AMBER),
    ("Stage 2: HEPA-H13 Filter", "Fine Particulate Filtration",
     "• Dense micro-glass fiber mat\n• Certified ≥99.97% efficiency at 0.3 μm particles\n• Measured Prototype Efficiency (Table 4.8):\n  - PM1.0: 95.7% (42 → 1.8 μg/m³)\n  - PM2.5: 95.7% (67 → 2.9 μg/m³)\n  - PM10: 98.6% (Combined with cyclone)", NAVY_LIGHT),
    ("Stage 3: Activated Carbon Bed", "Gas & Odour Adsorption",
     "• Massive microporous internal surface area (>1000 m²/g)\n• Langmuir physical adsorption for VOCs, CO, NO₂, NH₃, H₂S\n• Measured: ~60–70% VOC reduction; H₂S reduced below detection limit.\n• Scientific Fact: HEPA cannot filter gases; carbon handles gas removal.", RGBColor(109, 40, 217))
]

for i, (title, tag, desc, col) in enumerate(stages):
    x = Inches(0.6 + i * 4.1)
    card = add_card(s14, x, Inches(4.2), Inches(3.9), Inches(2.7), bg_color=SLATE_BG, border_color=col, border_width=1.5)
    tb = s14.shapes.add_textbox(x + Inches(0.15), Inches(4.3), Inches(3.6), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = tag.upper()
    p0.font.bold = True
    p0.font.size = Pt(9)
    p0.font.color.rgb = col
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.bold = True
    p1.font.size = Pt(11.5)
    p1.font.color.rgb = NAVY
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = DARK_TEXT

# ==========================================
# SLIDE 15: PROTOTYPE & EXPERIMENTAL EVALUATION
# ==========================================
s15 = prs.slides.add_slide(blank_layout)
add_header(s15, "14. Experimental Design", "Prototype and Experimental Evaluation", "Test environments, evaluation protocol, and real-time operational dashboard interfaces", "Experimental Setup")

# Left: Web Dashboard
add_card(s15, Inches(0.6), Inches(1.6), Inches(5.8), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/dashboard_screenshot.jpg")):
    s15.shapes.add_picture(get_path("extracted_figs/dashboard_screenshot.jpg"), Inches(0.7), Inches(1.7), width=Inches(5.6), height=Inches(4.8))
tb_s15a = s15.shapes.add_textbox(Inches(0.7), Inches(6.55), Inches(5.6), Inches(0.3))
tb_s15a.text_frame.paragraphs[0].text = "Figure 4.1: NirmalNode real-time web dashboard (AQI gauge, 1h/2h AI forecasts, sensor cards, auto-AI fan)"
tb_s15a.text_frame.paragraphs[0].font.size = Pt(9)
tb_s15a.text_frame.paragraphs[0].font.italic = True
tb_s15a.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right Top: XAI Dashboard
add_card(s15, Inches(6.6), Inches(1.6), Inches(6.1), Inches(2.7), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/xai_dashboard_screenshot.jpg")):
    s15.shapes.add_picture(get_path("extracted_figs/xai_dashboard_screenshot.jpg"), Inches(6.7), Inches(1.7), width=Inches(5.9), height=Inches(2.2))
tb_s15b = s15.shapes.add_textbox(Inches(6.7), Inches(3.95), Inches(5.9), Inches(0.3))
tb_s15b.text_frame.paragraphs[0].text = "Figure 4.7: Explainable AI dashboard showing live SHAP contributions and active fan status"
tb_s15b.text_frame.paragraphs[0].font.size = Pt(8.5)
tb_s15b.text_frame.paragraphs[0].font.italic = True
tb_s15b.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right Bottom: Test Protocol Text
add_card(s15, Inches(6.6), Inches(4.4), Inches(6.1), Inches(2.5), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_s15t = s15.shapes.add_textbox(Inches(6.8), Inches(4.5), Inches(5.7), Inches(2.3))
tf_s15t = tb_s15t.text_frame
tf_s15t.word_wrap = True

p_t0 = tf_s15t.paragraphs[0]
p_t0.text = "Experimental Protocols & Scientific Honesty"
p_t0.font.bold = True
p_t0.font.size = Pt(12)
p_t0.font.color.rgb = NAVY

p_t1 = tf_s15t.add_paragraph()
p_t1.text = "• Controlled Laboratory Bench: Physical prototype tested with incense-smoke spike injection (~15 cm from inlet) to validate sensor response and closed-loop relay trigger.\n• Prequential Stream Benchmark: 500-sample industrial stream (sinusoidal baseline mean 28.3 μg/m³, periodic combustion spikes up to 77 μg/m³, Δt=2s) testing continuous online learning.\n• Scientific Honesty: Quantitative AI prequential accuracy is evaluated on the calibrated simulation stream; hardware bench test validates physical trigger and airflow."
p_t1.font.size = Pt(8.5)
p_t1.font.color.rgb = DARK_TEXT

# ==========================================
# SLIDE 16: AI RESULTS
# ==========================================
s16 = prs.slides.add_slide(blank_layout)
add_header(s16, "15. Quantitative AI Results", "Adaptive AI Performance", "Prequential evaluation metrics, model comparison arena, and hazard-detection verification", "Experimental Findings")

# Left: Model Comparison Chart
add_card(s16, Inches(0.6), Inches(1.6), Inches(6.4), Inches(3.8), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/model_arena_comparison.png")):
    s16.shapes.add_picture(get_path("extracted_figs/model_arena_comparison.png"), Inches(0.7), Inches(1.7), width=Inches(6.2), height=Inches(3.3))
tb_s16a = s16.shapes.add_textbox(Inches(0.7), Inches(5.05), Inches(6.2), Inches(0.3))
tb_s16a.text_frame.paragraphs[0].text = "Figure 4.2: Prequential forecasting error across 9 incremental models (Champion M8 lowest MAE = 10.62 μg/m³)"
tb_s16a.text_frame.paragraphs[0].font.size = Pt(8.5)
tb_s16a.text_frame.paragraphs[0].font.italic = True
tb_s16a.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right: Confusion Matrix
add_card(s16, Inches(7.2), Inches(1.6), Inches(5.5), Inches(3.8), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/confusion_matrix.png")):
    s16.shapes.add_picture(get_path("extracted_figs/confusion_matrix.png"), Inches(7.3), Inches(1.7), width=Inches(5.3), height=Inches(3.3))
tb_s16b = s16.shapes.add_textbox(Inches(7.3), Inches(5.05), Inches(5.3), Inches(0.3))
tb_s16b.text_frame.paragraphs[0].text = "Figure 4.3: Purifier trigger confusion matrix (N=500, Hazard threshold = 35.5 μg/m³)"
tb_s16b.text_frame.paragraphs[0].font.size = Pt(8.5)
tb_s16b.text_frame.paragraphs[0].font.italic = True
tb_s16b.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Bottom: 6 KPI Cards
kpis = [
    ("10.62", "MAE (μg/m³)", "Baseline was 15.8", NAVY),
    ("17.43", "RMSE (μg/m³)", "Baseline was 24.3", NAVY),
    ("0.7334", "R² Score", "Strong fit on stream", TEAL),
    ("0.940", "Hazard F1-Score", "Prec: 91.6% | Rec: 96.5%", EMERALD),
    ("97.2%", "Overall Accuracy", "AUC-ROC: 0.985", EMERALD),
    ("0.8%", "Missed Hazard Rate", "Only 4 FN in 500 samples!", ROSE)
]

for i, (val, label, sub, col) in enumerate(kpis):
    x = Inches(0.6 + i * 2.05)
    card = add_card(s16, x, Inches(5.55), Inches(1.9), Inches(1.35), bg_color=SLATE_BG, border_color=col, border_width=1.5)
    tb = s16.shapes.add_textbox(x, Inches(5.65), Inches(1.9), Inches(1.15))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = val
    p0.font.bold = True
    p0.font.size = Pt(17)
    p0.font.color.rgb = col
    p0.alignment = PP_ALIGN.CENTER
    p1 = tf.add_paragraph()
    p1.text = label
    p1.font.bold = True
    p1.font.size = Pt(8.5)
    p1.font.color.rgb = DARK_TEXT
    p1.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.size = Pt(7.5)
    p2.font.color.rgb = MUTED_TEXT
    p2.alignment = PP_ALIGN.CENTER

# ==========================================
# SLIDE 17: ADAPTATION & EXPLAINABILITY
# ==========================================
s17 = prs.slides.add_slide(blank_layout)
add_header(s17, "16. Online Adaptation & XAI", "Adaptation and Explainability", "Empirical proof of incremental convergence and transparent SHAP feature contributions", "Adaptivity Evidence")

# Left: Convergence Plot
add_card(s17, Inches(0.6), Inches(1.6), Inches(5.8), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/prequential_error_plot.jpg")):
    s17.shapes.add_picture(get_path("extracted_figs/prequential_error_plot.jpg"), Inches(0.7), Inches(1.7), width=Inches(5.6), height=Inches(4.8))
tb_s17a = s17.shapes.add_textbox(Inches(0.7), Inches(6.55), Inches(5.6), Inches(0.3))
tb_s17a.text_frame.paragraphs[0].text = "Figure 4.6: Prequential error convergence curve (Cold Start → Adaptation → Convergence)"
tb_s17a.text_frame.paragraphs[0].font.size = Pt(9)
tb_s17a.text_frame.paragraphs[0].font.italic = True
tb_s17a.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right Top: Feature Importance
add_card(s17, Inches(6.6), Inches(1.6), Inches(6.1), Inches(3.0), bg_color=WHITE, border_color=BORDER_COL)
if os.path.exists(get_path("extracted_figs/xai_feature_importance.png")):
    s17.shapes.add_picture(get_path("extracted_figs/xai_feature_importance.png"), Inches(6.7), Inches(1.7), width=Inches(5.9), height=Inches(2.5))
tb_s17b = s17.shapes.add_textbox(Inches(6.7), Inches(4.25), Inches(5.9), Inches(0.3))
tb_s17b.text_frame.paragraphs[0].text = "Figure 4.8: Global feature importance via Linear Feature Contribution (LFC / Exact SHAP)"
tb_s17b.text_frame.paragraphs[0].font.size = Pt(8.5)
tb_s17b.text_frame.paragraphs[0].font.italic = True
tb_s17b.text_frame.paragraphs[0].font.color.rgb = MUTED_TEXT

# Right Bottom: Synthesis Box
add_card(s17, Inches(6.6), Inches(4.7), Inches(6.1), Inches(2.2), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_s17c = s17.shapes.add_textbox(Inches(6.8), Inches(4.8), Inches(5.7), Inches(2.0))
tf_s17c = tb_s17c.text_frame
tf_s17c.word_wrap = True

p_c0 = tf_s17c.paragraphs[0]
p_c0.text = "Validation of the Adaptivity Claim"
p_c0.font.bold = True
p_c0.font.size = Pt(12)
p_c0.font.color.rgb = TEAL

p_c1 = tf_s17c.add_paragraph()
p_c1.text = "• Phase 1 (Cold Start, N=1–50): High initial MAE = 33.4 μg/m³.\n• Phase 2 (Adaptation, N=50–200): Steep error decline as streaming weights adjust.\n• Phase 3 (Convergence, N=200–500): Stabilizes at 10.62 μg/m³.\n➔ 68% error reduction achieved purely from live data without batch retraining!\n• XAI Transparency: Model relies primarily on physical temporal signals (PM2.5 EMA: 0.224, current PM2.5: 0.186, PM10: 0.142) — validating explainable behavior."
p_c1.font.size = Pt(8.5)
p_c1.font.color.rgb = DARK_TEXT

# ==========================================
# SLIDE 18: FEASIBILITY (PURIFICATION, POWER & COST)
# ==========================================
s18 = prs.slides.add_slide(blank_layout)
add_header(s18, "17. Practical Feasibility", "Practical Feasibility: Purification, Energy and Cost", "Authoritative verification of filtration efficiency, power budget, and BOM economics", "Engineering Feasibility")

# Left Column: Purification (Top) & Power (Bottom)
add_card(s18, Inches(0.6), Inches(1.6), Inches(5.0), Inches(2.5), bg_color=WHITE, border_color=BORDER_COL)
tb_puf = s18.shapes.add_textbox(Inches(0.7), Inches(1.7), Inches(4.8), Inches(2.3))
tf_puf = tb_puf.text_frame
tf_puf.word_wrap = True
p_puf0 = tf_puf.paragraphs[0]
p_puf0.text = "Purification Efficiency (Table 4.8)"
p_puf0.font.bold = True
p_puf0.font.size = Pt(11.5)
p_puf0.font.color.rgb = NAVY

p_puf1 = tf_puf.add_paragraph()
p_puf1.text = "• PM1.0 (HEPA stage): 42 → 1.8 μg/m³  ➔  95.7%\n• PM2.5 (HEPA stage): 67 → 2.9 μg/m³  ➔  95.7%\n• PM10 (Cyclone+HEPA): 98 → 1.4 μg/m³  ➔  98.6%\n• VOC / Odour (Carbon): Qualitative  ➔  ~60–70%"
p_puf1.font.size = Pt(9.5)
p_puf1.font.color.rgb = DARK_TEXT

add_card(s18, Inches(0.6), Inches(4.3), Inches(5.0), Inches(2.6), bg_color=SLATE_BG, border_color=BORDER_COL)
tb_pow = s18.shapes.add_textbox(Inches(0.7), Inches(4.4), Inches(4.8), Inches(2.4))
tf_pow = tb_pow.text_frame
tf_pow.word_wrap = True
p_pow0 = tf_pow.paragraphs[0]
p_pow0.text = "Power Consumption Profile (Table 4.9)"
p_pow0.font.bold = True
p_pow0.font.size = Pt(11.5)
p_pow0.font.color.rgb = NAVY

p_pow1 = tf_pow.add_paragraph()
p_pow1.text = "• Standby (Sensing/Idle): ≈ 1.8 W\n• Wi-Fi Transmitting (HTTP POST): ≈ 2.6 W\n• Purifier Fan ON (Full speed): ≈ 6.0 W\n• Worst-Case Peak Load: ≈ 8.6 W\n\n🔋 55.5 Wh Li-Po Battery Life: ~30h in standby; ~17h effective shift runtime at 25% duty cycle."
p_pow1.font.size = Pt(9)
p_pow1.font.color.rgb = DARK_TEXT

# Right Column: Complete BOM Table
add_card(s18, Inches(5.8), Inches(1.6), Inches(6.9), Inches(5.3), bg_color=WHITE, border_color=BORDER_COL)
tb_bom_t = s18.shapes.add_textbox(Inches(6.0), Inches(1.7), Inches(6.5), Inches(0.4))
tb_bom_t.text_frame.paragraphs[0].text = "Prototype Bill of Materials (Table 4.10) — Exact Retail Pricing"
tb_bom_t.text_frame.paragraphs[0].font.bold = True
tb_bom_t.text_frame.paragraphs[0].font.size = Pt(11.5)
tb_bom_t.text_frame.paragraphs[0].font.color.rgb = NAVY

# Table 4.10
bom_rows = [
    ("ESP32 Dev Module (WROOM-32)", "1", "350", "$3.18"),
    ("PMS5003 Laser Particulate Sensor", "1", "2,200", "$20.00"),
    ("MiCS-4514 Dual Gas Sensor (CO/NO₂)", "1", "1,650", "$15.00"),
    ("MQ135 Gas Sensor Module (VOC/NH₃)", "1", "180", "$1.64"),
    ("MQ136 Gas Sensor Module (H₂S)", "1", "220", "$2.00"),
    ("MP135 Sensor Module (Air Quality)", "1", "180", "$1.64"),
    ("BME280 Environmental Sensor (T/H/P)", "1", "280", "$2.55"),
    ("5V Relay Module (Fan Control)", "1", "90", "$0.82"),
    ("12V DC Brushless Fan", "1", "400", "$3.64"),
    ("Cyclone Separator (Fabricated)", "1", "350", "$3.18"),
    ("HEPA-H13 Filter Element", "1", "650", "$5.91"),
    ("Activated Carbon Filter Pad", "1", "250", "$2.27"),
    ("Enclosure, Wiring, PCB, Connectors", "1 set", "600", "$5.45"),
    ("TOTAL PROTOTYPE COST", "1 unit", "7,400 BDT", "$67.27 USD")
]

table_bom = s18.shapes.add_table(15, 4, Inches(6.0), Inches(2.1), Inches(6.5), Inches(4.6)).table
table_bom.columns[0].width = Inches(3.6)
table_bom.columns[1].width = Inches(0.8)
table_bom.columns[2].width = Inches(1.1)
table_bom.columns[3].width = Inches(1.0)

b_headers = ["Component", "Qty", "Cost (BDT)", "Cost (USD)"]
for c, h in enumerate(b_headers):
    cell = table_bom.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(8.5)
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER if c == 1 else (PP_ALIGN.RIGHT if c > 1 else PP_ALIGN.LEFT)

for r, rdata in enumerate(bom_rows):
    for c, val in enumerate(rdata):
        cell = table_bom.cell(r + 1, c)
        cell.fill.solid()
        if r == 13: # Total Row
            cell.fill.fore_color.rgb = RGBColor(224, 242, 254)
        else:
            cell.fill.fore_color.rgb = SLATE_BG if r % 2 == 0 else WHITE
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(8)
        p.font.name = 'Arial'
        if r == 13:
            p.font.bold = True
            p.font.color.rgb = NAVY
        else:
            p.font.color.rgb = DARK_TEXT
        p.alignment = PP_ALIGN.CENTER if c == 1 else (PP_ALIGN.RIGHT if c > 1 else PP_ALIGN.LEFT)

# ==========================================
# SLIDE 19: CORE CONTRIBUTIONS
# ==========================================
s19 = prs.slides.add_slide(blank_layout)
add_header(s19, "18. Summary of Novelty", "Core Contributions of NirmalNode", "Unified synthesis of the eight fundamental engineering innovations", "Summary of Novelty")

# Center Hub Box
hub = add_card(s19, Inches(5.1), Inches(2.9), Inches(3.1), Inches(1.6), bg_color=NAVY, border_color=TEAL, border_width=2.5)
tb_hub = s19.shapes.add_textbox(Inches(5.2), Inches(3.1), Inches(2.9), Inches(1.2))
tf_hub = tb_hub.text_frame
tf_hub.word_wrap = True
p_h0 = tf_hub.paragraphs[0]
p_h0.text = "NIRMALNODE"
p_h0.font.bold = True
p_h0.font.size = Pt(17)
p_h0.font.color.rgb = WHITE
p_h0.alignment = PP_ALIGN.CENTER
p_h1 = tf_hub.add_paragraph()
p_h1.text = "Integrated Edge-AI Platform"
p_h1.font.size = Pt(10)
p_h1.font.color.rgb = RGBColor(186, 230, 253)
p_h1.alignment = PP_ALIGN.CENTER

# 8 Surrounding Pillars
pillars = [
    ("1. Hotspot-Targeted", "Breathing zone focus", Inches(0.6), Inches(1.8)),
    ("2. Predictive Activation", "1–2 hr early trigger", Inches(5.0), Inches(1.8)),
    ("3. Incremental AI", "Zero batch retraining", Inches(9.2), Inches(1.8)),
    ("4. Green IoT Hardware", "1.8W ESP32 controller", Inches(0.6), Inches(3.5)),
    ("5. Green AI Paradigm", "Lightweight streaming", Inches(9.2), Inches(3.5)),
    ("6. Area-Specific Adaptation", "Re-tunes upon relocation", Inches(0.6), Inches(5.1)),
    ("7. Edge + Cloud Synergy", "Fast relay, rich analytics", Inches(5.0), Inches(5.1)),
    ("8. Ultra-Low-Cost ($67)", "Affordable for local SMEs", Inches(9.2), Inches(5.1))
]

for title, desc, x, y in pillars:
    card = add_card(s19, x, y, Inches(3.5), Inches(1.1), bg_color=SLATE_BG, border_color=BORDER_COL)
    tb = s19.shapes.add_textbox(x + Inches(0.1), y + Inches(0.15), Inches(3.3), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.bold = True
    p0.font.size = Pt(11)
    p0.font.color.rgb = NAVY
    p1 = tf.add_paragraph()
    p1.text = desc
    p1.font.size = Pt(9.5)
    p1.font.color.rgb = MUTED_TEXT

tb_s19_b = s19.shapes.add_textbox(Inches(0.6), Inches(6.5), Inches(12.133), Inches(0.5))
p_s19b = tb_s19_b.text_frame.paragraphs[0]
p_s19b.text = "The Closed-Loop Cycle: Sense ➔ Filter ➔ Predict ➔ Decide ➔ Purify ➔ Learn ➔ Adapt"
p_s19b.font.bold = True
p_s19b.font.size = Pt(11.5)
p_s19b.font.color.rgb = TEAL
p_s19b.alignment = PP_ALIGN.CENTER

# ==========================================
# SLIDE 20: LIMITATIONS, FUTURE WORK & TAKEAWAY
# ==========================================
s20 = prs.slides.add_slide(blank_layout)
add_header(s20, "19. Conclusion & Discussion", "Limitations, Future Direction & Final Takeaway", "Frank assessment of prototype scope, future deployment scaling, and closing takeaway", "Conclusion & Q&A")

# 3 Columns
cols_data = [
    ("Honest Academic Limitations", ROSE, [
        ("Single Bench-Scale Unit", "Evaluated as an isolated unit; multi-node factory mesh not yet physically deployed."),
        ("MOS Sensor Specificity", "MQ-series exhibit thermal drift & cross-sensitivity compared to optical gas analyzers."),
        ("Simulation Stream Benchmark", "Primary prequential AI benchmark used software-generated stream rather than multi-month factory deployment."),
        ("Indicative Prototype Cost", "Single-unit retail pricing in Dhaka; batch economies of scale not yet leveraged.")
    ]),
    ("Future Research Horizons", TEAL, [
        ("Multi-Node Factory Deployment", "Mesh network scaling across welding, boiler, and chemical bays (Figure 3.10)."),
        ("Federated Learning", "Nodes exchange privacy-preserving gradient updates without leaking raw factory telemetry."),
        ("Native Edge-AI Inference", "Quantizing champion linear/tree models for zero-cloud ESP32 native prediction."),
        ("Solar-Powered Field Variant", "20W PV panel + charge controller for off-grid operation in rural industrial SMEs.")
    ]),
    ("Core Capstone Takeaway", NAVY, [
        ("Final Contribution", "Moving industrial air quality management from passive observation to predictive, localized physical protection."),
        ("Defense Summary", "Demonstrated that protecting workers does not require expensive plant-wide HVAC—it requires intelligent, adaptive, pre-emptive action."),
        ("Committee Q&A", "Thank You!\nQuestions & Discussion.")
    ])
]

for i, (col_title, col_color, items) in enumerate(cols_data):
    x = Inches(0.6 + i * 4.1)
    card = add_card(s20, x, Inches(1.6), Inches(3.9), Inches(5.1), bg_color=SLATE_BG, border_color=col_color, border_width=1.5)
    tb = s20.shapes.add_textbox(x + Inches(0.2), Inches(1.8), Inches(3.5), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = col_title
    p0.font.bold = True
    p0.font.size = Pt(13)
    p0.font.color.rgb = col_color
    
    for heading, text in items:
        p = tf.add_paragraph()
        p.text = f"\n• {heading}: {text}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEXT

# Save PPTX
prs.save(output_pptx)
print(f"PowerPoint Presentation generated successfully: {output_pptx}")
print(f"Total slides generated: {len(prs.slides)}")
print(f"File size: {os.path.getsize(output_pptx):,} bytes")
