# AI/ML Job Salary Prediction

Predicting salaries for AI/ML job roles based on experience, education, skills, industry, company, location, remote-work type, and certifications.

## Overview

This project explores a dataset of 500 AI/ML job records and builds regression models to predict salary (USD) from job attributes. It covers the full workflow from exploratory data analysis to model comparison and prediction on new job profiles.

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
2. Preprocesses features (ordinal encoding for Education, one-hot encoding for Remote Work, label encoding for high-cardinality fields)
3. Trains and compares four models: Linear Regression, Decision Tree, Random Forest, and Gradient Boosting
4. Evaluates each model with MAE, RMSE, and R²
5. Visualizes predicted-vs-actual salary and residuals for the best-performing model
6. Reports feature importance
7. Includes a ready-to-edit cell for predicting salary on a custom job profile

## Usage

1. Open `AI_ML_Salary_Prediction.ipynb` in Google Colab.
2. Run the first cell and upload `ai_ml_job_analysis.csv` when prompted.
3. Run the remaining cells in order.

## Requirements

- Python 3
- pandas, numpy, matplotlib, seaborn, scikit-learn

(All pre-installed in Google Colab — no setup needed.)

## Results

Model performance (MAE, RMSE, R²) is printed and plotted in Section 6 of the notebook, with Random Forest and Gradient Boosting generally outperforming the linear baseline on this dataset.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

Vismay Vinod
