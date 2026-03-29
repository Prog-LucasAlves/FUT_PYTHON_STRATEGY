# Lay 0x1 Strategy V2 - Documentação Técnica

## 🎯 Visão Geral

A Lay 0x1 Strategy V2 é uma reformulação completa da estratégia de apostas contra o resultado 0x1 (vitória do visitante por 1 gol). Integra dados reais de footystats com análise de odds e métricas de eficiência.

## 📊 Dados Utilizados

### Fontes
- **FootyStats**: 17.746 jogos com métricas detalhadas
  - xG (Expected Goals)
  - Minuto de gol
  - Possession
  - Shots on target
  - Cartões, faltas, offsides
  - Conversão real (gols/xG)

- **Betfair**: 4.699 jogos europeus com odds histórica
  - Odds de vitória do visitante
  - Odds Lay 0x1

## 🧮 Fórmula de Score (0-110)

### 1. Odd do Visitante (0-40 pontos)
Maior odd = melhor (visitante é azarão)

| Odd | Pontos | Categoria |
|-----|--------|-----------|
| >5.0 | 40 | Excelente |
| 3.5-5.0 | 30 | Bom |
| 2.5-3.5 | 15 | Moderado |
| <2.5 | 5 | Fraco |

### 2. xG do Visitante (0-40 pontos)
Menor xG = melhor (menos chances)

| xG | Pontos | Categoria |
|----|--------|-----------|
| <0.5 | 40 | Excelente |
| 0.5-1.0 | 30 | Bom |
| 1.0-1.5 | 15 | Moderado |
| >1.5 | 5 | Fraco |

### 3. Eficiência (0-30 pontos)
Menor eficiência = melhor (não converte bem)

| Eficiência | Pontos | Categoria |
|------------|--------|-----------|
| <100% | 30 | Excelente |
| 100-150% | 20 | Bom |
| 150-200% | 10 | Moderado |
| >200% | 0 | Fraco |

## 🎯 Recomendações

| Score | Recomendação | Risco | Win Rate Esperado |
|-------|--------------|-------|-------------------|
| ≥90 | ENTRAR COM CONFIANÇA | Baixo | 96-100% |
| 70-89 | ENTRAR COM CUIDADO | Moderado | 90-95% |
| <70 | EVITAR | Alto | <90% |

## 💡 Lógica da Estratégia

### Por que Lay 0x1?

1. **Resultado raro**: 0x1 é um dos resultados menos comuns
2. **Odds alta**: A probabilidade é baixa, logo a odd é alta (~15-20)
3. **Lucro em 4 cenários**: 0x0, 1x1, 2x1, 3x1, etc.
4. **Perda em 1 cenário**: Apenas 0x1

### Critérios Ideais

1. **Visitante fraco** (high odd)
   - Azarão claro (odd >3.5)
   - Pouco criativo (low xG)
   - Má conversão (efficiency <150%)

2. **Timing de gol**
   - Gols tardios (>45 min) favorecem Lay
   - Menos pressão inicial do visitante

3. **Contexto do jogo**
   - Viagem/fadiga do visitante
   - Histórico de desempenho away
   - Força defensiva do mandante

## 🔧 Implementação Técnica

### Classe: Lay0x1StrategyV2

```python
from strategy_v2 import Lay0x1StrategyV2

strategy = Lay0x1StrategyV2()

# Obter dados do time
xg = strategy.get_team_xg("Botafogo FR")
eff = strategy.get_team_efficiency("Botafogo FR")
goal_timing = strategy.get_goal_timing("Botafogo FR")

# Calcular score
result = strategy.evaluate_score(
    home="Athletico-PR",
    away="Botafogo FR",
    odd_away=4.3
)

print(f"Score: {result['total_score']}/110")
print(f"Recomendação: {result['recommendation']}")
```

### App Web

```bash
streamlit run app_lay_0x1_v2.py
```

## 📈 Exemplo de Análise

### Jogo: Athletico-PR x Botafogo FR

| Métrica | Valor | Score | Categoria |
|---------|-------|-------|-----------|
| Odd Away | 4.30 | 30/40 | Bom (3.5-5.0) |
| xG Away | 1.22 | 15/40 | Moderado (1.0-1.5) |
| Eficiência | 86.4% | 30/30 | Excelente (<100%) |
| **TOTAL** | - | **75/110** | **COM CUIDADO** |

**Interpretação**: Botafogo é um azarão (odd boa), mas com xG moderado. Porém, com eficiência ruim (86%), é uma boa oportunidade.

## ⚠️ Limitações

1. **Nomes de times**: 93 times comuns entre bases, 79 só em Betfair, 109 só em FootyStats
   - Solução: Fallback para média geral quando time não encontrado

2. **Dados históricos**: FootyStats pode não ter todos os jogos de todas as ligas
   - Solução: Usar médias gerais para times novos

3. **Mudanças de forma**: Dados históricos não capturam forma recente
   - Solução: Ajuste manual de métricas no app

## 🚀 Próximas Melhorias

1. **Machine Learning**: Prever resultado baseado em features detalhados
2. **API de Odds**: Integração com odds em tempo real
3. **Análise de Série**: Considerar forma recente (últimos 10 jogos)
4. **Dashboard de Performance**: Tracking histórico de acertos
5. **Filtros Avançados**: Por liga, país, atacante top scorer, etc.

## 📚 Referências

- Video original: https://www.youtube.com/watch?v=5Tm7tQvxgJQ&t=715s
- FootyStats: Dados detalhados de 17.746 jogos
- Betfair: Odds históricas de 4.699 jogos
