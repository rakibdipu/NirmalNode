# -*- coding: utf-8 -*-
"""
Generates a complete, professional, 20-slide Capstone Defense presentation in PowerPoint (.pptx) format.
Source of Truth: NirmalNode Thesis & Project Files.
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

def path(p):
    return os.path.join(base_dir, p)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6] # Blank slide layout

# Color Palette (Light Academic Research Theme)
NAVY = RGBColor(30, 58, 138)        # #1E3A8A Primary Brand
NAVY_LIGHT = RGBColor(37, 99, 235)  # #2563EB
TEAL = RGBColor(15, 118, 110)       # #0F766E Secondary Accent
EMERALD = RGBColor(21, 128, 61)     # #15803D Success / Clean Air
AMBER = RGBColor(180, 83, 9)        # #B45309 Warning / Transition
ROSE = RGBColor(190, 18, 60)        # #BE123C Hazard / Critical
DARK_TEXT = RGBColor(15, 23, 42)    # #0F172A Body Text
MUTED_TEXT = RGBColor(100, 116, 139)# #64748B Subtitles
SLATE_BG = RGBColor(248, 250, 252)  # #F8FAFC Card BG
WHITE = RGBColor(255, 255, 255)
BORDER_COL = RGBColor(226, 232, 240)# #E2E8F0 Subtle Border

def add_header(slide, tag_text, title_text, subtitle_text, category_badge):
    # Top progress line / accent line
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = NAVY
    top_bar.line.fill.background()

    # Header container
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.25), Inches(10.2), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Tag
    p0 = tf.paragraphs[0]
    p0.text = tag_text.upper()
    p0.font.name = 'Arial'
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = TEAL

    # Title
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = 'Arial'
    p1.font.size = Pt(21)
    p1.font.bold = True
    p1.font.color.rgb = NAVY

    # Subtitle
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.name = 'Arial'
    p2.font.size = Pt(11)
    p2.font.color.rgb = MUTED_TEXT

    # Category Badge on Right
    badge_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.8), Inches(0.35), Inches(1.9), Inches(0.45))
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
    bp.font.size = Pt(10)
    bp.font.bold = True
    bp.font.color.rgb = NAVY

    # Divider line under header
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.42), Inches(12.133), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_COL
    line.line.fill.background()

print("Script template ready.")
