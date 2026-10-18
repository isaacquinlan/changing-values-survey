import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV exported from the survey spreadsheet.
# Required columns are the six percentage columns used below.
df = pd.read_csv("responses.csv")

def ternary_xy(a, b, c):
    total = a + b + c
    a, b, c = a / total, b / total, c / total
    return b + 0.5 * a, (np.sqrt(3) / 2) * a

def plot_ternary(df, columns, title, output_file):
    a_col, b_col, c_col = columns
    fig, ax = plt.subplots(figsize=(9, 8))
    A = np.array([0.5, np.sqrt(3)/2])  # Human Wellbeing
    B = np.array([0.0, 0.0])           # Individual Freedom
    C = np.array([1.0, 0.0])           # Equality / Fairness

    tri = np.array([A, B, C, A])
    ax.plot(tri[:,0], tri[:,1], linewidth=2)

    for t in [0.2, 0.4, 0.6, 0.8]:
        p1, p2 = A*t+B*(1-t), A*t+C*(1-t)
        ax.plot([p1[0],p2[0]],[p1[1],p2[1]],"--",linewidth=0.7,alpha=0.5)
        p1, p2 = B*t+A*(1-t), B*t+C*(1-t)
        ax.plot([p1[0],p2[0]],[p1[1],p2[1]],"--",linewidth=0.7,alpha=0.5)
        p1, p2 = C*t+A*(1-t), C*t+B*(1-t)
        ax.plot([p1[0],p2[0]],[p1[1],p2[1]],"--",linewidth=0.7,alpha=0.5)

    xy = np.array([ternary_xy(r[a_col],r[b_col],r[c_col])
                   for _, r in df.iterrows()])
    ax.scatter(xy[:,0],xy[:,1],s=42,alpha=0.78,
               edgecolors="black",linewidths=0.45)
    ax.text(A[0],A[1]+0.055,"Human Wellbeing",ha="center",
            va="bottom",fontsize=12,fontweight="bold")
    ax.text(B[0]-0.03,B[1]-0.045,"Individual Freedom",ha="left",
            va="top",fontsize=12,fontweight="bold")
    ax.text(C[0]+0.03,C[1]-0.045,"Equality / Fairness",ha="right",
            va="top",fontsize=12,fontweight="bold")
    ax.set_title(title,fontsize=16,pad=26)
    ax.set_aspect("equal")
    ax.set_xlim(-0.17,1.17)
    ax.set_ylim(-0.13,1.03)
    ax.axis("off")
    fig.text(0.5,0.02,f"Each dot represents one row (n={len(df)}).",
             ha="center",fontsize=10)
    fig.tight_layout(rect=[0,0.05,1,0.98])
    fig.savefig(output_file,dpi=220,bbox_inches="tight")
    plt.close(fig)

plot_ternary(df,
    ["today_human_wellbeing_pct","today_individual_freedom_pct","today_equality_fairness_pct"],
    "Aggregated Ternary Plot — Society Today (2026)",
    "aggregated_ternary_today_2026.png")

plot_ternary(df,
    ["2060_human_wellbeing_pct","2060_individual_freedom_pct","2060_equality_fairness_pct"],
    "Aggregated Ternary Plot — Society in 2060",
    "aggregated_ternary_future_2060.png")
