"""
Gera um arquivo CSV com dados de vendas FICTÍCIOS.

Uso:
    python src/gerar_dados.py
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_CSV = RAIZ / "data" / "vendas.csv"

PRODUTOS = {
    "Laptop Gamer": {"categoria": "Eletrônicos", "preco": 7500.00},
    "Mouse Vertical": {"categoria": "Acessórios", "preco": 250.00},
    "Teclado Mecânico": {"categoria": "Acessórios", "preco": 550.00},
    "Monitor Ultrawide": {"categoria": "Eletrônicos", "preco": 2800.00},
    "Cadeira Gamer": {"categoria": "Móveis", "preco": 1200.00},
    "Headset 7.1": {"categoria": "Acessórios", "preco": 800.00},
    "Placa de Vídeo": {"categoria": "Hardware", "preco": 4500.00},
    "SSD 1TB": {"categoria": "Hardware", "preco": 600.00},
}

CIDADES_ESTADOS = {
    "São Paulo": "SP", "Rio de Janeiro": "RJ", "Belo Horizonte": "MG",
    "Porto Alegre": "RS", "Salvador": "BA", "Curitiba": "PR", "Fortaleza": "CE",
}

PRODUTOS_COM_DESCONTO = ["Mouse Vertical", "Teclado Mecânico"]


def gerar_dados_ficticios(num_registros: int = 500, semente: int | None = None) -> pd.DataFrame:
    """Gera um DataFrame com vendas fictícias.

    Parâmetros
    ----------
    num_registros : quantidade de pedidos a gerar.
    semente : se informada, torna a geração reproduzível.
    """
    if semente is not None:
        random.seed(semente)
        np.random.seed(semente)

    lista_produtos = list(PRODUTOS)
    lista_cidades = list(CIDADES_ESTADOS)
    data_inicial = datetime(2026, 1, 1)
    vendas = []

    for i in range(num_registros):
        produto = random.choice(lista_produtos)
        cidade = random.choice(lista_cidades)
        quantidade = np.random.randint(1, 8)

        # 5 pedidos por dia, com hora sorteada
        data_pedido = data_inicial + timedelta(days=i // 5, hours=random.randint(0, 23))

        # Desconto aleatório de até 10% para mouse e teclado
        preco = PRODUTOS[produto]["preco"]
        if produto in PRODUTOS_COM_DESCONTO:
            preco *= np.random.uniform(0.9, 1.0)

        vendas.append({
            "ID_Pedido": 1000 + i,
            "Data_Pedido": data_pedido,
            "Nome_Produto": produto,
            "Categoria": PRODUTOS[produto]["categoria"],
            "Preco_Unitario": round(preco, 2),
            "Quantidade": quantidade,
            "ID_Cliente": np.random.randint(100, 150),
            "Cidade": cidade,
            "Estado": CIDADES_ESTADOS[cidade],
        })

    df = pd.DataFrame(vendas)
    df["Faturamento"] = (df["Preco_Unitario"] * df["Quantidade"]).round(2)
    df["Mes"] = df["Data_Pedido"].dt.to_period("M").astype(str)
    return df


if __name__ == "__main__":
    CAMINHO_CSV.parent.mkdir(exist_ok=True)
    df = gerar_dados_ficticios(500, semente=42)
    df.to_csv(CAMINHO_CSV, index=False)
    print(f"{len(df)} registros salvos em {CAMINHO_CSV}")
