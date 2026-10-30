# CL 443: full project report, with Experiments 5 and 6 updated (30 Oct 2026)

- `report/CL443_report.pdf`: the main report. Sections 1 to 7.5 are unchanged from the 23 Oct version.
  Section 7.6 (Galerkin test) and Section 8 (SINDy) are the new versions, and the Summary is updated.
  Section 10 lists the settled choices.
- `report/CL443_report_professor.pdf`: the version to show the professor. It has no "Decided" lines, no
  "Why" paragraphs and no interpretation of the Experiment 5–6 results: just the methods, definitions, tables and figures.
- `report/CL443_report.tex`: LaTeX source. `report/tables/*.tex` and `report/figs/*.pdf` are generated
  by the Python scripts. `report/main_figs/` holds the figures of Experiments 1 to 5, taken from the 23 Oct PDF.

## Reproduce

```bash
cd python
python3 lorenz.py        # results_lorenz.json  (~2 min)
python3 pde_sindy.py     # results_pde.json     (~2.5 min)
python3 figures.py && python3 tables.py
cd ../report && pdflatex CL443_report.tex && pdflatex CL443_report.tex
```

MATLAB / Octave (from `matlab/`): `test_quick`, `run_lorenz`, `run_pde_all`.
