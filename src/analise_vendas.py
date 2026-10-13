import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Lê o arquivo CSV (a coluna de data é lida como data)
df_vendas = pd.read_csv("data/vendas.csv", parse_dates = ['Data_Pedido'])

# Pergunta 1: O que vender? (produtos mais vendidos)
top_10_produtos = df_vendas.groupby('Nome_Produto')['Quantidade'].sum().sort_values(ascending = False).head(10)

# Pergunta 2: Quando agir? (faturamento por mês)
faturamento_mes = df_vendas.groupby('Mes')['Faturamento'].sum()

# Mesma série, ordenada do maior para o menor, para achar o mês campeão
meses_ordenados = faturamento_mes.sort_values(ascending = False)

# Pergunta 3: O que focar? (categoria mais vendida)
vendas_categoria = df_vendas.groupby('Categoria')['Quantidade'].sum().sort_values(ascending = False)

# Pergunta 4: Para onde expandir? (faturamento por estado)
faturamento_estado = df_vendas.groupby('Estado')['Faturamento'].sum().sort_values(ascending = False)


# Resumo das respostas
print("RESPOSTAS DAS 4 PERGUNTAS")
print("-" * 40)
print(f"O que vender?       {top_10_produtos.index[0]} ({top_10_produtos.iloc[0]} unidades)")
print(f"Quando agir?        {meses_ordenados.index[0]} (R$ {round(meses_ordenados.iloc[0], 2)})")
print(f"O que focar?        {vendas_categoria.index[0]} ({vendas_categoria.iloc[0]} unidades)")
print(f"Para onde expandir? {faturamento_estado.index[0]} (R$ {round(faturamento_estado.iloc[0], 2)})")


# Dashboard
sns.set_theme(style = "whitegrid")

# Cria uma figura com 4 gráficos (2 linhas x 2 colunas)
fig, axes = plt.subplots(2, 2, figsize = (16, 11))
fig.suptitle("Dashboard de Vendas - 4 Perguntas de Negócio", fontsize = 20)

# Gráfico 1: O que vender?
sns.barplot(x = top_10_produtos.values, y = top_10_produtos.index, color = "steelblue", ax = axes[0, 0])
axes[0, 0].set_title("1) O que vender? Produtos mais vendidos")
axes[0, 0].set_xlabel("Unidades vendidas")
axes[0, 0].set_ylabel("")

# Gráfico 2: Quando agir?
sns.lineplot(x = faturamento_mes.index, y = faturamento_mes.values, marker = "o", color = "steelblue", ax = axes[0, 1])
axes[0, 1].set_title("2) Quando agir? Faturamento por mês")
axes[0, 1].set_xlabel("Mês")
axes[0, 1].set_ylabel("Faturamento (R$)")

# Gráfico 3: O que focar?
sns.barplot(x = vendas_categoria.index, y = vendas_categoria.values, color = "steelblue", ax = axes[1, 0])
axes[1, 0].set_title("3) O que focar? Categoria mais vendida")
axes[1, 0].set_xlabel("")
axes[1, 0].set_ylabel("Unidades vendidas")

# Gráfico 4: Para onde expandir?
sns.barplot(x = faturamento_estado.values, y = faturamento_estado.index, color = "steelblue", ax = axes[1, 1])
axes[1, 1].set_title("4) Para onde expandir? Faturamento por estado")
axes[1, 1].set_xlabel("Faturamento (R$)")
axes[1, 1].set_ylabel("")

# Ajusta o espaçamento, salva a imagem e mostra o dashboard
plt.tight_layout()
plt.savefig("images/dashboard_vendas.png", dpi = 150)
plt.show()