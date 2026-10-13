"""
Análise de vendas fictícias e dashboard com as 4 perguntas de negócio:

    1) O que vender?        -> produtos mais vendidos (unidades)
    2) Quando agir?         -> mês com maior faturamento
    3) O que focar?         -> categoria mais vendida (unidades)
    4) Para onde expandir?  -> estado com maior faturamento

Uso:
    python src/analise_vendas.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_CSV = RAIZ / "data" / "vendas.csv"
CAMINHO_IMAGEM = RAIZ / "images" / "dashboard_vendas.png"

DESTAQUE = "#E4572E"  # item vencedor
NORMAL = "#4C78A8"    # demais itens


# ----------------------------------------------------------------------
# Carga e preparação
# ----------------------------------------------------------------------
def carregar_dados(caminho: Path = CAMINHO_CSV) -> pd.DataFrame:
    """Lê o CSV e garante os tipos e colunas necessários."""
    df = pd.read_csv(caminho, parse_dates=["Data_Pedido"])

    if "Faturamento" not in df.columns:
        df["Faturamento"] = (df["Preco_Unitario"] * df["Quantidade"]).round(2)

    df["Mes"] = df["Data_Pedido"].dt.to_period("M").astype(str)
    return df


# ----------------------------------------------------------------------
# As 4 perguntas
# ----------------------------------------------------------------------
def responder_perguntas(df: pd.DataFrame) -> dict[str, pd.Series]:
    """Calcula as séries usadas para responder cada pergunta."""
    return {
        "produtos": df.groupby("Nome_Produto")["Quantidade"].sum().sort_values(ascending=False),
        "mes": df.groupby("Mes")["Faturamento"].sum().sort_index(),
        "categorias": df.groupby("Categoria")["Quantidade"].sum().sort_values(ascending=False),
        "estados": df.groupby("Estado")["Faturamento"].sum().sort_values(ascending=False),
    }


def imprimir_resumo(r: dict[str, pd.Series]) -> None:
    mes_pico = r["mes"].idxmax()
    print("=" * 55)
    print("RESPOSTAS DAS 4 PERGUNTAS")
    print("=" * 55)
    print(f"O que vender?       {r['produtos'].index[0]} ({r['produtos'].iloc[0]} unidades)")
    print(f"Quando agir?        {mes_pico} (R$ {r['mes'].max():,.2f})")
    print(f"O que focar?        {r['categorias'].index[0]} ({r['categorias'].iloc[0]} unidades)")
    print(f"Para onde expandir? {r['estados'].index[0]} (R$ {r['estados'].iloc[0]:,.2f})")
    print("=" * 55)


# ----------------------------------------------------------------------
# Dashboard
# ----------------------------------------------------------------------
def _cores(n: int) -> list[str]:
    """Primeira barra (a maior) em destaque, as demais na cor normal."""
    return [DESTAQUE] + [NORMAL] * (n - 1)


def _rotulos_horizontais(ax, formato) -> None:
    for barra in ax.patches:
        ax.text(barra.get_width(), barra.get_y() + barra.get_height() / 2,
                " " + formato(barra.get_width()), va="center", fontsize=10)


def montar_dashboard(r: dict[str, pd.Series]) -> plt.Figure:
    sns.set_theme(style="whitegrid", palette="viridis")
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    fig.suptitle("Dashboard de Vendas - 4 Perguntas de Negócio", fontsize=20, fontweight="bold")

    produtos, mes, categorias, estados = r["produtos"], r["mes"], r["categorias"], r["estados"]
    mes_pico = mes.idxmax()

    # 1) O que vender?
    ax = axes[0, 0]
    sns.barplot(x=produtos.values, y=produtos.index, hue=produtos.index,
                palette=_cores(len(produtos)), legend=False, ax=ax)
    _rotulos_horizontais(ax, lambda v: f"{int(v)}")
    ax.set_title("1) O que vender? Produtos mais vendidos", fontsize=14, fontweight="bold")
    ax.set_xlabel("Unidades vendidas")
    ax.set_ylabel("")
    ax.set_xlim(0, produtos.max() * 1.15)

    # 2) Quando agir?
    ax = axes[0, 1]
    sns.lineplot(x=mes.index, y=mes.values, marker="o", linewidth=2.5, color=NORMAL, ax=ax)
    ax.scatter(mes_pico, mes.max(), color=DESTAQUE, s=150, zorder=5)
    ax.annotate(f"Pico: {mes_pico}\nR$ {mes.max():,.0f}", xy=(mes_pico, mes.max()),
                xytext=(0, 15), textcoords="offset points", ha="center",
                fontsize=10, fontweight="bold", color=DESTAQUE)
    ax.set_title("2) Quando agir? Faturamento por mês", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Faturamento (R$)")
    ax.set_ylim(0, mes.max() * 1.2)
    ax.tick_params(axis="x", rotation=45)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v / 1000:,.0f} mil")

    # 3) O que focar?
    ax = axes[1, 0]
    sns.barplot(x=categorias.index, y=categorias.values, hue=categorias.index,
                palette=_cores(len(categorias)), legend=False, ax=ax)
    for barra in ax.patches:
        ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height(),
                f"{int(barra.get_height())}", ha="center", va="bottom", fontsize=10)
    ax.set_title("3) O que focar? Categoria mais vendida", fontsize=14, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("Unidades vendidas")
    ax.set_ylim(0, categorias.max() * 1.15)

    # 4) Para onde expandir?
    ax = axes[1, 1]
    sns.barplot(x=estados.values, y=estados.index, hue=estados.index,
                palette=_cores(len(estados)), legend=False, ax=ax)
    _rotulos_horizontais(ax, lambda v: f"R$ {v / 1000:,.0f} mil")
    ax.set_title("4) Para onde expandir? Faturamento por estado", fontsize=14, fontweight="bold")
    ax.set_xlabel("Faturamento (R$)")
    ax.set_ylabel("")
    ax.set_xlim(0, estados.max() * 1.2)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v / 1000:,.0f} mil")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    return fig


def main() -> None:
    df = carregar_dados()
    resultados = responder_perguntas(df)
    imprimir_resumo(resultados)

    fig = montar_dashboard(resultados)
    CAMINHO_IMAGEM.parent.mkdir(exist_ok=True)
    fig.savefig(CAMINHO_IMAGEM, dpi=150, bbox_inches="tight")
    print(f"Dashboard salvo em {CAMINHO_IMAGEM}")
    plt.show()


if __name__ == "__main__":
    main()
