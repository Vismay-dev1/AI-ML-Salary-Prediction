# AI/ML Salary Prediction — Generated Project Record

The main deliverable is the **10-page PDF record**:

- [AI/ML Salary Prediction Project Record (PDF)](AI_ML_Salary_Prediction_Record.pdf)

The PDF presents the work across the full pipeline—not just one model phase—with section headings, numbered figure titles, explanatory page subtitles, and a final summary. Each chart/table is also available as an individual, titled PNG under [`figures/`](figures/), so it can be inserted into a presentation or printed separately.

## Included evidence

1. Source-data preview and missing-value audit
2. Salary distribution, numeric correlation heatmap, and experience-versus-salary scatter plot
3. Salary box plots by education, remote-work type, job title, and industry
4. Preprocessing and train/test split summary
5. Model metrics table and R²/RMSE bar-chart comparison
6. Best-model predicted-versus-actual plot and residual distribution
7. Random Forest feature-importance chart
8. Example custom-profile prediction

Machine-readable results are in [`results/model_metrics.csv`](results/model_metrics.csv) and [`results/run_summary.json`](results/run_summary.json). The JSON summary also records the dataset audit, split, custom prediction, and package versions used for the run.

## Results recorded from the checked-in dataset

- 500 records and 11 source columns; 400 train rows and 100 held-out test rows
- Four regressors compared: Linear Regression, Decision Tree, Random Forest, and Gradient Boosting
- Gradient Boosting had the highest held-out R² in this run: **0.9353** (MAE **$9,090.10**, RMSE **$12,646.38**)
- The example custom-profile cell uses Random Forest and predicts **$114,232.08**
- The source contains 166 blank `Certification` values. This record reproduces the notebook's current behavior, which converts those blanks to a string category during label encoding; see the report caveats before treating this as production-ready.

## Regenerate

From the repository root, install the dependencies and rerun the generator:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/generate_project_record.py
```

The script reads `ai_ml_job_analysis.csv` and recreates the PDF, PNGs, CSV metrics, and JSON run summary. Generated dates in the summary and PDF reflect the time of each run.
