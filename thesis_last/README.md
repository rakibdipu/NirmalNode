# NirmalNode Thesis -- LaTeX Project

## Contents
- `main.tex` -- main document driver (includes all front matter + chapters)
- `references.bib` -- bibliography (43 real sources extracted from your uploaded papers)
- `main.pdf` -- pre-compiled output (62 pages)
- `front/` -- title page, declaration, approval, acknowledgement, abstract,
  abbreviations, appendix
- `chapters/` -- Chapter 1 (Introduction), Chapter 2 (Literature Review),
  Chapter 3 (Methodology), Chapter 4 (Experimental Design), Chapter 5 (Conclusion)
- `figures/` -- empty folder for your own photos/scans (see below)

## How to compile
Requires a standard TeX Live installation (pdflatex + bibtex).

```
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

(Two pdflatex passes after bibtex are needed to resolve all cross-references
and the bibliography correctly.)

## What YOU still need to fill in
Every place that needs your personal input is marked in red in the PDF as
`[TODO: ...]` (LaTeX command `\TODO{}`). These fall into four groups:

1. **Personal/institutional details** -- your name, ID, university, supervisor,
   HOD, dates -- in `front/titlepage.tex`, `front/declaration.tex`,
   `front/approval.tex`, `front/acknowledgement.tex`.
2. **Photos** -- every `\FIGPLACE{...}` in the chapter files is a bordered
   placeholder box with a caption already written. To insert your own photo,
   replace the `\FIGPLACE{label}{caption}{width}` call with a normal
   `\includegraphics` figure, e.g.:
   ```latex
   \begin{figure}[htbp]
     \centering
     \includegraphics[width=0.75\textwidth]{figures/my_photo.jpg}
     \caption{Your caption here}
     \label{fig:whatever}
   \end{figure}
   ```
   Put your image files in the `figures/` folder.
3. **Experimental results** -- all tables in Chapter 4 (`chapter4_experimental_design.tex`)
   have `\TODO{}` cells for MAE/RMSE/R²/F1, purification efficiency, power
   consumption, and cost. Fill these in once you run the actual experiments.
4. **Datasheet/firmware/sample-data specifics** in `front/appendix.tex`.

## Notes on citations
All 43 references in `references.bib` were extracted directly from the papers
you supplied in `capstone_zip.zip` (title/authors/journal/year/DOI taken from
each paper's own first page) -- nothing was invented. If you add new sources
later, add a new `@article{...}` (or `@inproceedings`, `@techreport`, etc.)
entry to `references.bib` and cite it with `\cite{yourkey}` in the text.
