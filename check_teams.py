import pandas as pd

df_betfair = pd.read_csv("data_total/dados_betfair_atualizado.csv", sep=";")
df_footystats = pd.read_csv("data_total/dados_footystats.csv", sep=";")

print("=" * 100)
print("ANALISE - NOMES DOS TIMES")
print("=" * 100)

print("\nDADOS BETFAIR:")
print(f"  Shape: {df_betfair.shape}")
print(f"  Teams (Home): {df_betfair['Home'].nunique()}")
print(f"  Sample: {list(df_betfair['Home'].unique()[:3])}")

print("\nDADOS FOOTYSTATS:")
print(f"  Shape: {df_footystats.shape}")
print(f"  Teams (Home): {df_footystats['Home'].nunique()}")
print(f"  Sample: {list(df_footystats['Home'].unique()[:3])}")

betfair_teams = set(df_betfair["Home"].unique())
footystats_teams = set(df_footystats["Home"].unique())

print(f"\nComum: {len(betfair_teams & footystats_teams)}")
print(f"Só Betfair: {len(betfair_teams - footystats_teams)}")
print(f"  Exemplo: {list(betfair_teams - footystats_teams)[:5]}")
print(f"Só Footystats: {len(footystats_teams - betfair_teams)}")
print(f"  Exemplo: {list(footystats_teams - betfair_teams)[:5]}")

print(f"\nCOLUNAS FOOTYSTATS ({len(df_footystats.columns)}):")
print(list(df_footystats.columns))

print("\n" + "=" * 100)
print("PRIMEIRO JOGO DE CADA BASE:")
print("=" * 100)

print("\nBETFAIR:")
print(df_betfair[["Date", "Home", "Away", "Goals_H_FT", "Goals_A_FT"]].head(1))

print("\nFOOTYSTATS:")
print(df_footystats[["Home", "Away", "xG_H", "xG_A"]].head(1))
