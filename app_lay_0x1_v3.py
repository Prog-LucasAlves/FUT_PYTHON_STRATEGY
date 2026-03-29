"""
Lay 0x1 Strategy Dashboard - Version 4
Usando dados consolidados Betfair + FootyStats
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from strategy_v4 import Lay0x1StrategyV4

st.set_page_config(page_title="Lay 0x1 Strategy V4", layout="wide")


# ===== CACHE =====
@st.cache_resource
def load_strategy():
    return Lay0x1StrategyV4()


@st.cache_data
def load_consolidated_data():
    df = pd.read_csv("data_total/dados_consolidado_v2.csv", sep=";")
    return df


# Carregar dados
strategy = load_strategy()
df = load_consolidated_data()

# ===== HEADER =====
st.title("⚽ Lay 0x1 Strategy Dashboard V4")
st.markdown("**Estratégia de apostas para Lay 0x1 (visitante com 0 gols)**")
st.info("📊 Base: Dados consolidados (2.933 jogos) | Estratégia V4 com xG e Eficiência")

# ===== KPIs =====
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📊 Total de Jogos", len(df))

with col2:
    wr = (df["Lay_0x1_Outcome"] == 1).sum() / len(df) * 100
    st.metric("🎯 Win Rate Lay 0x1", f"{wr:.1f}%")

with col3:
    lucro = df["Profit_Lay_0x1"].sum()
    st.metric("💰 Lucro Total", f"{lucro:.2f}")

with col4:
    roi = lucro / len(df)
    st.metric("📈 ROI Médio", f"{roi:.4f}")

with col5:
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    st.metric("📅 Período", f"{min_date} a {max_date}"[-10:])

st.divider()

# ===== TABS =====
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🎮 Validador Daily", "ℹ️ Sobre"])

# ===== TAB 1: DASHBOARD =====
with tab1:
    st.subheader("Análise Histórica")

    col1, col2 = st.columns(2)

    with col1:
        # Win rate por faixa de odds
        st.subheader("Win Rate por Faixa de Odds")
        df["Odd_Range"] = pd.cut(df["Odd_A_Back"], bins=[0, 2.5, 3.5, 5.0, 100], labels=["<2.5", "2.5-3.5", "3.5-5.0", ">5.0"])
        wr_odds = df.groupby("Odd_Range")["Lay_0x1_Outcome"].agg(["sum", "count"])
        wr_odds["pct"] = (wr_odds["sum"] / wr_odds["count"] * 100).round(1)

        fig = px.bar(wr_odds.reset_index(), x="Odd_Range", y="pct", title="Win Rate por Faixa de Odds", labels={"pct": "Win Rate (%)"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Lucro por faixa de odds
        st.subheader("Lucro Total por Faixa de Odds")
        lucro_odds = df.groupby("Odd_Range")["Profit_Lay_0x1"].sum().reset_index()

        fig = px.bar(lucro_odds, x="Odd_Range", y="Profit_Lay_0x1", title="Lucro por Faixa de Odds", labels={"Profit_Lay_0x1": "Lucro"})
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição de xG do Visitante")
        fig = px.histogram(df, x="xG_A", nbins=30, title="Distribuição xG Away", labels={"xG_A": "xG Visitante"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Odd vs xG (Visitante)")
        fig = px.scatter(df, x="Odd_A_Back", y="xG_A", color="Lay_0x1_Outcome", title="Odd Away vs xG Away", labels={"Odd_A_Back": "Odd", "xG_A": "xG", "Lay_0x1_Outcome": "Resultado"})
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Tabela de estatísticas por liga
    st.subheader("Estatísticas por Liga")
    league_stats = df.groupby("League").agg({"Lay_0x1_Outcome": ["count", "sum"], "Profit_Lay_0x1": "sum", "xG_A": "mean", "Odd_A_Back": "mean"}).round(2)
    league_stats.columns = ["Jogos", "Wins", "Lucro", "xG Médio", "Odd Média"]
    league_stats["Win Rate %"] = (league_stats["Wins"] / league_stats["Jogos"] * 100).round(1)
    st.dataframe(league_stats, use_container_width=True)

# ===== TAB 2: VALIDADOR =====
with tab2:
    st.subheader("🎮 Validador - Jogos do Dia")

    st.info("""
    **Como usar:**
    1. Selecione a data
    2. Escolha um jogo
    3. Valide contra a estratégia

    **Recomendações:**
    - 🟢 Score 90+: CONFIANÇA (baixo risco)
    - 🟡 Score 70-89: CUIDADO (médio risco)
    - 🔴 Score <70: EVITAR (alto risco)
    """)

    # Procurar por arquivos de daily games
    day_files = sorted(list(Path("data_day").glob("dados_day_betfair_*.csv")))

    if len(day_files) > 0:
        # Extrair datas
        datas = []
        for f in day_files:
            date_str = f.stem.split("_")[-1]
            datas.append(date_str)

        datas = sorted(datas, reverse=True)

        col1, col2 = st.columns(2)

        with col1:
            data_selected = st.selectbox("Selecione uma data:", datas)

        with col2:
            st.write("")  # spacer

        # Carregar jogos da data
        arquivo = f"data_day/dados_day_betfair_{data_selected}.csv"
        try:
            df_day = pd.read_csv(arquivo, sep=";")
            st.success(f"✅ {len(df_day)} jogo(s) encontrado(s)")

            if len(df_day) > 0:
                # Seletor de jogo
                opcoes = []
                for idx, row in df_day.iterrows():
                    opcoes.append(f"{row['Home']} vs {row['Away']} ({row['Odd_A_Back']:.2f})")

                jogo_sel = st.selectbox("Escolha um jogo:", opcoes)
                idx_sel = opcoes.index(jogo_sel)
                row = df_day.iloc[idx_sel]

                st.divider()

                # Dados do jogo
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Mandante", row["Home"])
                with col2:
                    st.metric("Visitante", row["Away"])
                with col3:
                    st.metric("Odd Away", f"{row['Odd_A_Back']:.2f}")
                with col4:
                    st.metric("Odd 0x1 Lay", f"{row['Odd_CS_0x1_Lay']:.1f}")

                st.divider()

                # Validar
                if st.button("🎯 VALIDAR ENTRADA", use_container_width=True, type="primary"):
                    result = strategy.evaluate_score(home=row["Home"], away=row["Away"], odd_away=float(row["Odd_A_Back"]), odd_0x1_lay=float(row["Odd_CS_0x1_Lay"]))

                    st.divider()

                    # Score
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        color = "green" if result["total_score"] >= 90 else "orange" if result["total_score"] >= 70 else "red"
                        st.markdown(
                            f"""
                        <div style="text-align: center; padding: 20px; background-color: {color}40; border-radius: 10px;">
                            <h2 style="margin: 0;">{result["total_score"]}/110</h2>
                            <p style="margin: 5px 0; font-weight: bold;">SCORE</p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with col2:
                        color = "green" if result["total_score"] >= 90 else "orange" if result["total_score"] >= 70 else "red"
                        st.markdown(
                            f"""
                        <div style="text-align: center; padding: 20px; background-color: {color}40; border-radius: 10px;">
                            <p style="margin: 0; font-size: 14px;">RECOMENDAÇÃO</p>
                            <p style="margin: 5px 0; font-weight: bold;">{result["recommendation"]}</p>
                            <p style="margin: 0; font-size: 12px;">{result["risk"]}</p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with col3:
                        st.markdown(
                            f"""
                        <div style="text-align: center; padding: 20px; background-color: #00800040; border-radius: 10px;">
                            <p style="margin: 0; font-size: 14px;">xG VISITANTE</p>
                            <p style="margin: 5px 0; font-weight: bold;">{result["xg_away"]:.2f}</p>
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    st.divider()

                    # Análise
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Odd Away:** {result['odd_away']:.2f}\n**Score:** {result['odd_score']}/40")
                    with col2:
                        st.markdown(f"**xG Away:** {result['xg_away']:.2f}\n**Score:** {result['xg_score']}/40")
                    with col3:
                        st.markdown(f"**Shots Avg:** {result['shots_away_avg']:.1f}\n**Score:** {result['defense_score']}/30")

                    st.divider()
                    st.info(f"**Análise:** {result['rationale']}")

                    if result["total_score"] >= 90:
                        st.success("✅ ENTRAR COM CONFIANÇA")
                    elif result["total_score"] >= 70:
                        st.warning("🟡 ENTRAR COM CUIDADO")
                    else:
                        st.error("🔴 EVITAR")

        except Exception as e:
            st.error(f"Erro ao carregar {arquivo}: {e}")

    else:
        st.warning("Nenhum arquivo de daily games encontrado em data_day/")

# ===== TAB 3: SOBRE =====
with tab3:
    st.subheader("ℹ️ Sobre a Estratégia V4")

    st.markdown("""
    ### Estratégia Lay 0x1

    **Objetivo:** Apostar que o visitante terá 0 gols (não marcar)

    ### Componentes do Score (0-110)

    1. **Odd do Visitante (0-40)**
       - >5.0: 40 pontos (muito favorável)
       - 3.5-5.0: 30 pontos
       - 2.5-3.5: 15 pontos
       - <2.5: 5 pontos (desfavorável)

    2. **xG do Visitante (0-40)**
       - <0.5: 40 pontos (muito baixo)
       - 0.5-1.0: 30 pontos
       - 1.0-1.5: 15 pontos
       - >1.5: 5 pontos (alto)

    3. **Eficiência Defensiva (0-30)**
       - <8 shots: 30 pontos
       - 8-12 shots: 20 pontos
       - 12-15 shots: 10 pontos
       - >15 shots: 0 pontos

    ### Recomendações

    - **CONFIANÇA (90+):** Baixo risco, entrar com confiança
    - **CUIDADO (70-89):** Médio risco, entrar com proteção
    - **EVITAR (<70):** Alto risco, aguardar melhor oportunidade

    ### Base de Dados

    - **2.933 jogos consolidados** a partir de:
      - Betfair: Odds e resultados
      - FootyStats: xG, possession, shots, etc.
    - **Período:** 2023-09-03 a 2026-12-01
    - **Ligas:** Espanha, Inglaterra, Itália, Alemanha, Portugal, França, Brasil

    ### Validação Histórica

    - Win Rate Geral: 39.5%
    - Win Rate (Odds 5.0+): 50.9% ✅
    - Profit (Odds 5.0+): +151.54 ✅
    """)

    st.divider()
    st.markdown("**Desenvolvido com:** Python | Streamlit | Pandas | Plotly")
