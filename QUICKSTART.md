# Quick Start - Estratégia Lay 0x1

## 🚀 Começar em 5 Minutos

### 1. Visualizar o Dashboard

```bash
cd d:\Sports\FUT_PYTHON_STRATEGY
streamlit run app_lay_0x1.py
```

Abra o navegador em: `http://localhost:8501`

**O que você verá:**
- KPIs principais (Win Rate 92.5%, Lucro 9.473,90)
- Gráficos de performance
- Análise por faixas de odds/xG
- Critérios de entrada recomendados

---

### 2. Validar um Jogo do Dia

```python
from validate_entry import Lay0x1Validator

# Criar validador
validator = Lay0x1Validator()

# Validar seu jogo
result = validator.validate_match(
    home="Time Mandante",
    away="Time Visitante",
    odd_away=3.5,           # Odd de vitória do visitante
    xg_away=0.8,            # Expected Goals do visitante
    efficiency_away=120.0   # Opcional: %conversão
)

# Ver resultado
validator.print_validation(result)
```

**Output esperado:**
```
Score: 75/110
[ENTRAR COM CUIDADO]
Histórico Semelhante: 85.3% Win Rate
```

---

### 3. Entender os Critérios

**Score Total (0-110 pontos):**

| Score | Recomendação | Ação |
|---|---|---|
| 90+ | ✅ Excelente | ENTRAR COM CONFIANÇA |
| 70-89 | 🟡 Bom | ENTRAR COM CUIDADO |
| 50-69 | ⚠️ Moderado | CONSIDERAR COM CAUTELA |
| <50 | 🔴 Fraco | EVITAR |

**Cada Critério Vale:**

| Critério | Faixa | Pontos |
|---|---|---|
| **Odds Visitante** | >5.0 | 40 |
| | 3.5-5.0 | 30 |
| | 2.5-3.5 | 15 |
| | <2.5 | 5 |
| **xG Visitante** | <0.5 | 40 |
| | 0.5-1.0 | 30 |
| | 1.0-1.5 | 15 |
| | >1.5 | 5 |
| **Eficiência** | <100% | 30 |
| | 100-150% | 20 |
| | 150-200% | 10 |
| | >200% | 0 |

---

### 4. Exemplo Prático

**Cenário:** Você quer apostar contra 0x1 em: Barcelona vs Real Madrid

```
Dados encontrados:
- Barcelona é mandante
- Real Madrid (visitante) tem odd 2.5 (low)
- xG do Real Madrid: 1.8 (alto)
- Eficiência Real Madrid: 165% (alta)
```

**Validação:**
```python
validator.validate_match(
    home="Barcelona",
    away="Real Madrid",
    odd_away=2.5,
    xg_away=1.8,
    efficiency_away=165.0
)
```

**Score:** 20/110 → EVITAR 🔴

**Por quê?**
- Odd baixa (5 pts) + xG alto (5 pts) + Eficiência alta (10 pts) = Risco alto

---

### 5. Dados Importantes a Saber

**Win Rate por Faixa de Odds:**
- Odds > 5.0: **96.7%** ✅✅ (MELHOR)
- Odds 3.5-5.0: **93.8%** ✅
- Odds 2.5-3.5: **90.7%** ✅
- Odds 2.0-2.5: **89.5%** ⚠️
- Odds < 2.0: **86.5%** ⚠️ (PIOR)

**Win Rate por Faixa de xG:**
- xG < 0.5: **100%** ✅✅ (MELHOR)
- xG 1.0-1.5: **100%** ✅✅ (MELHOR)
- xG 0.5-1.0: **78.6%** ⚠️ (PIOR)

**Conclusão:**
- **Prefira odds altas + xG baixo** = Segurança máxima (96-100%)
- **Evite odds baixas + xG alto** = Risco elevado (78.6%)

---

### 6. Stake Management

**Exemplo com R$ 100 de stake:**

```
Stake por jogo: R$ 100
Odds típico 0x1: 15.50
Ganho por jogo (96%): R$ 96

Bankroll recomendado: 50 × R$ 100 = R$ 5.000

Lucro esperado por mês (20 jogos):
20 × R$ 96 = R$ 1.920 (38.4% ROI)
```

**Regras de Risco:**
- Max drawdown: -10 unidades
- Stop loss: Parar por 24h se perder 10 seguidas
- Never exceed: 2-5% do bankroll por jogo

---

### 7. Próximas Ações

**Hoje:**
- [ ] Visualizar dashboard
- [ ] Entender os critérios
- [ ] Validar 3-5 jogos de exemplo

**Semana que vem:**
- [ ] Coletar dados de jogos do dia (odds, xG)
- [ ] Usar validador para cada jogo
- [ ] Registrar previsões vs resultados
- [ ] Revisar acertos/erros

**Próximo mês:**
- [ ] Validar estatísticas em novo sample
- [ ] Ajustar thresholds se necessário
- [ ] Começar a apostar com micro-stakes

---

## 📊 Arquivos Principais

```
FUT_PYTHON_STRATEGY/
├── app_lay_0x1.py                          # Dashboard Streamlit
├── validate_entry.py                        # Validador de Jogos
├── README_ESTRATEGIA.md                    # Guia Completo
├── QUICKSTART.md                           # Este arquivo
│
└── data_total/
    ├── dados_betfair_atualizado.csv        # Dados + metricas
    ├── analise_faixas_odds.csv
    ├── analise_faixas_xg.csv
    ├── analise_faixas_efficiency.csv
    └── analise_combinada.csv
```

---

## 🎯 Checklist de Validação

Antes de apostar em um jogo, verifique:

- [ ] **Odd do visitante:** Você obteve de uma casa confiável?
- [ ] **xG do visitante:** Verificou em Understat ou similar?
- [ ] **Score:** Resultado >= 70/110?
- [ ] **Histórico:** Performance similar matches é >85%?
- [ ] **Bankroll:** Você tem 50+ unidades?
- [ ] **Stake:** Não excede 5% do seu bankroll?
- [ ] **Sentimento:** Você está calmo/racional?

Se tudo ✅, você pode APOSTAR com confiança!

---

## ❓ FAQ Rápido

**P: Por que 0x1 específico?**
R: 0x1 é um dos 28+ possíveis resultados. Odds altas (15-100+) porque é raro.

**P: Qual é a melhor configuração?**
R: Odds > 5.0 + xG < 1.0 → Win Rate 96-100%

**P: Quanto apostar?**
R: Comece com 2-5% do seu bankroll por jogo.

**P: Tenho 3 meses de dados?**
R: Não, você tem 4.699 jogos (histórico). Novo período precisa validação.

**P: E se meu xG é uma estimativa?**
R: Use 70% do valor estimated como conservative. Revise com dados reais.

---

## 🚨 Disclaimer

- Apostas envolvem risco financeiro real
- Histórico não garante resultados futuros
- Educação, não recomendação de apostas
- Sempre jogue responsavelmente

---

**Pronto para começar?** 🚀

```bash
streamlit run app_lay_0x1.py
```
