"""
Criar arquivo consolidado unificando Betfair + FootyStats
Merge por Data + Time (Home/Away)
"""

import numpy as np
import pandas as pd

print("=" * 100)
print("CONSOLIDAÇÃO DE DADOS - BETFAIR + FOOTYSTATS")
print("=" * 100)

# Carregar dados
df_betfair = pd.read_csv("data_total/dados_betfair_atualizado.csv", sep=";")
df_footystats = pd.read_csv("data_total/dados_footystats.csv", sep=";")

print("\n✓ Carregados:")
print(f"  Betfair: {df_betfair.shape[0]} linhas")
print(f"  FootyStats: {df_footystats.shape[0]} linhas")

# Verificar se ambas têm coluna de data
print("\n✓ Colunas com data:")
print(f"  Betfair: {[c for c in df_betfair.columns if 'date' in c.lower() or 'time' in c.lower()]}")
print(f"  FootyStats: {[c for c in df_footystats.columns if 'date' in c.lower() or 'time' in c.lower()]}")

# Preparar Betfair
df_betfair_prep = df_betfair.copy()

# Preparar FootyStats - adicionar coluna de datetime
df_footystats_prep = df_footystats.copy()

# Tentar converter datas para formato consistente
print("\n✓ Verificando formato de datas...")
print(f"  Betfair - Primeiras datas: {df_betfair_prep['Home'].iloc[:3].values if 'Home' in df_betfair_prep.columns else 'N/A'}")

# Verificar primeiro jogo de Betfair
print("\n✓ Primeiros jogos BETFAIR:")
for idx in range(min(3, len(df_betfair_prep))):
    row = df_betfair_prep.iloc[idx]
    print(f"  {row['Home']} x {row['Away']}")

print("\n✓ Primeiros jogos FOOTYSTATS:")
for idx in range(min(3, len(df_footystats_prep))):
    row = df_footystats_prep.iloc[idx]
    print(f"  {row['Home']} x {row['Away']} ({row['Date']})")

# Lista de times brasileiros que podem ter nomes diferentes
team_mapping = {
    # FootyStats → Betfair
    "Botafogo": "Botafogo FR",
    "Botafogo FR": "Botafogo FR",
    "Fluminense": "Fluminense",
    "Flamengo": "Flamengo",
    "Vasco": "Vasco",
    "Corinthians": "Corinthians",
    "São Paulo": "Sao Paulo",
    "Santos": "Santos",
    "Palmeiras": "Palmeiras",
    "Atletico Mineiro": "Ath Mineiro",
    "Atlético Mineiro": "Ath Mineiro",
    "Cruzeiro": "Cruzeiro",
    "América Mineiro": "America MG",
    "Bragantino": "Bragantino",
    "Atletico Paranaense": "Athletico-PR",
    "Athletico Paranaense": "Athletico-PR",
    "Atletico GO": "Atletico GO",
    "Juventude": "Juventude",
    "Fortaleza": "Fortaleza",
    "Cebolinha": "Cebolinha",
    "Bahia": "Bahia",
    "Sport Recife": "Sport",
    "Paysandu": "Paysandu",
    "Goias": "Goias",
    "Coritiba": "Coritiba",
    "Avaí": "Avai",
    "Internacional": "Internacional",
}

print(f"\n✓ Mapeamento manual de times brasileiros: {len(team_mapping)} times")

# Tentar fazer merge por times que têm correspondência direta
print("\n✓ Buscando correspondências por Data + Time...")

# Adicionar coluna de chave no betfair
if "Date" not in df_betfair_prep.columns:
    # Se não tiver coluna Date, tentar usar o índice ou criar uma
    print("⚠ Betfair não tem coluna 'Date', usando índice como temporal")
    df_betfair_prep["Date_Key"] = df_betfair_prep.index

# Normalizar nomes de times em FootyStats
df_footystats_prep["Home_Mapped"] = df_footystats_prep["Home"].map(lambda x: team_mapping.get(x, x))
df_footystats_prep["Away_Mapped"] = df_footystats_prep["Away"].map(lambda x: team_mapping.get(x, x))

print("\n✓ Contagem de times que foram mapeados:")
mapeados_home = df_footystats_prep[df_footystats_prep["Home_Mapped"] != df_footystats_prep["Home"]].shape[0]
mapeados_away = df_footystats_prep[df_footystats_prep["Away_Mapped"] != df_footystats_prep["Away"]].shape[0]
print(f"  Home: {mapeados_home}")
print(f"  Away: {mapeados_away}")

# Criar arquivo consolidado
# Como Betfair não tem data em coluna separada, vamos usar FootyStats como base e buscar correspondências

consolidated = []

for idx, row_fs in df_footystats_prep.iterrows():
    # Buscar correspondência em Betfair
    home_fs = row_fs["Home_Mapped"]
    away_fs = row_fs["Away_Mapped"]
    date_fs = row_fs["Date"]

    # Buscar em Betfair by Home/Away
    match_bf = df_betfair_prep[(df_betfair_prep["Home"] == home_fs) & (df_betfair_prep["Away"] == away_fs)]

    if len(match_bf) > 0:
        # Usar primeiro match
        row_bf = match_bf.iloc[0]

        # Consolidar
        consolidated_row = {
            "Date": date_fs,
            "Home": home_fs,
            "Away": away_fs,
            "League_FootyStats": row_fs["League"],
            "Goals_H_FT": row_fs["Goals_H_FT"],
            "Goals_A_FT": row_fs["Goals_A_FT"],
            "xG_H": row_fs.get("xG_H", np.nan),
            "xG_A": row_fs.get("xG_A", np.nan),
            "Odd_A_Back": row_bf.get("Odd_A_Back", np.nan),
            "Odd_CS_0x1_Lay": row_bf.get("Odd_CS_0x1_Lay", np.nan),
            "Possession_H": row_fs.get("Possession_H", np.nan),
            "Possession_A": row_fs.get("Possession_A", np.nan),
            "Shots_H": row_fs.get("Shots_H", np.nan),
            "Shots_A": row_fs.get("Shots_A", np.nan),
            "ShotsOnTarget_H": row_fs.get("ShotsOnTarget_H", np.nan),
            "ShotsOnTarget_A": row_fs.get("ShotsOnTarget_A", np.nan),
            "Attacks_H": row_fs.get("Attacks_H", np.nan),
            "Attacks_A": row_fs.get("Attacks_A", np.nan),
            "DangerousAttacks_H": row_fs.get("DangerousAttacks_H", np.nan),
            "DangerousAttacks_A": row_fs.get("DangerousAttacks_A", np.nan),
        }
        consolidated.append(consolidated_row)

df_consolidated = pd.DataFrame(consolidated)

print("\n✓ RESULTADO:")
print(f"  Registros consolidados: {len(df_consolidated)}")
print(f"  Taxa de consolidação: {len(df_consolidated) / len(df_footystats_prep) * 100:.1f}%")

# Salvar
output_file = "data_total/dados_consolidado_betfair_footystats.csv"
df_consolidated.to_csv(output_file, sep=";", index=False)

print(f"\n✓ Arquivo salvo: {output_file}")

# Amostra
print("\n✓ Amostra dos dados consolidados:")
print(df_consolidated.head(10).to_string())
