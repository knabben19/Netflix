# ==========================================
# 🎬 Sistema de Recomendação estilo Netflix
# Autor: Vinícius Knabben
# ==========================================

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Base de dados simulada
# -----------------------------
dados = {
    "Usuario": ["Ana", "Ana", "Ana", 
                "Carlos", "Carlos", "Carlos",
                "Marina", "Marina", "Marina",
                "João", "João", "João"],
    
    "Filme": ["Interestelar", "Matrix", "Vingadores",
              "Interestelar", "Matrix", "Titanic",
              "Matrix", "Vingadores", "Titanic",
              "Interestelar", "Titanic", "Vingadores"],
    
    "Nota": [5, 4, 5,
             4, 5, 2,
             5, 4, 4,
             5, 3, 4]
}

df = pd.DataFrame(dados)

# -----------------------------
# Criando matriz Usuario x Filme
# -----------------------------
matriz = df.pivot_table(index="Usuario", columns="Filme", values="Nota")

# Preencher valores NaN com 0
matriz = matriz.fillna(0)

# -----------------------------
# Calculando similaridade
# -----------------------------
similaridade = cosine_similarity(matriz)
similaridade_df = pd.DataFrame(similaridade, 
                               index=matriz.index, 
                               columns=matriz.index)

# -----------------------------
# Função de recomendação
# -----------------------------
def recomendar(usuario):
    
    if usuario not in matriz.index:
        print("Usuário não encontrado.")
        return
    
    print(f"\n🎯 Recomendações para {usuario}:\n")
    
    # Pega usuários similares (ordem decrescente)
    usuarios_similares = similaridade_df[usuario].sort_values(ascending=False)
    
    # Remove ele mesmo da lista
    usuarios_similares = usuarios_similares.drop(usuario)
    
    # Pega o usuário mais parecido
    usuario_mais_parecido = usuarios_similares.index[0]
    
    print(f"Usuário mais parecido: {usuario_mais_parecido}")
    
    # Filmes que o usuário ainda não viu
    filmes_usuario = matriz.loc[usuario]
    filmes_nao_vistos = filmes_usuario[filmes_usuario == 0].index
    
    recomendacoes = []
    
    for filme in filmes_nao_vistos:
        if matriz.loc[usuario_mais_parecido, filme] >= 4:
            recomendacoes.append(filme)
    
    if recomendacoes:
        for filme in recomendacoes:
            print(f"🍿 {filme}")
    else:
        print("Nenhuma recomendação encontrada.")

# -----------------------------
# Interface simples
# -----------------------------
if __name__ == "__main__":
    
    print("===================================")
    print(" 🎬 SISTEMA DE RECOMENDAÇÃO ")
    print("===================================")
    
    print("\nUsuários disponíveis:")
    for usuario in matriz.index:
        print(f"- {usuario}")
    
    escolha = input("\nDigite o nome do usuário: ")
    
    recomendar(escolha)