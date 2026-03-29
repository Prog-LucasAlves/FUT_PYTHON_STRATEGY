# 🎮 Como Usar Strategy V4

## ⚡ TL;DR (Início Rápido em 2 minutos)

```bash
# 1. Executar o Dashboard
streamlit run app_lay_0x1_v3.py

# 2. Abrir no navegador
# http://localhost:8501

# 3. Ir para aba "Validador Daily"
# 4. Selecionar um jogo
# 5. Clicar "VALIDAR ENTRADA"
```

---

## 📋 Índice

1. [Executar Dashboard](#executar-dashboard)
2. [Usar Programaticamente](#usar-programaticamente)
3. [Validar Jogos Daily](#validar-jogos-daily)
4. [Rodar Testes](#rodar-testes)
5. [Entender Scores](#entender-scores)
6. [Troubleshooting](#troubleshooting)

---

## 🖥️ Executar Dashboard

### Pré-requisitos
```bash
pip install streamlit pandas numpy plotly
```

### Executar
```bash
cd d:\Sports\FUT_PYTHON_STRATEGY
streamlit run app_lay_0x1_v3.py
```

### Resultado Esperado
```
You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

### Abrir Navegador
- Clique em: `http://localhost:8501`
- Ou copie a URL acima

### Funcionalidades

#### Tab 1: Dashboard
- Win rate por faixa de odds
- Lucro por faixa de odds
- Distribuição de xG
- Estatísticas por liga

#### Tab 2: Validador Daily
- Selecione data dos jogos
- Escolha um jogo
- Clique "VALIDAR ENTRADA"
- Receba recomendação com score

#### Tab 3: Sobre
- Explicação da estratégia
- Componentes do score
- Validação histórica

---

## 🐍 Usar Programaticamente

### Instalar dependências
```bash
pip install pandas numpy
```

### Exemplo 1: Score Simples
```python
from strategy_v4 import Lay0x1StrategyV4

# Criar estratégia
strategy = Lay0x1StrategyV4()

# Validar um jogo
result = strategy.evaluate_score(
    home='Manchester United',
    away='Liverpool',
    odd_away=2.50,
    odd_0x1_lay=11.5
)

# Exibir resultado
print(f"Score: {result['total_score']}/110")
print(f"Recomendação: {result['recommendation']}")
print(f"Risco: {result['risk']}")
print(f"xG Visitante: {result['xg_away']:.2f}")
```

**Output esperado:**
```
Score: 75/110
Recomendação: CUIDADO
Risco: Médio
xG Visitante: 1.20
```

---

### Exemplo 2: Analisar Múltiplos Jogos
```python
import pandas as pd
from strategy_v4 import Lay0x1StrategyV4

strategy = Lay0x1StrategyV4()

# Carregar arquivo com jogos do dia
games = pd.read_csv("data_day/dados_day_betfair_2024-12-25.csv", sep=";")

# Validar todos os jogos
results = []
for _, game in games.iterrows():
    score = strategy.evaluate_score(
        home=game['Home'],
        away=game['Away'],
        odd_away=game['Odd_A_Back'],
        odd_0x1_lay=game['Odd_CS_0x1_Lay']
    )
    results.append({
        'Jogo': f"{game['Home']} vs {game['Away']}",
        'Score': score['total_score'],
        'Recomendação': score['recommendation'],
        'xG_Away': score['xg_away']
    })

df_results = pd.DataFrame(results)

# Filtrar apenas CONFIANÇA
high_confidence = df_results[df_results['Score'] >= 90]
print(f"Jogos com CONFIANÇA: {len(high_confidence)}")
print(high_confidence)
```

---

### Exemplo 3: Estatísticas Históricas
```python
from strategy_v4 import Lay0x1StrategyV4

strategy = Lay0x1StrategyV4()
stats = strategy.get_historical_stats()

print(f"Total de jogos: {stats['total_games']}")
print(f"Win Rate Geral: {stats['lay_0x1_winrate']:.1f}%")
print(f"Lucro Total: {stats['total_profit']:.2f}")

print("\nPor faixa de odds:")
for odd_range, data in stats['by_odd_range'].items():
    print(f"  {odd_range}: {data['count']} jogos, {data['winrate']:.1f}% WR, {data['profit']:.2f} profit")
```

**Output esperado:**
```
Total de jogos: 2933
Win Rate Geral: 39.5%
Lucro Total: -990.20

Por faixa de odds:
  0.0-2.5: 727 jogos, 24.8% WR, -147.32 profit
  2.5-3.5: 657 jogos, 34.2% WR, -101.98 profit
  3.5-5.0: 656 jogos, 43.3% WR, -863.68 profit
  5.0-10.0: 619 jogos, 50.9% WR, 151.54 profit
```

---

## ✅ Validar Jogos Daily

### 1. Preparar arquivo de jogos
Coloque arquivo em: `data_day/dados_day_betfair_YYYYMMDD.csv`

Colunas necessárias:
- Home
- Away
- Odd_A_Back (odd do visitante)
- Odd_CS_0x1_Lay
- League (opcional)

### 2. Executar Dashboard
```bash
streamlit run app_lay_0x1_v3.py
```

### 3. Na aba "Validador Daily"
1. Selecione a data
2. Escolha um jogo
3. Clique "VALIDAR ENTRADA"
4. Leia a recomendação

### 4. Interpretar Resultado
- 🟢 90+/110: CONFIANÇA → Entrar com confiança
- 🟡 70-89/110: CUIDADO → Entrar com proteção
- 🔴 <70/110: EVITAR → Aguardar melhor oportunidade

---

## 🧪 Rodar Testes

### Executar
```bash
cd d:\Sports\FUT_PYTHON_STRATEGY
python test_strategy_v4.py
```

### Esperado
```
============================================================
🧪 TEST SUITE - Strategy V4 & App V3
============================================================

✅ TODOS OS TESTES PASSARAM!
```

### Testes Incluem
1. Carregamento da estratégia
2. Avaliação de scores
3. Estatísticas históricas
4. Dados consolidados
5. Validação app
6. Stats por time

---

## 📊 Entender Scores

### Score 0-110

**Componente 1: Odd Away (0-40 pontos)**
```
Odd > 5.0   → 40 pts ✅ (visitante muito menos favorito)
3.5-5.0     → 30 pts
2.5-3.5     → 15 pts
Odd < 2.5   → 5 pts  ❌ (visitante favorito)
```

**Componente 2: xG Away (0-40 pontos)**
```
xG < 0.5    → 40 pts ✅ (chance muito baixa)
0.5-1.0     → 30 pts
1.0-1.5     → 15 pts
xG > 1.5    → 5 pts  ❌ (chance alta)
```

**Componente 3: Defesa (0-30 pontos)**
```
<8 shots    → 30 pts ✅ (defesa forte)
8-12 shots  → 20 pts
12-15 shots → 10 pts
>15 shots   → 0 pts  ❌ (defesa fraca)
```

### Exemplo Prático
```
Jogo: Mallorca vs Granada CF
Odd_A_Back: 5.30 (forte) → 40 pts
xG_A: 0.87 (baixo) → 30 pts
Shots_A: 10 (médio) → 20 pts
━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: 90/110 → CONFIANÇA ✅
```

---

## 🔧 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
```

### Erro: "FileNotFoundError: dados_consolidado_v2.csv"
Certifique-se que está no diretório correto:
```bash
cd d:\Sports\FUT_PYTHON_STRATEGY
```

### Erro: "KeyError: 'Home'"
Verifique que seu CSV tem as colunas necessárias com nomes corretos.

### Dashboard não abre em localhost:8501
- Tente: http://127.0.0.1:8501
- Ou copy a URL impressa no terminal

### Scores todos iguais (70/110)
Você está usando a versão V3 antiga. Use V4:
```bash
streamlit run app_lay_0x1_v3.py
```

---

## 📚 Documentos Adicionais

- **QUICKSTART_V4.md** - Guia rápido
- **STRATEGY_V4_README.md** - Documentação técnica
- **STRATEGY_V4_FINAL.md** - Resumo detalhado
- **test_strategy_v4.py** - Exemplos funcionais

---

## 💬 Resumo

| Tarefa | Comando |
|--------|---------|
| Executar Dashboard | `streamlit run app_lay_0x1_v3.py` |
| Testar Strategy | `python test_strategy_v4.py` |
| Validar um jogo | Ver "Exemplo 1" acima |
| Analisar múltiplos | Ver "Exemplo 2" acima |
| Estatísticas | Ver "Exemplo 3" acima |

---

**✅ Você está pronto para usar Strategy V4!**

Dúvidas? Consulte os documentos ou rode os exemplos.
