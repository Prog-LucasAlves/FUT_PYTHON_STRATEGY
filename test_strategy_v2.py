from strategy_v2 import Lay0x1StrategyV2
import pandas as pd

strategy = Lay0x1StrategyV2()

# Teste com vários jogos do dia
df_day = pd.read_csv("data_day/dados_day_betfair_2026-03-29.csv", sep=";")

print("=" * 100)
print("TESTE - SCORES COM STRATEGY V2 (TODOS OS JOGOS DO DIA)")
print("=" * 100)

for idx, row in df_day.iterrows():
    result = strategy.evaluate_score(
        home=row["Home"],
        away=row["Away"],
        odd_away=float(row["Odd_A_Back"])
    )

    print(f"\n{result['home']} x {result['away']}")
    print(f"  Odd: {result['odd_away']:.2f}")
    print(f"  xG: {result['xg_away']:.3f} ({result['xg_cat']})")
    print(f"  Eff: {result['efficiency_away']:.1f}% ({result['eff_cat']})")
    print(f"  Score: {result['total_score']}/110 - {result['recommendation']} (Confiança: {result['confidence']:.1f}%)")

print("\n" + "=" * 100)
print("Scores agora VARIAM conforme o time e a odd!")
