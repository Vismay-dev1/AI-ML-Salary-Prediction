"""
Re-runs the analysis from AI_ML_Salary_Prediction.ipynb (same preprocessing,
same train/test split, same model settings) and writes:
  - reports/assets/charts/*.png   (charts used in the Word report and slides)
  - reports/assets/metrics.json   (numbers used in the slides and Word report)

Run from the repository root:
    python reports/build_charts.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyBboxPatch
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "reports", "assets")
CH = os.path.join(OUT, "charts")
os.makedirs(CH, exist_ok=True)

NAVY = "#0F172A"; INDIGO = "#6366F1"; TEAL = "#14B8A6"; AMBER = "#F59E0B"
ROSE = "#F43F5E"; SLATE = "#64748B"; LIGHT = "#E2E8F0"; VIOLET = "#A78BFA"
plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 200, "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": SLATE, "axes.labelcolor": NAVY, "text.color": NAVY,
    "xtick.color": NAVY, "ytick.color": NAVY, "axes.titleweight": "bold",
    "axes.titlesize": 14, "axes.titlepad": 14,
})
S = "Salary (USD)"
money = lambda v, _=None: f"${v/1000:,.0f}k"

def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(CH, name), bbox_inches="tight", facecolor="white")
    plt.close(fig)

# ---------------------------------------------------------------- data
df = pd.read_csv(os.path.join(ROOT, "ai_ml_job_analysis.csv"))
m = {}
m["rows"], m["cols"] = df.shape
m["salary_mean"] = df[S].mean(); m["salary_median"] = df[S].median()
m["salary_min"] = df[S].min(); m["salary_max"] = df[S].max(); m["salary_std"] = df[S].std()
m["n_titles"] = df["Job Title"].nunique(); m["n_companies"] = df["Company"].nunique()
m["n_locations"] = df["Location"].nunique(); m["n_industries"] = df["Industry"].nunique()
m["missing_cert"] = int(df["Certification"].isna().sum())
m["duplicates"] = int(df.duplicated().sum())
m["corr_exp_salary"] = df["Experience (Years)"].corr(df[S])
m["corr_skill_salary"] = df["Skill Count"].corr(df[S])
m["corr_exp_skill"] = df["Experience (Years)"].corr(df["Skill Count"])
m["skew"] = df[S].skew()
m["interns_over_5y"] = int(((df["Job Title"] == "Research Intern") & (df["Experience (Years)"] > 5)).sum())
m["remote_location_rows"] = int((df["Location"] == "Remote").sum())

def region(loc):
    if "India" in loc: return "India"
    if "USA" in loc: return "USA"
    if loc == "Remote": return "Remote"
    return "Europe / Canada / Singapore"
df["Region"] = df["Location"].map(region)
REG_COL = {"India": ROSE, "USA": INDIGO, "Europe / Canada / Singapore": TEAL, "Remote": AMBER}

# ---------------------------------------------------------------- charts: EDA
fig, ax = plt.subplots(figsize=(10, 5.2))
sns.histplot(df[S], bins=25, kde=True, color=INDIGO, edgecolor="white", ax=ax)
ax.axvline(m["salary_mean"], color=ROSE, ls="--", lw=2, label=f"Mean {money(m['salary_mean'])}")
ax.axvline(m["salary_median"], color=AMBER, ls="--", lw=2, label=f"Median {money(m['salary_median'])}")
ax.xaxis.set_major_formatter(plt.FuncFormatter(money))
ax.set_title("How salaries are spread out (500 jobs)"); ax.set_xlabel("Salary"); ax.set_ylabel("Number of jobs")
ax.legend(frameon=False); save(fig, "c01_salary_distribution.png")

order = ["Bachelors", "Masters", "PhD"]
fig, ax = plt.subplots(figsize=(9, 5.2))
sns.boxplot(data=df, x="Education", y=S, order=order, hue="Education", palette=[TEAL, INDIGO, VIOLET], legend=False, ax=ax, width=0.5)
ax.yaxis.set_major_formatter(plt.FuncFormatter(money))
for i, e in enumerate(order):
    ax.text(i, df[df.Education == e][S].median() + 6000, f"median\n{money(df[df.Education == e][S].median())}",
            ha="center", fontsize=9, color=NAVY)
ax.set_title("Higher education, higher salary (on average)"); ax.set_ylabel("Salary"); ax.set_xlabel("")
save(fig, "c02_education.png")

loc = df.groupby(["Location", "Region"])[S].mean().reset_index().sort_values(S)
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.barh(loc["Location"], loc[S], color=[REG_COL[r] for r in loc["Region"]])
for y, v in enumerate(loc[S]):
    ax.text(v + 1500, y, money(v), va="center", fontsize=9)
ax.xaxis.set_major_formatter(plt.FuncFormatter(money))
ax.set_title("Average salary by location: location matters a lot")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=c, label=r) for r, c in REG_COL.items()], frameon=False, loc="lower right")
ax.set_xlabel("Average salary")
save(fig, "c03_location.png")

jt = df.groupby("Job Title")[S].mean().sort_values()
fig, ax = plt.subplots(figsize=(10, 6.5))
colors = [ROSE if v < 60000 else INDIGO for v in jt.values]
ax.barh(jt.index, jt.values, color=colors)
for y, v in enumerate(jt.values):
    ax.text(v + 1200, y, money(v), va="center", fontsize=9)
ax.xaxis.set_major_formatter(plt.FuncFormatter(money))
ax.set_title("Average salary by job title"); ax.set_xlabel("Average salary")
save(fig, "c04_job_title.png")

ind = df.groupby("Industry")[S].mean().sort_values()
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(ind.index, ind.values, color=TEAL)
for y, v in enumerate(ind.values):
    ax.text(v + 1000, y, money(v), va="center", fontsize=9)
ax.xaxis.set_major_formatter(plt.FuncFormatter(money))
ax.set_title("Average salary by industry (smaller effect)"); ax.set_xlabel("Average salary")
save(fig, "c05_industry.png")

fig, ax = plt.subplots(figsize=(10, 5.8))
pal = {"Bachelors": TEAL, "Masters": INDIGO, "PhD": VIOLET}
for e in order:
    sub = df[df.Education == e]
    ax.scatter(sub["Experience (Years)"], sub[S], s=38, alpha=0.7, color=pal[e], label=e, edgecolor="white", lw=0.5)
z = np.polyfit(df["Experience (Years)"], df[S], 1)
xs = np.linspace(0, 20, 50)
ax.plot(xs, np.polyval(z, xs), color=ROSE, lw=2.5, label="Overall trend")
ax.yaxis.set_major_formatter(plt.FuncFormatter(money))
ax.set_title(f"More experience, higher salary (correlation r = {m['corr_exp_salary']:.2f})")
ax.set_xlabel("Years of experience"); ax.set_ylabel("Salary"); ax.legend(frameon=False)
save(fig, "c06_experience_scatter.png")

df["Experience band"] = pd.cut(df["Experience (Years)"], [-0.1, 3, 6, 10, 15, 20],
                               labels=["0-3 yrs", "3-6 yrs", "6-10 yrs", "10-15 yrs", "15-20 yrs"])
eb = df.groupby("Experience band", observed=True)[S].agg(["mean", "count"])
m["exp_bands"] = {str(k): {"mean": float(v["mean"]), "count": int(v["count"])} for k, v in eb.iterrows()}
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(eb.index.astype(str), eb["mean"], color=[TEAL, "#2DD4BF", INDIGO, VIOLET, ROSE], width=0.6)
for b, (v, c) in zip(bars, zip(eb["mean"], eb["count"])):
    ax.text(b.get_x() + b.get_width() / 2, v + 2000, f"{money(v)}\n(n={c})", ha="center", fontsize=9)
ax.yaxis.set_major_formatter(plt.FuncFormatter(money)); ax.set_ylim(0, eb["mean"].max() * 1.25)
ax.set_title("Average salary grows with each experience band"); ax.set_ylabel("Average salary")
save(fig, "c07_experience_bands.png")

rw = df.groupby("Remote Work")[S].agg(["mean", "count"]).reindex(["No", "Hybrid", "Yes"])
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(["Not remote (No)", "Hybrid", "Remote (Yes)"], rw["mean"], color=[SLATE, INDIGO, TEAL], width=0.55)
for b, v, c in zip(bars, rw["mean"], rw["count"]):
    ax.text(b.get_x() + b.get_width() / 2, v + 1500, f"{money(v)}\n(n={c})", ha="center", fontsize=10)
ax.yaxis.set_major_formatter(plt.FuncFormatter(money)); ax.set_ylim(0, rw["mean"].max() * 1.25)
ax.set_title("Remote work makes little difference to salary"); ax.set_ylabel("Average salary")
save(fig, "c08_remote.png")

cert = df.groupby("Certification")[S].mean().sort_values()
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), gridspec_kw={"width_ratios": [2.4, 1]})
ax1.barh(cert.index, cert.values, color=INDIGO)
for y, v in enumerate(cert.values):
    ax1.text(v + 1000, y, money(v), va="center", fontsize=9)
ax1.xaxis.set_major_formatter(plt.FuncFormatter(money)); ax1.set_title("Average salary by certification")
miss = df["Certification"].isna().sum()
ax2.pie([len(df) - miss, miss], labels=["Has certification", "Missing (\"None\")"], colors=[INDIGO, LIGHT],
        autopct="%1.0f%%", startangle=90, wedgeprops=dict(width=0.38, edgecolor="white"), textprops={"fontsize": 10})
ax2.set_title("A third of rows have no certification")
save(fig, "c09_certification.png")

num = df[["Experience (Years)", "Skill Count", S]].rename(columns={"Experience (Years)": "Experience", S: "Salary"})
fig, ax = plt.subplots(figsize=(6.5, 5.3))
sns.heatmap(num.corr(), annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, square=True,
            linewidths=2, linecolor="white", cbar_kws={"shrink": 0.8}, annot_kws={"size": 13, "weight": "bold"}, ax=ax)
ax.set_title("How strongly numbers move together")
save(fig, "c10_correlation.png")

# ---------------------------------------------------------------- preprocessing (same as notebook)
data = df.drop(columns=["ID", "Region", "Experience band"]).copy()
data["Education"] = data["Education"].map({"Bachelors": 0, "Masters": 1, "PhD": 2})
data = pd.get_dummies(data, columns=["Remote Work"], prefix="Remote")
label_cols = ["Job Title", "Industry", "Company", "Location", "Certification"]
encoders = {}
for col in label_cols:
    le = LabelEncoder(); data[col] = le.fit_transform(data[col].astype(str)); encoders[col] = le
X = data.drop(columns=[S]); y = data[S]
m["features"] = list(X.columns)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
m["train_size"], m["test_size"] = len(Xtr), len(Xte)
sc = StandardScaler(); Xtr_s = sc.fit_transform(Xtr); Xte_s = sc.transform(Xte)

res, preds = {}, {}
def ev(name, yp):
    res[name] = {"MAE": float(mean_absolute_error(yte, yp)), "RMSE": float(np.sqrt(mean_squared_error(yte, yp))),
                 "R2": float(r2_score(yte, yp))}
    preds[name] = yp
lr = LinearRegression().fit(Xtr_s, ytr); ev("Linear Regression", lr.predict(Xte_s))
dt = DecisionTreeRegressor(max_depth=8, random_state=42).fit(Xtr, ytr); ev("Decision Tree", dt.predict(Xte))
rf = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1).fit(Xtr, ytr); ev("Random Forest", rf.predict(Xte))
gb = GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=3, random_state=42).fit(Xtr, ytr); ev("Gradient Boosting", gb.predict(Xte))
m["results"] = res
m["baseline_mae"] = float(mean_absolute_error(yte, np.full(len(yte), ytr.mean())))
best = max(res, key=lambda k: res[k]["R2"]); m["best_model"] = best

kf = KFold(5, shuffle=True, random_state=42)
cv_models = {
    "Linear Regression": make_pipeline(StandardScaler(), LinearRegression()),
    "Decision Tree": DecisionTreeRegressor(max_depth=8, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=3, random_state=42),
}
cv = {}
for n, mdl in cv_models.items():
    s = cross_val_score(mdl, X, y, cv=kf, scoring="r2"); cv[n] = {"mean": float(s.mean()), "std": float(s.std())}
m["cv"] = cv

names = list(res.keys())
cols = [SLATE, AMBER, INDIGO, TEAL]
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, (metric, title, fmt) in zip(axes, [("R2", "R² score (higher = better)", "{:.3f}"),
                                           ("RMSE", "RMSE in USD (lower = better)", "${:,.0f}"),
                                           ("MAE", "MAE in USD (lower = better)", "${:,.0f}")]):
    vals = [res[n][metric] for n in names]
    bars = ax.bar(["Linear\nReg.", "Decision\nTree", "Random\nForest", "Gradient\nBoosting"], vals, color=cols, width=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.01 if v > 0 else v, fmt.format(v), ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_title(title, fontsize=12)
    if metric != "R2": ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1000:,.0f}k"))
    else: ax.set_ylim(0, 1.05)
save(fig, "c11_model_comparison.png")

fig, ax = plt.subplots(figsize=(9, 5))
cvm = [cv[n]["mean"] for n in names]; cvs = [cv[n]["std"] for n in names]
ax.bar(names, cvm, yerr=cvs, color=cols, capsize=8, width=0.55, error_kw=dict(ecolor=NAVY, lw=1.5))
for i, v in enumerate(cvm): ax.text(i, v + 0.04, f"{v:.2f}", ha="center", fontweight="bold")
ax.set_ylim(0, 1.1); ax.set_ylabel("R² (average of 5 folds)")
ax.set_title("Cross-validation: the ranking holds on 5 different splits")
save(fig, "c12_cross_validation.png")

yp = preds[best]
fig, ax = plt.subplots(figsize=(7.5, 7))
ax.scatter(yte, yp, s=50, alpha=0.7, color=AMBER, edgecolor="white")
lims = [min(yte.min(), yp.min()) - 5000, max(yte.max(), yp.max()) + 5000]
ax.plot(lims, lims, "--", color=NAVY, lw=1.8, label="Perfect prediction")
ax.fill_between(lims, [l - 20000 for l in lims], [l + 20000 for l in lims], color=TEAL, alpha=0.12, label="±$20k zone")
ax.xaxis.set_major_formatter(plt.FuncFormatter(money)); ax.yaxis.set_major_formatter(plt.FuncFormatter(money))
ax.set_xlim(lims); ax.set_ylim(lims)
ax.set_xlabel("Actual salary"); ax.set_ylabel("Predicted salary"); ax.legend(frameon=False, loc="upper left")
ax.set_title(f"Predicted vs actual on 100 unseen jobs ({best})")
save(fig, "c13_pred_vs_actual.png")

resid = yte.values - yp
fig, ax = plt.subplots(figsize=(9, 5))
sns.histplot(resid, bins=25, kde=True, color=VIOLET, edgecolor="white", ax=ax)
ax.axvline(0, color=NAVY, ls="--", lw=1.8)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v/1000:,.0f}k"))
ax.set_title("Prediction errors are centred on zero"); ax.set_xlabel("Error = actual - predicted"); ax.set_ylabel("Count")
save(fig, "c14_residuals.png")
m["resid_within_20k"] = float(np.mean(np.abs(resid) < 20000))
m["resid_mean"] = float(resid.mean())

imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values()
m["importance_rf"] = imp.sort_values(ascending=False).to_dict()
m["importance_gb"] = pd.Series(gb.feature_importances_, index=X.columns).sort_values(ascending=False).to_dict()
def fcolor(f):
    if f.startswith("Remote"): return AMBER
    if f in ("Experience (Years)", "Skill Count", "Education"): return TEAL
    return INDIGO
fig, ax = plt.subplots(figsize=(9.5, 6))
ax.barh([f.replace("_", " ") for f in imp.index], imp.values, color=[fcolor(f) for f in imp.index])
for y_, v in enumerate(imp.values): ax.text(v + 0.004, y_, f"{v*100:.1f}%", va="center", fontsize=9)
ax.set_xlabel("Importance (share of the model's decisions)")
ax.set_title("Which inputs the Random Forest relies on most")
ax.legend(handles=[Patch(color=TEAL, label="Numbers (experience, skills, education)"),
                   Patch(color=INDIGO, label="Job / place / company details"),
                   Patch(color=AMBER, label="Remote work")], frameon=False, loc="lower right")
save(fig, "c15_feature_importance.png")

# ---------------------------------------------------------------- workflow diagram
fig, ax = plt.subplots(figsize=(14, 3.6)); ax.set_xlim(0, 14); ax.set_ylim(0, 4); ax.axis("off")
steps = [("1. Load data", "500 job rows\nfrom a CSV file", INDIGO), ("2. Explore", "charts & averages\nfind patterns", VIOLET),
         ("3. Prepare", "turn words into\nnumbers", TEAL), ("4. Split", "80% to learn\n20% to test", AMBER),
         ("5. Train", "4 models learn\nthe patterns", ROSE), ("6. Evaluate", "score with MAE,\nRMSE, R²", INDIGO),
         ("7. Predict", "estimate salary\nfor a new job", TEAL)]
for i, (t, d, c) in enumerate(steps):
    x = 0.1 + i * 2.0
    ax.add_patch(FancyBboxPatch((x, 1.0), 1.75, 2.2, boxstyle="round,pad=0.05,rounding_size=0.25", fc=c, ec="none"))
    ax.text(x + 0.875, 2.75, t, ha="center", va="center", color="white", fontsize=11.5, fontweight="bold")
    ax.text(x + 0.875, 1.8, d, ha="center", va="center", color="white", fontsize=9.5)
    if i < len(steps) - 1:
        ax.annotate("", xy=(x + 2.0, 2.1), xytext=(x + 1.8, 2.1), arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.5))
save(fig, "c16_workflow.png")

# ---------------------------------------------------------------- new profile example (same as notebook)
newp = {"Job Title": "Machine Learning Engineer", "Experience (Years)": 5.0, "Education": "Masters", "Skill Count": 12,
        "Industry": "Technology", "Company": "Google", "Location": "Bengaluru, India", "Remote Work": "Yes",
        "Certification": "AWS ML Specialty"}
def encode_profile(profile):
    nd = pd.DataFrame([profile]); nd["Education"] = nd["Education"].map({"Bachelors": 0, "Masters": 1, "PhD": 2})
    nd = pd.get_dummies(nd, columns=["Remote Work"], prefix="Remote")
    for col in label_cols:
        known = set(encoders[col].classes_)
        # same fallback as the notebook: unseen labels become the first known label (alphabetically)
        nd[col] = nd[col].apply(lambda v: v if v in known else encoders[col].classes_[0])
        nd[col] = encoders[col].transform(nd[col].astype(str))
    for col in X.columns:
        if col not in nd.columns: nd[col] = 0
    return nd[X.columns]
nd = encode_profile(newp)
m["example_profile"] = newp
m["example_pred_rf"] = float(rf.predict(nd)[0]); m["example_pred_gb"] = float(gb.predict(nd)[0])
# The notebook's location "Bengaluru, India" is not in the data (the data says "Bangalore, India"),
# so the notebook silently falls back to "Austin, USA". Corrected spelling for comparison:
fixed = dict(newp, **{"Location": "Bangalore, India"})
nd2 = encode_profile(fixed)
m["example_profile_fixed"] = fixed
m["example_pred_rf_fixed"] = float(rf.predict(nd2)[0]); m["example_pred_gb_fixed"] = float(gb.predict(nd2)[0])
m["example_fallback_location"] = encoders["Location"].classes_[0]

# ---------------------------------------------------------------- save metrics
m["n_missing_by_col"] = {k: int(v) for k, v in df.isnull().sum().items()}
m["edu_means"] = df.groupby("Education")[S].mean().to_dict()
m["remote_means"] = df.groupby("Remote Work")[S].mean().to_dict()
m["region_means"] = df.groupby("Region")[S].mean().to_dict()
m["region_counts"] = df["Region"].value_counts().to_dict()
m["title_means"] = df.groupby("Job Title")[S].mean().sort_values(ascending=False).to_dict()
m["loc_means"] = df.groupby("Location")[S].mean().sort_values(ascending=False).to_dict()
m["ind_means"] = df.groupby("Industry")[S].mean().sort_values(ascending=False).to_dict()
m["cert_means"] = df.groupby("Certification")[S].mean().sort_values(ascending=False).to_dict()
m["edu_counts"] = df["Education"].value_counts().to_dict()
m["title_counts"] = df["Job Title"].value_counts().to_dict()
m["ind_counts"] = df["Industry"].value_counts().to_dict()
m["loc_counts"] = df["Location"].value_counts().to_dict()
m["cert_counts"] = df["Certification"].value_counts(dropna=False).to_dict()
with open(os.path.join(OUT, "metrics.json"), "w") as f:
    json.dump(m, f, indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o))
print("Charts:", sorted(os.listdir(CH)))
print("Best:", best, res[best])
print("Example RF/GB:", m["example_pred_rf"], m["example_pred_gb"], "fixed:", m["example_pred_rf_fixed"], m["example_pred_gb_fixed"])
