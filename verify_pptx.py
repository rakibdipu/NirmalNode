import pptx

pptx_path = r"c:\Users\ASUS\Downloads\capstone 3.2\NirmalNode_Capstone_Defense_NEW.pptx"
prs = pptx.Presentation(pptx_path)

print(f"Total Slides: {len(prs.slides)}")
print(f"Slide Dimensions: {prs.slide_width / 914400:.2f} x {prs.slide_height / 914400:.2f} inches (16:9 Widescreen)")

all_text = []
for i, slide in enumerate(prs.slides):
    shapes_count = len(slide.shapes)
    slide_text = []
    has_table = False
    has_image = False
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                if p.text.strip():
                    slide_text.append(p.text.strip())
        if shape.has_table:
            has_table = True
            for r in shape.table.rows:
                row_str = " | ".join(c.text.strip() for c in r.cells)
                slide_text.append(row_str)
        if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
            has_image = True
            
    full_s_text = " ".join(slide_text)
    all_text.append(full_s_text)
    header = slide_text[1] if len(slide_text) > 1 else (slide_text[0] if slide_text else "No text")
    print(f"Slide {i+1:2d}: {shapes_count:2d} shapes | Table: {str(has_table):5s} | Image: {str(has_image):5s} | Title: {header[:45]}")

corpus = " ".join(all_text)
checks = {
    "Champion M8 lowest MAE (10.62)": "10.62" in corpus,
    "RMSE (17.43)": "17.43" in corpus,
    "R2 (0.7334)": "0.7334" in corpus,
    "Hazard F1 (0.940)": "0.940" in corpus,
    "Missed Hazard Rate (0.8%)": "0.8%" in corpus,
    "PM1.0 efficiency (95.7%)": "95.7%" in corpus,
    "PM10 efficiency (98.6%)": "98.6%" in corpus,
    "Total BOM (7,400 BDT)": "7,400" in corpus,
    "Total BOM USD ($67.27)": "67.27" in corpus,
    "Worst-case power (8.6 W)": "8.6 W" in corpus,
    "Standby power (1.8 W)": "1.8 W" in corpus,
    "Mandatory 2026 paper Aurnab": "Aurnab" in corpus,
    "Mandatory 2026 paper Ghosh": "Ghosh" in corpus,
}

print("\n--- Numerical & Literature Verifications ---")
all_ok = True
for k, v in checks.items():
    print(f"[{'PASS' if v else 'FAIL'}] {k}")
    if not v:
        all_ok = False

print(f"\nAll verification passed: {all_ok}")
