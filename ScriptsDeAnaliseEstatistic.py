import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import (
    t,
    mannwhitneyu,
    ttest_ind,
    fisher_exact,
    norm,
)

# ==========================================
# 1. DADOS (N = 81: n_A = 40, n_B = 41)
# ==========================================

# Tempos de permanência convertidos de milissegundos para segundos
tempo_A = np.array([
    153314, 178655, 2411, 2113, 35584, 34914, 2425, 224698, 2289, 26085,
    126324, 1775, 1986, 1732, 169228, 355873, 51026, 200557, 297906, 2722,
    2099, 2501, 26390, 265514, 251314, 2742, 128301, 2796, 177656, 262811,
    131173, 213582, 2328, 129699, 108174, 20933, 55873, 98756, 15284, 69599
], dtype=float) / 1000.0

tempo_B = np.array([
    2922, 14683, 18771, 3190, 670257, 1785, 78843, 81845, 9568, 2245,
    59066, 2864, 103981, 3547, 50427, 4565, 2059, 64681, 88688, 22191,
    87259, 122149, 11432, 65066, 98377, 117025, 1734, 6226, 10722, 1300,
    97472, 13514, 2628, 224497, 11068, 45328, 1621, 9012, 2548, 24405,
    149257
], dtype=float) / 1000.0

notas_A = np.array([
    6, 6, 1, 5, 2, 5, 7, 6, 1, 5, 6, 5, 2, 0, 7, 7, 5, 7, 7, 2,
    3, 1, 7, 7, 5, 2, 7, 2, 6, 6, 7, 7, 1, 7, 7, 6, 4, 7, 0, 4
], dtype=float)

notas_B = np.array([
    6, 6, 3, 7, 6, 3, 7, 7, 5, 3, 6, 2, 5, 6, 7, 6, 2, 4, 6, 5,
    7, 7, 4, 6, 6, 7, 1, 3, 6, 3, 7, 6, 4, 7, 5, 7, 2, 5, 3, 7, 7
], dtype=float)

aceites = np.array([34, 32], dtype=int)
totais = np.array([len(tempo_A), len(tempo_B)], dtype=int)

# ==========================================
# 2. FUNÇÕES ESTATÍSTICAS AUXILIARES
# ==========================================

def resumo_numerico(x):
    q1, med, q3 = np.percentile(x, [25, 50, 75])
    iqr = q3 - q1
    n = len(x)
    media = np.mean(x)
    dp = np.std(x, ddof=1)
    ep = dp / np.sqrt(n)
    ic_low, ic_high = t.interval(0.95, df=n - 1, loc=media, scale=ep)
    return {
        "n": n,
        "media": media,
        "dp": dp,
        "ic95": (ic_low, ic_high),
        "mediana": med,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
    }

def cohens_d_welch(x, y):
    nx, ny = len(x), len(y)
    vx, vy = np.var(x, ddof=1), np.var(y, ddof=1)
    s_pooled = np.sqrt(((nx - 1) * vx + (ny - 1) * vy) / (nx + ny - 2))
    return (np.mean(y) - np.mean(x)) / s_pooled if s_pooled > 0 else 0.0

def cliff_delta_e_rank_biserial(x, y):
    # Positivo indica valores maiores em y (Grupo B) do que em x (Grupo A)
    nx, ny = len(x), len(y)
    diffs = y[:, None] - x[None, :]
    gt = np.sum(diffs > 0)
    lt = np.sum(diffs < 0)
    delta = (gt - lt) / (nx * ny)
    # Correlação rank-biserial a partir de U de y sobre x
    u_y = mannwhitneyu(y, x, alternative="two-sided").statistic
    r_rb = 1.0 - (2.0 * u_y) / (nx * ny)
    return delta, r_rb

def hodges_lehmann_diff(x, y, n_boot=5000, seed=42):
    # Diferença de localização (mediana de y_j - x_i) + IC 95% bootstrap
    pairwise_diffs = (y[:, None] - x[None, :]).ravel()
    hl = np.median(pairwise_diffs)
    rng = np.random.default_rng(seed)
    boot_vals = np.empty(n_boot)
    for b in range(n_boot):
        bx = rng.choice(x, size=len(x), replace=True)
        by = rng.choice(y, size=len(y), replace=True)
        boot_vals[b] = np.median((by[:, None] - bx[None, :]).ravel())
    ci_low, ci_high = np.percentile(boot_vals, [2.5, 97.5])
    return hl, (ci_low, ci_high)

def comparar_continuas(x, y, nome_x="Grupo A", nome_y="Grupo B"):
    rx, ry = resumo_numerico(x), resumo_numerico(y)
    u_stat, p_mw = mannwhitneyu(x, y, alternative="two-sided")
    u_y = mannwhitneyu(y, x, alternative="two-sided").statistic
    delta, r_rb = cliff_delta_e_rank_biserial(x, y)
    hl, hl_ic = hodges_lehmann_diff(x, y)
    t_welch, p_welch = ttest_ind(x, y, equal_var=False)
    d_cohen = cohens_d_welch(x, y)

    # Welch em log10 (apenas para tempos estritamente positivos)
    if np.all(x > 0) and np.all(y > 0):
        lx, ly = np.log10(x), np.log10(y)
        t_log, p_log = ttest_ind(lx, ly, equal_var=False)
        d_log = cohens_d_welch(lx, ly)
    else:
        t_log, p_log, d_log = np.nan, np.nan, np.nan

    return {
        "rx": rx, "ry": ry,
        "u_x": u_stat, "u_y": u_y, "p_mw": p_mw,
        "delta": delta, "r_rb": r_rb,
        "hl": hl, "hl_ic": hl_ic,
        "t_welch": t_welch, "p_welch": p_welch, "d_cohen": d_cohen,
        "t_log": t_log, "p_log": p_log, "d_log": d_log,
    }

def wilson_ci(k, n, alpha=0.05):
    z = norm.ppf(1.0 - alpha / 2.0)
    p = k / n
    denom = 1.0 + z**2 / n
    center = (p + z**2 / (2.0 * n)) / denom
    half = (z * np.sqrt((p * (1.0 - p) + z**2 / (4.0 * n)) / n)) / denom
    return max(0.0, center - half), min(1.0, center + half)

def newcombe_diff_ci(k1, n1, k2, n2, alpha=0.05):
    # Diferença p2 - p1 com IC de Newcombe (método 10 / sem continuidade)
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson_ci(k1, n1, alpha)
    l2, u2 = wilson_ci(k2, n2, alpha)
    diff = p2 - p1
    low = diff - np.sqrt((p2 - l2)**2 + (u1 - p1)**2)
    high = diff + np.sqrt((u2 - p2)**2 + (p1 - l1)**2)
    return diff, max(-1.0, low), min(1.0, high)

def tost_welch(x, y, margin=0.70, alpha=0.05):
    # Testa equivalência: H0_1: (mean_y - mean_x) <= -margin; H0_2: (mean_y - mean_x) >= +margin
    nx, ny = len(x), len(y)
    vx, vy = np.var(x, ddof=1), np.var(y, ddof=1)
    se = np.sqrt(vx / nx + vy / ny)
    df = (vx / nx + vy / ny)**2 / ((vx / nx)**2 / (nx - 1) + (vy / ny)**2 / (ny - 1))
    diff = np.mean(y) - np.mean(x)
    t_lower = (diff - (-margin)) / se
    p_lower = t.sf(t_lower, df=df)
    t_upper = (diff - margin) / se
    p_upper = t.cdf(t_upper, df=df)
    p_tost = max(p_lower, p_upper)
    return p_tost, p_lower, p_upper, diff, df

def imprimir_bloco_continuo(titulo, res):
    rx, ry = res["rx"], res["ry"]
    print(f"\n--- {titulo} ---")
    print(f"Grupo A (n={rx['n']}): média={rx['media']:.2f} ± {rx['dp']:.2f} "
          f"[IC95%: {rx['ic95'][0]:.2f}; {rx['ic95'][1]:.2f}], "
          f"mediana={rx['mediana']:.2f} (Q1-Q3: {rx['q1']:.2f}-{rx['q3']:.2f})")
    print(f"Grupo B (n={ry['n']}): média={ry['media']:.2f} ± {ry['dp']:.2f} "
          f"[IC95%: {ry['ic95'][0]:.2f}; {ry['ic95'][1]:.2f}], "
          f"mediana={ry['mediana']:.2f} (Q1-Q3: {ry['q1']:.2f}-{ry['q3']:.2f})")
    print(f"Mann-Whitney: U_A={res['u_x']:.1f}, U_B={res['u_y']:.1f}, p={res['p_mw']:.4f} | "
          f"Hodges-Lehmann (B-A)={res['hl']:.2f} [IC95%: {res['hl_ic'][0]:.2f}; {res['hl_ic'][1]:.2f}] | "
          f"Cliff delta={res['delta']:.3f}, r_rb={res['r_rb']:.3f}")
    print(f"Welch bruto: t={res['t_welch']:.3f}, p={res['p_welch']:.4f}, d={res['d_cohen']:.3f}")
    if not np.isnan(res["p_log"]):
        print(f"Welch log10: t={res['t_log']:.3f}, p={res['p_log']:.4f}, d_log={res['d_log']:.3f}")

# ==========================================
# 3. ANÁLISES ESTATÍSTICAS
# ==========================================

print("==========================================")
print("1. TEMPO DE PERMANÊNCIA (H1)")
print("==========================================")

res_tempo_full = comparar_continuas(tempo_A, tempo_B)
imprimir_bloco_continuo("Amostra integral (N = 81)", res_tempo_full)

# Critério simétrico de outlier: > Q3 + 3*IQR (calculado na amostra combinada) ou > 300 s
tempo_all = np.concatenate([tempo_A, tempo_B])
q3_all = np.percentile(tempo_all, 75)
iqr_all = np.percentile(tempo_all, 75) - np.percentile(tempo_all, 25)
limite_simetrico = min(q3_all + 3.0 * iqr_all, 300.0)

mask_A_sim = tempo_A <= limite_simetrico
mask_B_sim = tempo_B <= limite_simetrico
print(f"\nLimite simétrico adotado: {limite_simetrico:.2f} s "
      f"(removidos: A={np.sum(~mask_A_sim)}, B={np.sum(~mask_B_sim)})")
res_tempo_sim = comparar_continuas(tempo_A[mask_A_sim], tempo_B[mask_B_sim])
imprimir_bloco_continuo("Sensibilidade com critério simétrico", res_tempo_sim)

# Sensibilidade sem o outlier isolado de 670,26 s no Grupo B
mask_B_no670 = tempo_B < 600.0
res_tempo_no670 = comparar_continuas(tempo_A, tempo_B[mask_B_no670])
imprimir_bloco_continuo("Sensibilidade sem outlier de 670,26 s no Grupo B", res_tempo_no670)

# Período pseudoaleatório inicial (primeiros 49 registros)
res_tempo_rand49 = comparar_continuas(tempo_A[:27], tempo_B[:22])
imprimir_bloco_continuo("Período inicial randomizado (n = 49: 27 A / 22 B)", res_tempo_rand49)

# Estratificação: cliques rápidos (< 3 s) vs. leitores ativos (>= 3 s)
idx_A_rap = tempo_A < 3.0
idx_B_rap = tempo_B < 3.0
res_tempo_ativos = comparar_continuas(tempo_A[~idx_A_rap], tempo_B[~idx_B_rap])
imprimir_bloco_continuo("Leitores ativos (>= 3 s: A n=28, B n=30)", res_tempo_ativos)

print("\n==========================================")
print("2. NOTAS NO QUESTIONÁRIO (H2) E EFICIÊNCIA")
print("==========================================")

res_notas_full = comparar_continuas(notas_A, notas_B)
imprimir_bloco_continuo("Notas na amostra integral (N = 81)", res_notas_full)

p_tost, p_low, p_high, diff_notas, df_notas = tost_welch(notas_A, notas_B, margin=0.70)
print(f"\nTOST (margem ±0,70 pt, gl={df_notas:.1f}): p_TOST={p_tost:.4f} "
      f"(p_inf={p_low:.4f}, p_sup={p_high:.4f}), dif_média={diff_notas:.2f}")

# Notas estratificadas por tempo (< 3 s vs. >= 3 s)
print(f"\nNotas cliques rápidos (< 3 s): "
      f"A={np.mean(notas_A[idx_A_rap]):.2f} (n={np.sum(idx_A_rap)}) vs. "
      f"B={np.mean(notas_B[idx_B_rap]):.2f} (n={np.sum(idx_B_rap)})")
res_notas_ativos = comparar_continuas(notas_A[~idx_A_rap], notas_B[~idx_B_rap])
imprimir_bloco_continuo("Notas leitores ativos (>= 3 s)", res_notas_ativos)

# Eficiência temporal exploratória: acertos por minuto entre leitores ativos
eff_A = notas_A[~idx_A_rap] / (tempo_A[~idx_A_rap] / 60.0)
eff_B = notas_B[~idx_B_rap] / (tempo_B[~idx_B_rap] / 60.0)
res_eff_ativos = comparar_continuas(eff_A, eff_B)
imprimir_bloco_continuo("Acertos por minuto (leitores ativos >= 3 s)", res_eff_ativos)

print("\n==========================================")
print("3. PROPORÇÕES DE CONFIRMAÇÃO (E1 - DESCRITIVO)")
print("==========================================")

props = aceites / totais
for nome, k, n, p in zip(["Grupo A", "Grupo B"], aceites, totais, props):
    w_low, w_high = wilson_ci(k, n)
    print(f"{nome}: {k}/{n} ({p*100:.2f}%), IC95% Wilson = [{w_low*100:.1f}%; {w_high*100:.1f}%]")

diff_p, nc_low, nc_high = newcombe_diff_ci(aceites[0], totais[0], aceites[1], totais[1])
_, p_fisher = fisher_exact(
    np.array([[aceites[0], totais[0] - aceites[0]],
              [aceites[1], totais[1] - aceites[1]]]),
    alternative="two-sided"
)
print(f"Diferença (B - A): {diff_p*100:+.2f} p.p., IC95% Newcombe = [{nc_low*100:+.1f}; {nc_high*100:+.1f}] p.p. "
      f"| Fisher (descritivo) p = {p_fisher:.3f}")

# ==========================================
# 4. GRÁFICOS PADRONIZADOS EM PDF VETORIAL
# ==========================================

cores = ["#0072F0", "#F02020"]
grupos = ["Grupo A (Texto)", "Grupo B (Visual)"]

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
wilson_bounds = np.array([wilson_ci(k, n) for k, n in zip(aceites, totais)]) * 100.0
yerr_wilson = np.vstack([
    np.maximum(0.0, taxas - wilson_bounds[:, 0]),
    np.maximum(0.0, wilson_bounds[:, 1] - taxas),
])

x = np.arange(len(grupos))
barras = ax.bar(x, taxas, width=0.48, color=cores, edgecolor="black", linewidth=0.7)
ax.errorbar(x, taxas, yerr=yerr_wilson, fmt="none", ecolor="black",
            elinewidth=1.4, capsize=6, capthick=1.4)

for i, (barra, taxa, sup) in enumerate(zip(barras, taxas, wilson_bounds[:, 1])):
    ax.text(barra.get_x() + barra.get_width() / 2, sup + 1.5,
            f"{taxa:.2f}%\n({aceites[i]}/{totais[i]})",
            ha="center", va="bottom", fontsize=9.5)

ax.set_xticks(x)
ax.set_xticklabels(grupos)
ax.set_ylim(0, 118)
ax.set_yticks(np.arange(0, 101, 20))
ax.set_ylabel("Confirmação no Botão Final (%)")
ax.set_title("Proporção de Confirmação por Grupo (IC 95% de Wilson)")
ax.grid(axis="y", linestyle="--", alpha=0.35)
ax.set_axisbelow(True)

nota_rodape = (
    f"Diferença (B − A): {diff_p*100:+.2f} p.p. "
    f"(IC 95% Newcombe: {nc_low*100:+.1f} a {nc_high*100:+.1f} p.p.)"
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
