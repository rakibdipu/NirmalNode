# -*- coding: utf-8 -*-
"""
Builds the complete 20-slide NirmalNode Capstone Defense presentation
in PowerPoint (.pptx) with the Z.ai / GLM-inspired premium dark minimalist aesthetic.

Design Philosophy:
- Dark near-black / charcoal canvas (#08090C)
- Off-white typography (#F8FAFC, #FFFFFF) with muted slate secondary text (#94A3B8)
- Luminous Electric Cyan (#00F0FF) restrained accent
- Large bold typography, short confident headings
- Generous whitespace, no box-box cards or rounded rectangular containers around text
- Direct canvas typography, thin hairline dividers (#1E222D)
- True editorial AI research/product presentation feeling
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

# Z.ai / GLM Dark Palette
BG_COLOR = RGBColor(8, 9, 12)       # #08090C Deepest Charcoal / Near-Black
BG_CARD = RGBColor(16, 18, 24)      # #101218 Subtle surface when strictly needed
WHITE = RGBColor(255, 255, 255)     # #FFFFFF Pure White Headline
OFF_WHITE = RGBColor(241, 245, 249) # #F1F5F9 Off-White
CYAN = RGBColor(0, 240, 255)        # #00F0FF Luminous Electric Cyan Accent
CYAN_MUTED = RGBColor(34, 211, 238) # #22D3EE
SLATE_MUTED = RGBColor(148, 163, 184)# #94A3B8 Secondary Text
SLATE_DARK = RGBColor(71, 85, 105)  # #475569 Tertiary / Micro Labels
LINE_COLOR = RGBColor(30, 34, 45)   # #1E222D Precision Hairline Dividers
LINE_BRIGHT = RGBColor(45, 52, 68)  # #2D3444
EMERALD = RGBColor(0, 220, 130)     # #00DC82 Clean / Success
TEAL = RGBColor(20, 184, 166)        # #14B8A6
AMBER = RGBColor(245, 158, 11)      # #F59E0B Warning / Transient
ROSE = RGBColor(244, 63, 94)        # #F43F5E Hazard / Critical

def set_slide_background(slide):
    # Create a full-bleed dark rectangle
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()
    return bg

def add_header(slide, mono_tag, headline, subheadline=None):
    set_slide_background(slide)
    
    # Top Hairline Accent
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.015))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = LINE_COLOR
    top_line.line.fill.background()

    # Header text block sitting directly on canvas
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.733), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_tag = tf.paragraphs[0]
    p_tag.text = mono_tag.upper()
    p_tag.font.name = 'Arial'
    p_tag.font.size = Pt(8.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = CYAN

    p_head = tf.add_paragraph()
    p_head.text = headline
    p_head.font.name = 'Arial'
    p_head.font.size = Pt(21)
    p_head.font.bold = True
    p_head.font.color.rgb = WHITE

    if subheadline:
        p_sub = tf.add_paragraph()
        p_sub.text = subheadline
        p_sub.font.name = 'Arial'
        p_sub.font.size = Pt(10.5)
        p_sub.font.color.rgb = SLATE_MUTED

def add_hairline(slide, left, top, width, height=0.015, color=LINE_COLOR):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(height))
    line.fill.solid()
    line.fill.fore_color.rgb = color
    line.line.fill.background()
    return line

# =========================================================================
# SLIDE 1: TITLE SLIDE (Cover / Minimalist AI Product Editorial)
# =========================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Subtle grid / corner cross mark
add_hairline(s1, Inches(0.8), Inches(0.8), Inches(11.733), 0.015, LINE_COLOR)

tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(7.5), Inches(5.6))
tf1 = tb1.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

# Tag
p_tag = tf1.paragraphs[0]
p_tag.text = "CAPSTONE DEFENSE 2026 // DEPT. OF IOT & ROBOTICS ENGINEERING"
p_tag.font.name = 'Arial'
p_tag.font.size = Pt(8.5)
p_tag.font.bold = True
p_tag.font.color.rgb = CYAN

# University
p_u = tf1.add_paragraph()
p_u.text = "University of Frontier Technology, Bangladesh"
p_u.font.name = 'Arial'
p_u.font.size = Pt(11)
p_u.font.color.rgb = SLATE_MUTED

# Main Title
p_t = tf1.add_paragraph()
p_t.text = "\nNIRMALNODE"
p_t.font.name = 'Arial'
p_t.font.size = Pt(46)
p_t.font.bold = True
p_t.font.color.rgb = WHITE

# Subtitle
p_s = tf1.add_paragraph()
p_s.text = "Green IoT and Adaptive AI-Assisted Local Air Purification System for Industrial Hotspots"
p_s.font.name = 'Arial'
p_s.font.size = Pt(14)
p_s.font.bold = True
p_s.font.color.rgb = CYAN_MUTED

# Technical metadata
p_m = tf1.add_paragraph()
p_m.text = "\nPresenters:  Aar Raisatunnesa Hridika  •  Md Rakib Hassan Dipu\nSupervisor:  Md. Ashiqussalehin, Lecturer, Dept. of IoT & Robotics Engineering\nDate:        September 2026"
p_m.font.name = 'Arial'
p_m.font.size = Pt(10)
p_m.font.color.rgb = SLATE_MUTED

# Core specs pill line
p_spec = tf1.add_paragraph()
p_spec.text = "\n[ SPEC // 1.8W Standby • 95.7% PM2.5 Capture • Zero Retraining AI • ৳ 7,400 / $67.27 BOM ]"
p_spec.font.name = 'Arial'
p_spec.font.size = Pt(9)
p_spec.font.bold = True
p_spec.font.color.rgb = EMERALD

# Right side: Atmospheric Image with sleek hairline frame
if os.path.exists(get_path("real_world_hotspots.jpg")):
    img_card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(8.4), Inches(1.2), Inches(4.133), Inches(5.3))
    img_card.fill.solid()
    img_card.fill.fore_color.rgb = BG_CARD
    img_card.line.color.rgb = LINE_COLOR
    img_card.line.width = Pt(1)
    
    s1.shapes.add_picture(get_path("real_world_hotspots.jpg"), Inches(8.45), Inches(1.25), width=Inches(4.033), height=Inches(4.7))
    
    tb_c = s1.shapes.add_textbox(Inches(8.45), Inches(6.05), Inches(4.033), Inches(0.4))
    p_ic = tb_c.text_frame.paragraphs[0]
    p_ic.text = "FIG 1.1 // INDUSTRIAL EXPOSURE HOTSPOTS (BANGLADESH)"
    p_ic.font.size = Pt(7.5)
    p_ic.font.bold = True
    p_ic.font.color.rgb = SLATE_MUTED

# =========================================================================
# SLIDE 2: THE PROBLEM (Editorial Split)
# =========================================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "01 // PROBLEM MOTIVATION", "Why Industrial Air Pollution Needs a Local Solution", "The spatial mismatch between macro-scale ambient monitoring and concentrated worker exposure")

# Left: Hotspot image with thin border
if os.path.exists(get_path("real_world_hotspots.jpg")):
    s2.shapes.add_picture(get_path("real_world_hotspots.jpg"), Inches(0.8), Inches(1.8), width=Inches(5.2), height=Inches(4.6))
    tb_c2 = s2.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(5.2), Inches(0.35))
    tb_c2.text_frame.paragraphs[0].text = "FIG 1.1: WELDING BAY METAL FUMES & BOILER COMBUSTION PLUMES"
    tb_c2.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c2.text_frame.paragraphs[0].font.bold = True
    tb_c2.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

# Vertical hairline divider
add_hairline(s2, Inches(6.3), Inches(1.8), Inches(0.015), 4.9, LINE_COLOR)

# Right: High-impact typography directly on canvas (NO BOXES)
tb_p2 = s2.shapes.add_textbox(Inches(6.6), Inches(1.8), Inches(5.9), Inches(5.0))
tf_p2 = tb_p2.text_frame
tf_p2.word_wrap = True
tf_p2.margin_left = tf_p2.margin_top = tf_p2.margin_right = tf_p2.margin_bottom = 0

p_stat = tf_p2.paragraphs[0]
p_stat.text = "5 µg/m³"
p_stat.font.name = 'Arial'
p_stat.font.size = Pt(36)
p_stat.font.bold = True
p_stat.font.color.rgb = CYAN

p_stat_lbl = tf_p2.add_paragraph()
p_stat_lbl.text = "WHO 2021 ANNUAL PM2.5 GUIDELINE"
p_stat_lbl.font.size = Pt(8.5)
p_stat_lbl.font.bold = True
p_stat_lbl.font.color.rgb = SLATE_MUTED

p_body = tf_p2.add_paragraph()
p_body.text = "\n• Non-Anthropogenic Baseline: Natural background levels in Bangladesh already approach this limit, leaving zero tolerance for industrial emissions (Pai et al., 2022).\n\n• Micro-Hotspot Concentration: Pollution is not uniform across cities—it concentrates acutely in welding bays, boiler rooms, generator bays, and chemical stores (Ali et al., 2025).\n\n• Severe Worker Exposure: Unprotected workers directly inhale concentrated toxic fumes, leading to acute lung impairment, cardiovascular strain, and elevated mental health risks (Nasri et al., 2023; Alhadhrami et al., 2024).\n\n• Economic Impasse: Plant-wide HVAC filtration is financially impossible for resource-constrained SMEs (<1% purifier adoption in Bangladesh, Chowdhury et al., 2025)."
p_body.font.size = Pt(10)
p_body.font.color.rgb = OFF_WHITE

p_takeaway = tf_p2.add_paragraph()
p_takeaway.text = "\nCORE PREMISE // Air purification must be localized to the worker breathing zone, pre-emptive, and low-cost."
p_takeaway.font.size = Pt(9.5)
p_takeaway.font.bold = True
p_takeaway.font.color.rgb = CYAN

# =========================================================================
# SLIDE 3: WHERE TRADITIONAL APPROACHES FALL SHORT
# =========================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "02 // CRITIQUE OF EXISTING SYSTEMS", "The Broken Chain in Conventional Paradigms", "Why traditional sensing, conventional air cleaners, and static AI models fail at industrial hotspots")

cols = [
    ("PASSIVE", CYAN, "Traditional IoT Monitoring",
     "Measures ambient air and logs time-series to dashboards.\n\n"
     "• Real-time multi-gas sensing\n"
     "• Cloud dashboard visualization\n"
     "• Zero physical countermeasure\n\n"
     "FAIL STATE // Merely informs workers they are being poisoned without taking physical action."),
    ("REACTIVE", AMBER, "Conventional Purifiers",
     "Mechanical room-scale air cleaners operating on feedback.\n\n"
     "• Filters entire room air volume\n"
     "• Continuous high power draw\n"
     "• Operates after threshold is crossed\n\n"
     "FAIL STATE // Triggers too late; workers have already inhaled peak hazardous plume."),
    ("STATIC", ROSE, "Static Offline AI",
     "Batch machine learning models trained on fixed historical data.\n\n"
     "• Fixed offline parameters\n"
     "• No post-deployment updates\n"
     "• Vulnerable to concept drift\n\n"
     "FAIL STATE // Accuracy severely degrades when moved to new industrial sites with different emission profiles.")
]

for i, (tag, col, title, body) in enumerate(cols):
    left = Inches(0.8 + i * 4.0)
    # Text directly on canvas
    tb = s3.shapes.add_textbox(left, Inches(1.8), Inches(3.6), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = tag
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = col
    
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    
    p2 = tf.add_paragraph()
    p2.text = "\n" + body
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = OFF_WHITE
    
    if i < 2:
        add_hairline(s3, left + Inches(3.8), Inches(1.8), Inches(0.015), 4.3, LINE_COLOR)

# Bottom synthesis bar
add_hairline(s3, Inches(0.8), Inches(6.3), Inches(11.733), 0.015, LINE_COLOR)
tb_s3b = s3.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.4))
tb_s3b.text_frame.margin_left = tb_s3b.text_frame.margin_top = 0
p_s3b = tb_s3b.text_frame.paragraphs[0]
p_s3b.text = "SYNTHESIS // Spatial Mismatch (Room ≠ Hotspot) • Temporal Lag (Reactive ≠ Pre-emptive) • Intelligence Rigidity (Static ≠ Adaptive) • Cost Barrier"
p_s3b.font.size = Pt(9)
p_s3b.font.bold = True
p_s3b.font.color.rgb = SLATE_MUTED

# =========================================================================
# SLIDE 4: RECENT RESEARCH LANDSCAPE (2024–2026)
# =========================================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "03 // STATE OF THE ART", "Recent Research Landscape (2024–2026)", "Comparative evaluation matrix incorporating four recent 2026 studies confirming the research void")

rows, cols_cnt = 10, 7
table_shape = s4.shapes.add_table(rows, cols_cnt, Inches(0.8), Inches(1.7), Inches(11.733), Inches(4.6))
t = table_shape.table
t.columns[0].width = Inches(2.2) # Paper
t.columns[1].width = Inches(0.7) # Year
t.columns[2].width = Inches(2.4) # Approach
t.columns[3].width = Inches(1.0) # Prediction
t.columns[4].width = Inches(1.1) # Purification
t.columns[5].width = Inches(1.1) # Adaptivity
t.columns[6].width = Inches(3.233) # Gap

headers = ["Recent Study", "Year", "Main Approach", "Prediction?", "Purification?", "Adaptivity", "Identified Gap / Limitation"]
for c, h in enumerate(headers):
    cell = t.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = BG_CARD
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = 'Arial'
    p.font.bold = True
    p.font.size = Pt(8.5)
    p.font.color.rgb = CYAN
    p.alignment = PP_ALIGN.CENTER if c in [1,3,4,5] else PP_ALIGN.LEFT

papers_data = [
    ("Alam et al. (JARSET)", "2025", "Fixed IoT node in developing areas", "No", "No", "Static", "Observation only; no prediction or physical action"),
    ("Ramadhani et al. (IEEE IAICT)", "2025", "Low-cost sensor IoT air monitoring", "No", "No", "Static", "Threshold alerts only; lacks predictive automation"),
    ("Ali et al. (Air Qual. Atmos.)", "2025", "Long-term PM2.5 hotspots in Bangladesh", "No", "No", "N/A", "Satellite mapping; lacks real-time worker intervention"),
    ("Basak et al. (J. Agrofor. Env.)", "2025", "Spatial PM2.5/PM10 Tejgaon industrial", "No", "No", "N/A", "Quantifies exposure; proposes no engineering countermeasure"),
    ("Aurnab & Khanam (WAS Poll.)", "2026", "Landfill gas emission/dispersion in Dhaka", "No", "No", "Static", "Dispersion model only; lacks localized worker protection"),
    ("Ghosh et al. (Heliyon)", "2026", "Atmospheric CO2 remote sensing over BD", "No", "No", "N/A", "Macro observation; disconnected from localized mitigation"),
    ("Jaegle (EngRxiv)", "2026", "Innovative particulate filtration technologies", "No", "Yes (Mat.)", "Static", "Filter materials test; lacks sensor-AI closed-loop"),
    ("Kabir et al. (Pollution)", "2026", "PM2.5 mortality & economic loss in 6 BD cities", "Statistical", "No", "N/A", "Macro epidemiological loss ($23B); no engineering mitigation"),
    ("NirmalNode (This Work)", "2026", "Hotspot Green IoT + Adaptive AI Purifier", "Yes (1-2h)", "Yes (Pred.)", "Incremental", "First closed-loop, adaptive, pre-emptive hotspot system ($67)")
]

for r, rdata in enumerate(papers_data):
    is_2026 = r in [4, 5, 6, 7]
    is_nn = (r == 8)
    for c, val in enumerate(rdata):
        cell = t.cell(r + 1, c)
        cell.fill.solid()
        if is_nn:
            cell.fill.fore_color.rgb = RGBColor(12, 35, 45) # Subtle glowing cyan tint
        elif is_2026:
            cell.fill.fore_color.rgb = RGBColor(18, 22, 30) # Subtle highlight
        else:
            cell.fill.fore_color.rgb = BG_CARD if r % 2 == 0 else BG_COLOR

        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = 'Arial'
        p.font.size = Pt(8)
        if is_nn:
            p.font.bold = True
            p.font.color.rgb = CYAN if c in [0, 1, 3, 4, 5] else WHITE
        elif is_2026 and c == 1:
            p.font.bold = True
            p.font.color.rgb = CYAN
        elif c in [3, 4] and val == "No":
            p.font.color.rgb = ROSE
        elif c in [3, 4] and "Yes" in val:
            p.font.color.rgb = EMERALD
        else:
            p.font.color.rgb = OFF_WHITE
        p.alignment = PP_ALIGN.CENTER if c in [1,3,4,5] else PP_ALIGN.LEFT

tb_s4b = s4.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.4))
tb_s4b.text_frame.margin_left = tb_s4b.text_frame.margin_top = 0
tb_s4b.text_frame.paragraphs[0].text = "TAKEAWAY // All four 2026 papers focus on passive observation, macro modeling, or isolated materials. None close the loop to adaptive physical purification."
tb_s4b.text_frame.paragraphs[0].font.size = Pt(8.5)
tb_s4b.text_frame.paragraphs[0].font.bold = True
tb_s4b.text_frame.paragraphs[0].font.color.rgb = CYAN

# =========================================================================
# SLIDE 5: RESEARCH GAP
# =========================================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "04 // RESEARCH GAP", "The Broken Chain in Existing Systems", "Synthesizing the exact technical voids between sensing, intelligence, and physical mitigation")

# Minimalist technical flow banner
tb_flow = s5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.6))
tf_flow = tb_flow.text_frame
tf_flow.margin_left = tf_flow.margin_top = 0
p_fl = tf_flow.paragraphs[0]
p_fl.text = "SENSING LAYER   ➔   AI PREDICTION   ➔   [ THE CRITICAL VOID ]   ➔   PHYSICAL PURIFIER   ➔   ONLINE LEARNING"
p_fl.font.size = Pt(11)
p_fl.font.bold = True
p_fl.font.color.rgb = CYAN
add_hairline(s5, Inches(0.8), Inches(2.4), Inches(11.733), 0.015, LINE_COLOR)

gaps = [
    ("01 // DECOUPLED ARCHITECTURE", "Prior IoT and AI models terminate at visualization dashboards; they are never coupled to automated physical air purification."),
    ("02 // ROOM-SCALE MISALIGNMENT", "Air cleaners in the literature are evaluated exclusively as room/vehicle units, demanding excessive power while ignoring worker micro-zones."),
    ("03 // REACTIVE LATENCY DELAY", "Conventional purifiers activate only after hazard thresholds are crossed; workers inhale the dangerous plume during reaction latency."),
    ("04 // STATIC MODEL RIGIDITY", "Offline models cannot adapt to sensor aging or relocation across different industrial zones (e.g., Gazipur to Narayanganj)."),
    ("05 // EVIDENCE WITHOUT MITIGATION", "Occupational studies document acute worker health deterioration but propose no low-cost engineering countermeasure."),
    ("06 // PROHIBITIVE SME ADOPTION", "High commercial purifier costs lead to <1% adoption in Bangladesh. An ultra-low-cost ($67) integrated system is absent.")
]

for i, (num_title, desc) in enumerate(gaps):
    col = i % 3
    row = i // 3
    x = Inches(0.8 + col * 4.0)
    y = Inches(2.6 + row * 1.8)
    
    tb = s5.shapes.add_textbox(x, y, Inches(3.6), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p0 = tf.paragraphs[0]
    p0.text = num_title
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = ROSE
    
    p1 = tf.add_paragraph()
    p1.text = desc
    p1.font.size = Pt(9)
    p1.font.color.rgb = OFF_WHITE

add_hairline(s5, Inches(0.8), Inches(6.3), Inches(11.733), 0.015, LINE_COLOR)
tb_s5b = s5.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.4))
tb_s5b.text_frame.margin_left = tb_s5b.text_frame.margin_top = 0
tb_s5b.text_frame.paragraphs[0].text = "NIRMALNODE MANDATE // Close this gap with localized, predictively-actuated, incrementally-learning air purification for $67.27."
tb_s5b.text_frame.paragraphs[0].font.size = Pt(9.5)
tb_s5b.text_frame.paragraphs[0].font.bold = True
tb_s5b.text_frame.paragraphs[0].font.color.rgb = EMERALD

# =========================================================================
# SLIDE 6: WHAT MAKES NIRMALNODE DIFFERENT (CORE NOVELTY)
# =========================================================================
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "05 // CORE NOVELTY", "What Makes NirmalNode Different?", "Comparing the traditional open-loop paradigm against NirmalNode's closed-loop architecture")

# Left Column: Traditional open loop
tb_tr = s6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.4))
tf_tr = tb_tr.text_frame
tf_tr.word_wrap = True
tf_tr.margin_left = tf_tr.margin_top = 0

p0 = tf_tr.paragraphs[0]
p0.text = "TRADITIONAL PARADIGM"
p0.font.size = Pt(13)
p0.font.bold = True
p0.font.color.rgb = SLATE_MUTED

p1 = tf_tr.add_paragraph()
p1.text = "\nSENSE  ➔  DISPLAY / PREDICT  ➔  REACTIVE RESPONSE\n\n• Spatial: City/room scale (diluted focus)\n• Temporal: Reactive lag (cleans after peak)\n• Intelligence: Static offline AI (frozen weights)\n• Systems: Sensing decoupled from physical purifier\n• Economics: High capex ($500–$2000), <1% adoption"
p1.font.size = Pt(9.5)
p1.font.color.rgb = SLATE_MUTED

# Divider
add_hairline(s6, Inches(5.6), Inches(1.8), Inches(0.015), 4.4, LINE_COLOR)

# Right Column: NirmalNode Closed Loop
tb_nn = s6.shapes.add_textbox(Inches(6.0), Inches(1.8), Inches(6.5), Inches(4.4))
tf_nn = tb_nn.text_frame
tf_nn.word_wrap = True
tf_nn.margin_left = tf_nn.margin_top = 0

p_nn0 = tf_nn.paragraphs[0]
p_nn0.text = "NIRMALNODE CLOSED-LOOP ARCHITECTURE"
p_nn0.font.size = Pt(13)
p_nn0.font.bold = True
p_nn0.font.color.rgb = CYAN

p_nn_flow = tf_nn.add_paragraph()
p_nn_flow.text = "\nSENSE ➔ FILTER ➔ PREDICT ➔ DECIDE ➔ PURIFY ➔ LEARN ➔ ADAPT"
p_nn_flow.font.size = Pt(10)
p_nn_flow.font.bold = True
p_nn_flow.font.color.rgb = WHITE

p_nn_pills = tf_nn.add_paragraph()
p_nn_pills.text = "\nEight Explicit Technical Novelties:\n" \
                  "1. Hotspot Targeted: Protects worker breathing zone directly\n" \
                  "2. Predictive Actuation: Pre-emptive trigger 1–2 hours in advance\n" \
                  "3. Green IoT Architecture: Ultra-low-power ESP32 controller (1.8W)\n" \
                  "4. Green AI Paradigm: Streaming linear/tree models, zero GPU\n" \
                  "5. Incremental / Online Learning: River/partial_fit (no full retraining)\n" \
                  "6. Area-Specific Adaptation: Auto-recalibrates when relocated\n" \
                  "7. Edge + Cloud Synergy: Local millisecond relay, cloud analytics\n" \
                  "8. Ultra-Low-Cost Deployment: 7,400 BDT ($67.27 USD) total BOM"
p_nn_pills.font.size = Pt(9)
p_nn_pills.font.color.rgb = OFF_WHITE

add_hairline(s6, Inches(0.8), Inches(6.3), Inches(11.733), 0.015, LINE_COLOR)
tb_s6b = s6.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.4))
tb_s6b.text_frame.margin_left = tb_s6b.text_frame.margin_top = 0
tb_s6b.text_frame.paragraphs[0].text = "CORE DISTINCTION // NirmalNode transforms air quality management from passive monitoring to intelligent, localized physical protection."
tb_s6b.text_frame.paragraphs[0].font.size = Pt(9)
tb_s6b.text_frame.paragraphs[0].font.bold = True
tb_s6b.text_frame.paragraphs[0].font.color.rgb = CYAN

# =========================================================================
# SLIDE 7: RESEARCH OBJECTIVES
# =========================================================================
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "06 // RESEARCH ROADMAP", "Six Concrete Research Objectives", "Measurable engineering milestones governing system realization and experimental validation")

objs = [
    ("01", "Low-Cost Multi-Sensor Node", "Design and integrate an ESP32 hardware node continuously acquiring PM1.0, PM2.5, PM10, CO, NO₂, VOC, NH₃, H₂S, and ambient temp/humidity/pressure at worker micro-zones."),
    ("02", "Cloud Telemetry Pipeline", "Construct an edge-to-cloud data pipeline transmitting JSON telemetry over Wi-Fi (HTTP REST / MQTT) with time-, day-, and location-tagged circular buffer storage."),
    ("03", "1–2 Hour Ahead Forecasting", "Develop an Adaptive AI model pre-trained on historical Bangladesh air-quality records, forecasting hotspot-level PM2.5 concentrations 1–2 hours in advance."),
    ("04", "Incremental Adaptive Learning", "Implement stream-learning estimators (SGD Regressor, Passive-Aggressive, Hoeffding Trees) to update weights continuously without full retraining, adapting to relocations."),
    ("05", "3-Stage Purification Unit", "Engineer and prototype a localized filtration train (cyclone separator, HEPA-H13 filter, activated-carbon pad, 12V fan) triggered automatically ahead of hazard threshold crossings."),
    ("06", "Multi-Dimensional Evaluation", "Rigorously validate forecasting accuracy (MAE, RMSE, R², F1), prequential convergence, physical filtration efficiency (PM1.0, PM2.5, PM10), power profile, and BOM economics.")
]

for i, (num, title, desc) in enumerate(objs):
    col = i % 2
    row = i // 2
    x = Inches(0.8 + col * 5.9)
    y = Inches(1.8 + row * 1.5)
    
    tb_num = s7.shapes.add_textbox(x, y, Inches(0.8), Inches(1.2))
    tb_num.text_frame.margin_left = tb_num.text_frame.margin_top = 0
    p_num = tb_num.text_frame.paragraphs[0]
    p_num.text = num
    p_num.font.size = Pt(28)
    p_num.font.bold = True
    p_num.font.color.rgb = CYAN
    
    tb_txt = s7.shapes.add_textbox(x + Inches(0.9), y, Inches(4.8), Inches(1.3))
    tf_txt = tb_txt.text_frame
    tf_txt.word_wrap = True
    tf_txt.margin_left = tf_txt.margin_top = 0
    p_t = tf_txt.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE
    p_d = tf_txt.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(8.5)
    p_d.font.color.rgb = OFF_WHITE

add_hairline(s7, Inches(0.8), Inches(6.3), Inches(11.733), 0.015, LINE_COLOR)
tb_s7b = s7.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.4))
tb_s7b.text_frame.margin_left = tb_s7b.text_frame.margin_top = 0
tb_s7b.text_frame.paragraphs[0].text = "STRUCTURE // Objectives O1–O5 govern Methodology (Chapter 3); Objective O6 governs Experimental Validation (Chapter 4)."
tb_s7b.text_frame.paragraphs[0].font.size = Pt(8.5)
tb_s7b.text_frame.paragraphs[0].font.bold = True
tb_s7b.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

# =========================================================================
# SLIDE 8: END-TO-END SYSTEM ARCHITECTURE
# =========================================================================
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "07 // SYSTEM METHODOLOGY", "NirmalNode: End-to-End Five-Layer Architecture", "Authentic engineering block diagram spanning physical sensing to closed-loop physical purification")

# Left: Our authentic dark academic architecture diagram
dark_arch_path = get_path("figures_academic/five_layer_architecture_dark.png")
if os.path.exists(dark_arch_path):
    s8.shapes.add_picture(dark_arch_path, Inches(0.8), Inches(1.8), width=Inches(7.6), height=Inches(4.6))
    tb_c8 = s8.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(7.6), Inches(0.35))
    tb_c8.text_frame.paragraphs[0].text = "FIG 3.1 // FIVE-LAYER SYSTEM ARCHITECTURE (AUTHENTIC ACADEMIC SPECIFICATION)"
    tb_c8.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c8.text_frame.paragraphs[0].font.bold = True
    tb_c8.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

# Right: Technical breakdown sitting directly on canvas
add_hairline(s8, Inches(8.6), Inches(1.8), Inches(0.015), 4.6, LINE_COLOR)
tb_s8 = s8.shapes.add_textbox(Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.6))
tf_s8 = tb_s8.text_frame
tf_s8.word_wrap = True
tf_s8.margin_left = tf_s8.margin_top = 0

p0 = tf_s8.paragraphs[0]
p0.text = "ARCHITECTURAL PARTITIONING"
p0.font.size = Pt(11)
p0.font.bold = True
p0.font.color.rgb = CYAN

layers_txt = "\n• Layer 1 (Physical Sensing):\n  12 continuous channels at worker breathing zone (PMS5003 laser, MiCS-4514, MQ135, MQ136, MP135, BME280).\n\n• Layer 2 (Edge Firmware):\n  ESP32 MCU running 2s non-blocking timer, clean-air R0 calibration, EMA noise filtering (α=0.25).\n\n• Layer 3 (Cloud Transport):\n  Wi-Fi HTTP REST (/api/ingest) & MQTT, JSON packetization, 500-sample circular buffer.\n\n• Layer 4 (Adaptive AI Engine):\n  Streaming prequential learner (River/scikit-learn), champion M8 blend, 1–2h lookahead forecast.\n\n• Layer 5 (Physical Purification):\n  Cyclone + HEPA-H13 + Activated Carbon unit triggered ahead of hazard threshold."
p1 = tf_s8.add_paragraph()
p1.text = layers_txt
p1.font.size = Pt(8.5)
p1.font.color.rgb = OFF_WHITE

# =========================================================================
# SLIDE 9: HARDWARE IMPLEMENTATION
# =========================================================================
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "08 // HARDWARE SUBSYSTEM", "Physical Integration and Interfacing", "Comprehensive multi-sensor hardware architecture centered on a single low-power ESP32 controller")

if os.path.exists(get_path("fig01_hardware_composite.png")):
    s9.shapes.add_picture(get_path("fig01_hardware_composite.png"), Inches(0.8), Inches(1.8), width=Inches(7.4), height=Inches(4.6))
    tb_c9 = s9.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(7.4), Inches(0.35))
    tb_c9.text_frame.paragraphs[0].text = "FIG 3.5 // HARDWARE INTERFACING & WIRING DIAGRAM (SOURCE: PROTOTYPE IMPLEMENTATION)"
    tb_c9.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c9.text_frame.paragraphs[0].font.bold = True
    tb_c9.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

add_hairline(s9, Inches(8.4), Inches(1.8), Inches(0.015), 4.6, LINE_COLOR)
tb_s9 = s9.shapes.add_textbox(Inches(8.6), Inches(1.8), Inches(3.9), Inches(4.6))
tf_s9 = tb_s9.text_frame
tf_s9.word_wrap = True
tf_s9.margin_left = tf_s9.margin_top = 0

p0 = tf_s9.paragraphs[0]
p0.text = "HARDWARE SPECIFICATIONS"
p0.font.size = Pt(11)
p0.font.bold = True
p0.font.color.rgb = CYAN

hw_text = "\n• Controller: ESP32 DevKit V1 (Tensilica 32-bit dual-core 240MHz, 520KB SRAM, built-in Wi-Fi & BLE)\n\n• Particulate: Plantower PMS5003 laser scattering (UART2 GPIO16/17, mass PM1.0/2.5/10 + 6 bin counts)\n\n• Dual Gas: MiCS-4514 (Analog ADC: CO RED GPIO34, NO2 OX GPIO35)\n\n• Broad Gas: MQ135 (VOC/NH3/Smoke GPIO32) & MP135 (Relative VOC GPIO36)\n\n• Toxic Gas: MQ136 (H2S / Sulphur GPIO33)\n\n• Environmental: BME280 (Temp, Humidity, Pressure I2C)\n\n• Actuator: Optocoupled 5V Relay (GPIO25) driving 12V 0.5A Brushless Exhaust Fan\n\n• Power Bus: 3S Li-Po (11.1V, 55.5 Wh) + BMS + Buck (5V 3A)"
p1 = tf_s9.add_paragraph()
p1.text = hw_text
p1.font.size = Pt(8)
p1.font.color.rgb = OFF_WHITE

# =========================================================================
# SLIDE 10: HARDWARE ARCHITECTURE & DATA FLOW
# =========================================================================
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "09 // SIGNAL PROCESSING", "From Sensors to Edge Signal Processing", "Deterministic acquisition loop, on-device EMA filtering, and low-latency wireless dispatch")

if os.path.exists(get_path("extracted_figs/hardware_block_diagram.png")):
    s10.shapes.add_picture(get_path("extracted_figs/hardware_block_diagram.png"), Inches(0.8), Inches(1.8), width=Inches(6.6), height=Inches(4.6))
    tb_c10 = s10.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(6.6), Inches(0.35))
    tb_c10.text_frame.paragraphs[0].text = "FIG 3.5B // HARDWARE BUS-LEVEL BLOCK DIAGRAM (PERIPHERAL TO MCU MAPPING)"
    tb_c10.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c10.text_frame.paragraphs[0].font.bold = True
    tb_c10.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

add_hairline(s10, Inches(7.6), Inches(1.8), Inches(0.015), 4.6, LINE_COLOR)
tb_s10 = s10.shapes.add_textbox(Inches(7.9), Inches(1.8), Inches(4.6), Inches(4.6))
tf_s10 = tb_s10.text_frame
tf_s10.word_wrap = True
tf_s10.margin_left = tf_s10.margin_top = 0

p0 = tf_s10.paragraphs[0]
p0.text = "EDGE SIGNAL CONDITIONING"
p0.font.size = Pt(11)
p0.font.bold = True
p0.font.color.rgb = CYAN

p_eq = tf_s10.add_paragraph()
p_eq.text = "\nx̂[k] = α · x_raw[k] + (1 - α) · x̂[k-1]"
p_eq.font.size = Pt(13)
p_eq.font.bold = True
p_eq.font.color.rgb = WHITE

p_flow = tf_s10.add_paragraph()
p_flow.text = "Smoothing factor α = 0.25 suppresses high-frequency sensor noise while retaining instant response to sudden industrial smoke plumes.\n\n" \
              "1. Synchronous Sampling (Δt = 2s):\n" \
              "ESP32 polls digital UART2 packets from PMS5003 and 12-bit ADC values synchronously.\n\n" \
              "2. JSON Record Serialization:\n" \
              "Assembles calibrated feature vector into structured payload with timestamp and node ID.\n\n" \
              "3. Wireless Dispatch & Control Return:\n" \
              "Dispatched via Wi-Fi to Flask backend (/api/ingest); returns relay state in HTTP response."
p_flow.font.size = Pt(8.5)
p_flow.font.color.rgb = OFF_WHITE

# =========================================================================
# SLIDE 11: SOFTWARE & DATA PIPELINE
# =========================================================================
s11 = prs.slides.add_slide(blank_layout)
add_header(s11, "10 // SOFTWARE ARCHITECTURE", "Software and Data Processing Pipeline", "Dual-partitioned architecture spanning low-level C++ firmware to real-time Python cloud microservices")

if os.path.exists(get_path("software_block_diagram.png")):
    s11.shapes.add_picture(get_path("software_block_diagram.png"), Inches(0.8), Inches(1.8), width=Inches(6.6), height=Inches(4.6))
    tb_c11 = s11.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(6.6), Inches(0.35))
    tb_c11.text_frame.paragraphs[0].text = "FIG 3.6 // SOFTWARE BLOCK DIAGRAM (FIRMWARE ➔ BACKEND ➔ DASHBOARD)"
    tb_c11.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c11.text_frame.paragraphs[0].font.bold = True
    tb_c11.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

add_hairline(s11, Inches(7.6), Inches(1.8), Inches(0.015), 4.6, LINE_COLOR)
tb_s11 = s11.shapes.add_textbox(Inches(7.9), Inches(1.8), Inches(4.6), Inches(4.6))
tf_s11 = tb_s11.text_frame
tf_s11.word_wrap = True
tf_s11.margin_left = tf_s11.margin_top = 0

p0 = tf_s11.paragraphs[0]
p0.text = "PIPELINE LATENCY & EXECUTION"
p0.font.size = Pt(11)
p0.font.bold = True
p0.font.color.rgb = CYAN

sw_text = "\n• ESP32 Firmware (AirGuard_WiFi.ino):\n" \
          "  - 48-hour burn-in baseline R0 calibration\n" \
          "  - 2-second non-blocking timer loop\n" \
          "  - In-situ EMA noise filtering\n" \
          "  - Direct GPIO25 relay driver\n\n" \
          "• Python Flask Backend (server.py):\n" \
          "  - High-throughput /api/ingest REST endpoint\n" \
          "  - Synchronous AdaptiveAIEngine.predict_and_learn()\n" \
          "  - 500-sample circular telemetry buffer\n" \
          "  - Decision round-trip latency: <15 ms\n\n" \
          "• Real-Time Web Dashboard (app.js):\n" \
          "  - 2-second polling of /api/latest\n" \
          "  - Real-time EPA AQI gauge & Chart.js plots\n" \
          "  - Auto-AI / Manual purifier control toggles"
p1 = tf_s11.add_paragraph()
p1.text = sw_text
p1.font.size = Pt(8.5)
p1.font.color.rgb = OFF_WHITE

# =========================================================================
# SLIDE 12: ADAPTIVE AI ENGINE
# =========================================================================
s12 = prs.slides.add_slide(blank_layout)
add_header(s12, "11 // MACHINE LEARNING", "Adaptive AI: Prediction That Keeps Learning", "Streaming incremental learning algorithms eliminating batch retraining overhead")

if os.path.exists(get_path("extracted_figs/ai_model_arena_pipeline.png")):
    s12.shapes.add_picture(get_path("extracted_figs/ai_model_arena_pipeline.png"), Inches(0.8), Inches(1.8), width=Inches(6.4), height=Inches(4.6))
    tb_c12 = s12.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(6.4), Inches(0.35))
    tb_c12.text_frame.paragraphs[0].text = "FIG 3.7 // INCREMENTAL MODEL ARENA PIPELINE (PREQUENTIAL EVALUATION)"
    tb_c12.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c12.text_frame.paragraphs[0].font.bold = True
    tb_c12.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

add_hairline(s12, Inches(7.4), Inches(1.8), Inches(0.015), 4.6, LINE_COLOR)
tb_s12 = s12.shapes.add_textbox(Inches(7.7), Inches(1.8), Inches(4.8), Inches(4.6))
tf_s12 = tb_s12.text_frame
tf_s12.word_wrap = True
tf_s12.margin_left = tf_s12.margin_top = 0

p0 = tf_s12.paragraphs[0]
p0.text = "ZERO BATCH RETRAINING"
p0.font.size = Pt(13)
p0.font.bold = True
p0.font.color.rgb = CYAN

ai_text = "\nModel parameters update sample-by-sample via the prequential (test-then-train) protocol using River & scikit-learn partial_fit.\n\n" \
          "• 9 Candidate Models Evaluated in Arena:\n" \
          "  - M1–M3: SGD Ridge, Lasso, ElasticNet\n" \
          "  - M4: SGD Huber (Robust to smoke outlier spikes)\n" \
          "  - M5: SGD Support Vector Regressor (SVR)\n" \
          "  - M6–M7: Passive-Aggressive Regressors (C=1.0, C=0.1)\n" \
          "  - M8 (Champion): SGD + PA Blend (MAE = 10.62)\n" \
          "  - M9: Baseline Exponential Moving Average\n\n" \
          "• Area-Specific Relocation Adaptation:\n" \
          "When moved between industrial sites (e.g., Gazipur to Narayanganj), incoming stream gradients automatically shift model weights without human intervention."
p1 = tf_s12.add_paragraph()
p1.text = ai_text
p1.font.size = Pt(8.5)
p1.font.color.rgb = OFF_WHITE

# =========================================================================
# SLIDE 13: PREDICTIVE DECISION ENGINE
# =========================================================================
s13 = prs.slides.add_slide(blank_layout)
add_header(s13, "12 // ACTUATION LOGIC", "From Forecasts to Pre-Emptive Airflow Clearance", "Threshold-based predictive activation closing the loop between AI forecasts and physical hardware")

if os.path.exists(get_path("extracted_figs/purifier_decision_flowchart.png")):
    s13.shapes.add_picture(get_path("extracted_figs/purifier_decision_flowchart.png"), Inches(0.8), Inches(1.8), width=Inches(5.4), height=Inches(4.6))
    tb_c13 = s13.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(5.4), Inches(0.35))
    tb_c13.text_frame.paragraphs[0].text = "FIG 3.9 // CLOSED-LOOP DECISION FLOWCHART (ALGORITHM 2)"
    tb_c13.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c13.text_frame.paragraphs[0].font.bold = True
    tb_c13.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

add_hairline(s13, Inches(6.4), Inches(1.8), Inches(0.015), 4.6, LINE_COLOR)
tb_s13 = s13.shapes.add_textbox(Inches(6.7), Inches(1.8), Inches(5.8), Inches(4.6))
tf_s13 = tb_s13.text_frame
tf_s13.word_wrap = True
tf_s13.margin_left = tf_s13.margin_top = 0

p0 = tf_s13.paragraphs[0]
p0.text = "DECISION ENGINE MATHEMATICS"
p0.font.size = Pt(11)
p0.font.bold = True
p0.font.color.rgb = CYAN

dec_text = "\nThreshold Activation Rule (Equation 3.12):\n" \
           "   d_t = FAN_ON   if ŷ_(t+h) ≥ 35.5 μg/m³\n" \
           "   d_t = FAN_OFF  if ŷ_(t+h) < 35.5 μg/m³\n\n" \
           "• Reactive Paradigm Failure:\n" \
           "  Pollution rises ➔ Sensor crosses limit ➔ Fan starts ➔ Worker has already inhaled the peak toxic plume during the delay.\n\n" \
           "• NirmalNode Predictive Advantage:\n" \
           "  AI forecasts spike 1–2h ahead ➔ Fan activates pre-emptively ➔ Chamber airflow establishes ➔ Breathing zone cleared BEFORE hazard peaks!\n\n" \
           "• Bench Experimental Validation:\n" \
           "  In sudden smoke injection tests, pre-emptive trigger fired 4–6 seconds before PM2.5 reached 35.5 μg/m³ at the inlet probe.\n\n" \
           "• Hysteresis Buffer:\n" \
           "  Built-in run-down timer eliminates relay chatter during marginal crossings."
p1 = tf_s13.add_paragraph()
p1.text = dec_text
p1.font.size = Pt(8.5)
p1.font.color.rgb = OFF_WHITE

# =========================================================================
# SLIDE 14: PURIFICATION SUBSYSTEM
# =========================================================================
s14 = prs.slides.add_slide(blank_layout)
add_header(s14, "13 // FILTRATION TRAIN", "Sequential 3-Stage Physical Decontamination", "Centrifugal pre-filter, HEPA-H13 micro-fibers, and activated carbon adsorption bed")

if os.path.exists(get_path("extracted_figs/purification_pipeline.png")):
    s14.shapes.add_picture(get_path("extracted_figs/purification_pipeline.png"), Inches(0.8), Inches(1.8), width=Inches(11.733), height=Inches(2.1))
    tb_c14 = s14.shapes.add_textbox(Inches(0.8), Inches(3.95), Inches(11.733), Inches(0.3))
    tb_c14.text_frame.paragraphs[0].text = "FIG 3.3 // THREE-STAGE PURIFICATION TRAIN (CYCLONE ➔ HEPA-H13 ➔ ACTIVATED CARBON)"
    tb_c14.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c14.text_frame.paragraphs[0].font.bold = True
    tb_c14.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

add_hairline(s14, Inches(0.8), Inches(4.3), Inches(11.733), 0.015, LINE_COLOR)

stg_cols = [
    ("STAGE 01 // PRE-FILTER", AMBER, "Cyclone Separator",
     "• Centrifugal force: F_c = m·v_t² / r\n"
     "• Extracts coarse dust (>10 μm: metal shavings, wood dust, grit)\n"
     "• Multiplies expensive HEPA filter lifespan by 3×–5× by preventing dust caking."),
    ("STAGE 02 // PARTICULATE", CYAN, "HEPA-H13 Filter",
     "• Dense micro-glass fiber mat (≥99.97% @ 0.3 μm)\n"
     "• Measured Efficiency (Table 4.8):\n"
     "  - PM1.0: 95.7% (42 → 1.8 μg/m³)\n"
     "  - PM2.5: 95.7% (67 → 2.9 μg/m³)\n"
     "  - PM10: 98.6% (Combined with cyclone)"),
    ("STAGE 03 // GAS & ODOUR", EMERALD, "Activated Carbon Bed",
     "• Microporous surface area (>1000 m²/g)\n"
     "• Langmuir physical adsorption for VOCs, CO, NO₂, NH₃, H₂S\n"
     "• Measured: ~60–70% VOC reduction; H₂S dropped below sensor threshold.\n"
     "• FACT: HEPA cannot filter gases; carbon bed handles gas hazards.")
]

for i, (tag, col, title, desc) in enumerate(stg_cols):
    left = Inches(0.8 + i * 4.0)
    tb = s14.shapes.add_textbox(left, Inches(4.45), Inches(3.6), Inches(2.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p0 = tf.paragraphs[0]
    p0.text = tag
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = col
    
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(8)
    p2.font.color.rgb = OFF_WHITE
    
    if i < 2:
        add_hairline(s14, left + Inches(3.8), Inches(4.45), Inches(0.015), 2.4, LINE_COLOR)

# =========================================================================
# SLIDE 15: PROTOTYPE & EXPERIMENTAL EVALUATION
# =========================================================================
s15 = prs.slides.add_slide(blank_layout)
add_header(s15, "14 // EXPERIMENTAL DESIGN", "Laboratory Testbed and Live Operational Dashboards", "Controlled prototype environment and explainable AI interfaces")

if os.path.exists(get_path("extracted_figs/dashboard_screenshot.jpg")):
    s15.shapes.add_picture(get_path("extracted_figs/dashboard_screenshot.jpg"), Inches(0.8), Inches(1.8), width=Inches(5.6), height=Inches(4.6))
    tb_c15a = s15.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(5.6), Inches(0.35))
    tb_c15a.text_frame.paragraphs[0].text = "FIG 4.1 // REAL-TIME WEB DASHBOARD (AQI GAUGE, 1H/2H FORECASTS, AUTO-AI)"
    tb_c15a.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c15a.text_frame.paragraphs[0].font.bold = True
    tb_c15a.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

if os.path.exists(get_path("extracted_figs/xai_dashboard_screenshot.jpg")):
    s15.shapes.add_picture(get_path("extracted_figs/xai_dashboard_screenshot.jpg"), Inches(6.8), Inches(1.8), width=Inches(5.733), height=Inches(2.5))
    tb_c15b = s15.shapes.add_textbox(Inches(6.8), Inches(4.35), Inches(5.733), Inches(0.3))
    tb_c15b.text_frame.paragraphs[0].text = "FIG 4.7 // EXPLAINABLE AI DASHBOARD (SHAP FEATURE CONTRIBUTIONS)"
    tb_c15b.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c15b.text_frame.paragraphs[0].font.bold = True
    tb_c15b.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

add_hairline(s15, Inches(6.8), Inches(4.7), Inches(5.733), 0.015, LINE_COLOR)
tb_s15t = s15.shapes.add_textbox(Inches(6.8), Inches(4.85), Inches(5.733), Inches(1.7))
tf_s15t = tb_s15t.text_frame
tf_s15t.word_wrap = True
tf_s15t.margin_left = tf_s15t.margin_top = 0

p0 = tf_s15t.paragraphs[0]
p0.text = "TEST PROTOCOLS & SCIENTIFIC HONESTY"
p0.font.size = Pt(10)
p0.font.bold = True
p0.font.color.rgb = CYAN

test_txt = "• Controlled Bench Lab: Physical prototype tested with point-source incense-smoke injection (~15 cm from inlet) to validate sensor response and closed-loop relay trigger.\n" \
           "• Prequential Stream Benchmark: 500-sample industrial stream (sinusoidal baseline mean 28.3 μg/m³, periodic combustion spikes up to 77 μg/m³, Δt=2s) testing continuous online learning.\n" \
           "• Scientific Honesty: Quantitative AI prequential accuracy is evaluated on the calibrated simulation stream; hardware bench test validates physical trigger and airflow."
p1 = tf_s15t.add_paragraph()
p1.text = test_txt
p1.font.size = Pt(8)
p1.font.color.rgb = OFF_WHITE

# =========================================================================
# SLIDE 16: AI RESULTS (Massive Typographic Stats)
# =========================================================================
s16 = prs.slides.add_slide(blank_layout)
add_header(s16, "15 // EXPERIMENTAL RESULTS", "Adaptive AI Performance Metrics", "Prequential evaluation metrics, model comparison arena, and hazard-detection verification")

if os.path.exists(get_path("extracted_figs/model_arena_comparison.png")):
    s16.shapes.add_picture(get_path("extracted_figs/model_arena_comparison.png"), Inches(0.8), Inches(1.8), width=Inches(6.2), height=Inches(3.3))
    tb_c16a = s16.shapes.add_textbox(Inches(0.8), Inches(5.15), Inches(6.2), Inches(0.3))
    tb_c16a.text_frame.paragraphs[0].text = "FIG 4.2 // PREQUENTIAL FORECASTING ERROR ACROSS 9 STREAMING MODELS"
    tb_c16a.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c16a.text_frame.paragraphs[0].font.bold = True
    tb_c16a.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

if os.path.exists(get_path("extracted_figs/confusion_matrix.png")):
    s16.shapes.add_picture(get_path("extracted_figs/confusion_matrix.png"), Inches(7.3), Inches(1.8), width=Inches(5.233), height=Inches(3.3))
    tb_c16b = s16.shapes.add_textbox(Inches(7.3), Inches(5.15), Inches(5.233), Inches(0.3))
    tb_c16b.text_frame.paragraphs[0].text = "FIG 4.3 // PURIFIER TRIGGER CONFUSION MATRIX (N=500, THRESHOLD = 35.5 µg/m³)"
    tb_c16b.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c16b.text_frame.paragraphs[0].font.bold = True
    tb_c16b.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

add_hairline(s16, Inches(0.8), Inches(5.55), Inches(11.733), 0.015, LINE_COLOR)

# 5 Massive Typographic KPI Stats (NO BOXES, sitting directly on canvas)
kpis_s16 = [
    ("10.62", "MAE (µg/m³)", "Champion M8 Blend (Baseline: 15.8)", CYAN),
    ("17.43", "RMSE (µg/m³)", "Baseline was 24.3", WHITE),
    ("0.7334", "R² Score", "Strong fit on streaming data", WHITE),
    ("0.940", "Hazard F1-Score", "Prec: 91.6% | Rec: 96.5%", EMERALD),
    ("0.8%", "Missed Hazard Rate", "Only 4 FN in 500 samples!", ROSE)
]

for i, (val, label, sub, col) in enumerate(kpis_s16):
    left = Inches(0.8 + i * 2.4)
    tb = s16.shapes.add_textbox(left, Inches(5.7), Inches(2.3), Inches(1.2))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = 0
    
    p0 = tf.paragraphs[0]
    p0.text = val
    p0.font.size = Pt(24)
    p0.font.bold = True
    p0.font.color.rgb = col
    
    p1 = tf.add_paragraph()
    p1.text = label
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.size = Pt(7.5)
    p2.font.color.rgb = SLATE_MUTED

# =========================================================================
# SLIDE 17: ADAPTATION & EXPLAINABILITY
# =========================================================================
s17 = prs.slides.add_slide(blank_layout)
add_header(s17, "16 // ADAPTIVITY EVIDENCE", "Empirical Convergence & SHAP Feature Attribution", "Validation of continuous online adaptation and transparent physical feature rankings")

if os.path.exists(get_path("extracted_figs/prequential_error_plot.jpg")):
    s17.shapes.add_picture(get_path("extracted_figs/prequential_error_plot.jpg"), Inches(0.8), Inches(1.8), width=Inches(5.6), height=Inches(4.6))
    tb_c17a = s17.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(5.6), Inches(0.35))
    tb_c17a.text_frame.paragraphs[0].text = "FIG 4.6 // PREQUENTIAL ERROR CONVERGENCE (COLD START ➔ STABILIZATION)"
    tb_c17a.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c17a.text_frame.paragraphs[0].font.bold = True
    tb_c17a.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

if os.path.exists(get_path("extracted_figs/xai_feature_importance.png")):
    s17.shapes.add_picture(get_path("extracted_figs/xai_feature_importance.png"), Inches(6.8), Inches(1.8), width=Inches(5.733), height=Inches(2.7))
    tb_c17b = s17.shapes.add_textbox(Inches(6.8), Inches(4.55), Inches(5.733), Inches(0.3))
    tb_c17b.text_frame.paragraphs[0].text = "FIG 4.8 // GLOBAL FEATURE IMPORTANCE (LFC / EXACT SHAP DECOMPOSITION)"
    tb_c17b.text_frame.paragraphs[0].font.size = Pt(8)
    tb_c17b.text_frame.paragraphs[0].font.bold = True
    tb_c17b.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

add_hairline(s17, Inches(6.8), Inches(4.9), Inches(5.733), 0.015, LINE_COLOR)
tb_s17t = s17.shapes.add_textbox(Inches(6.8), Inches(5.05), Inches(5.733), Inches(1.5))
tf_s17t = tb_s17t.text_frame
tf_s17t.word_wrap = True
tf_s17t.margin_left = tf_s17t.margin_top = 0

p0 = tf_s17t.paragraphs[0]
p0.text = "68% ERROR COLLAPSE VIA LIVE STREAMING"
p0.font.size = Pt(11)
p0.font.bold = True
p0.font.color.rgb = CYAN

conv_txt = "• Phase 1 (Cold Start, N=1–50): Initial MAE = 33.4 μg/m³ on raw distribution.\n" \
           "• Phase 2 (Adaptation, N=50–200): Steep error collapse as weights adjust on live stream.\n" \
           "• Phase 3 (Convergence, N=200–500): Stabilizes at 10.62 μg/m³ (68% error drop without offline batch retraining).\n" \
           "• Explainability: Dominant weights align with physical causality: PM2.5 EMA (0.224), PM2.5 current (0.186), PM10 (0.142)."
p1 = tf_s17t.add_paragraph()
p1.text = conv_txt
p1.font.size = Pt(8)
p1.font.color.rgb = OFF_WHITE

# =========================================================================
# SLIDE 18: FEASIBILITY (PURIFICATION, POWER & COST)
# =========================================================================
s18 = prs.slides.add_slide(blank_layout)
add_header(s18, "17 // FEASIBILITY ANALYSIS", "Physical Efficiency, Power Budget and BOM Economics", "Measured purification effectiveness, power profile, and full bill of materials")

# Left: Purification + Power directly on canvas
tb_puf_pow = s18.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4.5), Inches(4.6))
tf_pp = tb_puf_pow.text_frame
tf_pp.word_wrap = True
tf_pp.margin_left = tf_pp.margin_top = 0

p0 = tf_pp.paragraphs[0]
p0.text = "PURIFICATION EFFICIENCY (TABLE 4.8)"
p0.font.size = Pt(10)
p0.font.bold = True
p0.font.color.rgb = CYAN

p_pe = tf_pp.add_paragraph()
p_pe.text = "• PM1.0 (HEPA stage): 42 → 1.8 μg/m³  ➔  95.7%\n" \
            "• PM2.5 (HEPA stage): 67 → 2.9 μg/m³  ➔  95.7%\n" \
            "• PM10 (Cyclone+HEPA): 98 → 1.4 μg/m³  ➔  98.6%\n" \
            "• VOC / Odour (Carbon): Qualitative  ➔  ~60–70%"
p_pe.font.size = Pt(8.5)
p_pe.font.color.rgb = OFF_WHITE

p1 = tf_pp.add_paragraph()
p1.text = "\nPOWER CONSUMPTION PROFILE (TABLE 4.9)"
p1.font.size = Pt(10)
p1.font.bold = True
p1.font.color.rgb = CYAN

p_pw = tf_pp.add_paragraph()
p_pw.text = "• Standby (Sensing/Idle): ≈ 1.8 W\n" \
            "• Wi-Fi Transmitting (HTTP POST): ≈ 2.6 W\n" \
            "• Purifier Fan ON (Full Speed): ≈ 6.0 W\n" \
            "• Worst-Case Peak Total: ≈ 8.6 W\n\n" \
            "🔋 55.5 Wh Li-Po Battery Life: ~30h in standby; ~17h effective shift runtime at 25% duty cycle."
p_pw.font.size = Pt(8.5)
p_pw.font.color.rgb = OFF_WHITE

add_hairline(s18, Inches(5.6), Inches(1.8), Inches(0.015), 4.6, LINE_COLOR)

# Right: Minimalist BOM Table
tb_bom_lbl = s18.shapes.add_textbox(Inches(5.9), Inches(1.7), Inches(6.6), Inches(0.3))
tb_bom_lbl.text_frame.margin_left = tb_bom_lbl.text_frame.margin_top = 0
tb_bom_lbl.text_frame.paragraphs[0].text = "PROTOTYPE BILL OF MATERIALS (TABLE 4.10) — DHAKA RETAIL PRICING"
tb_bom_lbl.text_frame.paragraphs[0].font.size = Pt(9.5)
tb_bom_lbl.text_frame.paragraphs[0].font.bold = True
tb_bom_lbl.text_frame.paragraphs[0].font.color.rgb = CYAN

bom_items_data = [
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

table_bom = s18.shapes.add_table(15, 4, Inches(5.9), Inches(2.05), Inches(6.6), Inches(4.4)).table
table_bom.columns[0].width = Inches(3.7)
table_bom.columns[1].width = Inches(0.7)
table_bom.columns[2].width = Inches(1.1)
table_bom.columns[3].width = Inches(1.1)

b_headers = ["Component", "Qty", "Cost (BDT)", "Cost (USD)"]
for c, h in enumerate(b_headers):
    cell = table_bom.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = BG_CARD
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.bold = True
    p.font.size = Pt(8)
    p.font.color.rgb = CYAN
    p.alignment = PP_ALIGN.CENTER if c == 1 else (PP_ALIGN.RIGHT if c > 1 else PP_ALIGN.LEFT)

for r, rdata in enumerate(bom_items_data):
    is_tot = (r == 13)
    for c, val in enumerate(rdata):
        cell = table_bom.cell(r + 1, c)
        cell.fill.solid()
        if is_tot:
            cell.fill.fore_color.rgb = RGBColor(12, 35, 45)
        else:
            cell.fill.fore_color.rgb = BG_CARD if r % 2 == 0 else BG_COLOR
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.size = Pt(7.5)
        p.font.name = 'Arial'
        if is_tot:
            p.font.bold = True
            p.font.color.rgb = CYAN
        else:
            p.font.color.rgb = OFF_WHITE
        p.alignment = PP_ALIGN.CENTER if c == 1 else (PP_ALIGN.RIGHT if c > 1 else PP_ALIGN.LEFT)

# =========================================================================
# SLIDE 19: CORE CONTRIBUTIONS
# =========================================================================
s19 = prs.slides.add_slide(blank_layout)
add_header(s19, "18 // SUMMARY OF NOVELTY", "Core Contributions of NirmalNode", "Unified synthesis of the eight fundamental engineering innovations")

tb_hero = s19.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.6))
tf_hero = tb_hero.text_frame
tf_hero.margin_left = tf_hero.margin_top = 0
p_hero = tf_hero.paragraphs[0]
p_hero.text = "NIRMALNODE // CLOSED-LOOP LOCAL AIR PURIFICATION PLATFORM"
p_hero.font.size = Pt(14)
p_hero.font.bold = True
p_hero.font.color.rgb = CYAN
add_hairline(s19, Inches(0.8), Inches(2.4), Inches(11.733), 0.015, LINE_COLOR)

pillars_s19 = [
    ("01 // HOTSPOT PURIFICATION", "Targeting worker breathing zones directly, eliminating plant-wide HVAC energy waste."),
    ("02 // PREDICTIVE ACTIVATION", "1–2h lookahead triggers purifier pre-emptively, clearing zone before peak plume arrives."),
    ("03 // INCREMENTAL AI", "Sample-by-sample learning via River/partial_fit, totally eliminating batch retraining."),
    ("04 // GREEN IOT HARDWARE", "Single ESP32 controller architecture consuming just 1.8W in continuous sensing mode."),
    ("05 // GREEN AI PARADIGM", "Lightweight streaming linear and tree estimators; zero GPU or heavy server dependency."),
    ("06 // AREA-SPECIFIC ADAPTATION", "Gradient updates automatically adapt model parameters when moved between factory sites."),
    ("07 // EDGE-CLOUD CO-DESIGN", "Sub-15ms local relay actuation synchronized with persistent historical cloud analytics."),
    ("08 // ULTRA-LOW-COST DEPLOYMENT", "Full prototype bill of materials at 7,400 BDT ($67.27 USD), accessible to Bangladeshi SMEs.")
]

for i, (title, desc) in enumerate(pillars_s19):
    col = i % 2
    row = i // 2
    x = Inches(0.8 + col * 5.9)
    y = Inches(2.6 + row * 0.95)
    
    tb = s19.shapes.add_textbox(x, y, Inches(5.6), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_MUTED
    
    p1 = tf.add_paragraph()
    p1.text = desc
    p1.font.size = Pt(8.5)
    p1.font.color.rgb = OFF_WHITE

add_hairline(s19, Inches(0.8), Inches(6.3), Inches(11.733), 0.015, LINE_COLOR)
tb_s19b = s19.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.4))
tb_s19b.text_frame.margin_left = tb_s19b.text_frame.margin_top = 0
tb_s19b.text_frame.paragraphs[0].text = "THE CLOSED LOOP // SENSE  ➔  FILTER  ➔  PREDICT  ➔  DECIDE  ➔  PURIFY  ➔  LEARN  ➔  ADAPT"
tb_s19b.text_frame.paragraphs[0].font.size = Pt(10)
tb_s19b.text_frame.paragraphs[0].font.bold = True
tb_s19b.text_frame.paragraphs[0].font.color.rgb = WHITE

# =========================================================================
# SLIDE 20: LIMITATIONS, FUTURE DIRECTION & FINAL TAKEAWAY
# =========================================================================
s20 = prs.slides.add_slide(blank_layout)
add_header(s20, "19 // CONCLUSION & DISCUSSION", "Limitations, Future Horizons & Final Takeaway", "Frank assessment of prototype scope, future deployment scaling, and concluding defense summary")

s20_cols = [
    ("HONEST LIMITATIONS", ROSE,
     "• Single Bench-Scale Prototype:\n  Evaluated as an isolated unit; multi-node factory mesh not yet physically deployed.\n\n"
     "• MOS Sensor Specificity:\n  MQ-series exhibit thermal drift & cross-sensitivity compared to reference optical analyzers.\n\n"
     "• Simulation Stream Benchmark:\n  Primary prequential AI benchmark used calibrated software stream rather than multi-month factory logging.\n\n"
     "• Retail Prototype Pricing:\n  Single-unit retail pricing in Dhaka; batch economies of scale not yet leveraged."),
    ("FUTURE RESEARCH HORIZONS", TEAL,
     "• Multi-Node Factory Deployment:\n  Mesh network scaling across welding, boiler, and chemical bays (Figure 3.10).\n\n"
     "• Federated Learning:\n  Nodes exchange privacy-preserving gradient updates without leaking raw industrial telemetry.\n\n"
     "• Native Edge-AI Inference:\n  Quantizing champion linear/tree models for zero-cloud ESP32 native prediction.\n\n"
     "• Solar-Powered Field Variant:\n  20W PV panel + charge controller for off-grid operation in rural industrial SMEs."),
    ("CORE CAPSTONE TAKEAWAY", WHITE,
     "\"Moving industrial air quality management from passive observation to predictive, localized physical protection.\"\n\n"
     "NirmalNode demonstrates that protecting vulnerable industrial workers does not require expensive, plant-wide HVAC—it requires intelligent, adaptive, and pre-emptive hotspot action.\n\n"
     "Thank You.\nQuestions & Discussion.")
]

for i, (col_title, col_color, body) in enumerate(s20_cols):
    left = Inches(0.8 + i * 4.0)
    tb = s20.shapes.add_textbox(left, Inches(1.8), Inches(3.6), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    
    p0 = tf.paragraphs[0]
    p0.text = col_title
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = col_color
    
    p1 = tf.add_paragraph()
    p1.text = "\n" + body
    p1.font.size = Pt(8.5)
    p1.font.color.rgb = OFF_WHITE if i < 2 else CYAN
    
    if i < 2:
        add_hairline(s20, left + Inches(3.8), Inches(1.8), Inches(0.015), 4.3, LINE_COLOR)

add_hairline(s20, Inches(0.8), Inches(6.3), Inches(11.733), 0.015, LINE_COLOR)
tb_s20b = s20.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.4))
tb_s20b.text_frame.margin_left = tb_s20b.text_frame.margin_top = 0
tb_s20b.text_frame.paragraphs[0].text = "Aar Raisatunnesa Hridika & Md Rakib Hassan Dipu  •  Supervisor: Md. Ashiqussalehin  •  Dept. of IoT & Robotics Engineering, UFT"
tb_s20b.text_frame.paragraphs[0].font.size = Pt(8.5)
tb_s20b.text_frame.paragraphs[0].font.color.rgb = SLATE_MUTED

prs.save(output_pptx)
print(f"Z.ai / GLM-styled PowerPoint generated successfully: {output_pptx}")
print(f"Total slides: {len(prs.slides)}")
print(f"File size: {os.path.getsize(output_pptx):,} bytes")
