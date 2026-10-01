# -*- coding: utf-8 -*-
"""Shared setup for the report content. Every number comes from outputs.json (real execution of the
notebook) or is computed from ai_ml_job_analysis.csv at build time. Code is read from the notebook itself."""
import json, os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
A = os.path.join(HERE, "assets")
REC = json.load(open(os.path.join(A, "outputs.json")))
OUT = json.load(open(os.path.join(A, "out_images.json")))
F = REC["facts"]; ENV = REC["env"]
NB = json.load(open(os.path.join(REPO, "AI_ML_Salary_Prediction.ipynb")))
DF = pd.read_csv(os.path.join(REPO, "ai_ml_job_analysis.csv"))
RAW_CERT = pd.read_csv(os.path.join(REPO, "ai_ml_job_analysis.csv"), keep_default_na=False)["Certification"]
N_NONE = int((RAW_CERT == "None").sum())
N_NAN = int(DF["Certification"].isna().sum())

def code(i): return "".join(NB["cells"][i]["source"])
def img(n): return os.path.join(A, n)
def imgs(l): return [img(x) for x in (l if isinstance(l, list) else [l])]
def fig_of(cell): return img(REC["cells"][str(cell)]["figs"][0])

R = F["results"]
def m(model, k): return R[model][k]
usd = lambda v: f"${v:,.2f}"
usd0 = lambda v: f"${v:,.0f}"
GB, RF, DT, LR = "Gradient Boosting", "Random Forest", "Decision Tree", "Linear Regression"
IMP = F["importances"]; IMPK = list(IMP.keys())
sd = F["salary_describe"]
corr = F["corr"]

B = []   # the block list consumed by the renderers
def H1(t, new=True, center=False): B.append(("h1", t, new, center))
def H2(t, new=False): B.append(("h2", t, new))
def H3(t, new=False): B.append(("h3", t, new))
def P(t): B.append(("p", t))
def NOTE(t): B.append(("note", t))
def BUL(items): B.append(("bul", items))
def NUM(items): B.append(("num", items))
def CODE(t): B.append(("code", t))
def IMG(files, caption, width_cm=None): B.append(("img", imgs(files), caption, width_cm))
def TBL(head, rows, widths, aligns=None, caption=None, fs=12): B.append(("table", head, rows, widths, aligns, caption, fs))
def SP(pt=12): B.append(("sp", pt))
def LINE(t, bold=False, size=None, center=True, after=6): B.append(("line", t, bold, size, center, after))

def prog(title, code_blocks, outputs, explanation, new=True):
    """Standard program section: Program (code) -> Output (images) -> Explanation."""
    H2(title, new)
    H3("Program")
    for c in code_blocks: CODE(c)
    H3("Output")
    for o in outputs: IMG(o[0], o[1], o[2] if len(o) > 2 else None)
    H3("Explanation")
    for e in explanation:
        BUL(e) if isinstance(e, list) else P(e)

def sub(title, c, outs, expl, new=True):
    H3(title, new); H3("Program"); CODE(c); H3("Output")
    for o in outs: IMG(*o)
    H3("Explanation")
    for e in expl: P(e)
