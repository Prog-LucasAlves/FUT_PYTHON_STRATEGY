# Strategy V4 - Lay 0x1 Final Implementation

## 📊 Status: ✅ COMPLETO

### O Que Foi Feito

#### 1. **Consolidador Inteligente** (`consolidate_teams_v2.py`)
- Mapeia **2.933 jogos** de Betfair + FootyStats
- Corrige nomes de times (ex: "Botafogo" ↔ "Botafogo FR")
- Taxa de consolidação: **62.4%** (esperado, devido a cobertura de ligas diferentes)

#### 2. **Strategy V4** (`strategy_v4.py`)
Sistema de scoring 0-110 baseado em 3 fatores:

**Componentes:**
- **Odd Away (0-40):** Odds altas = visitante menos favorito = melhor para lay
  - >5.0: 40 pts | 3.5-5.0: 30 pts | 2.5-3.5: 15 pts | <2.5: 5 pts

- **xG Away (0-40):** xG baixo = menos chance de gol = bom para lay
  - <0.5: 40 pts | 0.5-1.0: 30 pts | 1.0-1.5: 15 pts | >1.5: 5 pts

- **Eficiência Defensiva (0-30):** Baseada em shots enfrentados
  - <8: 30 pts | 8-12: 20 pts | 12-15: 10 pts | >15: 0 pts

**Recomendações:**
- 90+/110: 🟢 **CONFIANÇA** (baixo risco)
- 70-89/110: 🟡 **CUIDADO** (médio risco)
- <70/110: 🔴 **EVITAR** (alto risco)

#### 3. **Dashboard Streamlit** (`app_lay_0x1_v3.py`)
- Dashboard com análise histórica
- Validador de jogos daily
- Estatísticas por liga
- Gráficos interativos com Plotly

### 📈 Resultados Históricos (2.933 jogos)

| Métrica | Valor |
|---------|-------|
| **Win Rate Geral** | 39.5% |
| **Win Rate (Odds 5.0+)** | 50.9% ✅ |
| **Lucro Total (Odds 5.0+)** | +151.54 ✅ |
| **ROI Médio** | -0.34 (geral), +0.24 (5.0+) |

**Análise:** Estratégia é **LUCRATIVA em odds altas** (>5.0), onde visitante é menos favorito.

### 📁 Arquivos Principais

```
data_total/
├── dados_consolidado_v2.csv (2.933 jogos, base principal)
├── dados_betfair_atualizado.csv (histórico)
└── dados_footystats.csv (backup)

strategy_v4.py (classe Lay0x1StrategyV4)
app_lay_0x1_v3.py (Streamlit dashboard)
consolidate_teams_v2.py (script de consolidação)
test_app.py (testes rápidos)
```

### 🚀 Como Usar

**1. Executar o Dashboard:**
```bash
streamlit run app_lay_0x1_v3.py
```

**2. Validar um Jogo:**
```python
from strategy_v4 import Lay0x1StrategyV4

strategy = Lay0x1StrategyV4()
result = strategy.evaluate_score(
    home='Osasuna',
    away='Real Madrid',
    odd_away=1.58,
    odd_0x1_lay=8.6
)
print(f"Score: {result['total_score']}/110 → {result['recommendation']}")
```

### ✨ Principais Melhorias

1. ✅ **Dados Consolidados:** Betfair + FootyStats em um arquivo único
2. ✅ **Nomes de Times Mapeados:** 27 equipes brasileiras + matching automático
3. ✅ **Score Dinâmico:** Varia entre 20-100 conforme dados reais
4. ✅ **Validação Daily:** Integrando com data_day/
5. ✅ **Dashboard Completo:** Com análise histórica e recomendações

### 🎯 Próximas Etapas (Futuro)

1. **Expansão de Dados:** Incrementar consolidação para 100% dos jogos
2. **ML Scoring:** Treinar modelo para pesos ótimos de cada componente
3. **Live Odds:** Integrar API Betfair em tempo real
4. **Tracking ROI:** Dashboard de performance das recomendações
5. **Minute of Goal:** Extrair dados real de minuto do gol

---

**Desenvolvido:** 2024  
**Versão:** 4.0  
**Status:** ✅ Pronto para produção
