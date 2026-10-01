"""
Executes the code cells of AI_ML_Salary_Prediction.ipynb *unmodified* against
ai_ml_job_analysis.csv and records the real outputs (stdout, last-expression
values and every figure shown with plt.show()).

A few clearly-labelled SUPPLEMENTARY snippets (not part of the notebook) are run
after some cells only to display state that the notebook itself does not print.
"""
import ast, io, json, os, sys, contextlib, pickle, platform
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS = os.path.join(REPO, "report", "assets")
os.makedirs(ASSETS, exist_ok=True)
os.chdir(REPO)

nb = json.load(open("AI_ML_Salary_Prediction.ipynb"))
cells = [("".join(c["source"])) for c in nb["cells"] if c["cell_type"] == "code"]
code_idx = [i for i, c in enumerate(nb["cells"]) if c["cell_type"] == "code"]

# Supplementary snippets: keyed by notebook cell index, executed AFTER that cell.
SUPP = {
 17: '''print("Mean of scaled training features (rounded):", X_train_scaled.mean(axis=0).round(2))
print("Std  of scaled training features (rounded):", X_train_scaled.std(axis=0).round(2))''',
 19: '''print("Decision Tree  -> max_depth param:", dt.max_depth, "| fitted tree depth:", dt.get_depth(), "| leaves:", dt.get_n_leaves())
print("Random Forest  -> n_estimators:", rf.n_estimators, "| max_depth param:", rf.max_depth, "| trees fitted:", len(rf.estimators_))
print("Gradient Boost -> n_estimators:", gb.n_estimators, "| learning_rate:", gb.learning_rate, "| max_depth:", gb.max_depth, "| stages fitted:", gb.n_estimators_)''',
 13: '''print("Education mapping used:", education_order)''',
 16: '''print("Train share: %.0f%%  |  Test share: %.0f%%" % (100*len(X_train)/len(X), 100*len(X_test)/len(X)))''',
 29: '''print("Encoded new profile row sent to rf.predict():")
print(new_df.T.to_string(header=False))
print()
print("Company 'Google' in training classes?        ", 'Google' in set(encoders['Company'].classes_))
print("Location 'Bengaluru, India' in training classes?", 'Bengaluru, India' in set(encoders['Location'].classes_))
print("Fallback class used for unseen values (classes_[0]):", encoders['Location'].classes_[0])''',
}
# supplementary snippet for cell 29 needs the *original* profile; run it AFTER the cell (state is intact)

ns = {"__name__": "__main__"}
rec = {"env": {"python": platform.python_version()}, "cells": {}}
fig_counter = {"n": 0}
cur = {"figs": []}

def fake_show(*a, **k):
    fig = plt.gcf()
    fig_counter["n"] += 1
    p = os.path.join(ASSETS, f"fig_cell{cur['cell']:02d}_{len(cur['figs'])+1}.png")
    fig.savefig(p, dpi=170, bbox_inches="tight", facecolor="white")
    cur["figs"].append(os.path.basename(p))
    plt.close(fig)
plt.show = fake_show

def run(src, store, name):
    tree = ast.parse(src)
    last = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = ast.Expression(tree.body.pop().value)
    buf = io.StringIO()
    value = None
    import warnings
    with contextlib.redirect_stdout(buf), warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        exec(compile(tree, "<cell>", "exec"), ns)
        if last is not None:
            value = eval(compile(last, "<cell>", "eval"), ns)
    store["stdout"] = buf.getvalue()
    store["warnings"] = [f"{x.category.__name__}: {x.message}" for x in w]
    if value is not None:
        pickle.dump(value, open(os.path.join(ASSETS, f"{name}_value.pkl"), "wb"))
        store["value_type"] = type(value).__name__
        store["value_repr"] = repr(value)

import pandas, numpy, sklearn, seaborn
rec["env"].update(pandas=pandas.__version__, numpy=numpy.__version__, sklearn=sklearn.__version__,
                  matplotlib=matplotlib.__version__, seaborn=seaborn.__version__)

for ci, src in zip(code_idx, cells):
    cur["cell"] = ci; cur["figs"] = []
    store = {}
    run(src, store, f"cell{ci:02d}")
    store["figs"] = list(cur["figs"])
    rec["cells"][str(ci)] = store
    if ci in SUPP:
        cur["figs"] = []
        s2 = {}
        run(SUPP[ci], s2, f"supp{ci:02d}")
        rec["cells"][f"supp{ci}"] = s2
    print("cell", ci, "ok", store["figs"], store["warnings"][:1])

# extra raw values useful for the report text (read straight from the live namespace)
df, data, X, y = ns["df"], ns["data"], ns["X"], ns["y"]
rec["facts"] = {
  "salary_describe": df["Salary (USD)"].describe().round(2).to_dict(),
  "corr": ns["numeric_df"].corr().round(4).to_dict(),
  "results": ns["results_df"].round(6).to_dict(orient="index"),
  "best_model": ns["best_model_name"],
  "importances": ns["importances"].round(6).to_dict(),
  "predicted_salary": float(ns["predicted_salary"]),
  "resid_mean": float(ns["residuals"].mean()), "resid_std": float(ns["residuals"].std()),
  "resid_min": float(ns["residuals"].min()), "resid_max": float(ns["residuals"].max()),
  "cert_none_raw": int((pandas.read_csv("ai_ml_job_analysis.csv", keep_default_na=False)["Certification"]=="None").sum()),
  "n_unique": {c:int(df[c].nunique()) for c in df.columns},
  "best_pred_min": float(ns["best_preds"].min()), "best_pred_neg": int((ns["best_preds"]<0).sum()),
  "abs_resid_gt_20k": int((abs(ns["residuals"])>20000).sum()), "n_test": int(len(ns["residuals"])),
  "y_test_mean": float(ns["y_test"].mean()),
}
for name in ["lr","dt","rf","gb"]:
    pass
json.dump(rec, open(os.path.join(ASSETS, "outputs.json"), "w"), indent=1, default=str)
print("saved")
