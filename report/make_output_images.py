"""Renders the REAL outputs captured by run_notebook.py (outputs.json / *.pkl) as clean
notebook-style output images. Nothing is typed in by hand: every string comes from the run."""
import json, os, pickle, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
rec = json.load(open(os.path.join(A, "outputs.json")))
plt.rcParams["font.family"] = ["DejaVu Sans Mono", "DejaVu Sans"]
DPI = 200
MAXW = 7.4  # inches before the table is split into column groups

def text_image(text, name, fs=11):
    lines = []
    for l in text.rstrip("\n").split("\n"):
        if len(l) > 80:
            ind = len(l) - len(l.lstrip())
            lines += textwrap.wrap(l, 80, subsequent_indent=" " * (ind + 2), break_long_words=False, replace_whitespace=False, drop_whitespace=False) or [l]
        else: lines.append(l)
    # strip leading blank line (Jupyter prints none)
    while lines and lines[0] == "": lines.pop(0)
    cw = 0.602 * fs / 72
    lh = fs * 1.45 / 72
    pad = 0.16
    w = max(len(l) for l in lines) * cw * 1.05 + 2 * pad
    h = len(lines) * lh + 2 * pad
    fig = plt.figure(figsize=(w, h), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    ax.add_patch(Rectangle((0.01, 0.01), w - 0.02, h - 0.02, fill=True, fc="white", ec="#9e9e9e", lw=0.9))
    for i, l in enumerate(lines):
        if "\u2705" in l:   # emoji glyph is not in the available fonts: draw it as a green check badge
            pre, post = l.split("\u2705", 1)
            ax.text(pad, h - pad - i * lh, pre + "  " + post, va="top", ha="left", fontsize=fs, color="#212121")
            bx = pad + len(pre) * cw; by = h - pad - i * lh - lh * 0.88; s = lh * 0.8
            ax.add_patch(Rectangle((bx, by), s, s, fc="#4caf50", ec="none"))
            ax.plot([bx + .2*s, bx + .42*s, bx + .8*s], [by + .5*s, by + .27*s, by + .75*s], color="white", lw=1.6)
        else:
            ax.text(pad, h - pad - i * lh, l, va="top", ha="left", fontsize=fs, color="#212121")
    fig.savefig(os.path.join(A, name), dpi=DPI, facecolor="white"); plt.close(fig)
    return name

def col_strings(s):
    if pd.api.types.is_float_dtype(s):
        return [x.strip() for x in s.to_string(index=False, header=False).split("\n")]
    return [("NaN" if (isinstance(x, float) and pd.isna(x)) else str(x)) for x in s]

def df_images(df, name, fs=10, groups=None):
    idx = [str(i) for i in df.index]
    cols = {c: col_strings(df[c]) for c in df.columns}
    cw = 0.602 * fs / 72
    def wrap_header(h): return textwrap.wrap(str(h), 13) or [""]
    widths = {c: max([len(x) for x in cols[c]] + [max(len(p) for p in wrap_header(c))]) for c in df.columns}
    iw = max(len(i) for i in idx)
    if groups is None:
        groups, cur, curw = [], [], iw
        for c in df.columns:
            need = widths[c] + 3
            if cur and (curw + need) * cw + 0.4 > MAXW:
                groups.append(cur); cur, curw = [], iw
            cur.append(c); curw += need
        if cur: groups.append(cur)
    names = []
    for gi, g in enumerate(groups):
        hl = max(len(wrap_header(c)) for c in g)
        rh = fs * 1.9 / 72
        hh = hl * fs * 1.35 / 72 + 0.12
        w = ((iw + 2) + sum(widths[c] + 3 for c in g)) * cw + 0.2
        h = hh + len(idx) * rh + 0.1
        fig = plt.figure(figsize=(w, h), dpi=DPI)
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
        ax.add_patch(Rectangle((0.01, 0.01), w - 0.02, h - 0.02, fc="white", ec="#9e9e9e", lw=0.9))
        # header
        ax.plot([0.1, w - 0.1], [h - hh, h - hh], color="#444", lw=0.9)
        x = 0.1 + (iw + 2) * cw
        xs = {}
        for c in g:
            x += (widths[c] + 3) * cw; xs[c] = x - 1.5 * cw   # right edge for right-aligned text
        for c in g:
            for k, part in enumerate(wrap_header(c)):
                ax.text(xs[c], h - 0.07 - k * fs * 1.35 / 72, part, ha="right", va="top", fontsize=fs, fontweight="bold")
        for r in range(len(idx)):
            y0 = h - hh - (r + 1) * rh
            if r % 2 == 1:
                ax.add_patch(Rectangle((0.03, y0), w - 0.06, rh, fc="#f3f3f3", ec="none", zorder=0))
            ty = y0 + rh / 2
            ax.text(0.1, ty, idx[r], ha="left", va="center", fontsize=fs, fontweight="bold")
            for c in g:
                ax.text(xs[c], ty, cols[c][r], ha="right", va="center", fontsize=fs)
        fn = f"{name}_{gi+1}.png"
        fig.savefig(os.path.join(A, fn), dpi=DPI, facecolor="white"); plt.close(fig)
        names.append(fn)
    return names

def val(cell): return pickle.load(open(os.path.join(A, f"cell{cell:02d}_value.pkl"), "rb"))
def so(cell): return rec["cells"][str(cell)]["stdout"]

out = {}
out["p1"] = text_image(so(2), "out_p1.png")
out["p2"] = df_images(val(3), "out_p2")
out["p3"] = text_image(so(5), "out_p3.png")
out["p4"] = text_image(rec["cells"]["7"]["value_repr"], "out_p4.png")
out["p5_desc"] = df_images(val(6), "out_p5_desc")
out["p6"] = df_images(val(13), "out_p6")
out["p6_map"] = text_image(rec["cells"]["supp13"]["stdout"], "out_p6_map.png")
out["p7"] = text_image(so(14), "out_p7.png")
out["p8"] = text_image(so(16) + rec["cells"]["supp16"]["stdout"], "out_p8.png")
out["p9"] = text_image(rec["cells"]["supp17"]["stdout"], "out_p9.png")
out["p10"] = text_image(rec["cells"]["supp19"]["stdout"], "out_p10.png")
out["p11"] = text_image(so(19), "out_p11.png")
out["p12"] = df_images(val(21), "out_p12")
out["p13"] = text_image(so(24), "out_p13.png")
imp = val(27)
out["p15"] = text_image(imp.to_string() + "\ndtype: float64", "out_p15.png")
out["p16"] = text_image(so(29), "out_p16.png")
out["p16_supp"] = text_image(rec["cells"]["supp29"]["stdout"], "out_p16_supp.png")
json.dump(out, open(os.path.join(A, "out_images.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
