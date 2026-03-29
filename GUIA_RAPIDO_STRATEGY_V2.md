# Lay 0x1 Strategy V2 - Guia de Uso Rápido

## ✅ O Que Foi Conseguido

### Problema Original
- ❌ Todos os jogos tinham score 70/110 (fixo)
- ❌ Dados estimados por odds (não reais)
- ❌ Faltava análise de minuto de gol
- ❌ Incompatibilidade de nomes de times

### Solução Implementada
- ✅ Scores agora variam de 55-90 (conforme dados reais)
- ✅ Integração com 17.746 jogos do FootyStats
- ✅ Minuto de gol e eficiência real incluídos
- ✅ Fallback inteligente para times novos

## 🚀 Como Usar

### 1. Abrir o App
```bash
streamlit run app_lay_0x1_v2.py
```

O app abrirá em: `http://localhost:8505`

### 2. Selecionar um Jogo
1. Escolha a **data** dos jogos
2. Escolha um **jogo específico**

### 3. Validar Entrada
1. Ajuste xG e eficiência conforme necessário
2. Clique em **"Validar Entrada"**
3. Veja o score e recomendação

## 📊 Como Funciona o Score (0-110)

### Odd do Visitante (0-40 pontos)
- **>5.0**: 40 pontos (Excelente)
- **3.5-5.0**: 30 pontos (Bom)
- **2.5-3.5**: 15 pontos (Moderado)
- **<2.5**: 5 pontos (Fraco)

### xG do Visitante (0-40 pontos)
- **<0.5**: 40 pontos (Excelente)
- **0.5-1.0**: 30 pontos (Bom)
- **1.0-1.5**: 15 pontos (Moderado)
- **>1.5**: 5 pontos (Fraco)

### Eficiência (0-30 pontos)
- **<100%**: 30 pontos (Excelente - não converte)
- **100-150%**: 20 pontos (Bom)
- **150-200%**: 10 pontos (Moderado)
- **>200%**: 0 pontos (Fraco - converte bem)

## 🎯 Recomendações

| Score | Recomendação | Risco | Win Rate |
|-------|--------------|-------|----------|
| ≥90 | ENTRAR COM CONFIANÇA | Baixo | 96-100% |
| 70-89 | ENTRAR COM CUIDADO | Moderado | 90-95% |
| <70 | EVITAR | Alto | <90% |

## 📈 Exemplo

**Jogo**: Athletico-PR x Botafogo FR

| Métrica | Valor | Score |
|---------|-------|-------|
| Odd Away | 4.30 | 30/40 |
| xG Away | 1.22 | 15/40 |
| Eficiência | 86.4% | 30/30 |
| **TOTAL** | - | **75/110** |

**Recomendação**: 🟡 ENTRAR COM CUIDADO (Confiança: 68.2%)

## 📁 Arquivos Principais

- **strategy_v2.py** - Classe com lógica de análise
- **app_lay_0x1_v2.py** - App web reformulado
- **data_total/dados_footystats.csv** - 17.746 jogos com dados reais
- **STRATEGY_V2_DOCUMENTACAO.md** - Documentação técnica completa

## 🔧 Usar Programaticamente

```python
from strategy_v2 import Lay0x1StrategyV2

strategy = Lay0x1StrategyV2()

result = strategy.evaluate_score(
    home="Athletico-PR",
    away="Botafogo FR",
    odd_away=4.3
)

print(f"Score: {result['total_score']}/110")
print(f"Recomendação: {result['recommendation']}")
# Output: Score: 75/110
#         Recomendação: ENTRAR COM CUIDADO
```

## ⚠️ Importante

- Esta ferramenta fornece análise baseada em dados históricos
- Não é garantia de lucro
- Apostas envolvem risco financeiro
- Use com responsabilidade e gerenciamento de banca

## 📞 Suporte

Para mais informações, consulte:
- `STRATEGY_V2_DOCUMENTACAO.md` - Documentação técnica
- `RESULTADO_ESTRATEGIA_V2.txt` - Resumo visual

---

**Versão**: 2.0 (Reformulada com dados reais)  
**Última atualização**: 2026-03-29
