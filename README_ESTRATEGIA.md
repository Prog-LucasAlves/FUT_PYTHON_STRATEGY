# Estratégia de Lay 0x1 (Contra 0x1)

## 📊 Visão Geral

Uma estratégia de apostas contra o resultado específico **0x1** (visitante ganha por 1x0). Baseada em análise histórica de 4.699 jogos com:

- **Win Rate: 92.5%** ✅
- **Lucro Total: 9.473,90 unidades** 💰
- **Lucro Médio por Jogo: 2.02 unidades** 📈

---

## 🎯 Como Funciona

### O Que é Lay 0x1?

**Lay (Apostar Contra)** significa você ganha quando o resultado NÃO é o especificado.

- **Você ganha se:** O resultado for QUALQUER COISA menos 0x1
  - Exemplos: 1x0, 1x1, 2x0, 2x1, 3x0, 0x0, etc.
  
- **Você perde se:** O resultado for EXATAMENTE 0x1
  - Probabilidade histórica: ~7.5%

### Por Que Funciona?

1. **Odds Altas**: Resultados específicos têm odds altas (8-100+)
2. **Muitas Possibilidades**: 0x1 é apenas UMA das muitas combinações de gols
3. **Probabilidade Favorável**: ~92.5% dos jogos não são 0x1

---

## 📈 Análise por Faixas

### Performance por Odds do Visitante

| Faixa de Odds | Jogos | Win Rate | Lucro Total | Lucro/Jogo |
|---|---|---|---|---|
| **Alta (>5.0)** | 1.421 | 96.7% ✅ | 2.555,54 | 1.80 |
| **Média-Alta (3.5-5.0)** | 1.040 | 93.8% ✅ | 2.743,80 | 2.64 |
| **Média (2.5-3.5)** | 1.058 | 90.7% ✅ | 1.948,60 | 1.84 |
| **Baixa-Média (2.0-2.5)** | 513 | 89.5% ✅ | 942,94 | 1.84 |
| **Baixa (<2.0)** | 667 | 86.5% ⚠️ | 1.283,02 | 1.92 |

### Performance por xG do Visitante

| Faixa de xG | Jogos | Win Rate | Lucro Total | Lucro/Jogo |
|---|---|---|---|---|
| **Muito Baixo (<0.5)** | 1.400 | 100.0% ✅✅ | 1.344,00 | 0.96 |
| **Baixo (0.5-1.0)** | 1.658 | 78.6% ⚠️ | 6.554,54 | 3.95 |
| **Médio (1.0-1.5)** | 1.040 | 100.0% ✅✅ | 998,40 | 0.96 |
| **Alto (1.5-2.0)** | 402 | 100.0% ✅✅ | 385,92 | 0.96 |
| **Muito Alto (>2.0)** | 199 | 100.0% ✅✅ | 191,04 | 0.96 |

---

## ✅ Critérios de Entrada Recomendados

### 🟢 ENTRADAS IDEAIS (Score 90+/110)

**Condições:**
- Odd do Visitante > 5.0
- xG do Visitante < 1.0
- Eficiência < 150%

**Ação:** APOSTAR COM CONFIANÇA

**Histórico:**
- Win Rate: 96-100%
- Lucro Médio: 1.80-2.07

---

### 🟡 ENTRADAS MODERADAS (Score 70-89/110)

**Condições:**
- Odd do Visitante 3.5-5.0
- xG do Visitante < 1.5
- Eficiência 100-150%

**Ação:** APOSTAR COM CUIDADO

**Histórico:**
- Win Rate: 90-95%
- Lucro Médio: 1.84-2.64

---

### 🔴 EVITAR (Score <50/110)

**Condições:**
- Odd do Visitante < 2.5
- xG do Visitante > 1.5
- Eficiência > 150%

**Ação:** EVITAR OU REDUZIR STAKE

**Histórico:**
- Win Rate: 78.6-90%
- Risco Elevado

---

## 💰 Gerenciamento de Risco

### Stake Management

```
Recomendado: FLAT STAKE (aposta fixa)

Exemplo com R$ 100:
- Stake por jogo: R$ 100 (1 unidade)
- Odds 0x1: ~15.50 (Betfair)
- Ganho por jogo: R$ 96 (0.96 unidades)
```

### Bankroll

**Mínimo recomendado:** 50 unidades

```
Exemplo:
Stake: R$ 100
Bankroll: 50 × R$ 100 = R$ 5.000
```

### Stop Loss

- **Drawdown máximo:** -10 unidades consecutivas
- **Ação:** Parar por 24h e revisar

### Target de ROI

- **Esperado:** 2%+ por jogo
- **Você teve:** 2.02% (EXCELENTE)
- **Meta anual:** 100-200% ROI

---

## 🔍 Como Validar um Jogo

### Passo 1: Reunir Dados

Para um jogo do dia, você precisa de:

1. **Odd do Visitante** (Vitória simples Away)
   - Onde encontrar: Betfair, Bet365, etc.
   
2. **xG do Visitante** (Expected Goals)
   - Onde encontrar: Understat, Wyscout, Stats Bomb
   - Fórmula: Histórico do time + estatísticas da temporada
   
3. **Eficiência do Visitante** (opcional)
   - Cálculo: (Gols / xG) × 100

### Passo 2: Usar o Validador

```python
from validate_entry import Lay0x1Validator

validator = Lay0x1Validator()

result = validator.validate_match(
    home="Time da Casa",
    away="Visitante",
    odd_away=3.5,
    xg_away=0.8,
    efficiency_away=120.0
)

validator.print_validation(result)
```

### Passo 3: Analisar o Score

- **90+/110:** ENTRAR COM CONFIANÇA ✅
- **70-89/110:** ENTRAR COM CUIDADO 🟡
- **50-69/110:** CONSIDERAR COM CAUTELA ⚠️
- **<50/110:** EVITAR 🔴

---

## 📱 Dashboard Streamlit

Para visualizar todas as análises em tempo real:

```bash
streamlit run app_lay_0x1.py
```

O dashboard inclui:

1. **Dashboard Principal**
   - KPIs principais
   - Gráficos de distribuição
   - Lucro acumulado

2. **Análise por Faixas**
   - Performance por odds
   - Performance por xG
   - Heatmaps Odds vs xG

3. **Estratégia Recomendada**
   - Critérios de entrada
   - Dicas de gerenciamento

4. **Detalhes de Jogos**
   - Filtros customizáveis
   - Download de dados

5. **Análise Avançada**
   - Correlações
   - Box plots
   - Estatísticas

---

## 📊 Dados do Histórico

### Onde Estão os Dados?

- **CSV Principal:** `data_total/dados_betfair_atualizado.csv`
- **Análises:** `data_total/analise_*.csv`

### Colunas Principais

```
Home, Away                    # Nomes dos times
Odd_H_Back, Odd_A_Back       # Odds de vitória
Odd_CS_0x1_Lay               # Odds do Lay 0x1
Goals_H_FT, Goals_A_FT       # Resultado final
xG_Home, xG_Away             # Expected Goals
Efficiency_Home/Away         # % de conversão
Lay_0x1_Result               # WIN/LOSS
Lay_0x1_Profit               # Lucro da aposta
```

---

## 🎓 Próximos Passos

### Curto Prazo (Próxima Semana)

1. ✅ Teste o validador com 5-10 jogos do dia
2. ✅ Compare previsões com resultados reais
3. ✅ Ajuste critérios se necessário

### Médio Prazo (Próximo Mês)

1. Coletar dados de novos jogos
2. Validar estatísticas em sample novo
3. Refinar modelo com feedback

### Longo Prazo (Próximos Meses)

1. Implementar automação de coleta
2. Integrar com API de betting
3. Criar sistema de alertas

---

## ⚠️ Disclaimer

- Apostas envolvem risco
- Histórico não garante resultados futuros
- Adapte stake ao seu bankroll e risco tolerance
- Use sempre proteções de stop loss
- Nunca aposte mais do que pode perder

---

## 📞 Suporte

Para dúvidas ou sugestões sobre a estratégia, revise:

1. Este arquivo README
2. Dashboard Streamlit
3. Análises em `data_total/`
4. Script `validate_entry.py`

---

**Última Atualização:** 2024
**Dados:** 4.699 jogos analisados
**Performance:** 92.5% Win Rate | 9.473,90 Lucro Total
