#!/usr/bin/env python3
"""Re-run the salary-analysis notebook workflow and build a shareable project record.

Run from any working directory with:
    python scripts/generate_project_record.py

The script reads the repository's CSV, recreates the notebook's preprocessing and
models, writes titled PNG figures plus result files, and assembles a multi-page PDF.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np
import pandas as pd
import seaborn as sns
import sklearn
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "ai_ml_job_analysis.csv"
OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
RESULTS_DIR = OUTPUT_DIR / "results"
PDF_PATH = OUTPUT_DIR / "AI_ML_Salary_Prediction_Record.pdf"

NAVY = "#16324F"
BLUE = "#2878B5"
TEAL = "#159A9C"
GOLD = "#E4A23A"
PURPLE = "#8064A2"
INK = "#263445"
MUTED = "#64748B"
PALE = "#F2F6FA"
GRID = "#DCE5EE"
WHITE = "#FFFFFF"

sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams.update({
    "figure.facecolor": WHITE,
    "axes.facecolor": WHITE,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK,
    "axes.titlecolor": NAVY,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titleweight": "bold",
    "savefig.facecolor": WHITE,
})


def figure_title(ax: plt.Axes, number: int, title: str) -> None:
    ax.set_title(f"FIGURE {number:02d}  |  {title}", loc="left", pad=12,
                 fontsize=13, fontweight="bold", color=NAVY)


def save_figure(fig: plt.Figure, filename: str) -> Path:
    path = FIGURE_DIR / filename
    fig.savefig(path, dpi=210, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    return path


def display_salary(value: float) -> str:
    return f"${value:,.2f}"


def compact_usd(value: float, _position: int | None = None) -> str:
    sign = "−" if value < 0 else ""
    magnitude = abs(value)
    if magnitude >= 1000:
        return f"{sign}${magnitude / 1000:.0f}k"
    return f"{sign}${magnitude:,.0f}"


def build_analysis(df: pd.DataFrame) -> dict:
    """Fit the same encoders, split, regressors and custom example as the notebook."""
    if df.empty:
        raise ValueError("The source dataset has no rows.")
    if "Salary (USD)" not in df.columns:
        raise ValueError("Expected target column 'Salary (USD)' was not found.")

    # Match notebook preprocessing so the report records the work that is present
    # in the submitted notebook, rather than silently changing its methodology.
    data = df.drop(columns=["ID"]).copy()
    education_order = {"Bachelors": 0, "Masters": 1, "PhD": 2}
    data["Education"] = data["Education"].map(education_order)
    if data["Education"].isna().any():
        raise ValueError("Education contains a value outside the notebook's ordinal map.")

    data = pd.get_dummies(data, columns=["Remote Work"], prefix="Remote")
    label_cols = ["Job Title", "Industry", "Company", "Location", "Certification"]
    encoders: dict[str, LabelEncoder] = {}
    for col in label_cols:
        if col not in data.columns:
            raise ValueError(f"Expected feature column {col!r} was not found.")
        encoder = LabelEncoder()
        # This deliberately mirrors the notebook: blank certification cells
        # become a "nan" category. The report calls this out as a limitation.
        data[col] = encoder.fit_transform(data[col].astype(str))
        encoders[col] = encoder

    X = data.drop(columns=["Salary (USD)"])
    y = data["Salary (USD)"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=8, random_state=42),
        "Random Forest": RandomForestRegressor(
            n_estimators=300, max_depth=12, random_state=42, n_jobs=-1
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=300, learning_rate=0.05, max_depth=3, random_state=42
        ),
    }
    predictions: dict[str, np.ndarray] = {}
    metric_rows: list[dict] = []
    for name, model in models.items():
        if name == "Linear Regression":
            model.fit(X_train_scaled, y_train)
            prediction = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            prediction = model.predict(X_test)
        predictions[name] = prediction
        metric_rows.append({
            "Model": name,
            "MAE": float(mean_absolute_error(y_test, prediction)),
            "RMSE": float(np.sqrt(mean_squared_error(y_test, prediction))),
            "R2": float(r2_score(y_test, prediction)),
        })

    metrics = pd.DataFrame(metric_rows).set_index("Model").sort_values(
        "R2", ascending=False
    )
    best_model_name = str(metrics["R2"].idxmax())
    best_predictions = predictions[best_model_name]

    # Keep the notebook's sample profile and its unseen-label fallback behavior.
    new_profile = {
        "Job Title": "Machine Learning Engineer",
        "Experience (Years)": 5.0,
        "Education": "Masters",
        "Skill Count": 12,
        "Industry": "Technology",
        "Company": "Google",
        "Location": "Bengaluru, India",
        "Remote Work": "Yes",
        "Certification": "AWS ML Specialty",
    }
    new_df = pd.DataFrame([new_profile])
    new_df["Education"] = new_df["Education"].map(education_order)
    new_df = pd.get_dummies(new_df, columns=["Remote Work"], prefix="Remote")
    unknown_profile_categories: list[str] = []
    for col in label_cols:
        known = set(encoders[col].classes_)
        if new_profile[col] not in known:
            unknown_profile_categories.append(col)
        new_df[col] = new_df[col].apply(
            lambda value: value if value in known else encoders[col].classes_[0]
        )
        new_df[col] = encoders[col].transform(new_df[col].astype(str))
    for col in X.columns:
        if col not in new_df.columns:
            new_df[col] = 0
    new_df = new_df[X.columns]
    profile_prediction = float(models["Random Forest"].predict(new_df)[0])

    return {
        "df": df,
        "data": data,
        "X": X,
        "y": y,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "metrics": metrics,
        "models": models,
        "predictions": predictions,
        "best_model_name": best_model_name,
        "best_predictions": best_predictions,
        "rf_importances": pd.Series(
            models["Random Forest"].feature_importances_, index=X.columns
        ).sort_values(ascending=False),
        "new_profile": new_profile,
        "profile_prediction": profile_prediction,
        "unknown_profile_categories": unknown_profile_categories,
        "missing_by_column": df.isna().sum(),
        "salary_mean": float(df["Salary (USD)"].mean()),
        "salary_median": float(df["Salary (USD)"].median()),
    }


def make_figures(analysis: dict) -> dict[str, Path]:
    """Save separately usable, titled evidence figures for the record."""
    df = analysis["df"]
    data = analysis["data"]
    X = analysis["X"]
    y_test = analysis["y_test"]
    metrics = analysis["metrics"]
    best_name = analysis["best_model_name"]
    best_predictions = analysis["best_predictions"]
    figures: dict[str, Path] = {}

    # Figure 01 — a readable sample of the source file.
    columns = [
        "ID", "Job Title", "Experience (Years)", "Education", "Industry",
        "Location", "Remote Work", "Salary (USD)",
    ]
    preview = df.loc[:, columns].head(6).copy().fillna("Missing")
    preview = preview.rename(columns={
        "Experience (Years)": "Experience (yrs)",
        "Remote Work": "Remote Type",
        "Salary (USD)": "Salary USD",
    })
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.axis("off")
    figure_title(ax, 1, f"SOURCE DATASET PREVIEW  ·  FIRST {len(preview)} RECORDS")
    ax.text(0, 0.91,
            f"{len(df):,} records  •  {df.shape[1]} source columns  •  Target: Salary (USD)",
            transform=ax.transAxes, color=MUTED, fontsize=10)
    table = ax.table(
        cellText=preview.values,
        colLabels=preview.columns,
        cellLoc="left",
        colLoc="left",
        loc="center",
        bbox=[0, 0.06, 1, 0.75],
        colWidths=[0.06, 0.20, 0.13, 0.11, 0.13, 0.16, 0.11, 0.10],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor(GRID)
        if row == 0:
            cell.set_facecolor(NAVY)
            cell.get_text().set_color(WHITE)
            cell.get_text().set_weight("bold")
        else:
            cell.set_facecolor(WHITE if row % 2 else PALE)
            cell.get_text().set_color(INK)
    figures["dataset_preview"] = save_figure(fig, "01_dataset_preview.png")

    # Figure 02 — data quality check; show non-zero columns while documenting
    # that the omitted fields have no missing entries.
    missing = analysis["missing_by_column"].sort_values(ascending=True)
    nonzero_missing = missing[missing > 0]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    if nonzero_missing.empty:
        ax.text(0.5, 0.52, "No missing values found", ha="center", va="center",
                fontsize=18, color=TEAL, transform=ax.transAxes)
        ax.set_yticks([])
        ax.set_xticks([])
    else:
        bars = ax.barh(nonzero_missing.index, nonzero_missing.values, color=GOLD,
                       height=0.55)
        ax.set_xlabel("Blank cells")
        ax.set_xlim(0, max(nonzero_missing.values) * 1.4)
        for bar, count in zip(bars, nonzero_missing.values):
            ax.text(bar.get_width() + max(nonzero_missing.values) * 0.025,
                    bar.get_y() + bar.get_height() / 2,
                    f"{count}  ({count / len(df):.1%} of records)",
                    va="center", fontsize=10, color=INK)
        ax.grid(axis="y", visible=False)
    total_missing = int(analysis["missing_by_column"].sum())
    figure_title(ax, 2, f"MISSING-VALUE AUDIT  ·  {total_missing:,} BLANK CELLS")
    ax.text(0, -0.22,
            "Only fields with missing entries are plotted; every other source field has zero blanks.",
            transform=ax.transAxes, fontsize=8.5, color=MUTED)
    figures["missing_values"] = save_figure(fig, "02_missing_values.png")

    # Figure 03 — target salary distribution.
    fig, ax = plt.subplots(figsize=(9, 5.1))
    sns.histplot(data=df, x="Salary (USD)", kde=True, bins=30, color=TEAL,
                 edgecolor=WHITE, ax=ax)
    ax.axvline(analysis["salary_median"], color=GOLD, linestyle="--", linewidth=2,
               label=f"Median  {display_salary(analysis['salary_median'])}")
    ax.set_xlabel("Salary (USD)")
    ax.set_ylabel("Number of job records")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
    ax.legend(frameon=True)
    figure_title(ax, 3, "SALARY DISTRIBUTION")
    figures["salary_distribution"] = save_figure(fig, "03_salary_distribution.png")

    # Figure 04 — correlation matrix for the numeric predictors and target.
    numeric_df = df.select_dtypes(include=[np.number]).drop(columns=["ID"], errors="ignore")
    fig, ax = plt.subplots(figsize=(7.2, 5.8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f",
                vmin=-1, vmax=1, square=True, linewidths=0.7,
                cbar_kws={"shrink": 0.78}, ax=ax)
    figure_title(ax, 4, "NUMERIC-FEATURE CORRELATION HEATMAP")
    figures["correlation_heatmap"] = save_figure(fig, "04_numeric_correlation_heatmap.png")

    # Figure 05 — numeric experience relationship, with education groups.
    fig, ax = plt.subplots(figsize=(9, 5.2))
    education_order = ["Bachelors", "Masters", "PhD"]
    sns.scatterplot(
        data=df, x="Experience (Years)", y="Salary (USD)", hue="Education",
        hue_order=education_order, palette=[BLUE, TEAL, GOLD], alpha=0.72,
        s=42, edgecolor="white", linewidth=0.25, ax=ax,
    )
    ax.set_xlabel("Experience (Years)")
    ax.set_ylabel("Salary (USD)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
    figure_title(ax, 5, "EXPERIENCE VS. SALARY")
    ax.legend(title="Education", frameon=True)
    figures["experience_vs_salary"] = save_figure(fig, "05_experience_vs_salary.png")

    # Figure 06 — salary by education.
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    sns.boxplot(data=df, x="Education", y="Salary (USD)",
                order=education_order, color=BLUE, width=0.58, ax=ax)
    ax.set_xlabel("Education")
    ax.set_ylabel("Salary (USD)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
    figure_title(ax, 6, "SALARY BY EDUCATION")
    figures["salary_by_education"] = save_figure(fig, "06_salary_by_education.png")

    # Figure 07 — salary by remote-work arrangement.
    remote_order = list(df["Remote Work"].value_counts().index)
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    sns.boxplot(data=df, x="Remote Work", y="Salary (USD)",
                order=remote_order, color=TEAL, width=0.58, ax=ax)
    ax.set_xlabel("Remote Work Type")
    ax.set_ylabel("Salary (USD)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
    figure_title(ax, 7, "SALARY BY REMOTE-WORK TYPE")
    figures["salary_by_remote_work"] = save_figure(fig, "07_salary_by_remote_work.png")

    # Figure 08 — job-title boxplots sorted by frequency, matching notebook order.
    title_order = df["Job Title"].value_counts().index
    fig, ax = plt.subplots(figsize=(12, 6.2))
    sns.boxplot(data=df, x="Job Title", y="Salary (USD)", order=title_order,
                color=PURPLE, width=0.62, ax=ax)
    ax.set_xlabel("Job Title")
    ax.set_ylabel("Salary (USD)")
    ax.tick_params(axis="x", rotation=63, labelsize=8)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
    figure_title(ax, 8, "SALARY BY JOB TITLE")
    figures["salary_by_job_title"] = save_figure(fig, "08_salary_by_job_title.png")

    # Figure 09 — industry boxplots.
    industry_order = df["Industry"].value_counts().index
    fig, ax = plt.subplots(figsize=(10, 5.2))
    sns.boxplot(data=df, x="Industry", y="Salary (USD)", order=industry_order,
                color=GOLD, width=0.62, ax=ax)
    ax.set_xlabel("Industry")
    ax.set_ylabel("Salary (USD)")
    ax.tick_params(axis="x", rotation=42, labelsize=8.5)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
    figure_title(ax, 9, "SALARY BY INDUSTRY")
    figures["salary_by_industry"] = save_figure(fig, "09_salary_by_industry.png")

    # Figure 10 — explicit record of data encoding and train/test split.
    fig, ax = plt.subplots(figsize=(10, 5.1))
    ax.axis("off")
    figure_title(ax, 10, "PREPROCESSING AND FEATURE-MATRIX SUMMARY")
    summary_lines = [
        ("ID", "Dropped as a record identifier"),
        ("Education", "Ordinal map: Bachelors = 0  ·  Masters = 1  ·  PhD = 2"),
        ("Remote Work", "One-hot encoded into " + ", ".join(
            col for col in X.columns if col.startswith("Remote_"))),
        ("High-cardinality fields", "Label encoded: Job Title, Industry, Company, Location, Certification"),
        ("Train / test split", f"{len(analysis['X_train']):,} train  ·  {len(analysis['X_test']):,} test  ·  random_state = 42"),
        ("Model inputs", f"{len(df):,} rows  ·  {X.shape[1]} feature columns"),
    ]
    y = 0.78
    for index, (label, description) in enumerate(summary_lines):
        fill = PALE if index % 2 == 0 else WHITE
        ax.add_patch(plt.Rectangle((0.02, y - 0.105), 0.96, 0.105,
                                   transform=ax.transAxes, color=fill, zorder=0))
        ax.text(0.045, y - 0.054, label, transform=ax.transAxes,
                color=NAVY, fontsize=10, fontweight="bold", va="center")
        ax.text(0.28, y - 0.054, description, transform=ax.transAxes,
                color=INK, fontsize=9.2, va="center", wrap=True)
        y -= 0.115
    ax.text(0.03, 0.045,
            "Note: this reproduces the notebook's current categorical handling; blank certification values become a separate 'nan' label.",
            transform=ax.transAxes, color=MUTED, fontsize=8.3, wrap=True)
    figures["preprocessing_summary"] = save_figure(fig, "10_preprocessing_summary.png")

    # Figure 11 — the exact metric table produced by the evaluation step.
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.axis("off")
    figure_title(ax, 11, "REGRESSION MODEL METRICS ON THE HELD-OUT TEST SET")
    table_rows = []
    for model_name, row in metrics.iterrows():
        table_rows.append([
            model_name,
            f"${row['MAE']:,.2f}",
            f"${row['RMSE']:,.2f}",
            f"{row['R2']:.4f}",
        ])
    table = ax.table(
        cellText=table_rows,
        colLabels=["Model", "MAE (USD) ↓", "RMSE (USD) ↓", "R² ↑"],
        cellLoc="center", colLoc="center", loc="center",
        bbox=[0.02, 0.12, 0.96, 0.72],
        colWidths=[0.38, 0.23, 0.23, 0.16],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor(GRID)
        if row == 0:
            cell.set_facecolor(NAVY)
            cell.get_text().set_color(WHITE)
            cell.get_text().set_weight("bold")
        else:
            cell.set_facecolor("#E8F4F4" if row == 1 else (WHITE if row % 2 else PALE))
            cell.get_text().set_color(INK)
    ax.text(0.02, 0.035,
            "Lower MAE/RMSE and higher R² indicate better held-out fit; values are in USD except R².",
            transform=ax.transAxes, color=MUTED, fontsize=8.5)
    figures["model_metrics_table"] = save_figure(fig, "11_model_metrics_table.png")

    # Figure 12 — model comparison bars, as in the notebook.
    fig, axes = plt.subplots(1, 2, figsize=(10, 6.5))
    ordered_metrics = metrics
    r2_bars = axes[0].bar(ordered_metrics.index, ordered_metrics["R2"], color=BLUE)
    axes[0].set_title("R² Score by Model", color=NAVY, fontweight="bold")
    axes[0].set_ylabel("R²")
    axes[0].set_ylim(0, 1.04)
    axes[0].tick_params(axis="x", rotation=28, labelsize=8.5)
    axes[0].bar_label(r2_bars, fmt="%.3f", padding=3, fontsize=8)
    rmse_bars = axes[1].bar(ordered_metrics.index, ordered_metrics["RMSE"], color=GOLD)
    axes[1].set_title("RMSE by Model", color=NAVY, fontweight="bold")
    axes[1].set_ylabel("RMSE (USD)")
    axes[1].yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
    axes[1].tick_params(axis="x", rotation=28, labelsize=8.5)
    axes[1].bar_label(rmse_bars, labels=[f"${v:,.0f}" for v in ordered_metrics["RMSE"]],
                      padding=3, fontsize=8)
    for ax in axes:
        ax.grid(axis="x", visible=False)
        ax.margins(y=0.16)
    fig.suptitle("FIGURE 12  |  MODEL COMPARISON", x=0.02, y=0.99, ha="left",
                 fontsize=13, fontweight="bold", color=NAVY)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    figures["model_comparison"] = save_figure(fig, "12_model_comparison.png")

    # Figure 13 — best model's out-of-sample predictions against actual values.
    fig, ax = plt.subplots(figsize=(7.5, 7.2))
    ax.scatter(y_test, best_predictions, alpha=0.68, color=GOLD,
               edgecolor="white", linewidth=0.35, s=52)
    low = float(min(y_test.min(), best_predictions.min()))
    high = float(max(y_test.max(), best_predictions.max()))
    ax.plot([low, high], [low, high], color=INK, linestyle="--", linewidth=1.8,
            label="Perfect prediction")
    ax.set_xlim(low - 4000, high + 4000)
    ax.set_ylim(low - 4000, high + 4000)
    ax.set_aspect("equal", adjustable="box")
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.xaxis.set_major_formatter(FuncFormatter(compact_usd))
    ax.yaxis.set_major_formatter(FuncFormatter(compact_usd))
    ax.tick_params(axis="both", labelsize=8.5)
    ax.set_xlabel("Actual Salary (USD)")
    ax.set_ylabel("Predicted Salary (USD)")
    ax.legend(loc="upper left", frameon=True)
    figure_title(ax, 13, f"PREDICTED VS. ACTUAL SALARY  ·  {best_name.upper()}")
    figures["actual_vs_predicted"] = save_figure(fig, "13_actual_vs_predicted.png")

    # Figure 14 — residual error distribution for that same selected model.
    residuals = np.asarray(y_test) - best_predictions
    fig, ax = plt.subplots(figsize=(9, 5.1))
    sns.histplot(residuals, kde=True, bins=30, color=PURPLE, edgecolor=WHITE, ax=ax)
    ax.axvline(0, color=INK, linestyle="--", linewidth=1.5, label="Zero error")
    ax.axvline(float(np.mean(residuals)), color=GOLD, linestyle="-", linewidth=1.8,
               label=f"Mean residual  ${np.mean(residuals):,.0f}")
    ax.set_xlabel("Residual (Actual − Predicted), USD")
    ax.set_ylabel("Number of test records")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:,.0f}"))
    ax.legend(frameon=True)
    figure_title(ax, 14, f"RESIDUAL DISTRIBUTION  ·  {best_name.upper()}")
    figures["residual_distribution"] = save_figure(fig, "14_residual_distribution.png")

    # Figure 15 — Random Forest feature importance, matching notebook section 8.
    importances = analysis["rf_importances"].sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(9, 6.4))
    bars = ax.barh(importances.index, importances.values, color=sns.color_palette("viridis", len(importances)))
    ax.bar_label(bars, labels=[f"{value:.3f}" for value in importances.values],
                 padding=3, fontsize=8)
    ax.set_xlim(0, max(importances.values) * 1.18)
    ax.set_xlabel("Relative importance")
    ax.set_ylabel("Model input")
    ax.grid(axis="y", visible=False)
    figure_title(ax, 15, "FEATURE IMPORTANCE  ·  RANDOM FOREST")
    figures["feature_importance"] = save_figure(fig, "15_random_forest_feature_importance.png")

    # Figure 16 — the example custom profile prediction printed by the notebook.
    profile = analysis["new_profile"]
    fig, ax = plt.subplots(figsize=(9, 5.7))
    ax.axis("off")
    figure_title(ax, 16, "SAMPLE CUSTOM-PROFILE SALARY PREDICTION")
    ax.add_patch(plt.Rectangle((0.02, 0.61), 0.96, 0.19,
                               transform=ax.transAxes, color=NAVY, zorder=0))
    ax.text(0.05, 0.75, "Random Forest estimate", transform=ax.transAxes,
            fontsize=11, color="#D5E8F5", va="center")
    ax.text(0.05, 0.665, display_salary(analysis["profile_prediction"]),
            transform=ax.transAxes, fontsize=24, color=WHITE,
            fontweight="bold", va="center")
    profile_fields = [
        ("Job Title", profile["Job Title"]),
        ("Experience", f"{profile['Experience (Years)']:.1f} years"),
        ("Education", profile["Education"]),
        ("Skills", str(profile["Skill Count"])),
        ("Industry / Company", f"{profile['Industry']}  /  {profile['Company']}"),
        ("Location", profile["Location"]),
        ("Remote Work", profile["Remote Work"]),
        ("Certification", profile["Certification"]),
    ]
    left_fields, right_fields = profile_fields[:4], profile_fields[4:]
    for index, (label, value) in enumerate(left_fields):
        yy = 0.52 - index * 0.105
        ax.text(0.05, yy, label, transform=ax.transAxes,
                color=MUTED, fontsize=10, va="center")
        ax.text(0.27, yy, value, transform=ax.transAxes,
                color=INK, fontsize=10.5, fontweight="normal", va="center")
    for index, (label, value) in enumerate(right_fields):
        yy = 0.52 - index * 0.105
        ax.text(0.60, yy, label, transform=ax.transAxes,
                color=MUTED, fontsize=9.5, va="center")
        ax.text(0.81, yy, value, transform=ax.transAxes,
                color=INK, fontsize=9.8, fontweight="normal", va="center")
    unknown = analysis["unknown_profile_categories"]
    note = (
        "Unseen categories use the notebook's first-known-label fallback: " + ", ".join(unknown) + "."
        if unknown else "All sample categories were found in the training data."
    )
    ax.text(0.03, 0.045, note,
            transform=ax.transAxes, color=MUTED, fontsize=9, wrap=True)
    figures["custom_profile_prediction"] = save_figure(fig, "16_custom_profile_prediction.png")

    return figures


def _add_page_header(fig: plt.Figure, section: str, title: str, subtitle: str) -> None:
    fig.text(0.075, 0.958, "AI/ML SALARY PREDICTION  /  PROJECT RECORD",
             color=BLUE, fontsize=8, fontweight="bold", va="top")
    fig.text(0.075, 0.92, title, color=NAVY, fontsize=19,
             fontweight="bold", va="top")
    fig.text(0.075, 0.881, subtitle, color=MUTED, fontsize=9.1, va="top")
    fig.add_artist(plt.Line2D([0.075, 0.925], [0.858, 0.858],
                              transform=fig.transFigure, color=GRID, linewidth=1))
    fig.text(0.925, 0.958, section.upper(), color=MUTED, fontsize=7.5,
             ha="right", va="top")


def _add_footer(fig: plt.Figure, page: int, total: int, date_label: str) -> None:
    fig.add_artist(plt.Line2D([0.075, 0.925], [0.062, 0.062],
                              transform=fig.transFigure, color=GRID, linewidth=0.8))
    fig.text(0.075, 0.038, f"Generated {date_label} from ai_ml_job_analysis.csv",
             color=MUTED, fontsize=7.3, va="center")
    fig.text(0.925, 0.038, f"{page:02d} / {total:02d}",
             color=MUTED, fontsize=7.3, ha="right", va="center")


def _place_image(fig: plt.Figure, image_path: Path, rect: tuple[float, float, float, float]) -> None:
    ax = fig.add_axes(rect)
    ax.imshow(mpimg.imread(image_path))
    ax.axis("off")


def make_pdf(analysis: dict, figures: dict[str, Path], generated_at: datetime) -> None:
    date_label = generated_at.strftime("%Y-%m-%d UTC")
    total_pages = 10
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with PdfPages(PDF_PATH, metadata={
        "Title": "AI/ML Salary Prediction — Project Record",
        "Author": "Vismay Vinod",
        "Subject": "Multi-page evidence record of data analysis, model evaluation and prediction outputs",
        "Keywords": "AI, machine learning, salary prediction, data analysis, regression",
    }) as pdf:
        # Page 1 — cover and workflow summary.
        fig = plt.figure(figsize=(8.5, 11), facecolor=PALE)
        fig.add_artist(plt.Rectangle((0, 0.72), 1, 0.28,
                                     transform=fig.transFigure, color=NAVY, zorder=0))
        fig.text(0.08, 0.94, f"PROJECT EVIDENCE  /  {generated_at.year}", color="#C8D9E8",
                 fontsize=9, fontweight="bold", va="top")
        fig.text(0.08, 0.885, "AI/ML Salary\nPrediction", color=WHITE,
                 fontsize=31, fontweight="bold", va="top", linespacing=1.12)
        fig.text(0.08, 0.785,
                 "A visual record of the dataset, exploratory analysis, preprocessing,\n"
                 "regression experiments, evaluation and sample prediction.",
                 color="#E2EDF5", fontsize=10, va="top", linespacing=1.35)

        best_name = analysis["best_model_name"]
        best_row = analysis["metrics"].loc[best_name]
        cards = [
            ("SOURCE RECORDS", f"{len(analysis['df']):,}", "AI/ML job listings"),
            ("MODEL INPUTS", str(analysis["X"].shape[1]), "encoded features"),
            ("MODELS TESTED", str(len(analysis["metrics"])), "regression models"),
            ("TOP TEST R²", f"{best_row['R2']:.3f}", best_name),
        ]
        card_y = 0.60
        for i, (label, value, detail) in enumerate(cards):
            x = 0.08 + i * 0.215
            fig.add_artist(plt.Rectangle((x, card_y), 0.19, 0.105,
                                         transform=fig.transFigure,
                                         facecolor=WHITE, edgecolor=GRID, linewidth=0.8))
            fig.text(x + 0.015, card_y + 0.078, label, color=MUTED,
                     fontsize=7, fontweight="bold", va="center")
            fig.text(x + 0.015, card_y + 0.046, value, color=NAVY,
                     fontsize=16, fontweight="bold", va="center")
            fig.text(x + 0.015, card_y + 0.019, detail, color=MUTED,
                     fontsize=7.1, va="center")

        fig.text(0.08, 0.54, "WORKFLOW RECORDED", color=NAVY,
                 fontsize=10, fontweight="bold")
        steps = ["Load data", "Explore", "Encode", "Split", "Train", "Evaluate", "Predict"]
        start_x, gap, box_w = 0.08, 0.122, 0.103
        for i, step in enumerate(steps):
            x = start_x + i * gap
            fig.add_artist(plt.Rectangle((x, 0.475), box_w, 0.043,
                                         transform=fig.transFigure,
                                         facecolor=BLUE if i in (0, 6) else WHITE,
                                         edgecolor=BLUE, linewidth=0.8))
            fig.text(x + box_w / 2, 0.4965, step,
                     color=WHITE if i in (0, 6) else NAVY,
                     fontsize=6.8, ha="center", va="center", fontweight="bold")
            if i < len(steps) - 1:
                fig.text(x + box_w + 0.008, 0.4965, "›", color=TEAL,
                         fontsize=14, ha="center", va="center")

        fig.text(0.08, 0.415, "IN THIS RECORD", color=NAVY,
                 fontsize=10, fontweight="bold")
        contents = [
            "Dataset preview and missing-value audit",
            "Salary distribution, correlation, and categorical comparisons",
            "Encoding and train/test split summary",
            "Four regression models with MAE, RMSE and R²",
            "Best-model diagnostics, Random Forest feature importance, and a sample prediction",
        ]
        for i, item in enumerate(contents):
            fig.text(0.095, 0.38 - i * 0.044, f"{i + 1:02d}   {item}",
                     color=INK, fontsize=8.8, va="center")

        total_missing = int(analysis["missing_by_column"].sum())
        missing_cert = int(analysis["missing_by_column"].get("Certification", 0))
        fig.add_artist(plt.Rectangle((0.08, 0.105), 0.84, 0.06,
                                     transform=fig.transFigure,
                                     facecolor="#FFF6E7", edgecolor="#F2D49A", linewidth=0.8))
        fig.text(0.10, 0.135,
                 f"Data note: {total_missing:,} blank cells in total; {missing_cert:,} are in Certification. "
                 "The current notebook treats these as a categorical 'nan' value.",
                 color=INK, fontsize=7.5, va="center", wrap=True)
        fig.text(0.08, 0.075,
                 f"Generated {date_label}  ·  Prepared by Vismay Vinod  ·  Source: ai_ml_job_analysis.csv",
                 color=MUTED, fontsize=7.4, va="center")
        fig.text(0.92, 0.075, "01 / 10", color=MUTED,
                 fontsize=7.4, ha="right", va="center")
        pdf.savefig(fig, facecolor=fig.get_facecolor())
        plt.close(fig)

        # Page 2 — source preview and completeness check.
        fig = plt.figure(figsize=(8.5, 11), facecolor=WHITE)
        _add_page_header(fig, "01  /  DATA", "Dataset and data quality",
                         f"Source: ai_ml_job_analysis.csv  ·  {len(analysis['df']):,} rows  ·  {analysis['df'].shape[1]} columns")
        _place_image(fig, figures["dataset_preview"], (0.08, 0.49, 0.84, 0.31))
        _place_image(fig, figures["missing_values"], (0.17, 0.105, 0.66, 0.33))
        _add_footer(fig, 2, total_pages, date_label)
        pdf.savefig(fig, facecolor=WHITE)
        plt.close(fig)

        # Page 3 — distribution, association and experience scatter.
        fig = plt.figure(figsize=(8.5, 11), facecolor=WHITE)
        _add_page_header(fig, "02  /  EXPLORATION", "Exploratory analysis",
                         "Salary range, numeric relationships, and experience patterns in the source records.")
        _place_image(fig, figures["salary_distribution"], (0.07, 0.55, 0.47, 0.29))
        _place_image(fig, figures["correlation_heatmap"], (0.55, 0.54, 0.39, 0.31))
        _place_image(fig, figures["experience_vs_salary"], (0.105, 0.11, 0.79, 0.40))
        _add_footer(fig, 3, total_pages, date_label)
        pdf.savefig(fig, facecolor=WHITE)
        plt.close(fig)

        # Page 4 — education and remote-work category breakdowns.
        fig = plt.figure(figsize=(8.5, 11), facecolor=WHITE)
        _add_page_header(fig, "03  /  EXPLORATION", "Salary by work and education",
                         "Box plots compare the spread and median salary across two categorical variables.")
        _place_image(fig, figures["salary_by_education"], (0.11, 0.49, 0.78, 0.31))
        _place_image(fig, figures["salary_by_remote_work"], (0.11, 0.105, 0.78, 0.31))
        _add_footer(fig, 4, total_pages, date_label)
        pdf.savefig(fig, facecolor=WHITE)
        plt.close(fig)

        # Page 5 — higher-cardinality salary comparisons.
        fig = plt.figure(figsize=(8.5, 11), facecolor=WHITE)
        _add_page_header(fig, "04  /  EXPLORATION", "Salary by role and industry",
                         "Job titles are ordered by frequency; industry categories are shown for comparison.")
        _place_image(fig, figures["salary_by_job_title"], (0.07, 0.48, 0.86, 0.34))
        _place_image(fig, figures["salary_by_industry"], (0.10, 0.105, 0.80, 0.31))
        _add_footer(fig, 5, total_pages, date_label)
        pdf.savefig(fig, facecolor=WHITE)
        plt.close(fig)

        # Page 6 — feature preparation and held-out metrics.
        fig = plt.figure(figsize=(8.5, 11), facecolor=WHITE)
        _add_page_header(fig, "05  /  MODELING", "Preprocessing and model outputs",
                         "The evaluation uses an 80/20 split with random_state = 42.")
        _place_image(fig, figures["preprocessing_summary"], (0.09, 0.51, 0.82, 0.32))
        _place_image(fig, figures["model_metrics_table"], (0.13, 0.12, 0.74, 0.33))
        _add_footer(fig, 6, total_pages, date_label)
        pdf.savefig(fig, facecolor=WHITE)
        plt.close(fig)

        # Page 7 — visual model comparison.
        fig = plt.figure(figsize=(8.5, 11), facecolor=WHITE)
        _add_page_header(fig, "06  /  MODELING", "Comparing four regressors",
                         "Decision Tree, Random Forest and Gradient Boosting improve on the linear baseline for this split.")
        _place_image(fig, figures["model_comparison"], (0.08, 0.32, 0.84, 0.50))
        best_name = analysis["best_model_name"]
        best_row = analysis["metrics"].loc[best_name]
        fig.add_artist(plt.Rectangle((0.10, 0.16), 0.80, 0.12,
                                     transform=fig.transFigure,
                                     facecolor=PALE, edgecolor=GRID, linewidth=0.8))
        card_items = [
            (0.13, "BEST MODEL", best_name),
            (0.41, "TEST R²", f"{best_row['R2']:.4f}"),
            (0.57, "MAE", display_salary(best_row["MAE"])),
            (0.75, "RMSE", display_salary(best_row["RMSE"])),
        ]
        for x, label, value in card_items:
            fig.text(x, 0.245, label, color=MUTED,
                     fontsize=7.2, fontweight="bold", va="center")
            fig.text(x, 0.198, value, color=NAVY,
                     fontsize=9.2, fontweight="bold", va="center")
        _add_footer(fig, 7, total_pages, date_label)
        pdf.savefig(fig, facecolor=WHITE)
        plt.close(fig)

        # Page 8 — diagnostics for the model selected by test-set R².
        fig = plt.figure(figsize=(8.5, 11), facecolor=WHITE)
        _add_page_header(fig, "07  /  EVALUATION", "Best-model diagnostics",
                         f"Predicted-vs-actual values and residuals for {analysis['best_model_name']} on held-out records.")
        _place_image(fig, figures["actual_vs_predicted"], (0.13, 0.49, 0.74, 0.34))
        _place_image(fig, figures["residual_distribution"], (0.11, 0.105, 0.78, 0.31))
        _add_footer(fig, 8, total_pages, date_label)
        pdf.savefig(fig, facecolor=WHITE)
        plt.close(fig)

        # Page 9 — inspect Random Forest's feature importances.
        fig = plt.figure(figsize=(8.5, 11), facecolor=WHITE)
        _add_page_header(fig, "08  /  INTERPRETATION", "Feature importance",
                         "Random Forest importances describe this fitted forest and are not causal effects.")
        _place_image(fig, figures["feature_importance"], (0.11, 0.22, 0.78, 0.57))
        fig.text(0.12, 0.14,
                 "Importance ranks each encoded input by its contribution to the fitted Random Forest's split decisions. "
                 "The notebook reports these values separately from the best-R² model.",
                 color=MUTED, fontsize=8.2, wrap=True, va="top")
        _add_footer(fig, 9, total_pages, date_label)
        pdf.savefig(fig, facecolor=WHITE)
        plt.close(fig)

        # Page 10 — sample prediction and transparent limitations.
        fig = plt.figure(figsize=(8.5, 11), facecolor=WHITE)
        _add_page_header(fig, "09  /  EXAMPLE", "Custom-profile prediction",
                         "A demonstration using the editable example profile from the notebook.")
        _place_image(fig, figures["custom_profile_prediction"], (0.08, 0.47, 0.84, 0.36))
        fig.text(0.10, 0.39, "READING THIS OUTPUT", color=NAVY,
                 fontsize=9.3, fontweight="bold", va="center")
        caveats = [
            "The custom-profile cell uses the Random Forest model, while model comparison selects the best model by test-set R².",
            "In this example, the unseen Location category uses the notebook's first-known-label fallback.",
            "The result is a model estimate from this 500-row project dataset, not a salary guarantee or a production-ready valuation.",
            "Before deployment, explicitly impute missing certifications and use a training-safe categorical encoder with unknown-category handling.",
        ]
        for i, caveat in enumerate(caveats):
            fig.text(0.115, 0.345 - i * 0.052, f"•  {caveat}",
                     color=INK, fontsize=8.1, va="center", wrap=True)
        fig.add_artist(plt.Rectangle((0.10, 0.105), 0.80, 0.06,
                                     transform=fig.transFigure,
                                     facecolor="#E8F4F4", edgecolor="#B8DDDC", linewidth=0.8))
        fig.text(0.12, 0.135,
                 "Record complete: data loaded · EDA · encoding · split · 4 models · evaluation · diagnostics · feature importance · example prediction",
                 color=NAVY, fontsize=7.5, fontweight="bold", va="center", wrap=True)
        _add_footer(fig, 10, total_pages, date_label)
        pdf.savefig(fig, facecolor=WHITE)
        plt.close(fig)


def write_results(analysis: dict, figures: dict[str, Path], generated_at: datetime) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    metrics_path = RESULTS_DIR / "model_metrics.csv"
    analysis["metrics"].to_csv(metrics_path, index_label="Model", float_format="%.8f")

    df = analysis["df"]
    salary = df["Salary (USD)"]
    missing = {str(k): int(v) for k, v in analysis["missing_by_column"].items()}
    metrics = []
    for name, row in analysis["metrics"].iterrows():
        metrics.append({
            "model": str(name),
            "mae_usd": float(row["MAE"]),
            "rmse_usd": float(row["RMSE"]),
            "r2": float(row["R2"]),
        })
    summary = {
        "generated_at_utc": generated_at.isoformat(),
        "source_dataset": "ai_ml_job_analysis.csv",
        "environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "matplotlib": matplotlib.__version__,
            "seaborn": sns.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "dataset": {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "missing_cells": int(df.isna().sum().sum()),
            "missing_by_column": missing,
            "salary_usd": {
                "minimum": float(salary.min()),
                "median": float(salary.median()),
                "mean": float(salary.mean()),
                "maximum": float(salary.max()),
            },
        },
        "preprocessing": {
            "dropped_columns": ["ID"],
            "education_ordinal_mapping": {"Bachelors": 0, "Masters": 1, "PhD": 2},
            "remote_work_encoding": "one-hot",
            "label_encoded_columns": [
                "Job Title", "Industry", "Company", "Location", "Certification"
            ],
            "note": "Matches the notebook; missing Certification values are converted to the string 'nan'.",
        },
        "split": {
            "train_rows": int(len(analysis["X_train"])),
            "test_rows": int(len(analysis["X_test"])),
            "test_size": 0.2,
            "random_state": 42,
            "predictor_columns": int(analysis["X"].shape[1]),
        },
        "models": metrics,
        "best_model_by_test_r2": analysis["best_model_name"],
        "custom_profile_prediction": {
            "model": "Random Forest",
            "salary_usd": analysis["profile_prediction"],
            "unknown_categories_using_fallback": analysis["unknown_profile_categories"],
        },
        "artifacts": {
            "report_pdf": str(PDF_PATH.relative_to(ROOT)),
            "model_metrics_csv": str(metrics_path.relative_to(ROOT)),
            "figures": [str(path.relative_to(ROOT)) for path in figures.values()],
        },
    }
    summary_path = RESULTS_DIR / "run_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    analysis = build_analysis(df)
    figures = make_figures(analysis)
    generated_at = datetime.now(timezone.utc)
    write_results(analysis, figures, generated_at)
    make_pdf(analysis, figures, generated_at)

    print(f"Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    print("Model results (sorted by test-set R²):")
    print(analysis["metrics"].to_string(formatters={
        "MAE": lambda value: f"${value:,.2f}",
        "RMSE": lambda value: f"${value:,.2f}",
        "R2": lambda value: f"{value:.4f}",
    }))
    print(f"Best model: {analysis['best_model_name']}")
    print(f"Sample Random Forest prediction: {display_salary(analysis['profile_prediction'])}")
    print(f"PDF record: {PDF_PATH.relative_to(ROOT)}")
    print(f"Figures: {len(figures)} PNG files in {FIGURE_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
