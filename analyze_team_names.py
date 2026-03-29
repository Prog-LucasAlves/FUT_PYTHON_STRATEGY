from difflib import SequenceMatcher

import pandas as pd

# Carregar bases
print("Carregando dados...")
df_betfair = pd.read_csv("data_total/dados_betfair_atualizado.csv", sep=";")
df_footystats = pd.read_csv("data_total/dados_footystats.csv", sep=";")

print(f"\nBetfair: {df_betfair.shape[0]} linhas")
print(f"FootyStats: {df_footystats.shape[0]} linhas")

# Verificar colunas
print(f"\nColunas Betfair (primeiras 10): {list(df_betfair.columns[:10])}")
print(f"Colunas FootyStats (primeiras 10): {list(df_footystats.columns[:10])}")

# Analisar nomes de times
betfair_teams_home = set(df_betfair["Home"].unique())
betfair_teams_away = set(df_betfair["Away"].unique())
footystats_teams = set(df_footystats["Home"].unique()) | set(df_footystats["Away"].unique())

print("\nTimes únicos:")
print(f"  Betfair (Home): {len(betfair_teams_home)}")
print(f"  Betfair (Away): {len(betfair_teams_away)}")
print(f"  FootyStats: {len(footystats_teams)}")

# Listar alguns nomes para entender padrão
print("\nExemplos de times Betfair (Home):")
for team in sorted(list(betfair_teams_home))[:10]:
    print(f"  - {team}")

print("\nExemplos de times FootyStats:")
for team in sorted(list(footystats_teams))[:10]:
    print(f"  - {team}")

# Buscar times com nomes similares
print("\nBuscando correspondências de nomes...")


def similar(a, b):
    """Calcula similaridade entre dois strings (0-1)"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


# Criar mapeamento
team_mapping = {}

for bf_team in betfair_teams_home:
    best_match = None
    best_score = 0

    for fs_team in footystats_teams:
        score = similar(bf_team, fs_team)
        if score > best_score:
            best_score = score
            best_match = fs_team

    if best_score > 0.8:  # Threshold de 80%
        team_mapping[best_match] = bf_team
        if best_score > 0.9:
            print(f"  ✓ {fs_team} → {bf_team} ({best_score:.2%})")

print(f"\nTotal de correspondências encontradas: {len(team_mapping)}")
print("\nExemplos de mapeamento:")
for fs_name, bf_name in sorted(list(team_mapping.items())[:5]):
    print(f"  {fs_name} → {bf_name}")
