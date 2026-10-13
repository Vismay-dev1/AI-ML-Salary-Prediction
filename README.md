# AI/ML Job Salary Prediction

Predicting salaries for AI/ML job roles based on experience, education, skills, industry, company, location, remote-work type, and certifications.

## Overview

This project explores 500 AI/ML job records and builds regression models to predict salary (USD) from job attributes. It covers the workflow from exploratory data analysis to model comparison and prediction on a new job profile.

## Dataset

`ai_ml_job_analysis.csv` — 500 rows, 11 columns:

| Column | Description |
|---|---|
| ID | Record identifier |
| Job Title | e.g. Machine Learning Engineer, AI Consultant, NLP Engineer |
| Experience (Years) | Years of professional experience |
| Education | Bachelors / Masters / PhD |
| Skill Count | Number of technical skills listed |
| Industry | e.g. Technology, Finance, Healthcare |
| Company | Employer name |
| Location | City, Country |
| Remote Work | Yes / No / Hybrid |
| Certification | Professional certification held |
| Salary (USD) | Target variable |

## Notebook

`AI_ML_Salary_Prediction.ipynb` — a Google Colab notebook that:

1. Loads and explores the dataset (distributions, correlations, salary breakdowns by category)
2. Preprocesses features (ordinal encoding for Education, one-hot encoding for Remote Work, and label encoding for high-cardinality fields)
3. Trains and compares Linear Regression, Decision Tree, Random Forest, and Gradient Boosting
4. Evaluates each model with MAE, RMSE, and R²
5. Visualizes predicted-vs-actual salary and residuals for the best-performing model
6. Reports feature importance
7. Includes a ready-to-edit cell for predicting salary on a custom job profile

## Project record and outputs

A reproducible generator creates a multi-page record covering the data, EDA, preprocessing, all four model results, diagnostics, feature importance, and the custom-profile example:

- **[Open the 10-page project record](outputs/AI_ML_Salary_Prediction_Record.pdf)**
- **[Browse the output files and individual figures](outputs/README.md)**
- Model metrics: `outputs/results/model_metrics.csv`
- Run summary: `outputs/results/run_summary.json`

To regenerate the PDF and the 16 standalone, numbered figure PNGs:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/generate_project_record.py
```

The generator reproduces the preprocessing and model settings in the notebook. In this run, Gradient Boosting had the highest held-out R² (0.9353; MAE $9,090.10; RMSE $12,646.38).

## Running the notebook

1. Open `AI_ML_Salary_Prediction.ipynb` in Google Colab.
2. Run the first cell and upload `ai_ml_job_analysis.csv` when prompted.
3. Run the remaining cells in order.

## Requirements

- Python 3
- pandas, numpy, matplotlib, seaborn, scikit-learn

(All pre-installed in Google Colab. For local use, install from `requirements.txt`.)

## Data note

The dataset has 166 blank `Certification` cells. The current notebook's preprocessing converts these blanks to a string label before encoding; the report calls this out as a limitation. The example profile also uses the notebook's fallback for an unseen `Location`. Treat the model output as a project demonstration rather than a production salary guarantee.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

Vismay Vinod
