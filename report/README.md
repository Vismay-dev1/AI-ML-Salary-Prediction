# Internship Project Demonstration Report

Final deliverables (same content, same figures):

* `AI_ML_Job_Salary_Prediction_Internship_Demonstration.docx` – editable Word version
* `AI_ML_Job_Salary_Prediction_Internship_Demonstration.pdf` – PDF version

When the DOCX is opened in Word, choose **Yes** if asked to update fields so that the Table of Contents page
numbers are refreshed for Word's own pagination (the pre-filled numbers come from the PDF layout).
Placeholders such as `[College Name]`, `[Guide Name]` etc. must be filled in by the student.

## How the report was produced (reproducible)

All results come from running the notebook's code cells **unmodified** on `ai_ml_job_analysis.csv`.

```bash
pip install pandas "numpy" scikit-learn matplotlib seaborn python-docx reportlab pillow
python run_notebook.py          # executes the notebook cells, saves outputs.json + graphs (assets/)
python make_output_images.py    # renders the captured outputs as clean output images
python make_diagrams.py         # workflow diagrams
python build_report.py          # builds the DOCX and the PDF
```

Environment used: Python 3.11.2, pandas 2.3.3, NumPy 2.4.6, scikit-learn 1.9.1, Matplotlib 3.11.2, Seaborn 0.13.2.
