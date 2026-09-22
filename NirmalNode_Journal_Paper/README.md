# NirmalNode -- Journal Paper LaTeX Project

## Paper Title
**A Closed-Loop Green IoT Node Integrating Incremental Pollution Forecasting
and Predictive Localized Air Purification for Industrial Hotspots**

## Authors
- Aar Raisatunnesa Hridika (ID: 2201014)
- Md Rakib Hassan Dipu (ID: 2201030)

Department of Internet of Things and Robotics Engineering,
University of Frontier Technology, Bangladesh

## File Structure
```
main.tex                  -- Master LaTeX driver
references.bib            -- Bibliography (45 entries)
sections/
  sec1_introduction.tex   -- Section 1: Introduction
  sec2_relatedwork.tex    -- Section 2: Related Work & Gap
  sec3_methodology.tex    -- Section 3: Materials & Methods
  sec4_results.tex        -- Section 4: Results
  sec5_discussion.tex     -- Section 5: Discussion
  sec6_limitations.tex    -- Section 6: Limitations & Future Work
  sec7_conclusion.tex     -- Section 7: Conclusion
figures/                  -- All 23 figures (PNG/JPG/JPEG)
```

## How to Compile (Overleaf recommended)
1. Upload this entire folder to Overleaf as a ZIP
2. Set main document to `main.tex`
3. Compiler: pdfLaTeX
4. Compile 3 times (pdflatex -> bibtex -> pdflatex -> pdflatex)

### Local compile (requires TeX Live):
```
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Target Specifications
- Length: 15-18 pages (including figures and tables)
- Style: Q1-level journal manuscript (Elsevier / Springer / IEEE compatible)
- Figures: 15 publication-quality figures embedded in-text
- Tables: 8 data tables with full captions

## Key Results (All verified against thesis source)
| Metric | Value |
|--------|-------|
| Champion model | M8: SGD+PA Blend (0.6/0.4) |
| Prequential MAE | 10.616 ug/m3 |
| Prequential RMSE | 17.431 ug/m3 |
| R-squared | 0.7334 (controlled) / 0.8853 (real-world) |
| Hazard F1-score | 0.940 (controlled) / 0.992 (real-world) |
| Hazard Recall (real) | 100.0% (FN = 0/500) |
| Cold-start error reduction | 68.2% (33.4 -> 10.616 ug/m3) |
| PM2.5 removal | 95.7% |
| PM10 removal | 98.6% |
| Peak power | 8.6 W |
| Prototype BOM | USD 67.27 / BDT 7,400 |
