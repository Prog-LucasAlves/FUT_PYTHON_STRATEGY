"""
Lay 0x1 Strategy Dashboard - Versão 2 Reformulada
Integra dados de footystats com scores reais
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from strategy_v2 import Lay0x1StrategyV2

st.set_page_config(
    page_title="Lay 0x1 Strategy Dashboard V2",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== SIDEBAR =====
st.sidebar.markdown("# ⚽ Lay 0x1 Strategy")
st.sidebar.markdown("Análise de apostas contra o resultado 0x1")
st.sidebar.divider()

# ===== HEADER PRINCIPAL =====
st.title("⚽ Lay 0x1 Strategy Dashboard")
st.markdown("**Validador de Entrada - Versão 2 com Dados Reais de FootyStats**")


# ===== CACHE =====
@st.cache_data
def load_strategy():
    """Carrega estratégia uma vez"""
    return Lay0x1StrategyV2()


@st.cache_data
def get_available_dates():
    """Obtém datas disponíveis nos arquivos"""
    data_dir = Path("data_day")
    dates = []

    if data_dir.exists():
        for file in data_dir.glob("dados_day_betfair_*.csv"):
            date_str = file.name.replace("dados_day_betfair_", "").replace(".csv", "")
            try:
                dates.append(date_str)
            except:
                pass

    return sorted(dates, reverse=True)


# ===== CARREGAR DADOS =====
strategy = load_strategy()
available_dates = get_available_dates()

if not available_dates:
    st.error("❌ Nenhum arquivo de jogo encontrado em data_day/")
    st.stop()

# ===== SELETOR DE DATA =====
st.divider()
st.subheader("📅 Selecione a Data")

col1, col2 = st.columns([3, 1])

with col1:
    data_selecionada = st.selectbox(
        "Data dos jogos:",
        available_dates,
        index=0,
        help="Selecione a data para validar os jogos",
    )

with col2:
    st.markdown("---")

# ===== CARREGAR JOGOS DO DIA =====
arquivo = f"data_day/dados_day_betfair_{data_selecionada}.csv"

try:
    df_day = pd.read_csv(arquivo, sep=";")
    st.success(f"✅ {len(df_day)} jogo(s) carregado(s) para {data_selecionada}")
except FileNotFoundError:
    st.error(f"❌ Arquivo não encontrado: {arquivo}")
    st.stop()

if df_day.empty:
    st.warning("⚠️ Nenhum jogo disponível para esta data")
    st.stop()

# ===== SELETOR DE JOGO =====
st.divider()
st.subheader("⚽ Selecione um Jogo")

# Criar opções
opcoes_jogos = {}
for idx, row in df_day.iterrows():
    opcao_texto = f"{row['Home']} x {row['Away']} ({row['League']}) - {row['Time']}"
    opcoes_jogos[opcao_texto] = idx

# Seletor
jogo_selecionado = st.selectbox(
    "Jogo:",
    list(opcoes_jogos.keys()),
    help="Escolha um jogo para análise",
)

idx_jogo = opcoes_jogos[jogo_selecionado]
row = df_day.iloc[idx_jogo]

# ===== DADOS DO JOGO =====
st.divider()
st.subheader("📊 Informações do Jogo")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Mandante", row["Home"])

with col2:
    st.metric("Visitante", row["Away"])

with col3:
    st.metric("Liga", row["League"])

with col4:
    st.metric("Horário", row["Time"])

# ===== ANÁLISE =====
st.divider()
st.subheader("🎯 Análise - Lay 0x1")

# Obter dados
home_team = row["Home"]
away_team = row["Away"]
odd_away_default = float(row["Odd_A_Back"])
odd_0x1_default = float(row["Odd_CS_0x1_Lay"])

# Inputs
col1, col2, col3 = st.columns(3)

with col1:
    odd_away = st.number_input(
        "Odd do Visitante (Away Back)",
        value=odd_away_default,
        min_value=1.0,
        max_value=50.0,
        step=0.1,
        help="Odd de vitória simples do visitante",
    )

with col2:
    odd_0x1 = st.number_input(
        "Odd Lay 0x1 (Back)",
        value=odd_0x1_default,
        min_value=1.0,
        max_value=100.0,
        step=0.5,
        help="Odd que você vai fazer lay",
    )

with col3:
    st.metric("Odd 0x1 Lay", f"{odd_0x1_default:.2f}")

# Dados do time
st.divider()
st.subheader("📈 Métricas do Time (Visitante)")

xg_real = strategy.get_team_xg(away_team)
eff_real = strategy.get_team_efficiency(away_team)
goal_timing = strategy.get_goal_timing(away_team)
team_info = strategy.get_team_info(away_team)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("xG Médio (Away)", f"{xg_real:.3f}")

with col2:
    st.metric("Eficiência", f"{eff_real:.1f}%")

with col3:
    st.metric("Minuto Gol Médio", f"{goal_timing:.0f} min")

with col4:
    if team_info:
        st.metric("Partidas (Away)", f"{team_info['Matches']}")
    else:
        st.metric("Partidas", "N/A")

# Inputs para ajuste
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    xg_ajuste = st.slider(
        "Ajuste xG",
        min_value=0.0,
        max_value=5.0,
        value=round(xg_real, 2),
        step=0.1,
        help="Ajuste conforme análise pessoal",
    )

with col2:
    eff_ajuste = st.slider(
        "Ajuste Eficiência (%)",
        min_value=50,
        max_value=250,
        value=int(round(eff_real)),
        step=5,
        help="Ajuste conforme forma atual",
    )

with col3:
    goal_timing_ajuste = st.slider(
        "Ajuste Min. Gol",
        min_value=10,
        max_value=90,
        value=int(round(goal_timing)),
        step=5,
        help="Ajuste do minuto médio de gol",
    )

# ===== BOTÃO DE VALIDAÇÃO =====
st.divider()

if st.button("🎯 Validar Entrada", use_container_width=True, type="primary"):
    # Calcular score
    result = strategy.evaluate_score(
        home=home_team,
        away=away_team,
        odd_away=odd_away,
        xg_away=xg_ajuste,
        efficiency_away=eff_ajuste,
        goal_timing=goal_timing_ajuste,
    )

    # ===== RESULTADO PRINCIPAL =====
    st.divider()
    st.subheader("✅ Resultado da Validação")

    col1, col2, col3 = st.columns(3)

    with col1:
        score_pct = result["confidence"]
        color = "🟢" if score_pct >= 85 else "🟡" if score_pct >= 65 else "🔴"

        st.markdown(
            f"""
        <div style="text-align: center; padding: 30px; background-color: #1f77b414; border-radius: 15px;">
            <h1 style="margin: 0; font-size: 48px;">{result['total_score']}/110</h1>
            <p style="margin: 10px 0; font-size: 18px; font-weight: bold;">Score Total</p>
            <p style="margin: 0; font-size: 14px;">Confiança: {score_pct:.1f}%</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        rec = result["recommendation"]
        color_map = {
            "ENTRAR COM CONFIANCA": "#00800040",
            "ENTRAR COM CUIDADO": "#FFA50040",
            "EVITAR": "#FF000040",
        }
        bg_color = color_map.get(rec, "#00800040")

        st.markdown(
            f"""
        <div style="text-align: center; padding: 30px; background-color: {bg_color}; border-radius: 15px;">
            <p style="margin: 0; font-size: 12px;">Recomendação</p>
            <p style="margin: 10px 0; font-size: 16px; font-weight: bold;">{rec}</p>
            <p style="margin: 0; font-size: 13px;">Baseado em análise real</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        pl_esperado = odd_0x1 - 1  # Lucro/Loss aproximado
        st.markdown(
            f"""
        <div style="text-align: center; padding: 30px; background-color: #9467bd40; border-radius: 15px;">
            <p style="margin: 0; font-size: 12px;">Lucro Estimado</p>
            <p style="margin: 10px 0; font-size: 18px; font-weight: bold;">@{odd_0x1:.2f}</p>
            <p style="margin: 0; font-size: 13px;">Lay Unit 1</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # ===== BREAKDOWN =====
    st.divider()
    st.subheader("📊 Análise Detalhada por Critério")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
        **Odd do Visitante**
        - Valor: {result['odd_away']:.2f}
        - Categoria: {result['odd_cat']}
        - Score: **{result['odd_score']}/40** ⭐
        """
        )

    with col2:
        st.markdown(
            f"""
        **xG do Visitante**
        - Valor: {result['xg_away']:.3f}
        - Categoria: {result['xg_cat']}
        - Score: **{result['xg_score']}/40** ⭐
        """
        )

    with col3:
        st.markdown(
            f"""
        **Eficiência de Conversão**
        - Valor: {result['efficiency_away']:.1f}%
        - Categoria: {result['eff_cat']}
        - Score: **{result['eff_score']}/30** ⭐
        """
        )

    # ===== INFORMAÇÕES DO TIME =====
    st.divider()
    st.subheader("🏆 Perfil do Time (Away)")

    if team_info and team_info.get("Matches", 0) > 0:
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Partidas", f"{team_info['Matches']}")

        with col2:
            st.metric("Ataques/Jogo", f"{team_info['Attacks']:.1f}")

        with col3:
            st.metric("Ataques Perigosos", f"{team_info['DangerousAttacks']:.1f}")

        with col4:
            st.metric("Chutes no Alvo", f"{team_info['ShotsOnTarget']:.1f}")

        with col5:
            st.metric("Gols/Jogo", f"{team_info['Goals_Away'] / team_info['Matches']:.2f}")
    else:
        st.info(f"⚠️ {away_team} não encontrado em footystats. Usando média geral.")

    # ===== RECOMENDAÇÃO FINAL =====
    st.divider()

    if result["total_score"] >= 90:
        st.success(
            f"""
        ## 🟢 ENTRAR COM CONFIANÇA

        **Score: {result['total_score']}/110 ({score_pct:.1f}%)**

        Este jogo atende os critérios ideais para Lay 0x1:
        - ✅ Odd adequada ({result['odd_away']:.2f})
        - ✅ xG baixo ({result['xg_away']:.3f})
        - ✅ Eficiência positiva ({result['efficiency_away']:.1f}%)

        **Recomendação:** Entrar com Unit padrão
        """
        )

    elif result["total_score"] >= 70:
        st.warning(
            f"""
        ## 🟡 ENTRAR COM CUIDADO

        **Score: {result['total_score']}/110 ({score_pct:.1f}%)**

        Este jogo é uma boa oportunidade com cuidado moderado:
        - ⚠️ Alguns critérios parcialmente ótimos
        - ⚠️ Risco moderado

        **Recomendação:** Entrar com 50-75% de Unit
        """
        )

    else:
        st.error(
            f"""
        ## 🔴 EVITAR

        **Score: {result['total_score']}/110 ({score_pct:.1f}%)**

        Este jogo não atende os critérios mínimos para Lay 0x1:
        - ❌ Odd fraca ({result['odd_away']:.2f})
        - ❌ xG alto ({result['xg_away']:.3f})
        - ❌ Eficiência baixa ({result['efficiency_away']:.1f}%)

        **Recomendação:** Esperar outros jogos
        """
        )

    # ===== DISCLAIMER =====
    st.divider()
    st.info(
        """
    **⚠️ AVISO IMPORTANTE**

    Esta ferramenta fornece sugestões baseadas em análise histórica de dados.
    Não é uma garantia de lucro. Apostas envolvem risco financeiro.
    Use por sua conta e risco e sempre respeite seu gerenciamento de banca.

    **Estratégia Lay 0x1:** Apostas contra o resultado específico 0x1 (derrota por 1 gol do mandante).
    """
    )
