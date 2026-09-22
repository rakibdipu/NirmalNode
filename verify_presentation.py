import os
import re

html_path = r"c:\Users\ASUS\Downloads\capstone 3.2\NirmalNode_Capstone_NEW.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

print("File size:", len(html), "bytes")

# Check slides
slide_ids = re.findall(r'id="(slide-[0-9]+)"', html)
print(f"Slides found ({len(slide_ids)}): {slide_ids}")

# Check images referenced in HTML
imgs = re.findall(r'src="([^"]+)"', html)
print(f"Images referenced ({len(imgs)}):")
missing = []
for img in sorted(set(imgs)):
    p = os.path.join(r"c:\Users\ASUS\Downloads\capstone 3.2", img)
    exists = os.path.exists(p)
    status = "FOUND" if exists else "MISSING!"
    print(f"  {img}: {status}")
    if not exists:
        missing.append(img)

print("Missing images count:", len(missing))

checks = {
    "Champion M8 lowest MAE (10.62)": "10.62" in html,
    "RMSE (17.43)": "17.43" in html,
    "R2 (0.7334)": "0.7334" in html,
    "Hazard F1 (0.940)": "0.940" in html,
    "Missed Hazard Rate (0.8%)": "0.8%" in html,
    "PM1.0 efficiency (95.7%)": "95.7%" in html,
    "PM10 efficiency (98.6%)": "98.6%" in html,
    "Total BOM (7,400 BDT)": "7,400" in html,
    "Total BOM USD ($67.27)": "67.27" in html,
    "Worst-case power (8.6 W)": "8.6 W" in html,
    "Standby power (1.8 W)": "1.8 W" in html,
    "Mandatory 2026 paper Aurnab": "Aurnab" in html,
    "Mandatory 2026 paper Ghosh": "Ghosh" in html,
}

print("\nKey Thesis Data Verification:")
all_passed = True
for k, v in checks.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")
    if not v:
        all_passed = False

print("\nAll verification passed?", all_passed)
