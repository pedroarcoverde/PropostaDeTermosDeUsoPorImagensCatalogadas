import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

# ==========================================
# 1. DADOS
# ==========================================

# Tempos de permanência convertidos de milissegundos para segundos
tempo_A = np.array([
    153314, 178655, 2411, 2113, 35584, 34914, 2425, 224698, 2289, 26085,
    126324, 1775, 1986, 1732, 169228, 355873, 51026, 200557, 297906, 2722,
    2099, 2501, 26390, 265514, 251314, 2742, 128301, 2796, 177656, 262811,
    131173, 213582, 2328, 129699, 108174, 20933, 55873, 98756, 15284, 69599
]) / 1000.0

tempo_B = np.array([
    2922, 14683, 18771, 3190, 670257, 1785, 78843, 81845, 9568, 2245,
    59066, 2864, 103981, 3547, 50427, 4565, 2059, 64681, 88688, 22191,
    87259, 122149, 11432, 65066, 98377, 117025, 1734, 6226, 10722, 1300,
    97472, 13514, 2628, 224497, 11068, 45328, 1621, 9012, 2548, 24405,
    149257
]) / 1000.0

notas_A = np.array([
    6, 6, 1, 5, 2, 5, 7, 6, 1, 5, 6, 5, 2, 0, 7, 7, 5, 7, 7, 2,
    3, 1, 7, 7, 5, 2, 7, 2, 6, 6, 7, 7, 1, 7, 7, 6, 4, 7, 0, 4
])

notas_B = np.array([
    6, 6, 3, 7, 6, 3, 7, 7, 5, 3, 6, 2, 5, 6, 7, 6, 2, 4, 6, 5,
    7, 7, 4, 6, 6, 7, 1, 3, 6, 3, 7, 6, 4, 7, 5, 7, 2, 5, 3, 7, 7
])

aceite_A = 34 / 40 * 100
aceite_B = 32 / 41 * 100

# ==========================================
#  CONFIGURAÇÕES VISUAIS
# ==========================================

# Cores padrão do trabalho
cores = ['#0072F0', '#F02020']
grupos = ['Grupo A (Texto)', 'Grupo B (Visual)']

plt.rcParams.update({
    'font.size': 11,
    'font.family': 'sans-serif',
    'axes.titlesize': 13,
    'axes.labelsize': 11
})

from scipy.stats import fisher_exact


# ==========================================
# Gráfico da Taxa de Aceite com IC 95%
# ==========================================

# Dados observados
aceites = np.array([34, 32])
totais = np.array([40, 41])

grupos = ['Grupo A (Texto)', 'Grupo B (Visual)']
cores = ['#0072F0', '#F02020']

# Proporções e taxas em porcentagem
proporcoes = aceites / totais
taxas = proporcoes * 100

# ------------------------------------------
# Intervalos de confiança de 95%
# Método de Wald, para manter compatibilidade
# com os intervalos apresentados na sua tabela.
# ------------------------------------------

z = 1.96

erros_proporcoes = z * np.sqrt(
    proporcoes * (1 - proporcoes) / totais
)

ic_inferior = np.maximum(
    0, proporcoes - erros_proporcoes
) * 100

ic_superior = np.minimum(
    1, proporcoes + erros_proporcoes
) * 100

# Erros inferiores e superiores para o Matplotlib
erros_grafico = np.array([
    taxas - ic_inferior,
    ic_superior - taxas
])

# ------------------------------------------
# Teste exato de Fisher (bicaudal)
# ------------------------------------------

# Linhas: Grupos A e B
# Colunas: Aceitou e Não aceitou
tabela_contingencia = np.array([
    [aceites[0], totais[0] - aceites[0]],
    [aceites[1], totais[1] - aceites[1]]
])

_, p_fisher = fisher_exact(
    tabela_contingencia,
    alternative='two-sided'
)

# ------------------------------------------
# Diferença entre proporções: Grupo B - Grupo A
# IC 95% pelo método de Wald
# ------------------------------------------

diferenca_pp = (proporcoes[1] - proporcoes[0]) * 100

erro_diferenca = z * np.sqrt(
    proporcoes[0] * (1 - proporcoes[0]) / totais[0]
    + proporcoes[1] * (1 - proporcoes[1]) / totais[1]
) * 100

ic_diferenca_inferior = diferenca_pp - erro_diferenca
ic_diferenca_superior = diferenca_pp + erro_diferenca

# ------------------------------------------
# Construção do gráfico
# ------------------------------------------

fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

x = np.arange(len(grupos))

barras = ax.bar(
    x,
    taxas,
    width=0.55,
    color=cores,
    edgecolor='black',
    linewidth=0.7,
    zorder=2
)

# Barras de erro: IC 95%
ax.errorbar(
    x,
    taxas,
    yerr=erros_grafico,
    fmt='none',
    ecolor='black',
    elinewidth=1.5,
    capsize=7,
    capthick=1.5,
    zorder=3
)

# Porcentagem e quantidade acima de cada intervalo
for i, (barra, taxa, superior) in enumerate(
    zip(barras, taxas, ic_superior)
):
    ax.text(
        barra.get_x() + barra.get_width() / 2,
        superior + 1.0,
        f'{taxa:.2f}%\n({aceites[i]}/{totais[i]})',
        ha='center',
        va='bottom',
        fontsize=10
    )

# Título e identificação dos eixos
ax.set_title(
    'Taxa de Aceite por Grupo',
    fontsize=14,
    pad=18
)

ax.set_ylabel('Taxa de aceite (%)', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(grupos, fontsize=10)

ax.set_ylim(0, 125)
ax.set_yticks(np.arange(0, 101, 20))

# Anotação do teste inferencial
p_formatado = f'{p_fisher:.3f}'.replace('.', ',')

ax.text(
    0.5,
    0.98,
    f'Teste exato de Fisher (bicaudal): p = {p_formatado}',
    transform=ax.transAxes,
    ha='center',
    va='top',
    fontsize=10
)

# Aparência
ax.grid(
    axis='y',
    linestyle='--',
    alpha=0.35,
    zorder=0
)
ax.set_axisbelow(True)

# Nota com a diferença entre proporções e seu IC
diferenca_formatada = f'{diferenca_pp:+.2f}'.replace('.', ',')
ic_inf_formatado = f'{ic_diferenca_inferior:+.1f}'.replace('.', ',')
ic_sup_formatado = f'{ic_diferenca_superior:+.1f}'.replace('.', ',')

nota = (
    f'Diferença B − A: {diferenca_formatada} p.p. '
    f'(IC 95%: {ic_inf_formatado} a {ic_sup_formatado} p.p.)'
)

fig.text(
    0.5,
    0.025,
    nota,
    ha='center',
    va='bottom',
    fontsize=9
)

fig.tight_layout(rect=[0, 0.08, 1, 0.96])
plt.show()


# ==========================================
#  GRÁFICO DE TEMPO DE PERMANÊNCIA
# ==========================================

fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

bp = ax.boxplot(
    [tempo_A, tempo_B],
    patch_artist=True,
    widths=0.45,
    showmeans=True,

    # Mediana preta para garantir contraste
    medianprops={
        'color': 'black',
        'linewidth': 2
    },

    # Média como losango preto
    meanprops={
        'marker': 'D',
        'markerfacecolor': 'black',
        'markeredgecolor': 'black',
        'markersize': 5
    },

    # Outliers como círculos vazios cinza
    flierprops={
        'marker': 'o',
        'markerfacecolor': 'white',
        'markeredgecolor': '#555555',
        'markersize': 4,
        'alpha': 0.8
    },

    # Bigodes e extremidades pretos
    whiskerprops={
        'color': 'black',
        'linewidth': 1.2
    },
    capprops={
        'color': 'black',
        'linewidth': 1.2
    },

    # Contorno das caixas preto
    boxprops={
        'edgecolor': 'black',
        'linewidth': 1.2
    }
)

# Aplicar cores às caixas
for caixa, cor in zip(bp['boxes'], cores):
    caixa.set_facecolor(cor)
    caixa.set_alpha(0.85)

ax.set_xticks([1, 2])
ax.set_xticklabels(['Grupo A (Texto)', 'Grupo B (Visual)'])

ax.set_yscale('log')
ax.set_ylabel('Tempo de Permanência (segundos)')
ax.set_title('Distribuição do Tempo de Permanência')

ax.grid(
    axis='y',
    linestyle='--',
    color='gray',
    alpha=0.35,
    which='both'
)

ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig('grafico_3_tMedio.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close(fig)

# ==========================================
#  GRÁFICO DE NOTAS MÉDIAS COM IC DE 95%
# ==========================================

medias_nota = np.array([
    np.mean(notas_A),
    np.mean(notas_B)
])

# Calcular os intervalos de confiança usando t de Student
dados_notas = [notas_A, notas_B]
margens_ic = []

for notas in dados_notas:
    n = len(notas)
    desvio = np.std(notas, ddof=1)
    erro_padrao = desvio / np.sqrt(n)

    valor_critico = t.ppf(0.975, df=n - 1)
    margem = valor_critico * erro_padrao

    margens_ic.append(margem)

margens_ic = np.array(margens_ic)

# Criar gráfico
fig, ax = plt.subplots(figsize=(7, 5), dpi=300)

barras = ax.bar(
    grupos,
    medias_nota,
    yerr=margens_ic,
    capsize=8,
    color=cores,
    alpha=0.9,
    width=0.45,
    error_kw={
        'ecolor': 'black',
        'elinewidth': 1.3,
        'capthick': 1.3
    }
)

# Valores das médias centralizados acima das barras de erro
for barra, media, margem in zip(barras, medias_nota, margens_ic):
    x = barra.get_x() + barra.get_width() / 2
    y = media + margem + 0.12

    ax.text(
        x,
        y,
        f'{media:.2f}',
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold'
    )

ax.set_ylim(0, 8)
ax.set_ylabel('Nota Média (Escala de 0 a 7)')
ax.set_title('Nota Média no Questionário (IC de 95%)')

ax.grid(
    axis='y',
    linestyle='--',
    color='gray',
    alpha=0.35
)

ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig('grafico_4_notasTempo.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close(fig)

# ==========================================
# RESULTADOS NUMÉRICOS
# ==========================================

print('===== TEMPO DE PERMANÊNCIA =====')

for nome, dados in zip(grupos, [tempo_A, tempo_B]):
    print(f'\n{nome}:')
    print(f'  Participantes: {len(dados)}')
    print(f'  Média: {np.mean(dados):.2f} segundos')
    print(f'  Mediana: {np.median(dados):.2f} segundos')
    print(f'  Desvio padrão: {np.std(dados, ddof=1):.2f} segundos')

print('\n===== NOTAS =====')

for nome, media, margem, notas in zip(
    grupos, medias_nota, margens_ic, dados_notas
):
    print(f'\n{nome}:')
    print(f'  Média: {media:.2f}')
    print(f'  IC 95%: [{media - margem:.2f}, {media + margem:.2f}]')
    print(f'  Participantes: {len(notas)}')

print('\n===== TAXAS DE ACEITE =====')
for grupo, taxa, inferior, superior in zip(
    grupos, taxas, ic_inferior, ic_superior
):
    print(
        f'{grupo}: {taxa:.2f}% '
        f'(IC 95%: {inferior:.1f}% a {superior:.1f}%)'
    )

print(f'\nTeste exato de Fisher: p = {p_fisher:.3f}')
print(
    f'Diferença B - A: {diferenca_pp:.2f} p.p. '
    f'(IC 95%: {ic_diferenca_inferior:.1f} a '
    f'{ic_diferenca_superior:.1f} p.p.)'
)

