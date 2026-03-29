# 🚀 Quick Start - Strategy V4

## Executar o Dashboard

```bash
streamlit run app_lay_0x1_v3.py
```

Depois abra: **http://localhost:8501**

---

## Usar a Estratégia Programaticamente

### 1. Validar um Jogo

```python
from strategy_v4 import Lay0x1StrategyV4

strategy = Lay0x1StrategyV4()

# Avaliar um jogo
result = strategy.evaluate_score(
    home="Manchester United",
    away="Liverpool",
    odd_away=2.50,
    odd_0x1_lay=11.5
)

print(f"Score: {result['total_score']}/110")
print(f"Recomendação: {result['recommendation']}")
print(f"xG Visitante: {result['xg_away']:.2f}")
```

### 2. Analisar Múltiplos Jogos

```python
import pandas as pd

games = pd.read_csv("data_day/dados_day_betfair_2024-12-25.csv", sep=";")

results = []
for _, game in games.iterrows():
    score = strategy.evaluate_score(
        home=game['Home'],
        away=game['Away'],
        odd_away=game['Odd_A_Back'],
        odd_0x1_lay=game['Odd_CS_0x1_Lay']
    )
    results.append(score)

# Filtrar apenas recomendações CONFIANÇA
confident = [r for r in results if r['total_score'] >= 90]
print(f"Jogos com CONFIANÇA: {len(confident)}")
```

### 3. Obter Estatísticas Históricas

```python
stats = strategy.get_historical_stats()

print(f"Win Rate Geral: {stats['lay_0x1_winrate']:.1f}%")
print(f"Win Rate (Odds 5.0+): {stats['by_odd_range']['5.0-10.0']['winrate']:.1f}%")
print(f"Lucro (Odds 5.0+): {stats['by_odd_range']['5.0-10.0']['profit']:.2f}")
```

---

## 📊 Entendendo o Score (0-110)

### Componentes

| Componente | Range | Interpretação |
|-----------|-------|----------------|
| **Odd Away** | 0-40 | Odds altas = visitante menos favorito = bom para lay |
| **xG Away** | 0-40 | xG baixo = menos chance de gol = bom para lay |
| **Defesa** | 0-30 | Menos shots sofridos = defesa melhor = bom para lay |

### Recomendações Finais

- 🟢 **90+/110:** CONFIANÇA → Entrar
- 🟡 **70-89/110:** CUIDADO → Entrar com proteção
- 🔴 **<70/110:** EVITAR → Aguardar melhor oportunidade

---

## 📁 Arquivos Importantes

```
data_total/
├── dados_consolidado_v2.csv ← Base de dados (2.933 jogos)
├── dados_betfair_atualizado.csv ← Backup histórico
└── dados_footystats.csv ← Backup stats

strategy_v4.py ← Classe principal
app_lay_0x1_v3.py ← Dashboard Streamlit
consolidate_teams_v2.py ← Script para consolidar dados
test_strategy_v4.py ← Testes completos
```

---

## 🧪 Rodar Testes

```bash
python test_strategy_v4.py
```

Todos os 6 testes devem passar ✅

---

## 📈 Resultados Esperados

Com base em **2.933 jogos** consolidados:

- **Win Rate Geral:** 39.5%
- **Win Rate (Odds 5.0+):** 50.9% ✅
- **Lucro (Odds 5.0+):** +151.54 ✅

**Conclusão:** Estratégia é **lucrativa em odds altas** (>5.0)

---

## 💡 Dicas

1. **Focus em Odds Altas:** Visitante com odds >5.0 é mais previsível
2. **Stake Management:** Use flat stake (aposta fixa) de 1.00 unidade
3. **Bankroll:** Mínimo 50 unidades para absorver drawdowns
4. **Daily Games:** Valide jogos do dia na aba "Validador Daily"
5. **Limite Drawdown:** Não ultrapasse -10 unidades consecutivas

---

**Desenvolvido:** 2024
**Versão:** 4.0
**Status:** ✅ Pronto para usar
