import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import t, mannwhitneyu, ttest_ind, fisher_exact, norm

# ==========================================
# 1. CARREGAMENTO DIRETO DO XLSX DO REPOSITÓRIO
# ========================================== 
df = pd.read_excel("ConsentRecords_rows.xlsx")
df["created_at"] = pd.to_datetime(df["created_at"], utc=True, errors="coerce")
df = df.sort_values("created_at").reset_index(drop=True)

df["tempo_s"] = df["latency_milliseconds"].astype(float) / 1000.0
df["nota"] = df["quiz_score"].astype(float)
df["aceitou"] = df["has_accepted"].astype(bool)

df_A = df[df["experimental_group"] == "A"]
df_B = df[df["experimental_group"] == "B"]

tempo_A, tempo_B = df_A["tempo_s"].to_numpy(), df_B["tempo_s"].to_numpy()
notas_A, notas_B = df_A["nota"].to_numpy(), df_B["nota"].to_numpy()

print(f"Total lido: N={len(df)} (n_A={len(df_A)}, n_B={len(df_B)})")

# ==========================================
# 2. FUNÇÕES ESTATÍSTICAS
# ==========================================
def resumo(x):
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    n, m, dp = len(x), np.mean(x), np.std(x, ddof=1)
    ic = t.interval(0.95, df=n - 1, loc=m, scale=dp / np.sqrt(n))
    return n, m, dp, ic, med, q1, q3

def cohens_d(x, y):
    nx, ny = len(x), len(y)
    sp = np.sqrt(((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / (nx + ny - 2))
    return (np.mean(y) - np.mean(x)) / sp if sp > 0 else 0.0

def cliff_e_hl(x, y, n_boot=4000, seed=42):
    diffs = (y[:, None] - x[None, :]).ravel()
    delta = (np.sum(diffs > 0) - np.sum(diffs < 0)) / len(diffs)
    hl = np.median(diffs)
    rng = np.random.default_rng(seed)
    boots = [np.median((rng.choice(y, len(y), True)[:, None] - rng.choice(x, len(x), True)[None, :]).ravel())
             for _ in range(n_boot)]
    return delta, hl, np.percentile(boots, [2.5, 97.5])

def bloco(titulo, x, y):
    na, ma, dpa, ica, meda, q1a, q3a = resumo(x)
    nb, mb, dpb, icb, medb, q1b, q3b = resumo(y)
    u_a, p_mw = mannwhitneyu(x, y, alternative="two-sided")
    u_b = na * nb - u_a
    delta, hl, hl_ic = cliff_e_hl(x, y)
    tw, pw = ttest_ind(x, y, equal_var=False)
    d = cohens_d(x, y)
    print(f"\n--- {titulo} ---")
    print(f"A (n={na}): media={ma:.2f}±{dpa:.2f} IC[{ica[0]:.2f}; {ica[1]:.2f}] | med={meda:.2f} ({q1a:.2f}-{q3a:.2f})")
    print(f"B (n={nb}): media={mb:.2f}±{dpb:.2f} IC[{icb[0]:.2f}; {icb[1]:.2f}] | med={medb:.2f} ({q1b:.2f}-{q3b:.2f})")
    print(f"MW: U_A={u_a:.1f}, U_B={u_b:.1f}, p={p_mw:.4f} | HL(B-A)={hl:.2f} IC[{hl_ic[0]:.2f}; {hl_ic[1]:.2f}] | Cliff={delta:.3f}")
    print(f"Welch: t={tw:.3f}, p={pw:.4f}, d={d:.3f}")
    if np.all(x > 0) and np.all(y > 0):
        tl, pl = ttest_ind(np.log10(x), np.log10(y), equal_var=False)
        print(f"Welch log10: t={tl:.3f}, p={pl:.4f}")

def wilson_ci(k, n, alpha=0.05):
    z = norm.ppf(1 - alpha / 2)
    p = k / n
    den = 1 + z**2 / n
    c = (p + z**2 / (2 * n)) / den
    h = z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n) / den
    return max(0.0, c - h), min(1.0, c + h)

def newcombe_ci(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson_ci(k1, n1)
    l2, u2 = wilson_ci(k2, n2)
    diff = p2 - p1
    return diff, diff - np.sqrt((p2 - l2)**2 + (u1 - p1)**2), diff + np.sqrt((u2 - p2)**2 + (p1 - l1)**2)

def tost_welch(x, y, margin=0.70):
    nx, ny = len(x), len(y)
    vx, vy = np.var(x, ddof=1), np.var(y, ddof=1)
    se = np.sqrt(vx / nx + vy / ny)
    df_w = (vx / nx + vy / ny)**2 / ((vx / nx)**2 / (nx - 1) + (vy / ny)**2 / (ny - 1))
    diff = np.mean(y) - np.mean(x)
    p_low = t.sf((diff + margin) / se, df=df_w)
    p_high = t.cdf((diff - margin) / se, df=df_w)
    return max(p_low, p_high), p_low, p_high, diff, df_w

# ==========================================
# 3. SAÍDAS PARA TABELAS 4.1 E 4.2
# ==========================================
bloco("TEMPO - Amostra integral (N=81)", tempo_A, tempo_B)

# Regra simétrica > 300 s (5 min)
mA_300, mB_300 = tempo_A <= 300.0, tempo_B <= 300.0
print(f"\nRemovidos (>300 s): A={np.sum(~mA_300)}, B={np.sum(~mB_300)}")
bloco("TEMPO - Critério simétrico (<= 300 s)", tempo_A[mA_300], tempo_B[mB_300])

# Sem outlier 670 s
bloco("TEMPO - Sem outlier de 670 s no Grupo B", tempo_A, tempo_B[tempo_B < 600.0])

# Período randomizado (antes de 2026-08-25 21:16 ou primeiros 49 registros ordenados)
df_rand = df.iloc[:49]
bloco("TEMPO - Período inicial randomizado (n=49)",
      df_rand[df_rand["experimental_group"] == "A"]["tempo_s"].to_numpy(),
      df_rand[df_rand["experimental_group"] == "B"]["tempo_s"].to_numpy())

# Leitores ativos (>= 3 s)
a_at, b_at = tempo_A >= 3.0, tempo_B >= 3.0
bloco("TEMPO - Leitores ativos (>= 3 s)", tempo_A[a_at], tempo_B[b_at])
bloco("TEMPO - Leitores ativos (>= 3 s, sem >300 s)",
      tempo_A[a_at & mA_300], tempo_B[b_at & mB_300])

bloco("NOTAS - Amostra integral (N=81)", notas_A, notas_B)
p_tost, pl, ph, dn, dfw = tost_welch(notas_A, notas_B, 0.70)
print(f"TOST (±0,70 pt, gl={dfw:.1f}): p_TOST={p_tost:.4f} (dif={dn:.2f})")

print(f"\nNOTAS cliques rápidos (< 3 s): A={np.mean(notas_A[~a_at]):.2f} (n={np.sum(~a_at)}) vs B={np.mean(notas_B[~b_at]):.2f} (n={np.sum(~b_at)})")
bloco("NOTAS - Leitores ativos (>= 3 s)", notas_A[a_at], notas_B[b_at])
bloco("ACERTOS/MIN - Leitores ativos (>= 3 s)",
      notas_A[a_at] / (tempo_A[a_at] / 60.0),
      notas_B[b_at] / (tempo_B[b_at] / 60.0))

# Proporções (E1)
kA, nA = int(df_A["aceitou"].sum()), len(df_A)
kB, nB = int(df_B["aceitou"].sum()), len(df_B)
wA, wB = wilson_ci(kA, nA), wilson_ci(kB, nB)
dp_p, nc_l, nc_u = newcombe_ci(kA, nA, kB, nB)
_, p_f = fisher_exact([[kA, nA - kA], [kB, nB - kB]], alternative="two-sided")
print(f"\n--- CONFIRMAÇÃO (E1) ---")
print(f"A: {kA}/{nA} ({kA/nA*100:.2f}%), Wilson [{wA[0]*100:.1f}%; {wA[1]*100:.1f}%]")
print(f"B: {kB}/{nB} ({kB/nB*100:.2f}%), Wilson [{wB[0]*100:.1f}%; {wB[1]*100:.1f}%]")
print(f"Dif (B-A): {dp_p*100:+.2f} p.p., Newcombe [{nc_l*100:+.1f}; {nc_u*100:+.1f}] p.p., Fisher p={p_f:.3f}")

# ==========================================
# 4. LISTAR FEEDBACKS REAIS PARA A TABELA 4.3
# ==========================================
fb = df[df["feedback"].notna() & (df["feedback"].astype(str).str.strip() != "")]
print(f"\n--- FEEDBACKS NÃO VAZIOS: total={len(fb)} "
      f"(A={sum(fb['experimental_group']=='A')}, B={sum(fb['experimental_group']=='B')}) ---")
for grp in ["A", "B"]:
    print(f"\n[Grupo {grp}]")
    for idx, txt in enumerate(fb[fb["experimental_group"] == grp]["feedback"], 1):
        print(f"  {idx}. {str(txt).strip()}")



# ==========================================
# 5. GERAÇÃO DOS GRÁFICOS EM PDF VETORIAL
# ==========================================
cores = ["#0072F0", "#F02020"]
grupos = ["Grupo A (Texto)", "Grupo B (Visual)"]

# Variáveis derivadas da seção 3 (Proporções E1)
aceites = np.array([kA, kB], dtype=int)
totais = np.array([nA, nB], dtype=int)
props = aceites / totais

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# --- Figura 4.1: Distribuição de frequências das notas (0 a 7) ---
fig, ax = plt.subplots(figsize=(7.2, 4.4))
pontuacoes = np.arange(0, 8)
cont_A = np.array([np.sum(notas_A == s) for s in pontuacoes])
cont_B = np.array([np.sum(notas_B == s) for s in pontuacoes])
largura = 0.38

b1 = ax.bar(pontuacoes - largura / 2, cont_A, width=largura, color=cores[0],
            edgecolor="black", linewidth=0.6, label="Grupo A (Texto)")
b2 = ax.bar(pontuacoes + largura / 2, cont_B, width=largura, color=cores[1],
            edgecolor="black", linewidth=0.6, label="Grupo B (Visual)")

for barras in (b1, b2):
    for barra in barras:
        h = barra.get_height()
        if h > 0:
            ax.text(barra.get_x() + barra.get_width() / 2, h + 0.25, f"{int(h)}",
                    ha="center", va="bottom", fontsize=8.5)

ax.set_xticks(pontuacoes)
ax.set_ylim(0, max(np.max(cont_A), np.max(cont_B)) + 2.2)
ax.set_xlabel("Pontuação no Questionário (escala de 0 a 7)")
ax.set_ylabel("Número de Participantes")
ax.set_title("Distribuição de Pontuações no Questionário por Grupo")
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig("grafico_distribuicao_notas.pdf", bbox_inches="tight")
plt.show()
plt.close(fig)

# --- Figura 4.2: Proporção de confirmação com IC 95% de Wilson ---
fig, ax = plt.subplots(figsize=(6.8, 4.4))
taxas = props * 100.0
wilson_bounds = np.array([wA, wB]) * 100.0
yerr_wilson = np.vstack([
    np.maximum(0.0, taxas - wilson_bounds[:, 0]),
    np.maximum(0.0, wilson_bounds[:, 1] - taxas),
])

x = np.arange(len(grupos))
barras = ax.bar(x, taxas, width=0.48, color=cores, edgecolor="black", linewidth=0.7)
ax.errorbar(x, taxas, yerr=yerr_wilson, fmt="none", ecolor="black",
            elinewidth=1.4, capsize=6, capthick=1.4)

for i, (barra, taxa, sup) in enumerate(zip(barras, taxas, wilson_bounds[:, 1])):
    taxa_fmt = f"{taxa:.2f}%".replace(".", ",")
    ax.text(barra.get_x() + barra.get_width() / 2, sup + 1.5,
            f"{taxa_fmt}\n({aceites[i]}/{totais[i]})",
            ha="center", va="bottom", fontsize=9.5)

ax.set_xticks(x)
ax.set_xticklabels(grupos)
ax.set_ylim(0, 118)
ax.set_yticks(np.arange(0, 101, 20))
ax.set_ylabel("Confirmação no Botão Final (%)")
ax.set_title("Proporção de Confirmação por Grupo (IC 95% de Wilson)")
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)

diff_fmt = f"{dp_p*100:+.2f}".replace(".", ",")
nc_l_fmt = f"{nc_l*100:+.1f}".replace(".", ",")
nc_u_fmt = f"{nc_u*100:+.1f}".replace(".", ",")
nota_rodape = (
    f"Diferença (B − A): {diff_fmt} p.p. "
    f"(IC 95% Newcombe: {nc_l_fmt} a {nc_u_fmt} p.p.)"
)
fig.text(0.5, 0.01, nota_rodape, ha="center", va="bottom", fontsize=8.8)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig("grafico_taxa_aceite.pdf", bbox_inches="tight")
plt.show()
plt.close(fig)

# --- Figura 4.3: Distribuição do tempo de permanência (escala logarítmica) ---
fig, ax = plt.subplots(figsize=(6.8, 4.5))
bp = ax.boxplot(
    [tempo_A, tempo_B],
    patch_artist=True,
    widths=0.42,
    showmeans=True,
    medianprops={"color": "black", "linewidth": 2.0},
    meanprops={"marker": "D", "markerfacecolor": "black",
               "markeredgecolor": "black", "markersize": 5},
    flierprops={"marker": "o", "markerfacecolor": "white",
                "markeredgecolor": "#444444", "markersize": 4.5, "alpha": 0.85},
    whiskerprops={"color": "black", "linewidth": 1.2},
    capprops={"color": "black", "linewidth": 1.2},
    boxprops={"edgecolor": "black", "linewidth": 1.2},
)
for caixa, cor in zip(bp["boxes"], cores):
    caixa.set_facecolor(cor)
    caixa.set_alpha(0.85)

ax.set_xticks([1, 2])
ax.set_xticklabels(grupos)
ax.set_yscale("log")
ax.set_ylabel("Tempo de Permanência na Página (segundos, escala log)")
ax.set_title("Distribuição do Tempo de Permanência por Grupo")
ax.grid(axis="y", linestyle="--", color="gray", alpha=0.35, which="both")
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig("grafico_tempo_permanencia.pdf", bbox_inches="tight")
plt.show()
plt.close(fig)
