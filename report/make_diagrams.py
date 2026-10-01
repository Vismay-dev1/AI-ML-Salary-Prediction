"""Workflow diagrams (vertical flow charts) used in the report."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams["font.family"] = ["DejaVu Serif"]
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

def flow(steps, name, bh=0.62, gap=0.34, w=4.6):
    n = len(steps)
    H = n * bh + (n - 1) * gap + 0.4
    fig = plt.figure(figsize=(w, H), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, H); ax.axis("off")
    y = H - 0.2
    for i, s in enumerate(steps):
        yb = y - bh
        ax.add_patch(FancyBboxPatch((0.35, yb), w - 0.7, bh, boxstyle="round,pad=0.0,rounding_size=0.06",
                                    fc="#eef2f7" if 0 < i < n - 1 else "#dfe7f1", ec="#1f3a5f", lw=1.1))
        ax.text(w / 2, yb + bh / 2, s, ha="center", va="center", fontsize=11, fontweight="bold", color="#10223a")
        if i < n - 1:
            ax.annotate("", xy=(w / 2, yb - gap + 0.02), xytext=(w / 2, yb - 0.02),
                        arrowprops=dict(arrowstyle="-|>", color="#1f3a5f", lw=1.3))
        y = yb - gap
    fig.savefig(os.path.join(A, name), dpi=220, facecolor="white"); plt.close(fig)

flow(["Dataset (CSV)", "Data Inspection", "Data Preprocessing", "Feature Engineering / Encoding", "Train-Test Split",
      "Feature Scaling", "Model Training", "Model Evaluation", "Model Comparison", "Salary Prediction"], "diagram_proposed.png")
flow(["Dataset", "Data Loading", "Data Inspection", "Exploratory Data Analysis", "Data Preprocessing", "Feature Encoding",
      "Train-Test Split", "Feature Scaling", "Model Training", "Model Evaluation", "Model Comparison", "Feature Importance",
      "New Salary Prediction"], "diagram_workflow.png", bh=0.5, gap=0.27)
